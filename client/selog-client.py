import os
import socket
import requests
import time
from datetime import datetime, timedelta
from subprocess import check_output

URL = "http://10.33.12.210"
HOST_IP = socket.gethostbyname(socket.gethostname())
LOG_PATH = "/var/log/selog"
MESSAGE_LINE = 300
SHUTDOWN_MSG = "exiting on signal 15"
KERNEL_INIT_MSG = "kernel: Initializing cgroup subsys cpuset"


def last_down_time():
    output = check_output(['last', '-FR', 'reboot']).strip().split('\n')
    down_date = [d.split()[9:14] for d in output]
    last_down= down_date[0]
    for d in down_date:
        if d != last_down:
            last_down = d
            break
    str_down_time = ' '.join(last_down)
    down_time = datetime.strptime(str_down_time, '%c')
    return down_time


def secure():
    with open("/var/log/secure", "r") as f:
        lines = f.readlines()
        dump = ''.join(lines[-MESSAGE_LINE:])
    return dump


def httpd_error():
    with open("/var/log/httpd/error_log", "r") as f:
        lines = f.readlines()
        dump = ''.join(lines[-MESSAGE_LINE:])
    return dump


def httpd_access():
    with open("/var/log/httpd/access_log", "r") as f:
        lines = f.readlines()
        dump = ''.join(lines[-MESSAGE_LINE:])
    return dump
    

def var_log_messages():
    with open("/var/log/messages", "r") as f:
        lines = f.readlines()
        for i in range(len(lines)):
            if KERNEL_INIT_MSG in lines[i]:
                last_boot = i
        dump = ''.join(lines[last_boot-MESSAGE_LINE:last_boot])
    return dump


def sar(option='all'):
    if option == 'cpu':
        arg = ['-u', 'ALL']
    elif option == 'paging':
        arg = ['-B']
    elif option == 'io':
        arg = ['-b']
    elif option == 'device':
        arg = ['-d']
    elif option == 'hugepage':
        arg = ['-H']
    elif option == 'queue':
        arg = ['-q']
    elif option == 'memorypage':
        arg = ['-R']
    elif option == 'memory':
        arg = ['-r']
    elif option == 'swap':
        arg = ['-S']
    elif option == 'files':
        arg = ['-v']
    elif option == 'swapping':
        arg = ['-W']
    elif option == 'task':
        arg = ['-w']
    elif option == 'tty':
        arg = ['-y']
    # -n keyword | ALL
    elif option == 'network':
        arg = ['-n']
    else:
        arg = ['-A']

    dump = []
    d = datetime.today()
    e_time = last_down_time()
    s_time = e_time - timedelta(hours=1)
    time_slice_args = ['-s', s_time.strftime('%H:%M:%S'), '-e', e_time.strftime('%H:%M:%S')]
    
    date = d.strftime('%d')
    command = ['sar', '-f', '/var/log/sa/sa'+date] + arg + time_slice_args
    print('command : '+ ' '.join(command))
    dump = check_output(command)

    return dump

def is_irregular():
    """
    check (ir)regular shutdown
    """
    with open("/var/log/messages", "r") as f:
        lines = f.readlines()
        for i in range(len(lines)):
            if KERNEL_INIT_MSG in lines[i]:
                last_boot = i

        for line in lines[last_boot-5:last_boot]:
            if SHUTDOWN_MSG in line:
                if 'rsyslogd' in line:
                    return False

    return True
   

def save_file(logs):
    print('save logs:')
    now = time.strftime("%Y%m%dT%H%M%S")
    prefix = now + '-' + HOST_IP + '-'
    for k, v in logs.items():
        filename = prefix + k + '.log'
        with open(os.path.join(LOG_PATH, filename), 'w') as f:
            f.write(v)
            print(filename)
    return prefix


if __name__ == '__main__':
    if is_irregular():
        logs = dict()
        logs['var_log_messages'] = var_log_messages()
        logs['sar_all'] = sar()
        logs['httpd_access'] = httpd_access()
        logs['httpd_error'] = httpd_error()
        logs['prefix'] = save_file(logs)
        requests.post(URL+'/collect', json=logs)
        print('send your logs '+URL)

    else:
        print('your last shutdown is normal')

