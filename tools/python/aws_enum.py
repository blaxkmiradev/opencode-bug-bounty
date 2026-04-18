#!/usr/bin/env python3
"""
AWS Metadata Service Scanner
Tests for AWS metadata exposure
"""

import requests
import argparse
import warnings
warnings.filterwarnings('ignore')

METADATA_URLS = [
    'http://169.254.169.254/latest/meta-data/',
    'http://169.254.169.254/latest/user-data/',
    'http://metadata.google.internal/computeMetadata/',
]

def scan(target):
    print(f"[*] AWS Metadata Scanner")
    print("="*50)
    
    found = []
    
    for url in METADATA_URLS:
        try:
            r = requests.get(url, timeout=5, verify=False)
            if r.status_code == 200 and len(r.text) > 0:
                print(f"[!] Metadata exposed: {url}")
                found.append(url)
        except:
            pass
    
    print("\n" + "="*50)
    print(f"[*] Found {len(found)} metadata endpoints")
    
    return found

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='AWS Metadata')
    parser.add_argument('target', nargs='?', default='local', help='Target')
    args = parser.parse_args()
    scan(args.target)