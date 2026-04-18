#!/usr/bin/env python3
"""
HTTP Method Scanner
Tests unsupported HTTP methods
"""

import requests
import argparse
import warnings
warnings.filterwarnings('ignore')

METHODS = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS', 'TRACE', 'CONNECT', 'TRACK', 'DEBUG']

def scan(target):
    print(f"[*] HTTP Method Scanner - {target}")
    print("="*50)
    
    if not target.startswith(('http://', 'https://')):
        target = 'https://' + target
    
    found = []
    
    for method in METHODS:
        try:
            r = requests.request(method, target, timeout=10, verify=False)
            if r.status_code < 500:
                print(f"[{r.status_code:3d}] {method:10s}")
                if method not in ['GET', 'POST', 'HEAD', 'OPTIONS']:
                    found.append(method)
        except Exception as e:
            pass
    
    print("\n" + "="*50)
    print(f"[*] Allowed methods: {len(found)+4}")
    
    return found

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='HTTP Method Scanner')
    parser.add_argument('target', help='Target URL')
    args = parser.parse_args()
    scan(args.target)