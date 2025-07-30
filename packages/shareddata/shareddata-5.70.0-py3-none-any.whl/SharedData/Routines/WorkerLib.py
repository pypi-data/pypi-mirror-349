# SharedData/Routines/WorkerLib.py

# implements a decentralized routines worker
# connects to worker pool
# broadcast heartbeat
# listen to commands

import os
import sys
import psutil
import time
import subprocess
import threading
from subprocess import DEVNULL
from threading import Thread
import signal


import pandas as pd
import numpy as np
from pathlib import Path

from SharedData.Logger import Logger
from SharedData.IO.ClientAPI import ClientAPI

def compare_routines(routine1,routine2):
    hash1 = hash_routine(routine1)
    hash2 = hash_routine(routine2)

    return hash1 == hash2

def hash_routine(routine):
    rhash = ''
    if ('repo' in routine):
        rhash = routine['repo']
    if ('branch' in routine):
        rhash += '#' + routine['branch']
    if ('routine' in routine):
        rhash += '/'+routine['routine']
    if ('args' in routine):
        rhash += ' ' + routine['args']
    return rhash

def upsert_routine(newroutine,routines):
    updated = False
    for routine in routines:
        if ('pid' in routine):
            if newroutine['pid'] == routine['pid']:
                routine.update(newroutine)
                updated = True
        elif compare_routines(newroutine,routine['command']):
            routine.update(newroutine)
            updated = True

    if not updated:
        routines.append(newroutine)

def update_routines(routines):

    source_path = Path(os.environ['SOURCE_FOLDER'])
    if os.name == 'posix':
        python_path = 'venv/bin/python'
    else:
        python_path = 'venv/Scripts/python.exe'

    processes = []
    for processes in psutil.process_iter(['pid', 'name', 'exe', 'cmdline']):
        try:
            if processes.info['cmdline'] and processes.info['cmdline'][0].startswith(str(source_path)):
                proc = processes.info
                if len(proc['cmdline']) >= 2:
                    idx = np.array(proc['cmdline']) == '-m'
                    if np.any(idx):
                        i = np.argmax(idx)
                        if 'SharedData' in proc['cmdline'][i+1]:
                            routine = {}
                            routine['pid'] = proc['pid']
                            routine['process'] = psutil.Process(routine['pid'])
                            routine['command'] = {}
                            routine['command']['repo'] = 'SharedData'
                            routine['command']['routine'] = proc['cmdline'][i+1].replace('SharedData.', '')
                            if len(proc['cmdline']) >= i+3:
                                routine['command']['args'] = ' '.join(proc['cmdline'][i+2:])
                            upsert_routine(routine,routines)
                    else:
                        idx = [str(source_path) in s for s in proc['cmdline']]
                        if np.any(idx):
                            i = np.argmax(idx)
                            for cmd in proc['cmdline'][i+1:]:
                                i=i+1
                                if str(source_path) in cmd:
                                    cmd = ' '.join(proc['cmdline'][i:])                                    
                                    routinestr = cmd.replace(str(source_path), '')
                                    if routinestr.startswith(os.sep):
                                        routinestr = routinestr[1:]
                                    cmdsplit = routinestr.split(os.sep)
                                    routine = {}
                                    routine['pid'] = proc['pid']
                                    routine['process'] = psutil.Process(routine['pid'])
                                    routine['command'] = {}
                                    if '#' in cmdsplit[0]:                                        
                                        routine['command']['repo'] = cmdsplit[0].split('#')[0]
                                        routine['command']['branch'] = cmdsplit[0].split('#')[1]
                                    else:
                                        routine['command']['repo'] = cmdsplit[0]
                                    
                                    scriptstr = os.sep.join(cmdsplit[1:])
                                    scriptsplit = scriptstr.split(' ')
                                    routine['command']['routine'] = scriptsplit[0]
                                    if len(scriptsplit) > 1:
                                        routine['command']['args'] = ' '.join(scriptsplit[1:])
                                    upsert_routine(routine,routines)
                                    break

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

def validate_command(command):
    """
    Cleans and validates the 'command' dictionary.
    Removes invalid or empty 'args' and ensures proper format.
    """
    # Sanitize 'args'
    if 'args' in command:
        # Remove 'args' if it's empty, 'nan' (str), or actual NaN (float from pandas)
        val = command['args']
        if (val == '') or (str(val).lower() == 'nan'):
            del command['args']
        elif isinstance(val, float) and np.isnan(val):
            del command['args']
        elif not isinstance(val, (str, dict)):
            # If it's not a string or dict (e.g. list), convert to string
            command['args'] = str(val)
                
    # Add default values or cleanup others as needed
    if 'branch' in command and command['branch'] == '':
        del command['branch']  # remove empty branch if not used

    return command

last_restart = {}
def process_command(command,routines,batch_jobs):

    if command['job'] == 'batch':
        start_time = time.time()
        job = command
        job.update({            
            'thread': None,
            'process': None,
            'subprocess': None,
            'start_time': start_time,
        })
        thread = Thread(target=run_routine,
                        args=(job['command'], job, True))
        job['thread'] = thread
        batch_jobs.append(job)
        thread.start()        
        return

    elif command['job'] == 'command':
        start_time = time.time()
        routine = {
            'command': command,
            'thread': None,
            'process': None,
            'subprocess': None,
            'start_time': start_time,
        }
        thread = Thread(target=send_command,args=(command['command'],))
        routine['thread'] = thread
        routines.append(routine)
        thread.start()

    elif command['job'] == 'install':
        if not isrunning(command,routines):
            start_time = time.time()
            routine = {
                'command': command,
                'thread': None,
                'start_time': start_time,
            }
            thread = Thread(target=install_repo,args=(command,False))
            routine['thread'] = thread
            routines.append(routine)
            thread.start()
        else:
            Logger.log.info('Already installing %s!\n' % (str(command)))

    elif command['job'] == 'routine':
        # expects command:
        # command = {
        #     "sender" : "MASTER",
        #     "target" : user,
        #     "job" : "routine",
        #     "repo" : routine.split('/')[0],
        #     "routine" : '/'.join(routine.split('/')[1:])+'.py',
        #     "branch" : branch,
        # }
        restart = True
        rhash = hash_routine(command)
        if rhash in last_restart.keys():
            if time.time()-last_restart[rhash] < 30:
                restart = False
        
        if restart:
            last_restart[rhash] = time.time()
            if not isrunning(command,routines):
                start_time = time.time()
                routine = {
                    'command': command,
                    'thread': None,
                    'process': None,
                    'subprocess': None,
                    'start_time': start_time,
                }
                thread = Thread(target=run_routine,
                                args=(command, routine))
                routine['thread'] = thread
                routines.append(routine)
                thread.start()
            else:
                Logger.log.info('Already running %s!\n' %
                                (str(command)))

    elif command['job'] == 'kill':
        kill_routine(command,routines)

    elif command['job'] == 'restart':
        #TODO: if called multiple times in a row it dupicates the routine        
        restart = True
        rhash = hash_routine(command)
        if rhash in last_restart.keys():
            if time.time()-last_restart[rhash] < 30:
                restart = False
        
        if restart:
            last_restart[rhash] = time.time()
            kill_routine(command,routines)
            routines = remove_finished_routines(routines)
            if not isrunning(command,routines):
                start_time = time.time()
                routine = {
                    'command': command,
                    'thread': None,
                    'process': None,
                    'subprocess': None,
                    'start_time': start_time,
                }
                thread = Thread(target=run_routine,
                                args=(command, routine))
                routine['thread'] = thread
                routines.append(routine)
                thread.start()

    elif command['job'] == 'stop':
        # TODO: implement a stop command
        pass

    elif command['job'] == 'status':

        Logger.log.info('Status: %i process' % (len(routines)))
        n = 0
        for routine in routines:
            n += 1
            rhash = hash_routine(routine['command'])            
            statusstr = 'Status %i: running %s' % (n, rhash)            
            if 'start_time' in routine:
                statusstr = '%s %.2fs' % (
                    statusstr, time.time()-routine['start_time'])
            Logger.log.info(statusstr)

    elif command['job'] == 'reset':
        reset_program()
    
    elif command['job'] == 'upgrade':
        Logger.log.info(f'Upgrading Worker {command.get("version", "latest")}...')
        if os.name == 'nt':
            if not 'version' in command:
                send_command(r'venv\Scripts\python.exe -m pip install shareddata --upgrade')
            else:
                send_command(r'venv\Scripts\python.exe -m pip install shareddata==%s' % command['version'])
        elif os.name == 'posix':
            if not 'version' in command:
                send_command('venv/bin/python -m pip install shareddata --upgrade ')
            else:
                send_command('venv/bin/python -m pip install shareddata==%s' % command['version'])

        reset_program()

    elif command['job'] == 'ping':
        Logger.log.info('pong')

    elif command['job'] == 'pong':
        Logger.log.info('ping')

import hashlib
from pathlib import Path
import sys, json

def hash_file(path: Path, block_size: int = 1 << 16) -> str:
    """Return SHA-256 hex digest of *path* (or None if path is absent)."""
    if not path.is_file():
        return None
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(block_size), b""):
            h.update(chunk)
    return h.hexdigest()

def load_last_hash(venv_root: Path) -> str | None:
    """Read the stored hash (and optional metadata) from .last_requirements_hash."""
    f = venv_root / ".last_requirements_hash"
    if not f.is_file():
        return None
    try:
        blob = json.loads(f.read_text())
        return blob.get("req_hash")
    except Exception:
        # legacy / corrupted file?  fall back to raw text
        return f.read_text().strip()
    
def save_last_hash(venv_root: Path, new_hash: str):
    """Persist hash atomically in <venv>/.last_requirements_hash."""
    venv_root.mkdir(parents=True, exist_ok=True)          # ensure dir exists
    tmp = venv_root / ".last_requirements_hash.tmp"
    dst = venv_root / ".last_requirements_hash"
    tmp.write_text(json.dumps({"req_hash": new_hash}))
    tmp.replace(dst)                                      # atomic on POSIX


installed_repos = {}
install_lock = threading.Lock()

def install_repo(command, quiet=False):

    install = False
    if not command['repo'] in installed_repos:
        with install_lock:
            installed_repos[command['repo']] = {}
            installed_repo = installed_repos[command['repo']]
            installed_repo['isinstalling'] = True            
            install = True
    else:
        with install_lock:
            installed_repo = installed_repos[command['repo']]            
        while True:
            with install_lock:
                if not installed_repo['isinstalling']:
                   break
            time.sleep(1)
        
        with install_lock:
            installage = time.time() - installed_repo['ts']
            if installage > 5*60:
                installed_repo['isinstalling'] = True
                install = True

    if not install:
        return True
    
    if install:
        with install_lock:
            installed_repo['ts'] = time.time()

        if not quiet:
            Logger.log.info('Installing %s...' % (command['repo']))
        runroutine = False
        if ('GIT_USER' not in os.environ) or ('GIT_TOKEN' not in os.environ) or ('GIT_ACRONYM' not in os.environ):
            Logger.log.error('Installing repo %s ERROR missing git parameters'
                             % (command['repo']))
        else:

            hasbranch, requirements_path, repo_path, python_path, env = get_env(command)

            repo_exists = repo_path.is_dir()
            venv_exists = python_path.is_file()            

            # GIT_URL=os.environ['GIT_PROTOCOL']+'://'+os.environ['GIT_USER']+':'+os.environ['GIT_TOKEN']+'@'\
            #     +os.environ['GIT_SERVER']+'/'+os.environ['GIT_ACRONYM']+'/'+command['repo']
            GIT_URL = os.environ['GIT_PROTOCOL']+'://'+os.environ['GIT_SERVER']+'/' +\
                os.environ['GIT_ACRONYM']+'/'+command['repo']

            # GIT PULL OR GIT CLONE
            if repo_exists:
                if not quiet:
                    Logger.log.info('Pulling repo %s' % (command['repo']))
                requirements_lastmod = 0
                if requirements_path.is_file():
                    requirements_lastmod = os.path.getmtime(
                        str(requirements_path))

                # Checkout branch before pulling
                if hasbranch:
                    checkout_cmd = ['git', '-C', str(repo_path), 'checkout', command['branch']]
                    if not send_command(checkout_cmd):
                        Logger.log.error(f'Checking out branch {command["branch"]} FAILED!')
                        runroutine = False
                    else:
                        Logger.log.info(f'Checked out branch {command["branch"]}')

                # pull existing repo
                if hasbranch:
                    cmd = ['git', '-C', str(repo_path),'pull', GIT_URL, command['branch']]
                else:
                    cmd = ['git', '-C', str(repo_path), 'pull', GIT_URL]

                pull_trials = 0
                max_trials = 10
                while pull_trials < max_trials:
                    if not send_command(cmd):
                        pull_trials += 1
                        if pull_trials<max_trials:
                            Logger.log.warning(f'Pulling repo {command["repo"]} FAILED! Retrying {pull_trials}/{max_trials}...')
                        else:
                            Logger.log.error(f'Pulling repo {command["repo"]} ERROR!')
                        runroutine = False
                        time.sleep(15)
                    else:
                        runroutine = True
                        break
                
                if (runroutine) and (requirements_path.is_file()):
                    venv_root     = repo_path / "venv"
                    new_hash      = hash_file(requirements_path)
                    stored_hash   = load_last_hash(venv_root)
                    install_requirements = (
                        not venv_exists or
                        new_hash is None or
                        stored_hash is None or
                        new_hash != stored_hash                        
                    )                    
                    runroutine = True
                    if not quiet:
                        Logger.log.info('Pulling repo %s DONE!' %
                                        (command['repo']))
                else:
                    install_requirements = False
                    runroutine = False                    
                    Logger.log.error(
                        'Pulling repo %s ERROR: requirements.txt not found!' % (command['repo']))

            else:
                if not quiet:
                    Logger.log.info('Cloning repo %s...' % (command['repo']))
                if hasbranch:
                    cmd = ['git', '-C', str(repo_path.parents[0]), 'clone',
                           '-b', command['branch'], GIT_URL, str(repo_path)]
                else:
                    cmd = ['git', '-C',
                           str(repo_path.parents[0]), 'clone', GIT_URL]
                if not send_command(cmd):
                    Logger.log.error('Cloning repo %s ERROR!' %
                                     (command['repo']))
                    runroutine = False
                else:
                    runroutine = True
                    if requirements_path.is_file():
                        install_requirements = True
                        if not quiet:
                            Logger.log.info('Cloning repo %s DONE!' %
                                            (command['repo']))
                    else:
                        install_requirements = False
                        Logger.log.error(
                            'Cloning repo %s ERROR: requirements.txt not found!' % (command['repo']))

            # TODO: ALLOW FOR PYTHON VERSION SPECIFICATION
            # CREATE VENV
            if (runroutine) and (not venv_exists):
                if not quiet:
                    Logger.log.info('Creating venv %s...' % (command['repo']))
                if not send_command(['python', '-m', 'venv', str(repo_path/'venv')]):
                    Logger.log.error('Creating venv %s ERROR!' %
                                     (command['repo']))
                    runroutine = False
                else:
                    runroutine = True
                    if requirements_path.is_file():
                        install_requirements = True
                        if not quiet:
                            Logger.log.info('Creating venv %s DONE!' %
                                            (command['repo']))
                    else:
                        install_requirements = False
                        Logger.log.error(
                            'Creating venv %s ERROR: requirements.txt not found!' % (command['repo']))

            # INSTALL REQUIREMENTS
            if (runroutine) and (install_requirements):
                if not quiet:
                    Logger.log.info('Installing requirements %s...' %
                                    (command['repo']))
                if not send_command([str(python_path), '-m', 'pip', 'install', '-r', str(requirements_path)], env=env):
                    Logger.log.error(
                        'Installing requirements %s ERROR!' % (command['repo']))
                    runroutine = False
                else:
                    runroutine = True
                    if not quiet:
                        Logger.log.info('Installing requirements %s DONE!' %
                                        (command['repo']))                        

        if runroutine:
            if install_requirements:
                venv_root = repo_path / "venv"
                new_hash = hash_file(requirements_path)
                save_last_hash(venv_root, new_hash)
            if not quiet:
                Logger.log.info('Installing %s DONE!' % (command['repo']))
        else:
            Logger.log.error('Installing %s ERROR!' % (command['repo']))

        with install_lock:
            if runroutine:
                installed_repo['ts'] = time.time()
            else:
                installed_repo['ts'] = time.time() - 5*60
            installed_repo['isinstalling'] = False
            
        return runroutine

import base64
import bson

def run_routine(command, routine, quiet=False):
    if not quiet:
        Logger.log.info('Running routine %s/%s' %
                        (command['repo'], command['routine']))

    installed = True
    if command['repo'] != 'SharedData':
        installed = install_repo(command, quiet=quiet)

    if installed:
        # RUN ROUTINE
        if not quiet:
            Logger.log.info('Starting process %s/%s...' %
                            (command['repo'], command['routine']))

        hasbranch, requirements_path, repo_path, python_path, env = get_env(
            command)

        if command['repo'] == 'SharedData':
            cmd = [str(python_path), '-m',
                   str('SharedData.'+command['routine'])]
        else:
            cmd = [str(python_path), str(repo_path/command['routine'])]

        if 'args' in command:
            if isinstance(command['args'], dict):
                bson_data = bson.BSON.encode(command['args'])
                b64_arg = base64.b64encode(bson_data).decode('ascii')
                cmd += ['--bson', b64_arg]
            else:
                _args = command['args'].split(' ')
                if isinstance(_args, (list, tuple)):
                    cmd += _args
                else:
                    cmd += [command['args']]
        
        if 'hash' in routine:
            cmd += ['--hash', routine['hash']]
            status_msg = {
                'date': routine['date'],
                'hash': routine['hash'],
                'status': 'RUNNING',                
            }            
            ClientAPI.post_collection(
                'Text','RT','WORKERPOOL','JOBS',
                value=status_msg
            ) 

        routine['subprocess'] = subprocess.Popen(
            cmd, env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, text=True
        )
        routine['pid'] = routine['subprocess'].pid
        routine['process'] = psutil.Process(routine['pid'])

        # read stdout and stderr in separate threads
        stdout_thread = threading.Thread(
            target=read_stdout, args=(routine['subprocess'].stdout,True))
        stderr_thread = threading.Thread(
            target=read_stderr, args=(routine['subprocess'].stderr,True, routine))
        stdout_thread.start()
        stderr_thread.start()
        routine['stdout_thread'] = stdout_thread
        routine['stderr_thread'] = stderr_thread

        if not quiet:
            Logger.log.info('Starting process %s/%s DONE!' %
                            (command['repo'], command['routine']))
    else:
        Logger.log.error(
            'Aborting routine %s, could not install repo' % (command['routine']))

def kill_routine(command, routines):    
    success = True

    def attempt_termination(proc):        
        try:             
            if proc is None:                
                return True                   
            if proc.is_running():
                proc.terminate()  # Send SIGTERM
                try:
                    proc.wait(timeout=15)
                    return True
                except psutil.TimeoutExpired:
                    try:
                        proc.kill()  # Force kill
                        proc.wait(timeout=5)
                        return True
                    except psutil.TimeoutExpired:
                        # Process is still running after force kill, give up
                        Logger.log.error(f"Failed to terminate process with PID {proc.pid} after force kill")
                        return False
            else:
                return True
            
        except psutil.NoSuchProcess:  # Process already terminated
            return True
        except Exception as e:
            Logger.log.error(f"Failed to terminate process with PID {proc.pid}: {str(e)}")
            return False
        
    if command['repo'] == 'ALL':
        Logger.log.info('Kill: ALL...')
        for routine in routines:
            if 'process' in routine:
                if not attempt_termination(routine['process']):
                    success = False                
        Logger.log.info('Kill: ALL DONE!')
    else:        
        for routine in routines:                        
            if compare_routines(routine['command'], command) and ('process' in routine):
                if not attempt_termination(routine['process']):
                    success = False    

    return success

def remove_finished_routines(routines):
    new_routines = []
    for routine in routines:
        remove_routine = False
        
        if 'process' in routine and routine['process'] is not None:
            is_running = False
            try:
                if 'subprocess' in routine:
                    exit_code = routine['subprocess'].poll()
                    if (not exit_code is None) and (exit_code != 0):
                        stderr = ''
                        if 'stderr' in routine:
                            if len(routine['stderr']) > 1:
                                stderr = '\n'.join(routine['stderr'])
                            else:
                                stderr = routine['stderr'][0]
                        Logger.log.error('Routine %s/%s exited with code %s\n STDERR: %s' %
                                         (routine['command']['repo'], routine['command']['routine'], exit_code, stderr))
                is_running = routine['process'].is_running()
            except:
                pass
            if not is_running:
                remove_routine = True

        elif 'thread' in routine and not routine['thread'].is_alive():
            remove_routine = True

        if not remove_routine:
            new_routines.append(routine)

    return new_routines

def remove_finished_batch_jobs(batch_jobs):
    
    nfinished, nerror = 0, 0
    new_routines = []
    for routine in batch_jobs:
        remove_routine = False
        
        if 'process' in routine and routine['process'] is not None:
            is_running = False
            try:
                if 'subprocess' in routine:
                    exit_code = routine['subprocess'].poll()
                    if (not exit_code is None):
                        if (exit_code != 0):
                            nerror+=1
                            status_message = {
                                'date':routine['date'],
                                'hash':routine['hash'],
                                'status':'ERROR',
                                'exit_code':exit_code,                                
                            }
                            if 'stderr' in routine:
                                if len(routine['stderr']) > 1:
                                    status_message['stderr'] = '\n'.join(routine['stderr'])
                                else:
                                    status_message['stderr'] = routine['stderr'][0]
                            
                            if 'start_time' in routine:                                
                                status_message['run_time'] = time.time() - routine['start_time']
                                status_message['finish_time'] = pd.Timestamp.utcnow()


                            ClientAPI.post_collection(
                                'Text','RT','WORKERPOOL','JOBS',
                                value=status_message
                            )
                        else:
                            nfinished+=1
                            status_message = {
                                'date':routine['date'],
                                'hash':routine['hash'],
                                'status':'COMPLETED',
                            }
                            if 'start_time' in routine:                                
                                status_message['run_time'] = time.time() - routine['start_time']
                                status_message['finish_time'] = pd.Timestamp.utcnow()

                            ClientAPI.post_collection(
                                'Text','RT','WORKERPOOL','JOBS',
                                value=status_message
                            )

                is_running = routine['process'].is_running()
            except:
                pass
            if not is_running:
                remove_routine = True

        elif 'thread' in routine and not routine['thread'].is_alive():
            remove_routine = True

        if not remove_routine:
            new_routines.append(routine)
    
    return new_routines, nfinished, nerror

def reset_program():
    """Restarts the current program, with file objects and descriptors
       cleanup
    """
    Logger.log.info('restarting worker...')
    try:
        p = psutil.Process(os.getpid())
        children = p.children(recursive=True)
        for child in children:
            child.kill()

    except Exception as e:
        Logger.log.error('restarting worker ERROR!')
        Logger.log.error(e)

    python = sys.executable
    os.execl(python, python, *sys.argv)

def read_stdout(stdout, print_to_console=False, routine=None):
    try:
        while True:            
            out = stdout.readline()
            if out:
                if routine is not None:
                    if 'stdout' not in routine:
                        routine['stdout'] = []    
                    routine['stdout'].append(out)
                    
                if print_to_console:
                   print(out)
                else:
                    out = out.replace('\n', '')
                    if (out != ''):
                        Logger.log.debug('<-' + out)
            else:
                break
    except:
        pass

def read_stderr(stderr, print_to_console=False, routine=None):
    try:
        while True:
            err = stderr.readline()
            if err:
                if routine is not None:
                    if 'stderr' not in routine:
                        routine['stderr'] = []    
                    routine['stderr'].append(err)

                if print_to_console:
                    print(err)
                else:
                    err = err.replace('\n', '')
                    if (err != ''):
                        if ('INFO' in err):
                            Logger.log.info('<-'+err)
                        elif ('WARNING' in err):
                            Logger.log.warning('<-'+err)
                        elif ('ERROR' in err):
                            Logger.log.error('<-'+err)
                        elif ('CRITICAL' in err):
                            Logger.log.critical('<-'+err)
                        else:
                            Logger.log.debug('<-'+err)                            
            else:
                break
    except:
        pass

def send_command(command, env=None, blocking=True):
    if isinstance(command, (list, tuple)):
        _command = ' '.join(command)
    else:
        _command = command
    
    Logger.log.debug('->%s' % _command)
    
    if env is None:
        process = subprocess.Popen(_command,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   universal_newlines=True, shell=True)
    else:
        process = subprocess.Popen(_command,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   universal_newlines=True, shell=True, env=env)

    stdout_thread = threading.Thread(
        target=read_stdout, args=([process.stdout]))
    stderr_thread = threading.Thread(
        target=read_stderr, args=([process.stderr]))
    stdout_thread.start()
    stderr_thread.start()

    if blocking:
        process.wait()  # block until process terminated

    stdout_thread.join()
    stderr_thread.join()

    rc = process.returncode
    success = rc == 0
    if success:
        Logger.log.debug('DONE!->%s' % (_command))
        return True
    else:
        Logger.log.error('ERROR!->%s' % (_command))
        return False

def list_process():
    source_path = Path(os.environ['SOURCE_FOLDER'])
    procdict = {}
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=None)
            if len(pinfo['cmdline']) > 0:
                if str(source_path) in pinfo['cmdline'][0]:
                    procdict[proc.pid] = {'proc': proc, 'pinfo': pinfo}
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return procdict

def get_env(command):
    hasbranch = False
    if 'branch' in command:
        if command['branch'] != '':
            hasbranch = True

    if command['repo'] == 'SharedData':
        repo_path = Path(os.environ['SOURCE_FOLDER'])
    elif hasbranch:
        repo_path = Path(os.environ['SOURCE_FOLDER']) / \
            (command['repo']+'#'+command['branch'])
    else:
        repo_path = Path(os.environ['SOURCE_FOLDER'])/command['repo']

    requirements_path = repo_path/'requirements.txt'
    if os.name == 'posix':
        python_path = repo_path/'venv/bin/python'
    else:
        python_path = repo_path/'venv/Scripts/python.exe'

    env = os.environ.copy()
    env['VIRTUAL_ENV'] = str(repo_path/'venv')
    env['PATH'] = str(repo_path/'venv')+';' + \
        str(python_path.parents[0])+';'+env['PATH']
    env['PYTHONPATH'] = str(repo_path/'venv')+';'+str(python_path.parents[0])
    env['GIT_TERMINAL_PROMPT'] = "0"

    return hasbranch, requirements_path, repo_path, python_path, env

def start_server(port, nthreads):
    # run API server
    command = {
        "sender": "MASTER",
        "target": os.environ['USER_COMPUTER'],
        "job": "routine",
        "repo": "SharedData",
        "routine": "IO.ServerAPI",
        "args": f"--port {port} --nthreads {nthreads}"
    }
    start_time = time.time()
    routine = {
        'command': command,
        'thread': None,
        'process': None,
        'subprocess': None,
        'start_time': start_time,
    }
    run_routine(command, routine)

def start_logger():
    # run logger
    command = {
        "sender": "MASTER",
        "target": os.environ['USER_COMPUTER'],
        "job": "routine",
        "repo": "SharedData",
        "routine": "IO.ReadLogs",
    }
    start_time = time.time()
    routine = {
        'command': command,
        'thread': None,
        'process': None,
        'subprocess': None,
        'start_time': start_time,
    }
    run_routine(command, routine)

def start_schedules(schedule_names):    
    # run scheduler
    command = {
        "sender": "MASTER",
        "target": os.environ['USER_COMPUTER'],
        "job": "routine",
        "repo": "SharedData",
        "routine": "Routines.Scheduler",
        "args": schedule_names,
    }
    start_time = time.time()
    routine = {
        'command': command,
        'thread': None,
        'process': None,
        'subprocess': None,
        'start_time': start_time,
    }
    run_routine(command, routine)

def isrunning(command,routines):
    isrunning = False
    
    for routine in routines:
        if compare_routines(routine['command'], command):
            isrunning = True
            break

    return isrunning
