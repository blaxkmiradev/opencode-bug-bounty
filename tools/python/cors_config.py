#!/usr/bin/env python3
"""
CORS Misconfiguration Scanner
Tests for CORS vulnerabilities
"""

import requests
import argparse
import warnings
warnings.filterwarnings('ignore')

PAYLOADS = [
    'http://evil.com',
    'https://evil.com',
    'null',
    '*',
]

def scan(target):
    print(f"[*] CORS Scanner - {target}")
    print("="*50)
    
    if not target.startswith(('http://', 'https://')):
        target = 'https://' + target
    
    found = []
    
    for payload in PAYLOADS:
        headers = {
            'Origin': payload,
            'User-Agent': 'Mozilla/5.0'
        }
        try:
            r = requests.get(target, headers=headers, timeout=10, verify=False)
            acao = r.headers.get('Access-Control-Allow-Origin', '')
            if payload in acao or '*' in acao:
                print(f"[!] CORS Misconfig: {acao}")
                found.append(acao)
        except:
            pass
    
    print("\n" + "="*50)
    print(f"[*] Found {len(found)} CORS issues")
    
    return found

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='CORS Scanner')
    parser.add_argument('target', help='Target URL')
    args = parser.parse_args()
    scan(args.target)