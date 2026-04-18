#!/usr/bin/env python3
"""
CSP Bypass Scanner
Usage: python csp_bypass.py https://target.com
"""

import sys
import requests
import urllib.parse
import re

class CSPBypassScanner:
    def __init__(self, target):
        self.target = target
        self.csp = ''
        self.directives = {}
        
    def get_csp(self):
        """Get CSP header"""
        try:
            r = requests.get(self.target, timeout=10)
            self.csp = r.headers.get('Content-Security-Policy', '')
            if not self.csp:
                self.csp = r.headers.get('Content-Security-Policy-Report-Only', '')
        except Exception as e:
            print(f"[!] Error: {e}")
        
        return self.csp
    
    def parse_csp(self):
        """Parse CSP into directives"""
        if not self.csp:
            return {}
        
        directives = {}
        for part in self.csp.split(';'):
            parts = part.strip().split()
            if parts:
                directive = parts[0]
                values = parts[1:] if len(parts) > 1 else []
                directives[directive] = values
        
        self.directives = directives
        return directives
    
    def check_bypasses(self):
        """Check for CSP bypasses"""
        bypasses = []
        
        # Check for unsafe-inline
        if 'unsafe-inline' in self.csp:
            bypasses.append({
                'type': 'unsafe-inline',
                'risk': 'High',
                'description': 'Allows inline scripts'
            })
        
        # Check for unsafe-eval
        if 'unsafe-eval' in self.csp:
            bypasses.append({
                'type': 'unsafe-eval',
                'risk': 'High', 
                'description': 'Allows eval()'
            })
        
        # Check for wildcards
        if '*' in self.csp or "script-src 'none'" not in self.csp:
            check_scripts = self.directives.get('script-src', [])
            if '*' in check_scripts:
                bypasses.append({
                    'type': 'wildcard script-src',
                    'risk': 'Critical',
                    'description': 'Allows scripts from any source'
                })
        
        # Check for data:
        if 'data:' in self.csp:
            bypasses.append({
                'type': 'data: protocol',
                'risk': 'High',
                'description': 'Allows data: URLs in scripts'
            })
        
        # Check for http:
        if 'http:' in self.csp:
            bypasses.append({
                'type': 'http: protocol',
                'risk': 'Medium',
                'description': 'Allows HTTP sources (not HTTPS)'
            })
        
        # Check for missing default-src
        if 'default-src' not in self.csp:
            bypasses.append({
                'type': 'missing default-src',
                'risk': 'Medium',
                'description': 'Uses default fallback'
            })
        
        # Check blob allowing
        if 'blob:' in self.csp:
            bypasses.append({
                'type': 'blob: protocol',
                'risk': 'High',
                'description': 'Allows blob: URLs'
            })
        
        return bypasses
    
    def generate_poc(self):
        """Generate CSP bypass PoC"""
        self.get_csp()
        self.parse_csp()
        bypasses = self.check_bypasses()
        
        print("\n" + "="*50)
        print("CSP BYPASS REPORT")
        print("="*50)
        print(f"\n[*] Full CSP: {self.csp}")
        
        if not self.csp:
            print("[!] No CSP header found!")
            return None
        
        # Show parsed directives
        print(f"\n[*] Directives:")
        for directive, values in self.directives.items():
            print(f"    {directive}: {values}")
        
        # Show bypasses
        if bypasses:
            print(f"\n[!] Found {len(bypasses)} bypasses:")
            for bypass in bypasses:
                print(f"    [{bypass['risk']}] {bypass['type']}")
                print(f"        {bypass['description']}")
        
        return bypasses


def main():
    if len(sys.argv) < 2:
        print("Usage: python csp_bypass.py <target>")
        sys.exit(1)
    
    target = sys.argv[1]
    scanner = CSPBypassScanner(target)
    scanner.generate_poc()


if __name__ == "__main__":
    main()