#!/usr/bin/env python3
"""
SMTP Scanner
Tests SMTP vulnerabilities
"""

import socket
import argparse

COMMANDS = ['HELO', 'MAIL', 'RCPT', 'DATA', 'QUIT', 'VRFY', 'EXPN']

def scan(target, port=25):
    print(f"[*] SMTP Scanner - {target}:{port}")
    print("="*50)
    
    found = []
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10)
        s.connect((target, port))
        resp = s.recv(1024).decode()
        
        if '220' in resp:
            print(f"[+] SMTP: {resp[:50]}")
            found.append('smtp')
            
            s.send(b'HELO test\r\n')
            resp = s.recv(1024).decode()
            
            for cmd in ['VRFY test', 'EXPN test']:
                s.send(f"{cmd}\r\n".encode())
                resp = s.recv(1024).decode()
                if '250' in resp:
                    print(f"  {cmd}: enabled")
            
            s.close()
    except Exception as e:
        print(f"[!] Error: {e}")
    
    print("\n" + "="*50)
    return found

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='SMTP Scanner')
    parser.add_argument('target', help='Target IP')
    parser.add_argument('--port', type=int, default=25, help='Port')
    args = parser.parse_args()
    scan(args.target, args.port)