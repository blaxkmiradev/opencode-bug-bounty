#!/usr/bin/env python3
"""
Port Scanner
Usage: python port_scanner.py target.com
"""

import sys
import socket
import concurrent.futures

class PortScanner:
    def __init__(self, target):
        self.target = target
        self.open_ports = []
        
        # Common ports
        self.ports = [
            (21, 'FTP'), (22, 'SSH'), (23, 'Telnet'), (25, 'SMTP'),
            (53, 'DNS'), (67, 'DHCP'), (68, 'DHCP'), (69, 'TFTP'),
            (80, 'HTTP'), (110, 'POP3'), (111, 'RPC'), (119, 'NNTP'),
            (123, 'NTP'), (135, 'MSRPC'), (137, 'NetBIOS'), (138, 'NetBIOS'),
            (139, 'SMB'), (143, 'IMAP'), (161, 'SNMP'), (162, 'SNMP'),
            (389, 'LDAP'), (443, 'HTTPS'), (445, 'SMB'), (465, 'SMTPS'),
            (514, 'Syslog'), (515, 'LPD'), (587, 'SMTP'), (636, 'LDAPS'),
            (808, 'HTTP-Alt'), (993, 'IMAPS'), (995, 'POP3S'), (1433, 'MSSQL'),
            (1521, 'Oracle'), (1723, 'PPTP'), (3306, 'MySQL'), (3389, 'RDP'),
            (5432, 'PostgreSQL'), (5900, 'VNC'), (5901, 'VNC'), (5985, 'WinRM'),
            (5986, 'WinRM'), (6379, 'Redis'), (8000, 'HTTP-Alt'), (8080, 'HTTP-Proxy'),
            (8443, 'HTTPS-Alt'), (8888, 'HTTP-Alt'), (9000, 'SonarQube'), (9090, 'HTTP-Alt'),
            (27017, 'MongoDB'),
        ]
    
    def check_port(self, port, service):
        """Check a port"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        try:
            result = sock.connect_ex((self.target, port))
            sock.close()
            if result == 0:
                return (port, service)
        except:
            pass
        return None
    
    def scan(self, threads=100):
        """Scan ports"""
        print(f"[*] Scanning {self.target}...")
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            futures = {executor.submit(self.check_port, p, s): (p, s) for p, s in self.ports}
            
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result:
                    print(f"[+] Port {result[0]} open ({result[1]})")
                    self.open_ports.append(result)
        
        return self.open_ports


def main():
    if len(sys.argv) < 2:
        print("Usage: python port_scanner.py <target>")
        sys.exit(1)
    
    target = sys.argv[1]
    
    # Resolve hostname if needed
    try:
        ip = socket.gethostbyname(target)
        print(f"[*] Resolved {target} to {ip}")
    except:
        ip = target
    
    scanner = PortScanner(ip)
    scanner.scan()


if __name__ == "__main__":
    main()