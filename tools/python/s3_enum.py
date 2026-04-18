#!/usr/bin/env python3
"""
S3 Bucket Enumerator
Discovers and tests S3 buckets
"""

import requests
import argparse
import warnings
warnings.filterwarnings('ignore')

def check_bucket(name, region='us-east-1'):
    urls = [
        f"https://{name}.s3.amazonaws.com",
        f"https://{name}.s3.{region}.amazonaws.com",
    ]
    for url in urls:
        try:
            r = requests.get(url, timeout=10, verify=False)
            if r.status_code == 200:
                return True, url
            elif r.status_code == 403:
                return 'private', url
        except:
            pass
    return False, None

def scan(domain):
    print(f"[*] S3 Bucket Scanner - {domain}")
    print("="*50)
    
    found = []
    common_names = [
        domain.split('.')[0],
        domain.replace('.', '-'),
        domain.replace('.', ''),
        domain.replace('.com', ''),
        'assets',
        'files',
        'uploads',
        'media',
        'backup',
        'backups',
    ]
    
    for name in common_names:
        status, url = check_bucket(name)
        if status:
            print(f"[+] {name}: {status}")
            found.append({'name': name, 'status': status})
        else:
            print(f"[-] {name}: not found")
    
    print("\n" + "="*50)
    print(f"[*] Found {len([f for f in found if f['status'] == True])} buckets")
    
    return found

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='S3 Enumerator')
    parser.add_argument('domain', help='Target domain')
    args = parser.parse_args()
    scan(args.domain)