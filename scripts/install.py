#!/usr/bin/env python3
"""
Bug Hunter - All-in-One Scanner
Usage: python bug_hunter.py target.com
"""

import sys
import requests
import urllib.parse
import socket
import concurrent.futures

class BugHunter:
    def __init__(self, target):
        self.target = target.replace('http://', '').replace('https://', '').split('/')[0]
        self.results = []
        self.port_results = []
        
        self.common_ports = [
            (21, 'FTP'), (22, 'SSH'), (23, 'Telnet'), (25, 'SMTP'),
            (53, 'DNS'), (80, 'HTTP'), (110, 'POP3'), (139, 'SMB'),
            (143, 'IMAP'), (443, 'HTTPS'), (445, 'SMB'), (993, 'IMAPS'),
            (995, 'POP3S'), (1433, 'MSSQL'), (3306, 'MySQL'),
            (3389, 'RDP'), (5432, 'PostgreSQL'), (5900, 'VNC'),
            (6379, 'Redis'), (8080, 'HTTP-Alt'), (8443, 'HTTPS-Alt'),
            (27017, 'MongoDB')
        ]
        
    def check_tcp_port(self, port, service):
        """Check if port is open"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((self.target, port))
            sock.close()
            if result == 0:
                return (port, service)
        except:
            pass
        return None
    
    def scan_ports(self, threads=50):
        """Quick port scan"""
        print(f"[*] Scanning ports on {self.target}...")
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            futures = {
                executor.submit(self.check_tcp_port, port, service): (port, service)
                for port, service in self.common_ports
            }
            
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result:
                    print(f"[+] Port open: {result[0]} ({result[1]})")
                    self.port_results.append(result)
        
        return self.port_results
    
    def check_http(self):
        """Check HTTP services"""
        print(f"[*] Checking HTTP at {self.target}...")
        
        urls = [
            f"http://{self.target}",
            f"https://{self.target}",
            f"http://{self.target}/admin",
            f"https://{self.target}/admin",
        ]
        
        for url in urls:
            try:
                r = requests.get(url, timeout=5, verify=False, allow_redirects=True)
                if r.status_code < 400:
                    print(f"[+] Found: {url} (Status: {r.status_code})")
                    self.results.append({'url': url, 'status': r.status_code})
                    
                    # Check for interesting headers
                    if 'server' in r.headers:
                        print(f"    Server: {r.headers['server']}")
                    if 'x-powered-by' in r.headers:
                        print(f"    X-Powered-By: {r.headers['x-powered-by']}")
            except Exception as e:
                pass
        
        return self.results
    
    def check_subdomains(self):
        """Check common subdomains"""
        print(f"[*] Checking subdomains...")
        
        subs = ['www', 'mail', 'ftp', 'admin', 'api', 'dev', 'test', 'staging']
        
        for sub in subs:
            domain = f"{sub}.{self.target}"
            try:
                ip = socket.gethostbyname(domain)
                print(f"[+] Found subdomain: {domain} -> {ip}")
                self.results.append({'subdomain': domain, 'ip': ip})
            except:
                pass
    
    def check_common_vulns(self):
        """Check for common vulnerabilities"""
        print(f"[*] Checking common vulnerabilities...")
        
        paths = [
            '/.git/config',
            '/.env',
            '/wp-config.php',
            '/phpinfo.php',
            '/server-status',
            '/actuator/env',
            '/debug',
            '/api/debug',
            '/admin',
            '/phpmyadmin',
            '/.DS_Store',
            '/.svn/entries',
            '/.hg/',
        ]
        
        for path in paths:
            url = f"http://{self.target}{path}"
            try:
                r = requests.get(url, timeout=5)
                if r.status_code == 200 and 'index' not in r.text.lower():
                    print(f"[+] Found: {path} (Status: {r.status_code})")
                elif r.status_code == 200:
                    print(f"[?] Found: {path} but needs auth")
            except:
                pass
    
    def check_tech(self):
        """Detect technologies"""
        print(f"[*] Detecting technologies...")
        
        url = f"http://{self.target}"
        try:
            r = requests.get(url, timeout=10, verify=False)
            text = r.text.lower()
            
            # Check for technologies
            tech = []
            if 'wordpress' in text:
                tech.append('WordPress')
            if 'drupal' in text:
                tech.append('Drupal')
            if 'joomla' in text:
                tech.append('Joomla')
            if 'react' in text or 'reactjs' in text:
                tech.append('React')
            if 'vue' in text:
                tech.append('Vue.js')
            if 'angular' in text:
                tech.append('Angular')
            if 'nginx' in r.headers.get('server', '').lower():
                tech.append('Nginx')
            if 'apache' in r.headers.get('server', '').lower():
                tech.append('Apache')
            if 'cloudflare' in r.headers.get('server', '').lower():
                tech.append('CloudFlare')
            
            if tech:
                print(f"[+] Technologies: {', '.join(tech)}")
            
            return tech
        except:
            pass
        
        return []
    
    def full_scan(self):
        """Run full scan"""
        print("="*50)
        print(f"Bug Hunter - Scanning {self.target}")
        print("="*50)
        
        self.scan_ports()
        self.check_subdomains()
        self.check_http()
        self.check_tech()
        self.check_common_vulns()
        
        print("\n" + "="*50)
        print("SCAN COMPLETE")
        print("="*50)
        
        return self.results


def main():
    if len(sys.argv) < 2:
        print("Usage: python bug_hunter.py <target>")
        print("Example: python bug_hunter.py example.com")
        sys.exit(1)
    
    target = sys.argv[1]
    hunter = BugHunter(target)
    hunter.full_scan()


if __name__ == "__main__":
    main()