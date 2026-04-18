#!/usr/bin/env python3
"""
MongoDB Scanner
Tests MongoDB vulnerabilities
"""

import socket
import argparse

def scan(target, port=27017):
    print(f"[*] MongoDB Scanner - {target}:{port}")
    print("="*50)
    
    found = []
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10)
        s.connect((target, port))
        
        s.send(b'\x00\x00\x00\x00\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
        resp = s.recv(1024)
        
        if resp:
            print(f"[+] MongoDB: detected")
            found.append('mongodb')
            
        s.close()
    except Exception as e:
        print(f"[!] Error: {e}")
    
    print("\n" + "="*50)
    return found

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='MongoDB Scanner')
    parser.add_argument('target', help='Target IP')
    parser.add_argument('--port', type=int, default=27017, help='Port')
    args = parser.parse_args()
    scan(args.target, args.port)