#!/usr/bin/env python3
"""
Secret/Key Scanner in JS/CSS/HTML
Usage: python secret_scanner.py https://target.com/
"""

import sys
import requests
import re

class SecretScanner:
    def __init__(self, target):
        self.target = target.rstrip('/')
        self.findings = []
        
        # Secret patterns
        self.patterns = [
            (r'AKIA[0-9A-Z]{16}', 'AWS Access Key'),
            (r'aws_(?:access_key|secret_access_key|session_token)', 'AWS Secret'),
            (r'xox[baprs]-[0-9a-zA-Z-]{10,}', 'Slack Token'),
            (r'ghp_[0-9a-zA-Z]{36}', 'GitHub Token'),
            (r'gho_[0-9a-zA-Z]{36}', 'GitHub OAuth'),
            (r'glpat-[0-9a-zA-Z-_]{20,}', 'GitLab Token'),
            (r'SK-[0-9a-zA-Z]{32,}', 'Stripe Key'),
            (r'sk-[0-9a-zA-Z]{24,}', 'Stripe Secret'),
            (r'AIza[0-9A-Za-z-_]{35}', 'Google API'),
            (r'[0-9]+-[0-9A-Za-z_]{32}\.apps\.googleusercontent\.com', 'Google OAuth'),
            (r'mongodb(\+srv)?://[^$]+', 'MongoDB URI'),
            (r'mysql://[^$]+', 'MySQL URI'),
            (r'postgres(ql)?:////[^$]+', 'PostgreSQL URI'),
            (r'redis://[^$]+', 'Redis URI'),
            (r'[\'"](?:api[_-]?key|api[_-]?token|apikey)[\'"]\s*[:=]\s*[\'"][0-9a-zA-Z-_]{20,}', 'API Key'),
            (r'-----BEGIN (?:RSA |EC )?PRIVATE KEY-----', 'Private Key'),
            (r'-----BEGIN CERTIFICATE-----', 'Certificate'),
            (b'\x30\x82', 'DER Certificate'),
            (r'sq0csp-[0-9A-Za-z-_]{43}', 'Google OAuth CSP'),
            (r'sk_live_[0-9a-zA-Z]{24,}', 'Stripe Live'),
            (r'sk_test_[0-9a-zA-Z]{24,}', 'Stripe Test'),
            (r'eyJ[a-zA-Z0-9_-]*\.eyJ[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*', 'JWT Token'),
        ]
    
    def scan_urls(self, url):
        """Scan a URL for secrets"""
        try:
            r = requests.get(url, timeout=10)
            content = r.text
            
            for pattern, name in self.patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                for match in matches:
                    if len(str(match)) > 10:
                        print(f"[!] {name}: {match[:50]}...")
                        self.findings.append({'url': url, 'type': name, 'secret': str(match)[:50]})
            
        except Exception as e:
            pass
    
    def scan(self):
        """Scan for secrets"""
        print(f"[*] Scanning {self.target}...")
        
        # Scan main page
        self.scan_urls(self.target)
        
        # Scan common JS/CSS paths
        paths = ['/app.js', '/main.js', '/bundle.js', '/api.js', '/app.min.js', 
                '/main.css', '/style.css', '/api.css']
        
        for path in paths:
            self.scan_urls(self.target + path)
        
        if self.findings:
            print(f"\n[!] Found {len(self.findings)} secrets")
        
        return self.findings


def main():
    if len(sys.argv) < 2:
        print("Usage: python secret_scanner.py <url>")
        sys.exit(1)
    
    target = sys.argv[1]
    scanner = SecretScanner(target)
    scanner.scan()


if __name__ == "__main__":
    main()