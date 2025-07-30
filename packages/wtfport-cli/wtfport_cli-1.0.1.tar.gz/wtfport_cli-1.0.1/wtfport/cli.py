#!/usr/bin/env python3

import sys
import os
import datetime
import psutil

def human_time(seconds):
    return str(datetime.timedelta(seconds=int(seconds)))

def find_process_using_port(port):
    for conn in psutil.net_connections(kind='inet'):
        if conn.laddr and conn.laddr.port == port and conn.status == 'LISTEN':
            pid = conn.pid
            if pid:
                try:
                    proc = psutil.Process(pid)
                    cmd = ' '.join(proc.cmdline()) or proc.name()
                    uptime = datetime.datetime.now().timestamp() - proc.create_time()
                    return {
                        "pid": pid,
                        "name": proc.name(),
                        "cmd": cmd,
                        "uptime": human_time(uptime)
                    }
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
    return None

def main():
    if len(sys.argv) != 2 or not sys.argv[1].isdigit():
        print("Usage: wtfport <port_number>")
        sys.exit(1)

    port = int(sys.argv[1])

    if port < 1024 and os.geteuid() != 0:
        print(f"Port {port} may require root access. Try running with sudo.")
        sys.exit(0) 

    info = find_process_using_port(port)

    if info:
        print(f"Port {port} is being used by '{info['cmd']}' (PID {info['pid']}) for {info['uptime']}.")
    else:
        print(f"WOW! Nothing on {port}, it's free!")

if __name__ == "__main__":
    main()
