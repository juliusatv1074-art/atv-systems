#!/usr/bin/env python3

import subprocess

def show_ip():
    try:
        result = subprocess.run(["ip", "a"], capture_output=True, text=True, check=True)
        lines = result.stdout.splitlines()

        ip_address = "Unknown"
        
        for line in lines:
            if "inet" in line and "brd" in line:
                parts = line.split()
                ip_address = parts[1].split("/")[0]
                break

        print()
        print("=================")
        print("IP Address")
        print("=================")
        print(ip_address)

        return ip_address
    
    except Exception as e:
        print(f'Error getting IP: {e}')
        return "Unknown"


def check_network():
    try:
        result = subprocess.run(["systemctl", "status", "NetworkManager"], capture_output=True, text=True)
        net_manager = result.stdout

        print()
        print("=================")
        print("NetworkManager")
        print("=================")

        if "active (running)" in net_manager:
            print("Status: RUNNING")
            return "RUNNING"
        else:
            print("Status: NOT RUNNING")
            return "NOT RUNNING"
    except Exception as e:
        print(f'Error checking Network: {e}')
        return "ERROR"

def check_firewall():
    try:
        result = subprocess.run(["sudo", "-n", "ufw", "status"], capture_output=True, text=True)

        print()
        print("=================")
        print("Firewall")
        print("=================")

        if result.returncode != 0:
            print("Status: COULD NOT CHECK")
            print(result.stderr.strip())
            return "ERROR"

        if "Status: active" in result.stdout:
            print("Status: ACTIVE")
            return "ACTIVE"
        
        print("Status: INACTIVE")
        return "INACTIVE"
    
    except Exception as e:
        print(f'Error checking firewall: {e}')
        return "ERROR"

def show_ports():
    try:
        result = subprocess.run(["ss", "-tuln"], capture_output=True, text=True, check =True)
        ports = result.stdout.splitlines()

        port_count = 0

        print()
        print("=================")
        print("Listening Ports")
        print("=================")

        for port in ports:
            if  "LISTEN" in port:
                print(port)
                port_count +=1
   
        print("\nTotal Ports:", port_count)

        return port_count
    except Exception as e:
        print(f'Error showing ports: {e}')
        return 0

def ping_google():
    try:
        result = subprocess.run(["ping", "-c", "4", "8.8.8.8"], capture_output=True, text=True)
        ping_G = result.stdout.splitlines()

        print()

        for ping in ping_G:
            if "packet loss" in ping:
                print("Result:", ping.strip())
            if "rtt" in ping:
                parts = ping.split("/")
                print("Average Latency:",parts[4], "ms")

        if "0% packet loss" in result.stdout:
            print("Connection: HEALTHY")
            return "HEALTHY"
        else:
            print("WARNING: Connection Problems")
            return "Connection Problems"
    except Exception as e:
        print(f'Error pinging: {e}')
        return "ERROR"

def scan_process():
    try:
        result = subprocess.run(["ps", "aux"], capture_output=True, text=True)
        scanner = result.stdout.splitlines()
        dangerous = ["telnet", "ftp","ncat", "netcat"]
        found = []

        print()
    
        for scan in scanner:
            for threat in dangerous:
                if threat in scan.lower() and threat not in found:
                    found.append(threat)

        if len(found) == 0:
            print("No dangerous processes found")
        else:
            for item in found:
                print("WARNING:", item)

        return found
    except Exception as e:
        print(f'Error scanning processes: {e}')
        return []

def save_report(ip, firewall, network, ports, ping, processes):
    with open("report.txt", "w") as f:
        f.write(f"IP Address: {ip}\n")
        f.write(f"Firewall: {firewall}\n")
        f.write(f"Checking Network: {network}\n")
        f.write(f"Show Ports: {ports}\n")
        f.write(f"Ping Google: {ping}\n")
        f.write(f"Scanning Running Processes: {processes}\n")
    
    print("\nReport saved to report.txt")

def show_summary():
    ip = show_ip()
    network = check_network()
    firewall = check_firewall()
    ports = show_ports()
    ping = ping_google()
    scan = scan_process()

    print("\n==============================")
    print(" System Health Report")
    print("==============================")
    print(f"IP Address: {ip}")
    print(f"Network: {network}")
    print(f"Firewall: {firewall}")
    print(f"Open Ports: {ports}")
    print(f"Ping: {ping}")
    print(f"Dangerous Processes: {len(scan)}")

    if firewall == "ACTIVE" and network == "RUNNING" and ping == "HEALTHY" and len(scan) == 0:
        print("Overall Status: SYSTEM HEALTHY")
    else:
        print("Overall Status: SYSTEM NEEDS ATTENTION")

    save_report(ip, firewall, network, ports, ping, scan)
    
def main():
    choice = ""

    while choice != "7":
        print("\nMenu")
        print("1. Show IP Address")
        print("2. Check NetworkManager")
        print("3. Check Firewall")
        print("4. Show Open Ports")
        print("5. Ping Google")
        print("6. Scan Running Processes")
        print("7. Generate report and Exit")
    
        choice = input("Choose: ")
    
        if choice == "1":
            show_ip()
        elif choice == "2":
            check_network()
        elif choice == "3":
            check_firewall()
        elif choice == "4":
            show_ports()
        elif choice == "5":
            ping_google()
        elif choice in "6":
            scan_process()
        elif choice == "7":
            show_summary()
            print("\nGoodbye Julius")
        else:
            print("Invalid choice. Enter a number from 1 to 7.")

if __name__ == "__main__":
    main()