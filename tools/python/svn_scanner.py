#!/usr/bin/env python3
"""
SVN Repository Scanner
Detects exposed .svn directories
"""

import requests
import argparse
import warnings
warnings.filterwarnings('ignore')

def scan(target):
    print(f"[*] SVN Repository Scanner - {target}")
    print("="*50)
    
    if not target.startswith(('http://', 'https://')):
        target = 'https://' + target
    
    found = []
    svn_paths = ['/.svn/entries', '/.svn/wc.db', '/.svn/format', '/svn/entries']
    
    for path in svn_paths:
        try:
            r = requests.get(target + path, timeout=10, verify=False)
            if r.status_code == 200:
                print(f"[!] Exposed: {path}")
                found.append(path)
        except:
            pass
    
    print("\n" + "="*50)
    if found:
        print(f"[!] Found {len(found)} SVN files")
    else:
        print("[*] No exposed SVN files found")
    
    return found

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='SVN Scanner')
    parser.add_argument('target', help='Target URL')
    args = parser.parse_args()
    scan(args.target)