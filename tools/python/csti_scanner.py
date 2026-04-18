#!/usr/bin/env python3
"""
CSTI (Client-Side Template Injection) Scanner
Detects template injection vulnerabilities
"""

import requests
import argparse
import warnings
warnings.filterwarnings('ignore')

PAYLOADS = [
    ("{{7*7}}", "jinja"),
    ("${7*7}", "handlebars"),
    ("<%= 7*7 %>", "erb"),
    ("{{7*7}}", "angular"),
    ("#{7*7}", "ruby"),
    ("{*7*7}", "twig"),
    ("{{7*'a'}}", "vue"),
]

def scan(target):
    print(f"[*] CSTI Scanner - {target}")
    print("="*50)
    
    if not target.startswith(('http://', 'https://')):
        target = 'https://' + target
    
    found = []
    params = ['name', 'title', 'q', 'search', 'query', 's', 'input']
    
    print("[*] Testing template injection...")
    for param in params:
        for payload, ptype in PAYLOADS:
            try:
                r = requests.get(target, params={param: payload}, timeout=10, verify=False)
                if '49' in r.text or '7' in r.text:
                    print(f"[!] Possible CSTI: {param} ({ptype})")
                    found.append({'param': param, 'type': ptype})
            except:
                pass
    
    print("\n" + "="*50)
    if found:
        print(f"[!] Found {len(found)} potential CSTI issues")
    else:
        print("[*] No CSTI vulnerabilities detected")
    
    return found

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='CSTI Scanner')
    parser.add_argument('target', help='Target URL')
    args = parser.parse_args()
    scan(args.target)