#!/usr/bin/env python3
"""
WebDAV Scanner
Tests for WebDAV vulnerabilities
"""

import requests
import argparse
import warnings
warnings.filterwarnings('ignore')

def scan(target):
    print(f"[*] WebDAV Scanner - {target}")
    print("="*50)
    
    if not target.startswith(('http://', 'https://')):
        target = 'https://' + target
    
    found = []
    dav_methods = ['PROPFIND', 'PROPPATCH', 'MKCOL', 'DELETE', 'PUT', 'COPY', 'MOVE']
    
    for method in dav_methods:
        try:
            r = requests.request(method, target, timeout=10, verify=False)
            if r.status_code < 500:
                print(f"[{r.status_code:3d}] {method}")
                if method not in ['GET', 'HEAD', 'OPTIONS']:
                    found.append(method)
        except:
            pass
    
    print("\n" + "="*50)
    print(f"[*] WebDAV methods: {found}")
    return found

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='WebDAV Scanner')
    parser.add_argument('target', help='Target URL')
    args = parser.parse_args()
    scan(args.target)