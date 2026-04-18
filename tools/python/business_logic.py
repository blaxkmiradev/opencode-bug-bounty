#!/usr/bin/env python3
"""
Business Logic Vulnerability Scanner
Tests for business logic vulnerabilities
"""

import requests
import argparse
import warnings
warnings.filterwarnings('ignore')

def test_price_manipulation(url):
    payloads = [
        ('price', '0.01'),
        ('amount', '0'),
        ('discount', '100'),
        ('quantity', '-1'),
    ]
    for param, value in payloads:
        try:
            r = requests.post(url, data={param: value}, timeout=10, verify=False)
            if r.status_code == 200:
                return True, param, value
        except:
            pass
    return False, None, None

def test_privilege_escalation(url):
    endpoints = ['/admin', '/dashboard', '/settings', '/profile']
    for ep in endpoints:
        try:
            r = requests.get(url + ep, timeout=10, verify=False)
            if r.status_code == 200:
                return True, ep
        except:
            pass
    return False, None

def test_otp_bypass(url):
    endpoints = ['/api/resend-otp', '/api/verify', '/resend', '/verify']
    for ep in endpoints:
        try:
            r = requests.get(url + ep, timeout=10, verify=False)
            if r.status_code != 404:
                return True, ep
        except:
            pass
    return False, None

def scan(target):
    print(f"[*] Business Logic Scanner - {target}")
    print("="*50)
    
    if not target.startswith(('http://', 'https://')):
        target = 'https://' + target
    
    found = []
    
    print("[*] Testing price manipulation...")
    vuln, param, value = test_price_manipulation(target)
    if vuln:
        print(f"[!] Price manipulation: {param}={value}")
        found.append({'type': 'price_manipulation', 'param': param})
    
    print("[*] Testing privilege escalation...")
    vuln, ep = test_privilege_escalation(target)
    if vuln:
        print(f"[!] Public access: {ep}")
        found.append({'type': 'privilege_escalation', 'endpoint': ep})
    
    print("[*] Testing OTP bypass...")
    vuln, ep = test_otp_bypass(target)
    if vuln:
        print(f"[!] OTP endpoint: {ep}")
        found.append({'type': 'otp_bypass', 'endpoint': ep})
    
    print("\n" + "="*50)
    if found:
        print(f"[!] Found {len(found)} business logic issues")
    else:
        print("[*] No obvious business logic flaws")
    
    return found

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Business Logic Scanner')
    parser.add_argument('target', help='Target URL')
    args = parser.parse_args()
    scan(args.target)