#!/usr/bin/env python3
"""
Mass Assignment Scanner
Tests for mass assignment vulnerabilities
"""

import requests
import argparse
import warnings
warnings.filterwarnings('ignore')

def scan(target):
    print(f"[*] Mass Assignment Scanner - {target}")
    print("="*50)
    
    if not target.startswith(('http://', 'https://')):
        target = 'https://' + target
    
    found = []
    params = ['role', 'admin', 'is_admin', 'user_role', 'privilege', 'permission', 'level', 'access']
    
    for param in params:
        try:
            r = requests.post(target, data={param: 'true'}, timeout=10, verify=False)
            if r.status_code == 200 and 'admin' not in r.text.lower():
                print(f"[?] Mass assignment: {param}")
                found.append(param)
        except:
            pass
    
    print("\n" + "="*50)
    print(f"[*] Found {len(found)} potential issues")
    
    return found

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Mass Assignment Scanner')
    parser.add_argument('target', help='Target URL')
    args = parser.parse_args()
    scan(args.target)