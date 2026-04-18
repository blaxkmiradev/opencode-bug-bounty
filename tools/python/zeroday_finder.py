#!/usr/bin/env python3
"""
Zero-Day Vulnerability Finder
Finds potential zero-day vulnerabilities through anomaly detection
"""

import requests
import time
import argparse
import warnings
warnings.filterwarnings('ignore')

PATTERNS = [
    ('error', 'error'),
    ('exception', 'exception'),
    ('warning', 'warning'),
    ('failed', 'fail'),
    ('undefined', 'undefined'),
    ('null', 'null'),
    ('NaN', 'nan'),
    ('undefined', 'undefined'),
]

def scan(target, depth=10):
    print(f"[*] Zero-Day Finder - {target}")
    print("="*50)
    
    if not target.startswith(('http://', 'https://')):
        target = 'https://' + target
    
    found = []
    params = ['id', 'page', 'q', 's', 'search', 'q', 'query', 'keyword', 'cat', 'category', 'sort', 'order', 'by', 'filter', 'view', 'mode', 'type', 'year']
    payloads = ['', ' ', 'a', '1', '1a', '<', '>', '/', '\\', '*', 'null', 'undefined', '999999999']
    
    for param in params[:10]:
        for payload in payloads[:3]:
            try:
                start = time.time()
                r = requests.get(target, params={param: payload}, timeout=10, verify=False)
                elapsed = time.time() - start
                
                for pattern, ptype in PATTERNS:
                    if pattern in r.text.lower():
                        if elapsed > 2 or r.status_code != 200:
                            print(f"[?] Anomaly: {param}={payload} ({ptype})")
                            found.append({'param': param, 'payload': payload, 'type': ptype})
            except:
                pass
    
    print("\n" + "="*50)
    print(f"[*] Found {len(found)} anomalies")
    
    return found

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Zero-Day Finder')
    parser.add_argument('target', help='Target URL')
    args = parser.parse_args()
    scan(args.target)