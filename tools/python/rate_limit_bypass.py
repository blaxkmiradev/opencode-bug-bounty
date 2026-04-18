#!/usr/bin/env python3
"""
Rate Limit Bypass Scanner
Tests for rate limiting vulnerabilities
"""

import requests
import argparse
import warnings
warnings.filterwarnings('ignore')

def scan(target):
    print(f"[*] Rate Limit Bypass Scanner - {target}")
    print("="*50)
    
    if not target.startswith(('http://', 'https://')):
        target = 'https://' + target
    
    found = []
    headers_list = [
        {'X-Forwarded-For': '10.10.10.10'},
        {'X-Real-IP': '10.10.10.10'},
        {'X-Originating-IP': '10.10.10.10'},
        {'X-Client-IP': '10.10.10.10'},
        {'Client-IP': '10.10.10.10'},
        {'X-Forwarded': '10.10.10.10'},
        {'X-Forwaded-For': '10.10.10.10'},
        {'X-IP': '10.10.10.10'},
        {'Forwarded-For': '10.10.10.10'},
        {'Forwarded': '10.10.10.10'},
    ]
    
    for headers in headers_list[:5]:
        try:
            r = requests.get(target, headers=headers, timeout=10, verify=False)
            if r.status_code == 200:
                print(f"[?] Bypass with: {list(headers.keys())[0]}")
                found.append(list(headers.keys())[0])
        except:
            pass
    
    print("\n" + "="*50)
    print(f"[*] Found {len(found)} bypass methods")
    
    return found

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Rate Limit Bypass')
    parser.add_argument('target', help='Target URL')
    args = parser.parse_args()
    scan(args.target)