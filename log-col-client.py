import os
import socket
from subprocess import check_output

host_ip = socket.gethostbyname(socket.gethostname())
KERNEL_INIT_MSG = "Initializing cgroup subsys cpuset"


def var_log_messages():
    with open("/var/log/messages","r") as f:
        dump = f.read()
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

    with open("/var/log/messages","r") as f:
        lines = f.readlines()
        for line in lines:
            if KERNEL_INIT_MSG in line:
                print(line)

    
    return False

   
if __name__ == '__main__':
    if check_regular():
        print(var_log_messages())
        print(sar_cpu())
        print(sar_all())
    else:
        print('your last shutdown is regular')
