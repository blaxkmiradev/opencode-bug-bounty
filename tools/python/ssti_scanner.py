#!/usr/bin/env python3
"""
SSTI (Server-Side Template Injection) Scanner
Tests for template injection
"""

import requests
import argparse
import warnings
warnings.filterwarnings('ignore')

PAYLOADS = [
    '{{7*7}}', '${7*7}', '<%= 7*7 %>', '{{config}}', '{7*7}',
    '{${{7*7}}}', '<#assign ex="freemarker"?>', '{{self.__class__.__mro__}}',
]

def scan(target):
    print(f"[*] SSTI Scanner - {target}")
    print("="*50)
    
    if not target.startswith(('http://', 'https://')):
        target = 'https://' + target
    
    found = []
    params = ['template', 'view', 'page', 'render', 'content']
    
    for param in params:
        for payload in PAYLOADS[:3]:
            try:
                r = requests.get(target, params={param: payload}, timeout=10, verify=False)
                if '49' in r.text or '7' in r.text or 'config' in r.text.lower():
                    print(f"[!] Possible SSTI: {param}")
                    found.append(param)
            except:
                pass
    
    print("\n" + "="*50)
    print(f"[*] Found {len(found)} potential issues")
    
    return found

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='SSTI Scanner')
    parser.add_argument('target', help='Target URL')
    args = parser.parse_args()
    scan(args.target)