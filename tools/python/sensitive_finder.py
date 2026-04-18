#!/usr/bin/env python3
"""
Sensitive Data Finder
Scans for exposed sensitive information
"""

import requests
import argparse
import warnings
import re
warnings.filterwarnings('ignore')

PATTERNS = {
    'aws_key': r'(AKIA|ABIA|ACCA|ASIA)[A-Z0-9]{16}',
    'aws_secret': r'(?i)aws(.{0,20})?(?-i)secret(.{0,20})?[\'\"=][0-9a-zA-Z/+]{40}',
    'private_key': r'-----BEGIN (RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----',
    'jwt': r'eyJ[A-Za-z0-9-_]+\.eyJ[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+',
    'google_api': r'AIza[0-9A-Za-z-_]{35}',
    'slack_token': r'xox[baprs]-([0-9a-zA-Z]{10,48})?',
    'github_token': r'ghp_[A-Za-z0-9]{36}',
    'stripe_key': r'(sk|pk)_(test|live)_[0-9a-zA-Z]{24,}',
    'firebase': r'AAAA[A-Za-z0-9_-]{7}:[A-Za-z0-9_-]{140}',
    'password': r'(?i)password[\'\"=:][^\s]{3,30}',
    'api_key': r'(?i)api[_-]?key[\'\"=:][^\s]{10,50}',
    'database_url': r'(?i)(mysql|postgres|mongodb)://[^\s]+',
    'bearer_token': r'Bearer [A-Za-z0-9\-_]+\.[A-Za-z0-9\-_]+\.[A-Za-z0-9\-_]+',
}

def scan(target):
    print(f"[*] Sensitive Data Finder - {target}")
    print("="*50)
    
    if not target.startswith(('http://', 'https://')):
        target = 'https://' + target
    
    found = []
    paths = ['/', '/api/', '/config', '/api/config', '/.env', '/settings', '/api/v1', '/admin']
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    for path in paths:
        try:
            r = requests.get(target + path, timeout=10, verify=False, headers=headers)
            text = r.text
            
            for name, pattern in PATTERNS.items():
                matches = re.findall(pattern, text)
                if matches:
                    for match in matches[:2]:
                        print(f"[!] Found {name}: {match[:50]}...")
                        found.append({'path': path, 'type': name, 'match': str(match)[:50]})
        except:
            pass
    
    print("\n" + "="*50)
    if found:
        print(f"[!] Found {len(found)} sensitive data exposures")
    else:
        print("[*] No sensitive data found")
    
    return found

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Sensitive Data Finder')
    parser.add_argument('target', help='Target URL')
    args = parser.parse_args()
    scan(args.target)