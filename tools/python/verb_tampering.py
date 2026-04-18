#!/usr/bin/env python3
"""
HTTP Verb Tampering Scanner
Tests for HTTP verb manipulation vulnerabilities
"""

import requests
import argparse
import warnings
warnings.filterwarnings('ignore')

VERBS = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS', 'TRACE', 'CONNECT']

def scan(target):
    print(f"[*] HTTP Verb Tampering Scanner - {target}")
    print("="*50)
    
    if not target.startswith(('http://', 'https://')):
        target = 'https://' + target
    
    found = []
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    for verb in VERBS:
        try:
            r = requests.request(verb, target, timeout=10, verify=False, headers=headers)
            if r.status_code < 500 and verb not in ['GET', 'POST']:
                print(f"[{r.status_code:3d}] {verb}")
                found.append(verb)
        except:
            pass
    
    print("\n" + "="*50)
    print(f"[*] Allowed verbs: {found}")
    
    return found

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Verb Tampering Scanner')
    parser.add_argument('target', help='Target URL')
    args = parser.parse_args()
    scan(args.target)