#!/usr/bin/env python3
"""
IDOR (Insecure Direct Object Reference) Scanner
Detects potential IDOR vulnerabilities
"""

import requests
import sys
import argparse
import warnings
import hashlib
warnings.filterwarnings('ignore')

def scan(target):
    print(f"[*] IDOR Scanner - {target}")
    print("="*50)
    
    if not target.startswith(('http://', 'https://')):
        target = 'https://' + target
    
    found = []
    endpoints = [
        '/api/user/1', '/api/user/2', '/user/1', '/user/2',
        '/api/profile/1', '/profile/1', '/api/order/1', '/order/1',
        '/api/account/1', '/account/1', '/api/transaction/1',
        '/api/settings', '/settings', '/api/admin',
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }
    
    print("[*] Testing horizontal IDOR...")
    for ep in endpoints:
        try:
            r1 = requests.get(target + ep.replace('1', '1').replace('2', '2'), 
                            timeout=10, verify=False, headers=headers)
            r2 = requests.get(target + ep.replace('1', '2').replace('2', '3'),
                            timeout=10, verify=False, headers=headers)
            
            if r1.status_code == 200 and r2.status_code == 200:
                if r1.text != r2.text:
                    h1 = hashlib.md5(r1.text.encode()).hexdigest()
                    h2 = hashlib.md5(r2.text.encode()).hexdigest()
                    if h1 != h2:
                        print(f"[!] POSSIBLE IDOR: {ep}")
                        found.append({'endpoint': ep, 'type': 'horizontal'})
        except:
            pass
    
    print("[*] Testing vertical IDOR (role escalation)...")
    role_paths = [
        '/api/admin/users', '/api/admin/settings',
        '/admin', '/dashboard/admin',
        '/wp-admin', '/administrator',
    ]
    for ep in role_paths:
        try:
            r = requests.get(target + ep, timeout=10, verify=False, headers=headers)
            if r.status_code != 403 and r.status_code != 401:
                print(f"[!] ACCESSIBLE: {ep} (status: {r.status_code})")
                found.append({'endpoint': ep, 'type': 'vertical'})
        except:
            pass
    
    print("[*] Testing parameter manipulation...")
    params_to_test = ['user_id', 'id', 'account_id', 'order_id', 'transaction_id']
    for param in params_to_test:
        try:
            r = requests.get(target + '/api/user', params={param: '1'}, timeout=10, verify=False)
            if r.status_code == 200:
                r2 = requests.get(target + '/api/user', params={param: '9999'}, timeout=10, verify=False)
                if r2.status_code == 200 and r.text != r2.text:
                    print(f"[!] PARAM MANIPULATION: {param}")
                    found.append({'param': param, 'type': 'parameter'})
        except:
            pass
    
    print("\n" + "="*50)
    if found:
        print(f"[!] Found {len(found)} potential IDOR issues")
        for f in found:
            print(f"  - {f}")
    else:
        print("[*] No IDOR vulnerabilities detected")
    
    return found

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='IDOR Scanner')
    parser.add_argument('target', help='Target URL')
    args = parser.parse_args()
    scan(args.target)