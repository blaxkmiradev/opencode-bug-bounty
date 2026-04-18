#!/usr/bin/env python3
"""
Comprehensive Bug Hunter Scanner
Usage: python full_scan.py target.com

Runs all scanners in sequence and generates unified report.
"""

import sys
import requests
import socket
import concurrent.futures
from datetime import datetime
import json

class FullScanner:
    def __init__(self, target):
        self.target = target.replace('https://', '').replace('http://', '').rstrip('/')
        self.results = {
            'target': self.target,
            'timestamp': datetime.now().isoformat(),
            'subdomains': [],
            'ports': [],
            'endpoints': [],
            'tech': {},
            'headers': {},
            'vulnerabilities': [],
            'cvss': []
        }
        
    def scan_ports(self):
        """Port scan"""
        common_ports = [
            (21, 'FTP'), (22, 'SSH'), (23, 'Telnet'), (25, 'SMTP'),
            (53, 'DNS'), (80, 'HTTP'), (110, 'POP3'), (143, 'IMAP'),
            (443, 'HTTPS'), (445, 'SMB'), (993, 'IMAPS'), (995, 'POP3S'),
            (1433, 'MSSQL'), (1521, 'Oracle'), (3306, 'MySQL'), (3389, 'RDP'),
            (5432, 'PostgreSQL'), (5900, 'VNC'), (6379, 'Redis'), (8080, 'HTTP-Alt'),
            (8443, 'HTTPS-Alt'), (27017, 'MongoDB')
        ]
        
        print("[1/6] Scanning ports...")
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            futures = {executor.submit(self.check_port, p, s): (p, s) for p, s in common_ports}
            for f in concurrent.futures.as_completed(futures):
                result = f.result()
                if result:
                    self.results['ports'].append(f"{result[0]}/{result[1]}")
                    print(f"    [+] {result[0]} ({result[1]})")
    
    def scan_subdomains(self):
        """Subdomain enumeration"""
        subs = ['www', 'mail', 'ftp', 'admin', 'api', 'dev', 'test', 'staging',
                'blog', 'shop', 'cdn', 'static', 'backup', 'old', 'portal',
                'webmail', 'secure', 'app', 'm', 'mobile', 'shop']
        
        print("\n[2/6] Enumerating subdomains...")
        with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
            futures = {executor.submit(self.check_subdomain, s): s for s in subs}
            for f in concurrent.futures.as_completed(futures):
                result = f.result()
                if result:
                    self.results['subdomains'].append(result)
                    print(f"    [+] {result}")
    
    def check_port(self, port, service):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            if sock.connect_ex((self.target, port)) == 0:
                sock.close()
                return (port, service)
        except:
            pass
        return None
    
    def check_subdomain(self, sub):
        try:
            domain = f"{sub}.{self.target}"
            ip = socket.gethostbyname(domain)
            return f"{domain} -> {ip}"
        except:
            pass
        return None
    
    def fingerprint(self):
        """Tech fingerprint"""
        print("\n[3/6] Fingerprinting...")
        url = f"https://{self.target}"
        try:
            r = requests.get(url, timeout=10, verify=False)
            headers = dict(r.headers)
            
            self.results['tech'] = {
                'server': headers.get('Server', 'Unknown'),
                'powered': headers.get('X-Powered-By', ''),
                'status': r.status_code,
                'cms': self.detect_cms(r.text)
            }
            print(f"    [+] Server: {self.results['tech']['server']}")
            print(f"    [+] CMS: {self.results['tech']['cms']}")
        except Exception as e:
            print(f"    [!] {e}")
    
    def detect_cms(self, text):
        """Detect CMS"""
        if 'wp-content' in text.lower() or 'wordpress' in text.lower():
            return 'WordPress'
        if 'joomla' in text.lower():
            return 'Joomla'
        if 'drupal' in text.lower():
            return 'Drupal'
        if 'magento' in text.lower():
            return 'Magento'
        if 'shopify' in text.lower():
            return 'Shopify'
        return 'Unknown'
    
    def scan_headers(self):
        """Security headers"""
        print("\n[4/6] Scanning security headers...")
        url = f"https://{self.target}"
        try:
            r = requests.get(url, timeout=10, verify=False)
            headers = dict(r.headers)
            
            required = {
                'CSP': 'Content-Security-Policy',
                'HSTS': 'Strict-Transport-Security',
                'X-Frame': 'X-Frame-Options',
                'X-Content': 'X-Content-Type-Options',
                'Referrer': 'Referrer-Policy',
                'Permissions': 'Permissions-Policy'
            }
            
            for key, header in required.items():
                value = headers.get(header, None)
                self.results['headers'][key] = value
                if value:
                    print(f"    [+] {key}: {value}")
                else:
                    print(f"    [!] {key}: Missing")
                    self.results['vulnerabilities'].append({
                        'type': 'Missing Security Header',
                        'name': header,
                        'severity': 'Medium'
                    })
        except Exception as e:
            print(f"    [!] {e}")
    
    def scan_endpoints(self):
        """Scan common endpoints"""
        print("\n[5/6] Scanning endpoints...")
        endpoints = ['/admin', '/login', '/dashboard', '/wp-admin', '/api',
                   '/admin.php', '/manage', '/config', '/settings']
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = {executor.submit(self.check_endpoint, e): e for e in endpoints}
            for f in concurrent.futures.as_completed(futures):
                result = f.result()
                if result:
                    self.results['endpoints'].append(result)
                    print(f"    [+] {result}")
    
    def check_endpoint(self, path):
        try:
            url = f"https://{self.target}{path}"
            r = requests.get(url, timeout=3, verify=False)
            if r.status_code < 400:
                return f"{path} ({r.status_code})"
        except:
            pass
        return None
    
    def save_report(self):
        """Save JSON report"""
        print("\n[6/6] Saving report...")
        filename = f"scan-{self.target}-{datetime.now().strftime('%Y%m%d')}.json"
        
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"    [+] Saved: {filename}")
        return filename
    
    def run(self):
        """Run full scan"""
        print(f"\n{'='*60}")
        print(f"  COMPREHENSIVE SCANNER - {self.target}")
        print(f"  Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}\n")
        
        self.scan_ports()
        self.scan_subdomains()
        self.fingerprint()
        self.scan_headers()
        self.scan_endpoints()
        self.save_report()
        
        # Summary
        print(f"\n{'='*60}")
        print("  SCAN COMPLETE")
        print("="*60)
        print(f"\n  Subdomains: {len(self.results['subdomains'])}")
        print(f"  Ports: {len(self.results['ports'])}")
        print(f"  Endpoints: {len(self.results['endpoints'])}")
        print(f"  Vulnerabilities: {len(self.results['vulnerabilities'])}")
        
        return self.results


def main():
    if len(sys.argv) < 2:
        print("""
Comprehensive Bug Hunter Scanner
==================================

Usage: python full_scan.py target.com

Examples:
  python full_scan.py anajak.cloud
  python full_scan.py khmersamnang.com
        """)
        sys.exit(1)
    
    target = sys.argv[1]
    scanner = FullScanner(target)
    scanner.run()


if __name__ == "__main__":
    main()