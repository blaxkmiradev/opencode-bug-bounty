#!/usr/bin/env python3
"""
MySQL Scanner
Tests MySQL database vulnerabilities
"""

import socket
import argparse

def scan(target, port=3306):
    print(f"[*] MySQL Scanner - {target}:{port}")
    print("="*50)
    
    found = []
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10)
        s.connect((target, port))
        
        banner = s.recv(1024)
        if banner:
            print(f"[+] MySQL: {banner[:50]}")
            found.append('mysql')
            
            s.send(b'\x00\x00\x00\x01\x85\xa6\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
            resp = s.recv(1024)
            
        s.close()
    except Exception as e:
        print(f"[!] Error: {e}")
    
    print("\n" + "="*50)
    return found

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='MySQL Scanner')
    parser.add_argument('target', help='Target IP')
    parser.add_argument('--port', type=int, default=3306, help='Port')
    args = parser.parse_args()
    scan(args.target, args.port)