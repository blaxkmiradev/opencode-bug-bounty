#!/usr/bin/env python3
"""
Hidden Parameter Discovery
Finds hidden form parameters
"""

import requests
import re
import argparse
import warnings
warnings.filterwarnings('ignore')

def scan(target):
    print(f"[*] Hidden Parameter Discovery - {target}")
    print("="*50)
    
    if not target.startswith(('http://', 'https://')):
        target = 'https://' + target
    
    found = []
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        r = requests.get(target, timeout=10, verify=False, headers=headers)
        
        hidden = re.findall(r'<input[^>]*type=["\']hidden["\'][^>]*name=["\']([^"\']+)["\']', r.text, re.I)
        found.extend(hidden)
        
        hidden += re.findall(r'<input[^>]*name=["\']([^"\']+)["\'][^>]*type=["\']hidden["\']', r.text, re.I)
        
        hidden_fields = re.findall(r'name=["\']([^"\']+)["\'][^>]*hidden', r.text, re.I)
        found.extend(hidden_fields)
        
        for f in found:
            print(f"[+] Found: {f}")
        
    except Exception as e:
        print(f"[!] Error: {e}")
    
    print("\n" + "="*50)
    print(f"[*] Found {len(found)} hidden parameters")
    
    return found

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Hidden Parameter Discovery')
    parser.add_argument('target', help='Target URL')
    args = parser.parse_args()
    scan(args.target)