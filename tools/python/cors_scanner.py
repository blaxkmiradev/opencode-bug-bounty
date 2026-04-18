#!/usr/bin/env python3
"""
CORS Misconfiguration Scanner
Usage: python cors_scanner.py https://target.com/api
"""

import sys
import requests
import urllib.parse

class CORSScanner:
    def __init__(self, target):
        self.target = target
        self.findings = []
        
    def test_origin(self, origin):
        """Test origin"""
        try:
            headers = {'Origin': origin}
            r = requests.get(self.target, headers=headers, timeout=10)
            acao = r.headers.get('Access-Control-Allow-Origin')
            print(f"[*] Origin: {origin} -> ACAO: {acao}")
            
            if acao == '*':
                self.findings.append({'origin': origin, 'issue': 'Wildcard', 'acao': acao})
            
            if acao == origin or acao == f'https://{urllib.parse.urlparse(origin).netloc}':
                self.findings.append({'origin': origin, 'issue': 'Echoed origin', 'acao': acao})
            
            if acao and 'null' in acao.lower():
                self.findings.append({'origin': origin, 'issue': 'Null', 'acao': acao})
            
            if r.headers.get('Access-Control-Allow-Credentials', '').lower() == 'true':
                if acao in ['*', origin]:
                    self.findings.append({'origin': origin, 'issue': 'Credentials + wildcard', 'acao': acao})
            
        except Exception as e:
            pass
        
        return None
    
    def scan(self):
        """Scan CORS"""
        print(f"[*] Scanning CORS on {self.target}...")
        
        origins = [
            'https://attacker.com',
            'http://attacker.com',
            'https://attacker.com/',
            'null',
            'null',
            'https://target.com.evil.com',
            'https://evil.com',
            'http://127.0.0.1',
            'https://localhost',
            'null',
        ]
        
        for origin in origins:
            self.test_origin(origin)
        
        if self.findings:
            print(f"\n[!] Found {len(self.findings)} CORS issues")
            for f in self.findings:
                print(f"    {f}")
        
        return self.findings


def main():
    if len(sys.argv) < 2:
        print("Usage: python cors_scanner.py <url>")
        sys.exit(1)
    
    target = sys.argv[1]
    scanner = CORSScanner(target)
    scanner.scan()


if __name__ == "__main__":
    main()