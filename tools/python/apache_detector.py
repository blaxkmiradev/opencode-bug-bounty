#!/usr/bin/env python3
"""
Apache Misconfiguration Scanner
Detects common Apache misconfigurations
"""

import requests
import argparse
import warnings
warnings.filterwarnings('ignore')

def scan(target):
    print(f"[*] Apache Misconfiguration Scanner - {target}")
    print("="*50)
    
    if not target.startswith(('http://', 'https://')):
        target = 'https://' + target
    
    found = []
    apache_paths = ['/server-status', '/server-info', '/.htaccess', '/.htpasswd']
    
    for path in apache_paths:
        try:
            r = requests.get(target + path, timeout=10, verify=False)
            if r.status_code == 200:
                print(f"[!] Exposed: {path}")
                found.append(path)
        except:
            pass
    
    print("\n" + "="*50)
    if found:
        print(f"[!] Found {len(found)} issues")
    else:
        print("[*] No Apache misconfigurations")
    
    return found

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Apache Scanner')
    parser.add_argument('target', help='Target URL')
    args = parser.parse_args()
    scan(args.target)