#!/usr/bin/env python3
"""
Git Repository Scanner
Detects exposed .git directories
"""

import requests
import argparse
import warnings
warnings.filterwarnings('ignore')

SENSITIVE_FILES = [
    '/.git/config',
    '/.git/HEAD',
    '/.git/index',
    '/.git/logs/HEAD',
    '/.git/ORIG_HEAD',
    '/.git/refs/stash',
    '/.git/description',
]

def scan(target):
    print(f"[*] Git Repository Scanner - {target}")
    print("="*50)
    
    if not target.startswith(('http://', 'https://')):
        target = 'https://' + target
    
    found = []
    
    for file in SENSITIVE_FILES:
        try:
            r = requests.get(target + file, timeout=10, verify=False)
            if r.status_code == 200 and len(r.text) > 0:
                print(f"[!] Exposed: {file}")
                found.append(file)
        except:
            pass
    
    print("\n" + "="*50)
    if found:
        print(f"[!] Found {len(found)} sensitive git files")
    else:
        print("[*] No exposed git files found")
    
    return found

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Git Scanner')
    parser.add_argument('target', help='Target URL')
    args = parser.parse_args()
    scan(args.target)