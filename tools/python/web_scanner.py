#!/usr/bin/env python3
"""
Web Vulnerability Scanner
Usage: python web_scanner.py https://target.com
"""

import sys
import requests
import urllib3
import concurrent.futures
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class WebScanner:
    def __init__(self, target):
        self.target = target.rstrip('/')
        self.findings = []
        self.session = requests.Session()
        
        self.checks = [
            ('SSL/TLS', self.check_ssl),
            ('CORS', self.check_cors),
            ('Clickjacking', self.check_clickjack),
            ('X-Frame-Options', self.check_xfo),
            ('CSP', self.check_csp),
            ('HSTS', self.check_hsts),
            ('Info Disclosure', self.check_info),
            (' TRACE', self.check_trace),
            ('Directory Listing', self.check_listing),
        ]
    
    def check_ssl(self):
        """Check SSL certificate"""
        try:
            r = requests.get(self.target.replace('http://', 'https://'), timeout=10, verify=False)
            if r.status_code == 200:
                return ('OK', 'SSL enabled')
        except:
            pass
        return ('WARNING', 'No SSL')
    
    def check_cors(self):
        """Check CORS configuration"""
        r = requests.get(self.target, timeout=10)
        acao = r.headers.get('Access-Control-Allow-Origin')
        if acao == '*':
            return ('MEDIUM', f'Wildcard origin: {acao}')
        elif acao:
            return ('INFO', f'CORS: {acao}')
        return ('OK', 'No CORS')
    
    def check_clickjack(self):
        """Check clickjacking protection"""
        r = requests.get(self.target, timeout=10)
        if r.headers.get('X-Frame-Options'):
            return ('OK', 'Protected')
        return ('MEDIUM', 'No X-Frame-Options')
    
    def check_xfo(self):
        """Check X-Frame-Options"""
        r = requests.get(self.target, timeout=10)
        xfo = r.headers.get('X-Frame-Options')
        if xfo:
            return ('OK', xfo)
        return ('MEDIUM', 'Missing')
    
    def check_csp(self):
        """Check Content Security Policy"""
        r = requests.get(self.target, timeout=10)
        csp = r.headers.get('Content-Security-Policy')
        if csp:
            return ('OK', 'CSP enabled')
        return ('LOW', 'No CSP')
    
    def check_hsts(self):
        """Check HSTS"""
        r = requests.get(self.target, timeout=10)
        hsts = r.headers.get('Strict-Transport-Security')
        if hsts:
            return ('OK', 'HSTS enabled')
        return ('LOW', 'No HSTS')
    
    def check_info(self):
        """Check information disclosure"""
        r = requests.get(self.target, timeout=10)
        info = []
        for header in ['Server', 'X-Powered-By', 'X-AspNet-Version']:
            if r.headers.get(header):
                info.append(f'{header}: {r.headers.get(header)}')
        if info:
            return ('LOW', ', '.join(info))
        return ('OK', 'No disclosure')
    
    def check_trace(self):
        """Check TRACE method"""
        try:
            r = requests.request('TRACE', self.target, timeout=5)
            if r.status_code == 200:
                return ('MEDIUM', 'TRACE enabled')
        except:
            pass
        return ('OK', 'TRACE disabled')
    
    def check_listing(self):
        """Check directory listing"""
        paths = ['/images/', '/js/', '/css/', '/backup/', '/logs/']
        for path in paths:
            r = requests.get(self.target + path, timeout=5)
            if r.status_code == 200 and 'Index' in r.headers.get('Content-Type', ''):
                return ('MEDIUM', f'Directory listing: {path}')
        return ('OK', 'No listing')
    
    def scan(self, threads=10):
        """Run full scan"""
        print(f"[*] Scanning {self.target}...")
        
        for name, check in self.checks:
            try:
                result = check()
                severity, details = result
                status = '✓' if severity == 'OK' else '!'
                print(f"[{status}] {name}: {details}")
                self.findings.append({'check': name, 'severity': severity, 'details': details})
            except Exception as e:
                print(f"[?] {name}: Error - {e}")
        
        return self.findings


def main():
    if len(sys.argv) < 2:
        print("Usage: python web_scanner.py <target>")
        sys.exit(1)
    
    target = sys.argv[1]
    scanner = WebScanner(target)
    scanner.scan()


if __name__ == "__main__":
    main()