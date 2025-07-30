import pandas as pd
import numpy as np
import time
from datetime import datetime
from tqdm import tqdm
import os

from SharedData.Logger import Logger
from SharedData.TableIndexJit import get_date_loc_jit, get_symbol_loc_jit, get_portfolio_loc_jit, get_tag_loc_jit, djb2_hash
from SharedData.Utils import mmaparray2df
       
class SharedNumpy(np.ndarray):

    def __new__(cls, type, *args, **kwargs):
        if type == 'MEMORY':
            obj = np.ndarray.__new__(cls, *args, **kwargs)
            obj.table = None
            return obj
        elif type == 'DISK':
            memmap = args[0]
            obj = memmap.view(cls)
            obj.memmap = memmap
            obj.table = None
            obj._df = None
            return obj
        else:
            raise Exception('Unknown type %s!' % (type))

    def free(self):
        self.table.free()

    def trim(self):
        self.table.trim()

    def write(self,force_write=False):
        if self.table.hdr['hasindex']==1 and self.table.hdr['isidxsorted']==0:
            self.sort_index()
        self.table.write(force_write)
        
    def rememmap(self):
        memmap = np.memmap(self.table.filepath, self.table.recdtype, 'r+', self.table.hdr.dtype.itemsize, (self.recordssize,))
        new_instance = memmap.view(self.__class__)
        new_instance.table = self.table
        new_instance.memmap = memmap
        self.table.records = new_instance
        return new_instance
    
    def reload(self):
        return self.table.reload()
    
    ################################# SYNC TABLE ########################################
    def subscribe(self, host, port=None, lookbacklines=1000, lookbackdate=None, method='websocket', snapshot=False, bandwidth=1e6, protocol='http'):
        self.table.subscribe(host, port, lookbacklines,
                             lookbackdate, method, snapshot, bandwidth,protocol)
        
    def publish(self, host, port=None, lookbacklines=1000, lookbackdate=None, method='websocket', snapshot=False, bandwidth=1e6, protocol='http'):
        self.table.publish(host, port, lookbacklines,
                             lookbackdate, method, snapshot, bandwidth,protocol)
    
    def read_stream(self, buffer):
        
        if len(buffer) >= self.itemsize:
            # Determine how many complete records are in the buffer
            num_records = len(
                buffer) // self.itemsize
            # Take the first num_records worth of bytes
            record_data = buffer[:num_records *
                                        self.itemsize]
            # And remove them from the buffer
            del buffer[:num_records *
                                self.itemsize]
            # Convert the bytes to a NumPy array of records
            rec = np.frombuffer(
                record_data, dtype=self.dtype)
            
            if self.table.hasindex:
                # Upsert all records at once
                self.upsert(rec)
            else:
                # Extend all records at once
                self.extend(rec)

        return buffer

    ############################## KEYLESS OPERATIONS ########################################

    def insert(self, new_records, acquire=True):
        errmsg = ''
        try:
            if acquire:
                self.table.acquire()

            nrec = new_records.size
            _count = self.count
            if (_count + nrec <= self.size):
                # convert new_records
                if (self.dtype != new_records.dtype):
                    new_records = self.convert(new_records)
                # fill mtime
                nidx = np.isnat(new_records['mtime'])
                if nidx.any():
                    new_records['mtime'][nidx] = time.time_ns()

                arr = super().__getitem__(slice(0, self.size))
                arr[_count:_count+nrec] = new_records
                self.count = _count + nrec
                self.mtime = datetime.now().timestamp()
            else:
                errmsg = 'Table max size reached!'
                Logger.log.error(errmsg)
        except Exception as e:
            errmsg = 'Error inserting %s!\n%s' % (self.table.relpath, str(e))
            Logger.log.error(errmsg)
        finally:
            if acquire:
                self.table.release()
            if errmsg:
                raise Exception(errmsg)

    def extend(self, new_records, acquire=True):
        errmsg = ''
        if self.table.type == 'MEMORY':
                raise Exception(
                    'Table %s is in memory, extend not supported!' % (self.table.relpath))

        if self.table.hdr['hasindex'] == 1:
            raise Exception(
                'Table %s has index, extend not supported!' % (self.table.relpath))
        
        try:            
            if acquire:
                self.table.acquire()
            
            if self.size < self.recordssize:
                self = self.rememmap()

            nrec = new_records.size
            _count = self.count.copy()
            
            if (_count + nrec > self.recordssize):
                # extend table by 10MB
                rec = self.table.records
                page_size = 4096
                extend_size = int(np.round(100 * 1024 * 1024 / page_size) * page_size)
                new_rows = int(np.floor(extend_size/rec.dtype.itemsize))
                new_rows = max(new_rows, nrec)

                new_recordssize = rec.size + new_rows
                hdr_bytes = self.table.hdr.dtype.itemsize
                rec_bytes = rec.dtype.itemsize * rec.size                
                totalbytes = hdr_bytes + rec_bytes + rec.dtype.itemsize*new_rows
                
                with open(self.table.filepath, 'ab+') as f:
                    # Seek to the end of the file
                    f.seek(totalbytes-1)
                    # Write a single null byte to the end of the file
                    f.write(b'\x00')
                    if os.name == 'posix':
                        os.posix_fallocate(f.fileno(), 0, totalbytes)
                    elif os.name == 'nt':
                        pass  # TODO: implement preallocation for windows in pyd

                # remap extended file
                if self.table.shf_data is not None:
                    self.table.shf_data.flush()
                self.table.shf_data = np.memmap(
                    self.table.filepath,rec.dtype,'r+',
                    hdr_bytes,(new_recordssize,) )
                self.table.records = SharedNumpy('DISK', self.table.shf_data)
                self.table.records.table = self.table                
                self.recordssize = new_recordssize

            # convert new_records
            if (self.dtype != new_records.dtype):
                new_records = self.convert(new_records)
            # fill mtime
            nidx = np.isnat(new_records['mtime'])
            if nidx.any():
                new_records['mtime'][nidx] = time.time_ns()
            # insert data
            self.table.records.insert(new_records, acquire=False)
            
            return self.table.records
        

        except Exception as e:
            errmsg = 'Error extending %s!\n%s' % (self.table.relpath, str(e))
            Logger.log.error(errmsg)
        finally:
            if acquire:
                self.table.release()
            if errmsg:
                raise Exception(errmsg)

    ############################## PRIMARY KEY OPERATIONS ########################################
    @property
    def loc(self):
        return _LocIndexer(self)

    def upsert(self, new_records, acquire=True):
        # TODO: check if index variables are valid
        if self.table.hdr['hasindex'] == 0:
            raise Exception('Table %s has no index!' % (self.table.relpath))

        if new_records.size > 0:

            # convert to same dtype record
            if isinstance(new_records, pd.DataFrame):
                new_records = self.table.df2records(new_records)
            elif (self.dtype != new_records.dtype):
                new_records = self.convert(new_records)

            utcnow = np.datetime64(time.time_ns(), 'ns') # add 1 second tolerance
            # fill mtime
            nidx = np.isnat(new_records['mtime'])
            if nidx.any():
                new_records['mtime'][nidx] = utcnow

            # remove invalid mtime
            invalididx = new_records['mtime'].astype(np.int64) > utcnow.astype(np.int64) + 1000000000
            if invalididx.any():
                new_records[invalididx]['mtime'] = utcnow
                Logger.log.warning('%s: %d records with invalid mtime check your system clock!' \
                                   % (self.table.relpath, invalididx.sum()))

            # check for null date
            if self.table.database!='Symbols':
                invalididx = np.isnat(new_records['date'])
                invalididx = invalididx | (new_records['date'] < self.table.mindate)
                invalididx = invalididx | (new_records['date'] >= self.table.maxdate)
                if invalididx.any():
                    new_records = new_records[~invalididx]
                # round date to period
                new_records['date'] = (new_records['date'].astype(np.int64) // self.table.periodns) * self.table.periodns

            if new_records.size > 0:
                # single record to array
                if new_records.shape == ():
                    new_records = np.array([new_records])

                try:
                    success = True
                    if acquire:
                        self.table.acquire()

                    # check if index is created & valid
                    if self.table.hdr['isidxcreated'] == 0:
                        self.index.create_index(self, self.pkey)

                    # upsert
                    minchgid = self.count
                    arr = super().__getitem__(slice(0, self.size))

                    self.table.hdr['isidxcreated'] == 0

                    self.count, minchgid, isidxsorted = self.index.upsert_func(
                        arr, self.count, new_records, self.pkey,
                        self.index.datelastidx, self.index.dateprevidx,
                        self.table.mindate, self.table.periodns,
                        self.index.portlastidx, self.index.portprevidx,
                        self.index.symbollastidx, self.index.symbolprevidx)

                    self.table.hdr['isidxsorted'] == 1 if isidxsorted else 0
                    self.table.hdr['isidxcreated'] == 1
                    minchgid = int(minchgid)
                    self.minchgid = minchgid
                    self.mtime = datetime.now().timestamp()

                except Exception as e:
                    Logger.log.error('Error upserting %s!\n%s' %
                                     (self.table.relpath, str(e)))
                    success = False
                finally:
                    if acquire:
                        self.table.release()
                    # table full
                    if self.count == self.size:
                        Logger.log.critical('Table %s is full!' %
                                           (self.table.relpath))
                    if not success:
                        raise Exception('Error upserting %s!' %
                                        (self.table.relpath))
                return minchgid

        return self.count

    def sort_index(self, start=0):
        self.index.sort_index(self, start)

    def get_loc(self, keys, acquire=True):
        success = False
        if self.table.hdr['hasindex'] != 1:
            raise Exception(f'Table {self.table.relpath} does not have index!')
        
        try:
            if acquire:
                self.table.acquire()

            # check if index is created & valid
            if self.table.hdr['isidxcreated'] == 0:
                self.index.create_index(self, self.pkey)

            loc = self.index.get_loc_func(
                self[:], self.pkey, keys).astype(np.int64)
            success = True
        except Exception as e:
            Logger.log.error('Error getting loc for %s!\n%s' %
                             (self.table.relpath, str(e)))
            loc = np.array([])
        finally:
            if acquire:
                self.table.release()
            if not success:
                raise Exception('Error getting loc for %s!' %
                                (self.table.relpath))
        return loc

    def get_date_loc(self, date, maxids=0):
        success = False
        if self.table.hdr['hasindex'] != 1:
            raise Exception(f'Table {self.table.relpath} does not have index!')
        try:
            self.table.acquire()

            # check if index is created & valid
            if self.table.hdr['isidxcreated'] == 0:
                self.index.create_index(self, self.pkey)
            
            if isinstance(date, pd.Timestamp):
                date = np.datetime64(date,'ns')

            datelastidx = self.table.index.datelastidx
            dateprevidx = self.table.index.dateprevidx            
            mindate = self.table.mindate
            periodns = self.table.periodns
            if (date < mindate) | (date >= self.table.maxdate):
                loc = np.array([])                
            else:                            
                loc = get_date_loc_jit(date, datelastidx, dateprevidx, mindate, periodns, maxids)
            
            success = True
        except Exception as e:
            Logger.log.error('Error getting date_loc for %s!\n%s' %
                             (self.table.relpath, str(e)))
        finally:
            self.table.release()
            if not success:
                raise Exception('Error getting date_loc for %s!' %
                                (self.table.relpath))
        return loc

    # get date loc greater than or equal to startdate
    def get_date_loc_gte(self,startdate):
        if self.table.hdr['hasindex'] != 1:
            raise Exception(f'Table {self.table.relpath} does not have index!')
        if isinstance(startdate, pd.Timestamp):
            startdate = np.datetime64(startdate,'ns')
        dateint = np.uint32( (np.uint64(startdate) - np.uint64(self.table.mindate)) // np.uint64(self.table.periodns) )
        datelastidx = self.table.index.datelastidx[dateint:]
        datelastidx = datelastidx[datelastidx!=-1]
        loc = []
        for i in datelastidx:    
            loc.extend(self.get_date_loc(self[i]['date']))
        return loc
    
    # get date loc less than or equal to enddate
    def get_date_loc_lte(self,enddate):
        if self.table.hdr['hasindex'] != 1:
            raise Exception(f'Table {self.table.relpath} does not have index!')
        if isinstance(enddate, pd.Timestamp):
            enddate = np.datetime64(enddate,'ns')
        dateint = np.uint32( (np.uint64(enddate) - np.uint64(self.table.mindate)) // np.uint64(self.table.periodns) )
        datelastidx = self.table.index.datelastidx[:dateint+1]
        datelastidx = datelastidx[datelastidx!=-1]
        loc = []
        for i in datelastidx:    
            loc.extend(self.get_date_loc(self[i]['date']))
        return loc
    
    # get date loc greater than or equal to startdate
    def get_date_loc_gte_lte(self,startdate, enddate):
        if self.table.hdr['hasindex'] != 1:
            raise Exception(f'Table {self.table.relpath} does not have index!')
        if isinstance(startdate, pd.Timestamp):
            startdate = np.datetime64(startdate,'ns')
        startdateint = np.uint32( (np.uint64(startdate) - np.uint64(self.table.mindate)) // np.uint64(self.table.periodns) )
        if isinstance(enddate, pd.Timestamp):
            enddate = np.datetime64(enddate,'ns')
        enddateint = np.uint32( (np.uint64(enddate) - np.uint64(self.table.mindate)) // np.uint64(self.table.periodns) )
        
        datelastidx = self.table.index.datelastidx[startdateint:enddateint+1]
        datelastidx = datelastidx[datelastidx!=-1]
        loc = []
        for i in datelastidx:    
            loc.extend(self.get_date_loc(self[i]['date']))
        return loc    

    def get_symbol_loc(self, symbol, maxids=0):
        if self.table.hdr['hasindex'] != 1:
            raise Exception(f'Table {self.table.relpath} does not have index!')
        success = False
        try:
            self.table.acquire()
            # check if index is created & valid
            if self.table.hdr['isidxcreated'] == 0:
                self.index.create_index(self, self.pkey)

            if not isinstance(symbol, bytes):
                symbol = symbol.encode('utf-8')
            
            _rec = np.full((1,),np.nan,dtype=self.dtype)
            _rec['symbol'] = symbol
            loc = get_symbol_loc_jit(self[:], self.index.symbollastidx,
                                 self.index.symbolprevidx, _rec, maxids)
            success = True
        except Exception as e:
            Logger.log.error('Error getting symbol_loc for %s!\n%s' %
                             (self.table.relpath, str(e)))
        finally:
            self.table.release()
            if not success:
                raise Exception('Error getting symbol_loc for %s!' %
                                (self.table.relpath))
        return loc

    def get_portfolio_loc(self, portfolio, maxids=0):
        if self.table.hdr['hasindex'] != 1:
            raise Exception(f'Table {self.table.relpath} does not have index!')
        success = False
        try:
            self.table.acquire()
            # check if index is created & valid
            if self.table.hdr['isidxcreated'] == 0:
                self.index.create_index(self, self.pkey)

            if not isinstance(portfolio, bytes):
                portfolio = portfolio.encode('utf-8')
            
            _rec = np.full((1,),np.nan,dtype=self.dtype)
            _rec['portfolio'] = portfolio
            loc = get_portfolio_loc_jit(
                self[:], self.index.portlastidx, self.index.portprevidx, _rec, maxids)
            success = True
        except Exception as e:
            Logger.log.error('Error getting portfolio_loc for %s!\n%s' %
                             (self.table.relpath, str(e)))
        finally:
            self.table.release()
            if not success:
                raise Exception('Error getting portfolio_loc for %s!' %
                                (self.table.relpath))
        return loc

    def get_tag_loc(self, tag, maxids=0):
        if self.table.hdr['hasindex'] != 1:
            raise Exception(f'Table {self.table.relpath} does not have index!')
        success = False
        try:
            self.table.acquire()
            # check if index is created & valid
            if self.table.hdr['isidxcreated'] == 0:
                self.index.create_index(self, self.pkey)

            if not isinstance(tag, bytes):
                tag = tag.encode('utf-8')

            _rec = np.full((1,),np.nan,dtype=self.dtype)
            _rec['tag'] = tag

            loc = get_tag_loc_jit(
                self[:], self.index.portlastidx, self.index.portprevidx, _rec, maxids)
            success = True
        except Exception as e:
            Logger.log.error('Error getting tag_loc for %s!\n%s' %
                             (self.table.relpath, str(e)))
        finally:
            self.table.release()
            if not success:
                raise Exception('Error getting tag_loc for %s!' %
                                (self.table.relpath))
        return loc

    ############################## CONVERSION ##############################
    @property
    def df(self):
        mmap_df = False
        if self._df is not None:
            if self._df.shape[0] < self.count:
                mmap_df = True
        else:
            mmap_df = True
            
        if mmap_df:
            indexcols = len(self.table.index.pkeycolumns)
            self._df = mmaparray2df(self[:], indexcols)            

        return self._df
                    
    def records2df(self, records):
        return self.table.records2df(records)

    def df2records(self, df):
        return self.table.df2records(df)

    def convert(self, new_records):
        rec = np.full((new_records.size,), fill_value=np.nan, dtype=self.dtype)
        for col in self.dtype.names:
            if col in new_records.dtype.names:
                try:
                    if np.issubdtype(self.dtype[col], np.integer):
                        nanidx = new_records[col] == b'nan'
                        new_records[col][nanidx] = 0
                        trueidx = new_records[col] == b'True'
                        new_records[col][trueidx] = 1
                        falseidx = new_records[col] == b'False'
                        new_records[col][falseidx] = 0
                    rec[col] = new_records[col].astype(self.dtype[col])
                except Exception as e:
                    Logger.log.error('Could not convert %s!' % (col))
        return rec

    def tags2df(self, dt, seltags, datetags=None):
        idx = pd.Index([])
        df = pd.DataFrame(columns=seltags)
        dfmtime = pd.DataFrame(columns=seltags)
        tag = seltags[0]        
        for tag in seltags:
            try:
                rec = self.loc[dt,tag]
                if len(rec)>0:            
                    values = self.records2df(rec).loc[dt].droplevel(0)
                    idx = idx.union(values.index)
                    df = df.reindex(idx)    
                    if not datetags is None:
                        if tag in datetags:
                            values['value'] = values['value'].apply(lambda x: pd.Timestamp.fromtimestamp(x))
                    df[tag] = values['value']
                    dfmtime[tag] = values['mtime']
            except Exception as e:
                Logger.log.error('Could not get %s %s!' % (tag,e))
        return df, dfmtime


    ############################## GETTERS / SETTERS ##############################    

    def __getitem__(self, key):
        if hasattr(self, 'table'):
            if self.size < self.recordssize:
                self = self.rememmap()

            arr = super().__getitem__(slice(0, self.count))  # slice arr
            if self.count > 0:
                return arr.__getitem__(key)
            else:
                return arr
        else:
            return super().__getitem__(key)
    
    def get_exists_remote(self):
        return self.table.get_exists_remote()

    @property
    def records(self):
        return super().__getitem__(slice(0, self.size))

    @property
    def count(self):
        return self.table.hdr['count']

    @count.setter
    def count(self, value):
        self.table.hdr['count'] = value

    @property
    def recordssize(self):
        return self.table.hdr['recordssize']

    @recordssize.setter
    def recordssize(self, value):
        self.table.hdr['recordssize'] = value

    @property
    def mtime(self):
        return self.table.hdr['mtime']

    @mtime.setter
    def mtime(self, value):
        self.table.hdr['mtime'] = value

    @property
    def minchgid(self):
        return self.table.hdr['minchgid']

    @minchgid.setter
    def minchgid(self, value):
        value = min(value, self.table.hdr['minchgid'])
        self.table.hdr['minchgid'] = value

    @property
    def index(self):
        return self.table.index

    @index.setter
    def index(self, value):
        self.table.index = value

    @property
    def pkey(self):
        return self.table.index.pkey

    @pkey.setter
    def pkey(self, value):
        self.table.index.pkey = value

class _LocIndexer:
    """
    .loc indexer for SharedNumpy, supporting advanced row- and col-wise selection,
    respecting database keys (date/symbol/tag/portfolio).
    """
    def __init__(self, data):
        self.data = data

    def __setitem__(self, key, value):
        errmsg = "Error: loc is readonly!"
        Logger.log.error(errmsg)
        raise Exception(errmsg)

    def __getitem__(self, index):
        row_index, col_index = self._parse_index(index)

        # ----- 1. Slice access (maybe with secondary key as col_index) -----
        if isinstance(row_index, slice):
            start, stop, step = self._slice_to_bounds(row_index)
            # If doing .loc[:,'AAPL'] for symbol-keyed tables
            if isinstance(col_index, str) and col_index not in self.data.dtype.names:
                locs = self._secondary_index_locs(row_key=col_index)
                if locs.size:
                    result = locs[(locs >= start) & (locs < stop)]
                    return self.data[result]
                else:
                    return np.array([], dtype=self.data.dtype)
            return self.data[start:stop:step][col_index]

        # ----- 2. MultiIndex access -----
        if isinstance(row_index, pd.MultiIndex):
            return self._multiindex_locs(row_index, col_index)

        # ----- 3. Tuple as (slice/Timestamp/int, key) -----
        if isinstance(row_index, tuple):
            # (slice, key-string)
            row_part, key_part = row_index
            if isinstance(row_part, slice) and isinstance(key_part, str):
                start, stop, step = self._slice_to_bounds(row_part)
                locs = self._secondary_index_locs(row_key=key_part)
                if locs.size:
                    result = locs[(locs >= start) & (locs < stop)]
                    return self.data[result]
                else:
                    return np.array([], dtype=self.data.dtype)
            elif row_part is None:
                return self.data[..., col_index]
            else:
                raise NotImplementedError("Tuple with this signature in .loc not handled.")

        # ----- 4. Integer row index -----
        if isinstance(row_index, int):
            # If col_index is a secondary key string (symbol/tag/portfolio/etc.)
            if isinstance(col_index, str) and col_index not in self.data.dtype.names:
                locs = self._secondary_index_locs(row_key=col_index)
                if locs.size:
                    # pick the nth match by row_index
                    return self.data[locs[row_index % len(locs)]]
                else:
                    raise IndexError(f"No entry for key '{col_index}'")
            return self.data[row_index][col_index]

        # ----- 5. Timestamp row index (date lookup, optionally with key in col_index) -----
        if isinstance(row_index, pd.Timestamp) or np.issubdtype(type(row_index), np.datetime64):
            # Get all matching locs by date
            row_index = np.datetime64(row_index, 'ns')
            locs = self.data.get_date_loc(row_index)
            if not isinstance(locs, np.ndarray):
                locs = np.array(locs)
            # If using symbol/tag/portfolio as col_index
            if isinstance(col_index, str) and col_index not in self.data.dtype.names:
                key_locs = self._secondary_index_locs(row_key=col_index)
                if key_locs.size and locs.size:
                    # Intersection: all rows with both this date and this key
                    result = np.intersect1d(locs, key_locs, assume_unique=True)
                    return self.data[result]
                return np.array([], dtype=self.data.dtype)
            # If col_index is an Index of secondary keys (DataFrame-like retrieve)
            if isinstance(col_index, pd.Index):
                idxname = self.data.table.index.pkeycolumns[1]
                all_locs = []
                for key in col_index:
                    sec_locs = self._secondary_index_locs(row_key=key)
                    all_locs.extend(np.intersect1d(locs, sec_locs, assume_unique=True))
                return self.data[np.sort(np.unique(all_locs))]
            # Only date filter
            return self.data[locs][col_index] if locs.size else np.array([], dtype=self.data.dtype)

        # ----- 6. Fallback: direct ---------
        return self.data[row_index][col_index]

    def _parse_index(self, index):
        # Returns (row_index, col_index) from all .loc[] calls
        if isinstance(index, tuple):
            if len(index) == 2:
                return index
            elif len(index) == 1:
                return index[0], slice(None)
        elif isinstance(index, pd.MultiIndex):
            return index, slice(None)
        elif isinstance(index, slice):
            return index, slice(None)
        elif isinstance(index, str):
            return None, index
        return index, slice(None)

    def _slice_to_bounds(self, s: slice):
        def bound(val, fallback):
            if val is None:
                return fallback
            if isinstance(val, pd.Timestamp):
                arr = self.data.get_date_loc(np.datetime64(val, 'ns'))
                return arr[0] if len(arr) > 0 else fallback
            return val
        start = bound(s.start, 0)
        stop = bound(s.stop, self.data.count)
        step = s.step if s.step is not None else 1
        return start, stop, step

    def _secondary_index_locs(self, row_key: str):
        # Looks up indices by secondary key type
        pkeycolumns = getattr(self.data.table.index, 'pkeycolumns', [])
        if len(pkeycolumns) < 2:
            return np.array([], dtype=int)
        idx_type = pkeycolumns[1]
        get_func = {
            'symbol': self.data.get_symbol_loc,
            'tag': self.data.get_tag_loc,
            'portfolio': self.data.get_portfolio_loc,
        }.get(idx_type)
        if get_func is None:
            return np.array([], dtype=int)
        out = get_func(row_key)
        if not isinstance(out, np.ndarray):
            out = np.array(out, dtype=int)
        return out

    def _multiindex_locs(self, row_index: pd.MultiIndex, col_index):
        dtype = np.dtype([(x, row_index.get_level_values(x).dtype) for x in row_index.names])
        record_keys = np.array([tuple(x) for x in row_index.values], dtype=dtype)
        record_keys = self.data.convert(record_keys)
        locs = self.data.get_loc(record_keys)
        locs = np.array(locs)
        locs = locs[locs >= 0]
        return self.data[locs][col_index]
