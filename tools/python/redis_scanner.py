#!/usr/bin/env python3
"""
Redis Scanner
Tests Redis vulnerabilities
"""

import socket
import argparse

def scan(target, port=6379):
    print(f"[*] Redis Scanner - {target}:{port}")
    print("="*50)
    
    found = []
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10)
        s.connect((target, port))
        
        banner = s.recv(1024).decode()
        if '+PONG' in banner or banner:
            print(f"[+] Redis: {banner[:50]}")
            found.append('redis')
            
            s.send(b'INFO\r\n')
            resp = s.recv(4096).decode()
            if '# ' in resp:
                print(f"  Info retrieved")
            
            s.close()
    except Exception as e:
        print(f"[!] Error: {e}")
    
    print("\n" + "="*50)
    return found

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Redis Scanner')
    parser.add_argument('target', help='Target IP')
    parser.add_argument('--port', type=int, default=6379, help='Port')
    args = parser.parse_args()
    scan(args.target, args.port)