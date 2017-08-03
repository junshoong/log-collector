import os
import socket
import requests
import time
from subprocess import check_output

URL = "http://10.33.12.210"
HOST_IP = socket.gethostbyname(socket.gethostname())
LOG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
MESSAGE_LINE = 300
SHUTDOWN_MSG = "exiting on signal 15"
KERNEL_INIT_MSG = "kernel: Initializing cgroup subsys cpuset"


def var_log_messages():
    with open("/var/log/messages", "r") as f:
        lines = f.readlines()
        for i in range(len(lines)):
            if KERNEL_INIT_MSG in lines[i]:
                last_boot = i
        dump = ''.join(lines[last_boot-MESSAGE_LINE:last_boot])
    return dump


def sar_cpu():
    dump = check_output(['sar', '-u', 'ALL'])
    return dump


def sar_all():
    dump = check_output(['sar', '-A'])
    return dump


def check_regular():
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
    if check_regular():
        logs = dict()
        logs['var_log_messages'] = var_log_messages()
        logs['sar_cpu'] = sar_cpu()
        logs['sar_all'] = sar_all()
        logs['prefix'] = save_file(logs)
        requests.post(URL+'/collect', json=logs)
        print('send your logs '+URL)

    else:
        print('your last shutdown is normal')
