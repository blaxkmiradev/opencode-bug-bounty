#!/usr/bin/env python3
"""
SAML Scanner
Tests SAML authentication for vulnerabilities
"""

import requests
import argparse
import warnings
warnings.filterwarnings('ignore')

PAYLOADS = [
    "<SAMLResponse></SAMLResponse>",
    "PHNhbWxSZXNwb25zZT48L3NhbWxSZXNwb25zZT4=",  # base64
]

def scan(target):
    print(f"[*] SAML Scanner - {target}")
    print("="*50)
    
    if not target.startswith(('http://', 'https://')):
        target = 'https://' + target
    
    found = []
    saml_paths = ['/saml', '/saml2', '/sso', '/acs', '/saml/acs']
    
    for path in saml_paths:
        try:
            r = requests.post(target + path, data={'SAMLResponse': PAYLOADS[0]}, timeout=10, verify=False)
            if r.status_code != 404:
                print(f"[?] SAML endpoint: {path} ({r.status_code})")
                found.append(path)
        except:
            pass
    
    print("\n" + "="*50)
    if found:
        print(f"[!] Found {len(found)} SAML endpoints")
    else:
        print("[*] No SAML endpoints found")
    
    return found

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='SAML Scanner')
    parser.add_argument('target', help='Target URL')
    args = parser.parse_args()
    scan(args.target)