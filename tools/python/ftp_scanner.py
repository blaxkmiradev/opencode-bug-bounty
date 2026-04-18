#!/usr/bin/env python3
"""
FTP Scanner
Tests for FTP vulnerabilities
"""

import socket
import argparse

COMMANDS = ['USER', 'PASS', 'LIST', 'RETR', 'STOR', 'CWD', 'PWD', 'QUIT']

def scan(target, port=21):
    print(f"[*] FTP Scanner - {target}:{port}")
    print("="*50)
    
    found = []
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10)
        s.connect((target, port))
        resp = s.recv(1024).decode()
        
        if '220' in resp:
            print(f"[+] FTP Banner: {resp[:100]}")
            found.append('ftp_open')
            
            for cmd in COMMANDS[:3]:
                s.send(f"{cmd}\r\n".encode())
                resp = s.recv(1024).decode()
                if '530' not in resp and '332' not in resp:
                    print(f"  {cmd}: OK")
            
            s.close()
    except Exception as e:
        print(f"[!] Error: {e}")
    
    print("\n" + "="*50)
    print(f"[*] FTP status: {found}")
    
    return found

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='FTP Scanner')
    parser.add_argument('target', help='Target IP')
    parser.add_argument('--port', type=int, default=21, help='Port')
    args = parser.parse_args()
    scan(args.target, args.port)