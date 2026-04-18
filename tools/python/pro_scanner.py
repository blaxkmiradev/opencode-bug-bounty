#!/usr/bin/env python3
"""
Bug Hunter Pro - Advanced Vulnerability Scanner
Usage: python pro_scanner.py target.com
"""

import sys
import requests
import concurrent.futures
import socket
import time
from datetime import datetime

class ProScanner:
    def __init__(self, target):
        self.target = target
        self.results = []
        self.findings = {'critical': [], 'high': [], 'medium': [], 'low': [], 'info': []}
        
    def check_port(self, port, service):
        """Check port status"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((self.target, port))
            sock.close()
            if result == 0:
                return (port, service)
        except:
            pass
        return None
    
    def check_tech(self):
        """Fingerprint technologies"""
        url = f"https://{self.target}" if not self.target.startswith('http') else self.target
        try:
            r = requests.get(url, timeout=10, verify=False)
            headers = dict(r.headers)
            
            # Server detection
            server = headers.get('Server', 'Unknown')
            powered = headers.get('X-Powered-By', '')
            
            return {'server': server, 'powered': powered, 'status': r.status_code}
        except Exception as e:
            return None
    
    def check_security_headers(self):
        """Check security headers"""
        url = f"https://{self.target}" if not self.target.startswith('http') else self.target
        try:
            r = requests.get(url, timeout=10, verify=False)
            headers = dict(r.headers)
            
            security = {
                'CSP': headers.get('Content-Security-Policy', None),
                'HSTS': headers.get('Strict-Transport-Security', None),
                'X-Frame': headers.get('X-Frame-Options', None),
                'X-Content': headers.get('X-Content-Type-Options', None),
                'Referrer': headers.get('Referrer-Policy', None),
                'Permissions': headers.get('Permissions-Policy', None),
            }
            return security
        except:
            return None
    
    def check_common_vulns(self):
        """Check common vulnerabilities"""
        url = f"https://{self.target}"
        paths = [
            '/.git/config', '.env', '/wp-config.php', '/phpinfo.php',
            '/server-status', '/actuator/env', '/debug', '/admin',
            '/phpmyadmin', '/.DS_Store', '/.svn/entries'
        ]
        
        found = []
        for path in paths:
            try:
                r = requests.get(url + path, timeout=5, verify=False)
                if r.status_code == 200:
                    found.append(path)
            except:
                pass
        return found
    
    def test_xss(self):
        """Quick XSS test"""
        url = f"https://{self.target}"
        if '?' in url:
            try:
                test_url = url + "?q=<script>alert(1)</script>"
                r = requests.get(test_url, timeout=5, verify=False)
                if '<script>alert(1)</script>' in r.text:
                    return True
            except:
                pass
        return False
    
    def test_sqli(self):
        """Quick SQLi test"""
        url = f"https://{self.target}"
        if '?' in url:
            try:
                test_urls = [
                    url + "?id=' OR '1'='1",
                    url + "?id=1' OR 1=1--"
                ]
                for test_url in test_urls:
                    r = requests.get(test_url, timeout=5, verify=False)
                    if 'sql' in r.text.lower() or 'error' in r.text.lower():
                        return True
            except:
                pass
        return False
    
    def subdomain_enum(self):
        """Enumerate common subdomains"""
        subs = ['www', 'mail', 'ftp', 'admin', 'api', 'dev', 'test', 'staging', 
                'blog', 'shop', 'cdn', 'static', 'backup', 'old', 'portal']
        
        found = []
        for sub in subs:
            domain = f"{sub}.{self.target}"
            try:
                ip = socket.gethostbyname(domain)
                found.append({'subdomain': domain, 'ip': ip})
            except:
                pass
        return found
    
    def scan(self, level='full'):
        """Run scan"""
        print(f"\n{'='*60}")
        print(f"  PRO SCANNER - {self.target}")
        print(f"  Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}\n")
        
        # Port scan
        if level in ['full', 'quick']:
            print("[*] Port Scan...")
            ports = [(80, 'HTTP'), (443, 'HTTPS'), (22, 'SSH'), (21, 'FTP'), 
                    (25, 'SMTP'), (3306, 'MySQL'), (5432, 'PostgreSQL'), (8080, 'HTTP-Alt')]
            
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                results = [executor.submit(self.check_port, p, s) for p, s in ports]
                for r in results:
                    result = r.result()
                    if result:
                        print(f"  [+] Port {result[0]} ({result[1]}) - OPEN")
                        self.findings['info'].append(f"Port {result[0]} ({result[1]})")
        
        # Tech fingerprint
        if level in ['full', 'quick']:
            print("\n[*] Tech Fingerprint...")
            tech = self.check_tech()
            if tech:
                print(f"  [+] Server: {tech['server']}")
                print(f"  [+] Powered: {tech['powered']}")
                self.findings['info'].append(f"Server: {tech['server']}")
                self.findings['info'].append(f"Powered: {tech['powered']}")
        
        # Security headers
        if level in ['full', 'quick']:
            print("\n[*] Security Headers...")
            security = self.check_security_headers()
            if security:
                missing = sum(1 for v in security.values() if v is None)
                if missing > 0:
                    print(f"  [!] Missing: {missing} security headers")
                    for header, value in security.items():
                        if value is None:
                            print(f"      - {header}")
                            self.findings['medium'].append(f"Missing {header}")
                else:
                    print(f"  [+] Good: All security headers present")
        
        # Common vulns
        if level in ['full']:
            print("\n[*] Checking Common Files...")
            vulns = self.check_common_vulns()
            if vulns:
                print(f"  [!] Found: {len(vulns)} files")
                for v in vulns:
                    print(f"      - {v}")
                    self.findings['high'].append(f"Exposed: {v}")
        
        # Subdomains
        if level in ['full']:
            print("\n[*] Subdomain Enumeration...")
            subs = self.subdomain_enum()
            if subs:
                print(f"  [+] Found: {len(subs)} subdomains")
                for s in subs[:10]:
                    print(f"      - {s['subdomain']} -> {s['ip']}")
                    self.findings['info'].append(f"Subdomain: {s['subdomain']}")
        
        # Summary
        print(f"\n{'='*60}")
        print(f"  SCAN COMPLETE")
        print(f"{'='*60}")
        
        total = sum(len(v) for v in self.findings.values())
        print(f"\n  Total Findings: {total}")
        
        for level in ['critical', 'high', 'medium', 'low']:
            if self.findings[level]:
                print(f"    {level.upper()}: {len(self.findings[level])}")
        
        return self.findings


def main():
    if len(sys.argv) < 2:
        print("""
Bug Hunter Pro Scanner
=======================

Usage: python pro_scanner.py target.com [level]
Levels: quick, full (default: quick)

Examples:
  python pro_scanner.py example.com
  python pro_scanner.py example.com full
  
  python pro_scanner.py khmersamnang.com
  python pro_scanner.py anajak.cloud full
        """)
        sys.exit(1)
    
    target = sys.argv[1]
    level = sys.argv[2] if len(sys.argv) > 2 else 'quick'
    
    scanner = ProScanner(target)
    scanner.scan(level)


if __name__ == "__main__":
    main()