#!/usr/bin/env python3
"""
Cookie Security Analyzer
Analyzes cookie security attributes
"""

import requests
import argparse
import warnings
warnings.filterwarnings('ignore')

def scan(target):
    print(f"[*] Cookie Security Analyzer - {target}")
    print("="*50)
    
    if not target.startswith(('http://', 'https://')):
        target = 'https://' + target
    
    found = []
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        r = requests.get(target, timeout=10, verify=False, headers=headers)
        
        for cookie in r.cookies:
            issues = []
            
            if not cookie.secure:
                issues.append("Secure flag missing")
            if not cookie.has_non_secure_attrs():
                issues.append("HttpOnly flag missing")
            if cookie.domain_initial_dot:
                issues.append("Domain starts with dot")
            
            expires = cookie.expires
            if expires and expires < 3600:
                issues.append("Short expiration")
            
            if issues:
                print(f"[!] {cookie.name}:")
                for iss in issues:
                    print(f"    - {iss}")
                found.append(cookie.name)
            else:
                print(f"[+] {cookie.name}: OK")
        
    except Exception as e:
        print(f"[!] Error: {e}")
    
    print("\n" + "="*50)
    print(f"[*] Analyzed {len(list(r.cookies))} cookies")
    
    return found

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Cookie Analyzer')
    parser.add_argument('target', help='Target URL')
    args = parser.parse_args()
    scan(args.target)