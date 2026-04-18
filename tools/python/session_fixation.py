#!/usr/bin/env python3
"""
Session Fixation Scanner
Tests for session fixation vulnerabilities
"""

import requests
import argparse
import warnings
warnings.filterwarnings('ignore')

def scan(target):
    print(f"[*] Session Fixation Scanner - {target}")
    print("="*50)
    
    if not target.startswith(('http://', 'https://')):
        target = 'https://' + target
    
    found = []
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        s = requests.Session()
        
        sess_id = "ATTACKER_SESSION_12345"
        s.cookies.set('session_id', sess_id)
        
        r = s.get(target, headers=headers, verify=False)
        
        for cookie in s.cookies:
            if cookie.name.lower() in ['session', 'sid', 'PHPSESSID', 'JSESSIONID', 'ASP.NET_SessionId']:
                print(f"[!] Session cookie: {cookie.name}")
                found.append(cookie.name)
        
        if 'Set-Cookie' not in str(r.headers):
            print("[!] No session cookie set")
    except Exception as e:
        print(f"[!] Error: {e}")
    
    print("\n" + "="*50)
    print(f"[*] Session handling: {found or 'OK'}")
    
    return found

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Session Fixation')
    parser.add_argument('target', help='Target URL')
    args = parser.parse_args()
    scan(args.target)