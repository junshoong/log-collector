import os
import socket
import requests
from subprocess import check_output

URL = "http://10.33.12.210"
KERNEL_INIT_MSG = "kernel: Initializing cgroup subsys cpuset"
SHUTDOWN_MSG = "exiting on signal 15"
MESSAGE_LINE = 300


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
   

if __name__ == '__main__':
    if check_regular():
        logs = dict()
        logs['var_log_messages'] = var_log_messages()
        logs['sar_cpu'] = sar_cpu()
        logs['sae_all'] = sar_all()
        requests.post(URL+'/collect', json=logs)
        print('your log send', URL)

    else:
        print('your last shutdown is regular')

