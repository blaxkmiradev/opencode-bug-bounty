#!/usr/bin/env python3
"""
Vulnerability Level Scanner
Usage: python vuln_level.py target.com
Scans and categorizes vulnerabilities by severity
"""

import sys
import requests
import concurrent.futures
import urllib.parse
import socket

class VulnLevelScanner:
    def __init__(self, target):
        self.target = target
        self.vulns = {'critical': [], 'high': [], 'medium': [], 'low': [], 'info': []}
        
        self.checks = []
        
    def check_critical(self):
        """Critical vulnerabilities"""
        checks = [
            ('RCE', self.test_rce, 'Critical'),
            ('SQLi Data', self.test_sqli_data, 'Critical'),
            ('Auth Bypass', self.test_auth_bypass, 'Critical'),
            ('SSRF Cloud', self.test_ssrf_cloud, 'Critical'),
        ]
        
        for name, func, severity in checks:
            result = func()
            if result:
                self.vulns[severity.lower()].append({'name': name, 'details': result})
    
    def check_high(self):
        """High severity vulnerabilities"""
        checks = [
            ('IDOR Write', self.test_idor_write, 'High'),
            ('Stored XSS', self.test_stored_xss, 'High'),
            ('Command Inj', self.test_cmdi, 'High'),
            ('JWT None', self.test_jwt_none, 'High'),
        ]
        
        for name, func, severity in checks:
            result = func()
            if result:
                self.vulns[severity.lower()].append({'name': name, 'details': result})
    
    def check_medium(self):
        """Medium severity vulnerabilities"""
        checks = [
            ('IDOR Read', self.test_idor_read, 'Medium'),
            ('Reflected XSS', self.test_reflected_xss, 'Medium'),
            ('Open Redirect', self.test_open_redirect, 'Medium'),
            ('CORS', self.test_cors, 'Medium'),
        ]
        
        for name, func, severity in checks:
            result = func()
            if result:
                self.vulns[severity.lower()].append({'name': name, 'details': result})
    
    def check_low(self):
        """Low severity vulnerabilities"""
        checks = [
            ('Self-XSS', self.test_self_xss, 'Low'),
            ('Info Disclosure', self.test_info_disclosure, 'Low'),
            ('Missing HSTS', self.test_missing_hsts, 'Low'),
            ('Missing CSP', self.test_missing_csp, 'Low'),
        ]
        
        for name, func, severity in checks:
            result = func()
            if result:
                self.vulns[severity.lower()].append({'name': name, 'details': result})
    
    # Test methods (simplified - would be full implementations in production)
    def test_rce(self):
        """Test for RCE"""
        payloads = ['; whoami', '| whoami', '&& whoami']
        for payload in payloads:
            try:
                url = f"http://{self.target}/ping?ip={payload}"
                r = requests.get(url, timeout=5)
                if 'root:' in r.text or 'www-data' in r.text:
                    return f"RCE via: {payload}"
            except:
                pass
        return None
    
    def test_sqli_data(self):
        """Test for SQLi with data exfiltration"""
        payloads = ["' UNION SELECT NULL--", "' UNION SELECT NULL,NULL--"]
        for payload in payloads:
            try:
                url = f"http://{self.target}/search?q={payload}"
                r = requests.get(url, timeout=5)
                if 'error' in r.text.lower() or 'sql' in r.text.lower():
                    return f"SQLi via: {payload}"
            except:
                pass
        return None
    
    def test_auth_bypass(self):
        """Test for auth bypass"""
        try:
            urls = [f"http://{self.target}/admin", f"http://{self.target}/api/admin"]
            for url in urls:
                r = requests.get(url, timeout=5)
                if r.status_code == 200 and 'login' not in r.text.lower():
                    return f"Auth bypass: {url}"
        except:
            pass
        return None
    
    def test_ssrf_cloud(self):
        """Test for SSRF to cloud metadata"""
        try:
            url = f"http://{self.target}/fetch"
            data = {'url': 'http://169.254.169.254/'}
            r = requests.post(url, data=data, timeout=5)
            if any(x in r.text.lower() for x in ['meta', 'instance', 'amazon']):
                return "SSRF to cloud metadata"
        except:
            pass
        return None
    
    def test_idor_write(self):
        """Test IDOR with write"""
        # Would test with two accounts
        return None
    
    def test_stored_xss(self):
        """Test for stored XSS"""
        try:
            url = f"http://{self.target}/comment"
            data = {'comment': '<script>alert(1)</script>'}
            r = requests.post(url, data=data, timeout=5)
            # Check if reflected in another page
            r2 = requests.get(url, timeout=5)
            if '<script>alert(1)</script>' in r2.text:
                return "Stored XSS in comment"
        except:
            pass
        return None
    
    def test_cmdi(self):
        """Test command injection"""
        payloads = ['; id', '| id', '& id']
        for payload in payloads:
            try:
                url = f"http://{self.target}/shell?cmd={payload}"
                r = requests.get(url, timeout=5)
                if 'uid=' in r.text or 'root' in r.text:
                    return f"CMDi via: {payload}"
            except:
                pass
        return None
    
    def test_jwt_none(self):
        """Test JWT with none algorithm"""
        return None
    
    def test_idor_read(self):
        """Test IDOR read"""
        try:
            for id in range(1, 5):
                url = f"http://{self.target}/user/{id}"
                r = requests.get(url, timeout=5)
                if r.status_code == 200:
                    # Would check if different user's data
                    pass
        except:
            pass
        return None
    
    def test_reflected_xss(self):
        """Test reflected XSS"""
        payloads = ['<script>alert(1)</script>', '<img src=x onerror=alert(1)>']
        for payload in payloads:
            try:
                url = f"http://{self.target}/search?q={payload}"
                r = requests.get(url, timeout=5)
                if payload in r.text:
                    return f"Reflected XSS via q"
            except:
                pass
        return None
    
    def test_open_redirect(self):
        """Test open redirect"""
        try:
            url = f"http://{self.target}/redirect?url=https://evil.com"
            r = requests.get(url, timeout=5, allow_redirects=False)
            if r.status_code in [301, 302]:
                loc = r.headers.get('Location', '')
                if 'evil' in loc:
                    return "Open redirect"
        except:
            pass
        return None
    
    def test_cors(self):
        """Test CORS misconfig"""
        try:
            url = f"http://{self.target}/api"
            r = requests.get(url, headers={'Origin': 'https://evil.com'}, timeout=5)
            acao = r.headers.get('Access-Control-Allow-Origin')
            if acao == '*' or 'evil' in acao:
                return f"CORS misconfig: {acao}"
        except:
            pass
        return None
    
    def test_self_xss(self):
        """Test self-XSS"""
        return None
    
    def test_info_disclosure(self):
        """Test information disclosure"""
        try:
            paths = ['/.git/', '/phpinfo.php', '/.env']
            for path in paths:
                url = f"http://{self.target}{path}"
                r = requests.get(url, timeout=5)
                if r.status_code == 200:
                    return f"Found: {path}"
        except:
            pass
        return None
    
    def test_missing_hsts(self):
        """Test missing HSTS"""
        try:
            r = requests.get(f"http://{self.target}", timeout=5)
            if not r.headers.get('Strict-Transport-Security'):
                return "HSTS not enabled"
        except:
            pass
        return None
    
    def test_missing_csp(self):
        """Test missing CSP"""
        try:
            r = requests.get(f"http://{self.target}", timeout=5)
            if not r.headers.get('Content-Security-Policy'):
                return "CSP not enabled"
        except:
            pass
        return None
    
    def scan(self):
        """Run full scan"""
        print(f"[*] Vulnerability Level Scanner for {self.target}")
        print("="*60)
        
        # Run checks by severity
        print("\n[*] Checking Critical...")
        self.check_critical()
        
        print("[*] Checking High...")
        self.check_high()
        
        print("[*] Checking Medium...")
        self.check_medium()
        
        print("[*] Checking Low...")
        self.check_low()
        
        print("\n" + "="*60)
        print("VULNERABILITY SCAN RESULTS")
        print("="*60)
        
        total = 0
        for level in ['critical', 'high', 'medium', 'low']:
            vulns = self.vulns[level]
            if vulns:
                print(f"\n[{level.upper()}] ({len(vulns)} found)")
                for v in vulns:
                    print(f"  - {v['name']}: {v['details']}")
                    total += 1
        
        if total == 0:
            print("\n[*] No vulnerabilities found (or limited scan)")
        
        print("\n" + "="*60)
        print(f"Total: {total} vulnerabilities")
        print("="*60)
        
        return self.vulns


def main():
    if len(sys.argv) < 2:
        print("""
Vulnerability Level Scanner
=====================

Usage: python vuln_level.py target.com
       python vuln_level.py target.com/endpoint

Scans and categorizes vulnerabilities by severity:
  Critical (9.0-10.0) - RCE, SQLi, Auth bypass
  High (7.0-8.9) - IDOR, Stored XSS, CMDi
  Medium (4.0-6.9) - IDOR read, Reflected XSS
  Low (0.1-3.9) - Self-XSS, Info disclosure
        """)
        sys.exit(1)
    
    target = sys.argv[1]
    scanner = VulnLevelScanner(target)
    scanner.scan()


if __name__ == "__main__":
    main()