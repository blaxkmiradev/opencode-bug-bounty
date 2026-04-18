#!/usr/bin/env python3
"""
DoS Vulnerability Tester
Tests for DoS vulnerabilities
"""

import requests
import argparse
import warnings
import time
warnings.filterwarnings('ignore')

PAYLOADS = [
    ("a" * 1000, "large_payload"),
    ("a" * 10000, "very_large"),
    ("/." * 1000, "long_path"),
    ("?a=" * 1000, "long_param"),
]

def scan(target):
    print(f"[*] DoS Vulnerability Tester - {target}")
    print("="*50)
    
    if not target.startswith(('http://', 'https://')):
        target = 'https://' + target
    
    found = []
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    for payload, ptype in PAYLOADS:
        try:
            start = time.time()
            r = requests.get(target, params={'q': payload}, timeout=15, verify=False, headers=headers)
            elapsed = time.time() - start
            
            if elapsed > 5:
                print(f"[!] Slow response ({elapsed:.2f}s): {ptype}")
                found.append(ptype)
            else:
                print(f"[*] OK: {ptype} ({elapsed:.2f}s)")
        except Exception as e:
            print(f"[!] Error: {ptype} - {e}")
    
    print("\n" + "="*50)
    if found:
        print(f"[!] Potential DoS: {len(found)} issues")
    else:
        print("[*] No obvious DoS vulnerabilities")
    
    return found

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='DoS Tester')
    parser.add_argument('target', help='Target URL')
    args = parser.parse_args()
    scan(args.target)