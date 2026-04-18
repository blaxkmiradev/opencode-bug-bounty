#!/usr/bin/env python3
"""
DOM-based XSS Scanner
Detects DOM-based XSS vulnerabilities
"""

import requests
import re
import argparse
import warnings
warnings.filterwarnings('ignore')

SOURCES = [
    'location.href', 'location.hash', 'location.search', 'document.URL',
    'document.referrer', 'window.name', 'innerHTML', 'outerHTML',
    'eval()', 'setTimeout()', 'setInterval()', 'document.write()',
]

def scan(target):
    print(f"[*] DOM-based XSS Scanner - {target}")
    print("="*50)
    
    if not target.startswith(('http://', 'https://')):
        target = 'https://' + target
    
    found = []
    
    try:
        r = requests.get(target, timeout=10, verify=False)
        html = r.text
        
        for src in SOURCES:
            if src in html:
                print(f"[?] Potentially dangerous: {src}")
                found.append(src)
    
    except Exception as e:
        print(f"[!] Error: {e}")
    
    print("\n" + "="*50)
    print(f"[*] Found {len(found)} potential DOM sinks")
    
    return found

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='DOM XSS')
    parser.add_argument('target', help='Target URL')
    args = parser.parse_args()
    scan(args.target)