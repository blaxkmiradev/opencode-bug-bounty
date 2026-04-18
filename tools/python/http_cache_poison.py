#!/usr/bin/env python3
"""
HTTP Header Injection Scanner
Tests for header injection vulnerabilities
"""

import requests
import argparse
import warnings
warnings.filterwarnings('ignore')

PAYLOADS = [
    'test\r\nInject: header',
    'test\nInject: header',
    'test\rInject: header',
    'test%0D%0AInject: header',
    'test%0AInject: header',
]

def scan(target):
    print(f"[*] HTTP Header Injection Scanner - {target}")
    print("="*50)
    
    if not target.startswith(('http://', 'https://')):
        target = 'https://' + target
    
    found = []
    params = ['q', 'search', 'query', 'name', 'id']
    
    for param in params:
        for payload in PAYLOADS[:2]:
            try:
                r = requests.get(target, params={param: payload}, timeout=10, verify=False)
                if 'inject' in r.headers or 'inject' in r.text.lower():
                    print(f"[!] Header injection: {param}")
                    found.append(param)
            except:
                pass
    
    print("\n" + "="*50)
    print(f"[*] Found {len(found)} potential issues")
    
    return found

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Header Injection Scanner')
    parser.add_argument('target', help='Target URL')
    args = parser.parse_args()
    scan(args.target)