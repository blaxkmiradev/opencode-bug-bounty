#!/usr/bin/env python3
"""
Fast Recon Tool - All-in-One Scanner  
Usage: python fast_scanner.py target.com
"""

import sys
import socket
import requests
import concurrent.futures
import urllib.parse

class FastRecon:
    def __init__(self, target):
        self.target = target
        self.results = []
        
        # Common subdomains
        self.subdomains = ['www', 'mail', 'ftp', 'admin', 'api', 'dev', 'test', 'staging', 'blog', 'shop', 'secure', 'cdn', 'static', 'app', 'portal', 'webmail']
        
        # Common ports
        self.ports = [(80, 'HTTP'), (443, 'HTTPS'), (22, 'SSH'), (21, 'FTP'), (25, 'SMTP'), (3306, 'MySQL'), (5432, 'PostgreSQL'), (6379, 'Redis'), (27017, 'MongoDB')]
        
        # Common paths
        self.paths = ['/admin', '/login', '/dashboard', '/wp-admin', '/phpmyadmin', '/api', '/config', '/.git', '/.env', '/server-status']
    
    def check_port(self, port, service):
        """Check port"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        try:
            result = sock.connect_ex((self.target, port))
            if result == 0:
                return (port, service)
        except:
            pass
        return None
    
    def check_path(self, path):
        """Check path"""
        url = f'http://{self.target}{path}'
        try:
            r = requests.get(url, timeout=3)
            if r.status_code < 400:
                return (path, r.status_code)
        except:
            pass
        return None
    
    def check_subdomain(self, sub):
        """Check subdomain"""
        domain = f"{sub}.{self.target}"
        try:
            ip = socket.gethostbyname(domain)
            return (domain, ip)
        except:
            pass
        return None
    
    def check_tech(self):
        """Check technologies"""
        url = f'http://{self.target}'
        try:
            r = requests.get(url, timeout=5)
            headers = dict(r.headers)
            server = headers.get('Server', '')
            powered = headers.get('X-Powered-By', '')
            return server, powered
        except:
            pass
        return None, None
    
    def scan(self, threads=50):
        """Run fast scan"""
        print(f"[*] Fast recon on {self.target}")
        print("=" * 40)
        
        # 1. Port scan
        print("\n[*] Port scan...")
        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            futures = [executor.submit(self.check_port, p, s) for p, s in self.ports]
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result:
                    print(f"[+] Port {result[0]} open ({result[1]})")
                    self.results.append(result)
        
        # 2. Path scan
        print("\n[*] Path scan...")
        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            futures = [executor.submit(self.check_path, p) for p in self.paths]
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result:
                    print(f"[+] Found: {result[0]} ({result[1]})")
                    self.results.append(result)
        
        # 3. Subdomain check
        print("\n[*] Subdomain check...")
        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            futures = [executor.submit(self.check_subdomain, s) for s in self.subdomains]
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result:
                    print(f"[+] Subdomain: {result[0]} -> {result[1]}")
                    self.results.append(result)
        
        # 4. Tech detection
        print("\n[*] Tech detection...")
        server, powered = self.check_tech()
        if server:
            print(f"[+] Server: {server}")
        if powered:
            print(f"[+] X-Powered-By: {powered}")
        
        print("\n" + "=" * 40)
        print(f"[+] Scan complete: {len(self.results)} findings")
        
        return self.results


def main():
    if len(sys.argv) < 2:
        print("Usage: python fast_scanner.py <target>")
        sys.exit(1)
    
    target = sys.argv[1]
    scanner = FastRecon(target)
    scanner.scan()


if __name__ == "__main__":
    main()