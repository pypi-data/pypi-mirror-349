#!/usr/bin/env python3

import sys
import os
import datetime
import psutil

# ANSI escape sequences for color
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"

def human_time(seconds):
    return str(datetime.timedelta(seconds=int(seconds)))

def find_processes_using_port(port):
    found = []
    seen_pids = set()
    try:
        for conn in psutil.net_connections(kind='inet'):
            if conn.laddr and conn.laddr.port == port and conn.status == psutil.CONN_LISTEN:
                pid = conn.pid
                if pid and pid not in seen_pids:
                    seen_pids.add(pid)
                    try:
                        proc = psutil.Process(pid)
                        cmd = ' '.join(proc.cmdline()) or proc.name()
                        uptime = datetime.datetime.now().timestamp() - proc.create_time()
                        found.append({
                            "pid": pid,
                            "name": proc.name(),
                            "cmd": cmd,
                            "uptime": human_time(uptime)
                        })
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue
    except psutil.AccessDenied:
        print(f"{RED}Access denied!. Try running as root.{RESET}")
        return None, True

    may_be_incomplete = os.geteuid() != 0
    return found, may_be_incomplete

def main():
    if len(sys.argv) != 2 or not sys.argv[1].isdigit():
        print(f"{YELLOW}Usage: wtfport <port_number>{RESET}")
        sys.exit(1)

    port = int(sys.argv[1])
    results, may_be_incomplete = find_processes_using_port(port)

    if results:
        print(f"{GREEN}Port {port} is being used by:{RESET}")
        for info in results:
            print(f"  {CYAN}• '{info['cmd']}' (PID {info['pid']}) running for {info['uptime']}{RESET}")
    elif may_be_incomplete:
        print(f"{YELLOW}Results may be incomplete. Try running with sudo to see all processes using port {port}.{RESET}")
    else:
        print(f"{GREEN}WOW! Nothing on {port}, it's free!{RESET}")

if __name__ == "__main__":
    main()
