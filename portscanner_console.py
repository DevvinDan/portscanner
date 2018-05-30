#!/usr/bin/env python
import portscanner
import subprocess
import sys
import socket
from datetime import datetime


ps = portscanner.PortScanner()

# Clear the console
subprocess.call('clear', shell=True)

# Input IPs and ports to scan

try:
    ip_string = input("Enter range of ip intervals(remote host names): ")
    ip_range = list(ps.get_ip_range(ip_string))
    port_string = input("Enter port(s) to scan: ")
    port_range = list(ps.get_port_range(port_string))
except:
    print("Error. Wrong input.")
    sys.exit()

try:
    for ip in ip_range:
        print("-" * 60)
        print("Please wait, scanning remote host", ip)
        print("-" * 60)

        # Measure scanning time
        t1 = datetime.now()

        for port in port_range:
            port_is_open = ps.scan_port(ip, port)
            if port_is_open:
                print("Port {} is open. Service: {}".format(port, ps.get_service_name(port)))

        t2 = datetime.now()
        print("Scanning completed in {}".format(t2 - t1))
except Exception as e:
    print(e)
