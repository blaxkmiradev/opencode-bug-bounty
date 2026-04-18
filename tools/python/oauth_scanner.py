#!/usr/bin/env python3
"""
OAuth 2.0 Scanner
Usage: python oauth_scanner.py https://target.com/oauth/authorize
"""

import sys
import requests

class OAuthScanner:
    def __init__(self, target):
        self.target = target
        self.findings = []
        
    def check_redirect(self):
        """Check redirect_uri validation"""
        try:
            params = {'client_id': 'test', 'redirect_uri': 'https://evil.com', 'response_type': 'code'}
            r = requests.get(self.target, params=params, timeout=10, allow_redirects=False)
            
            location = r.headers.get('Location', '')
            if 'evil.com' in location or location.startswith('https://evil'):
                print(f"[!] Open redirect in OAuth: {location}")
                self.findings.append({'type': 'Open redirect', 'value': location})
        except:
            pass
    
    def check_state(self):
        """Check state parameter"""
        r = requests.get(self.target, timeout=10)
        if 'state=' not in r.url:
            print("[!] No state parameter - CSRF vulnerability")
            self.findings.append({'type': 'Missing state', 'issue': 'CSRF'})
    
    def check_pkce(self):
        """Check PKCE support"""
        # Would need to test token endpoint
        print("[*] PKCE check not implemented")
    
    def scan(self):
        """Scan OAuth"""
        print(f"[*] Scanning OAuth on {self.target}...")
        
        self.check_redirect()
        self.check_state()
        
        return self.findings


def main():
    if len(sys.argv) < 2:
        print("Usage: python oauth_scanner.py <url>")
        sys.exit(1)
    
    target = sys.argv[1]
    scanner = OAuthScanner(target)
    scanner.scan()


if __name__ == "__main__":
    main()