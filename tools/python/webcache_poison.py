#!/usr/bin/env python3
"""
Web Cache Deception Scanner
Tests for web cache deception vulnerabilities
"""

import requests
import argparse
import warnings
warnings.filterwarnings('ignore')

PAYLOADS = [
    '/?q=test',
    '/?utm_source=test',
    '/?ref=test',
]

def scan(target):
    print(f"[*] Web Cache Deception Scanner - {target}")
    print("="*50)
    
    if not target.startswith(('http://', 'https://')):
        target = 'https://' + target
    
    found = []
    
    for payload in PAYLOADS:
        url = target + payload
        try:
            r1 = requests.get(url, timeout=10, verify=False)
            r2 = requests.get(url, timeout=10, verify=False)
            
            if r1.text == r2.text and r1.status_code == r2.status_code == 200:
                print(f"[?] Cacheable: {payload}")
                found.append(payload)
        except:
            pass
    
    print("\n" + "="*50)
    print(f"[*] Found {len(found)} cacheable endpoints")
    return found

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Cache Deception')
    parser.add_argument('target', help='Target URL')
    args = parser.parse_args()
    scan(args.target)