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

greeting = ("-" * 60 + "\n" +
            "Welcome to the Port Scanner!\n" +
            "-" * 60 + "\n" +
            "Please, follow this input format: [IP1 - IP2], [IP/mask], [IP]...\n" +
            "Type 'quit' for exit")
print(greeting)


program_running = True

while program_running:

    try:
        ip_string = input("Enter range of ip intervals(remote host names): ").strip()
        if ip_string == 'quit':
            program_running = False
            break
        ip_range = list(ps.get_ip_range(ip_string))
        port_string = input("Enter port(s) to scan: ")
        if port_string == 'quit':
            program_running = False
            break
        port_range = list(ps.get_port_range(port_string))
    except KeyboardInterrupt:
        sys.exit()
    except:
        print("Error. Wrong input.")
        continue

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
        print("An error occured during scanning")
        continue
