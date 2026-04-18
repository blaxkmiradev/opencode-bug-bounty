#!/usr/bin/env python3
"""
CSRF Token Checker
Checks for CSRF protection
"""

import requests
import argparse
import warnings
warnings.filterwarnings('ignore')

def scan(target):
    print(f"[*] CSRF Protection Checker - {target}")
    print("="*50)
    
    if not target.startswith(('http://', 'https://')):
        target = 'https://' + target
    
    issues = []
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        r = requests.get(target, timeout=10, verify=False, headers=headers)
        headers_list = [h.lower() for h in r.headers.keys()]
        
        if 'x-csrf-token' not in headers_list and 'x-xsrf-token' not in headers_list:
            issues.append("Missing CSRF token header")
        
        cookies = list(r.cookies.keys())
        if 'csrf' not in ''.join(cookies).lower():
            issues.append("No CSRF cookie found")
        
        if not r.cookies.get('SameSite'):
            issues.append("Cookie missing SameSite attribute")
        
        forms = 0
        if '<form' in r.text.lower():
            issues.append(f"Forms found - check manually")
        
        if 'same-origin' not in r.headers.get('Referer', '').lower():
            issues.append("Weak Referer check")
        
        print(f"[*] CSRF Headers: {len([h for h in headers_list if 'csrf' in h])}")
        print(f"[*] CSRF Cookies: {len([c for c in cookies if 'csrf' in c.lower()])}")
        
    except Exception as e:
        print(f"[!] Error: {e}")
    
    print("\n" + "="*50)
    if issues:
        print("[!] Issues found:")
        for iss in issues:
            print(f"  - {iss}")
    else:
        print("[*] CSRF protection appears adequate")
    
    return issues

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='CSRF Checker')
    parser.add_argument('target', help='Target URL')
    args = parser.parse_args()
    scan(args.target)