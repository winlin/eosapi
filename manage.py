#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import ujson as json
import time
import socket
import fcntl
import struct
import signal
import subprocess
from ipabase import read_json_conf

SD_CONF_FILE = 'main.cfg'

KILL_SIGNAL = '-15'
FORCE_KILL_SIGNAL = '-9'

#PYTHON3 = '/usr/bin/python3'
PYTHON3 = 'python3'

def usage():
    if len(sys.argv) != 2:
        print('*' * 80)
        print('Usage:', sys.argv[0], 'run|start|stop|restart|forcestop|forcerestart') 
        print('*' * 80)
        sys.exit(1)
    
def exec_shell(shell_cmd):
    try:
        print('Run cmd:', shell_cmd)
        result = subprocess.call(shell_cmd, shell=True)
        print('Result:', result)
        return result
    except Exception as e:
        print(e)
    return 1

def get_interface_ip(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s',
                            ifname[:15]))[20:24])

def run(sandbox_conf):
    run_cmd = "cd %s && %s main.py --port=%d --address=%s --debug=True --logging=debug --log_path=%s --conf_file=%s" % (
        sandbox_conf['pwd'],
        PYTHON3,
        sandbox_conf['port'][0],
        '127.0.0.1', #get_interface_ip('eth0'),
        sandbox_conf['log_path'],
        os.path.abspath(SD_CONF_FILE) 
    )
    exec_shell(run_cmd)

def start(sandbox_conf):
    for port in sandbox_conf['port']:
        start_cmd = "cd %s && nohup %s main.py --port=%d --address=%s --logging=%s --log_path=%s --debug=%s --conf_file=%s > /dev/null 2>&1 &" % (
            sandbox_conf['pwd'],
            PYTHON3,
            port,
            sandbox_conf['address'],
            sandbox_conf['logging'],
            sandbox_conf['log_path'],
            sandbox_conf['debug'],
            os.path.abspath(SD_CONF_FILE) 
        )
        result = exec_shell(start_cmd)

def stop(sandbox_conf, kill_signal=FORCE_KILL_SIGNAL):
    for port in sandbox_conf['port']:
        stop_cmd = ''' ps aux | grep "port=%d" | grep "python" | awk '{print $2}' | xargs rkill %s''' % (port, kill_signal)
        exec_shell(stop_cmd)
        stop_cmd = ''' ps aux | grep "port=%d" | grep "python" | awk '{print $2}' | xargs kill %s''' % (port, kill_signal)
        exec_shell(stop_cmd)

def restart(sandbox_conf):
    stop(sandbox_conf)
    time.sleep(5)
    start(sandbox_conf)
    
def handle_action(action_str):
    sandbox_conf = read_json_conf(SD_CONF_FILE)
    if not sandbox_conf:
        print('Not existed or file empty:', SD_CONF_FILE)
        return False
    
    if len(sandbox_conf['port']) == 0:
        print('PORT needed')
        return False
    sandbox_conf['pwd'] = os.path.abspath(os.curdir)
    if action_str == 'run':
        run(sandbox_conf)
    elif action_str == 'start':
        start(sandbox_conf)
    elif action_str == 'stop':
        stop(sandbox_conf, KILL_SIGNAL)
    elif action_str == 'restart':
        stop(sandbox_conf, KILL_SIGNAL)
        time.sleep(2)
        start(sandbox_conf)
    elif action_str == 'forcestop':
        stop(sandbox_conf, FORCE_KILL_SIGNAL)
    elif action_str == 'forcerestart':
        stop(sandbox_conf, FORCE_KILL_SIGNAL)
        time.sleep(2)
        start(sandbox_conf)
    else:
        print('Unsupport cmd:', action_str)
        return False
    return True
        
#############################################################################
if __name__ == "__main__":
    usage()
    
    # signal handler
    def sig_handler(sig, frame):
       handle_action('stop')

    signal.signal(signal.SIGTERM, sig_handler)
    signal.signal(signal.SIGINT, sig_handler)
    
    if handle_action(sys.argv[1]):
        sys.exit(0)
    else:
        sys.exit(1)
    
