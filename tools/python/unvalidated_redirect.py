#!/usr/bin/env python3
"""
Open Redirect Scanner
Tests for unvalidated redirects
"""

import requests
import argparse
import warnings
warnings.filterwarnings('ignore')

PAYLOADS = [
    'http://evil.com',
    'https://evil.com',
    '//evil.com',
    '/\\evil.com',
    '///evil.com/',
    'javascript:alert(1)',
]

def scan(target):
    print(f"[*] Open Redirect Scanner - {target}")
    print("="*50)
    
    if not target.startswith(('http://', 'https://')):
        target = 'https://' + target
    
    found = []
    params = ['redirect', 'url', 'next', 'return', 'continue', 'dest', 'destination', 'target', ' destination', 'open']
    
    for param in params:
        for payload in PAYLOADS[:3]:
            try:
                r = requests.get(target, params={param: payload}, timeout=10, verify=False, allow_redirects=False)
                if r.status_code in [301, 302, 303, 307, 308]:
                    loc = r.headers.get('Location', '')
                    if 'evil' in loc or payload in loc:
                        print(f"[!] Open redirect: {param}")
                        found.append(param)
            except:
                pass
    
    print("\n" + "="*50)
    print(f"[*] Found {len(found)} open redirects")
    
    return found

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Open Redirect Scanner')
    parser.add_argument('target', help='Target URL')
    args = parser.parse_args()
    scan(args.target)