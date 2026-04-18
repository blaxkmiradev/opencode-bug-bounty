#!/usr/bin/env python3
"""
Insecure Deserialization Scanner
Tests for deserialization vulnerabilities
"""

import requests
import argparse
import warnings
warnings.filterwarnings('ignore')

PAYLOADS = [
    'rO0ABXQ=',  # java base64
    'O:8:"Test":0:{}',  # php serialized
    '{"@type":"java.lang.Class","val":"java.lang.Runtime"}',  # json
]

def scan(target):
    print(f"[*] Insecure Deserialization Scanner - {target}")
    print("="*50)
    
    if not target.startswith(('http://', 'https://'))):
        target = 'https://' + target
    
    found = []
    paths = ['/api/deserialize', '/api/unserialize', '/rpc', '/rest/api']
    
    for path in paths:
        for payload in PAYLOADS:
            try:
                r = requests.post(target + path, data={'data': payload}, timeout=10, verify=False)
            except:
                pass
    
    print("\n" + "="*50)
    print(f"[*] Check complete")
    
    return found

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Deserialization Scanner')
    parser.add_argument('target', help='Target URL')
    args = parser.parse_args()
    scan(args.target)