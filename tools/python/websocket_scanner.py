#!/usr/bin/env python3
"""
WebSocket Scanner
Tests WebSocket security
"""

import requests
import json
import argparse
import warnings
warnings.filterwarnings('ignore')

def scan(target):
    print(f"[*] WebSocket Scanner - {target}")
    print("="*50)
    
    if not target.startswith(('http://', 'https://')):
        target = 'https://' + target
    
    found = []
    ws_paths = ['/ws', '/websocket', '/api/ws', '/socket.io', '/socket']
    
    for path in ws_paths:
        try:
            r = requests.get(target + path, timeout=10, verify=False)
            if r.status_code == 200:
                print(f"[?] WebSocket: {path}")
                found.append(path)
            elif 'websocket' in r.text.lower():
                print(f"[!] WebSocket found: {path}")
                found.append(path)
        except:
            pass
    
    print("\n" + "="*50)
    print(f"[*] Found {len(found)} WebSocket endpoints")
    return found

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='WebSocket Scanner')
    parser.add_argument('target', help='Target URL')
    args = parser.parse_args()
    scan(args.target)