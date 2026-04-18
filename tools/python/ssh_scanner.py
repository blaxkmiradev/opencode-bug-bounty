#!/usr/bin/env python3
"""
SSH Scanner
Tests SSH configuration
"""

import socket
import argparse

def scan(target, port=22):
    print(f"[*] SSH Scanner - {target}:{port}")
    print("="*50)
    
    found = []
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10)
        s.connect((target, port))
        
        banner = s.recv(1024).decode()
        print(f"[+] SSH Banner: {banner[:50]}")
        found.append('ssh')
        
        s.send(b'SSH-2.0-Test\r\n')
        resp = s.recv(1024).decode()
        if 'SSH' in resp:
            print(f"  Version negotiation")
        
        s.close()
    except Exception as e:
        print(f"[!] Error: {e}")
    
    print("\n" + "="*50)
    return found

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='SSH Scanner')
    parser.add_argument('target', help='Target IP')
    parser.add_argument('--port', type=int, default=22, help='Port')
    args = parser.parse_args()
    scan(args.target, args.port)