#!/usr/bin/env python3
"""
PostgreSQL Scanner
Tests PostgreSQL vulnerabilities
"""

import socket
import argparse

def scan(target, port=5432):
    print(f"[*] PostgreSQL Scanner - {target}:{port}")
    print("="*50)
    
    found = []
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10)
        s.connect((target, port))
        
        banner = s.recv(1024).decode()
        if 'PQ' in banner or banner:
            print(f"[+] PostgreSQL: {banner[:50]}")
            found.append('postgres')
            
            s.close()
    except Exception as e:
        print(f"[!] Error: {e}")
    
    print("\n" + "="*50)
    return found

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='PostgreSQL Scanner')
    parser.add_argument('target', help='Target IP')
    parser.add_argument('--port', type=int, default=5432, help='Port')
    args = parser.parse_args()
    scan(args.target, args.port)