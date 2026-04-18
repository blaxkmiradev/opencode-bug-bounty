#!/usr/bin/env python3
"""
Web Cache Poisoning Scanner
Tests for web cache poisoning vulnerabilities
"""

import requests
import argparse
import warnings
warnings.filterwarnings('ignore')

PAYLOADS = [
    ("Cache-Control", "no-store"),
    ("Pragma", "no-cache"),
    ("X-Forwarded-Host", "evil.com"),
    ("X-Host", "evil.com"),
    ("X-Original-URL", "/admin"),
]

def scan(target):
    print(f"[*] Web Cache Poisoning Scanner - {target}")
    print("="*50)
    
    if not target.startswith(('http://', 'https://')):
        target = 'https://' + target
    
    found = []
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    for header, value in PAYLOADS:
        test_headers = headers.copy()
        test_headers[header] = value
        try:
            r = requests.get(target, headers=test_headers, timeout=10, verify=False)
            if r.status_code == 200:
                print(f"[*] {header}: {value}")
        except:
            pass
    
    print("\n" + "="*50)
    print("[*] Cache poisoning check complete")
    
    return found

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Cache Poisoning Scanner')
    parser.add_argument('target', help='Target URL')
    args = parser.parse_args()
    scan(args.target)