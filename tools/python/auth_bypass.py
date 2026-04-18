#!/usr/bin/env python3
"""
Authentication Bypass Scanner
Tests for authentication bypass vulnerabilities
"""

import requests
import argparse
import warnings
warnings.filterwarnings('ignore')

def scan(target):
    print(f"[*] Authentication Bypass Scanner - {target}")
    print("="*50)
    
    if not target.startswith(('http://', 'https://')):
        target = 'https://' + target
    
    found = []
    auth_paths = ['/admin', '/dashboard', '/manage', '/login', '/signin', '/wp-admin', '/administrator']
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    for path in auth_paths:
        try:
            r = requests.get(target + path, timeout=10, verify=False, headers=headers)
            if r.status_code == 200:
                print(f"[?] Accessible: {path}")
                found.append(path)
            elif r.status_code == 401 or r.status_code == 403:
                print(f"[*] Protected: {path}")
        except:
            pass
    
    print("\n" + "="*50)
    print(f"[*] Found {len(found)} accessible paths")
    
    return found

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Auth Bypass')
    parser.add_argument('target', help='Target URL')
    args = parser.parse_args()
    scan(args.target)