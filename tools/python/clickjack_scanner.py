#!/usr/bin/env python3
"""
Clickjacking Scanner
Detects clickjacking vulnerabilities
"""

import requests
import argparse
import warnings
warnings.filterwarnings('ignore')

def scan(target):
    print(f"[*] Clickjacking Scanner - {target}")
    print("="*50)
    
    if not target.startswith(('http://', 'https://')):
        target = 'https://' + target
    
    found = []
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        r = requests.get(target, timeout=10, verify=False, headers=headers)
        header_keys = [h.lower() for h in r.headers.keys()]
        
        if 'x-frame-options' not in header_keys:
            found.append("Missing X-Frame-Options")
        
        if 'content-security-policy' in header_keys:
            csp = r.headers.get('Content-Security-Policy', '')
            if 'frame-ancestors' not in csp.lower():
                found.append("CSP missing frame-ancestors")
        else:
            found.append("No CSP header")
        
        if 'frame' in r.text.lower() and 'iframe' in r.text.lower():
            found.append("Potential iframe in page")
        
    except Exception as e:
        print(f"[!] Error: {e}")
    
    print("\n" + "="*50)
    if found:
        print("[!] Clickjacking vulnerabilities:")
        for f in found:
            print(f"  - {f}")
    else:
        print("[*] Protected against clickjacking")
    
    return found

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Clickjacking Scanner')
    parser.add_argument('target', help='Target URL')
    args = parser.parse_args()
    scan(args.target)