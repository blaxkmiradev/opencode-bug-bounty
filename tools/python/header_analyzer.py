#!/usr/bin/env python3
"""
HTTP Header Security Analyzer
Usage: python header_analyzer.py https://target.com
"""

import sys
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class HeaderAnalyzer:
    def __init__(self, target):
        self.target = target.rstrip('/')
        self.headers = {}
        self.security_headers = {
            # Security headers to check
            'Content-Security-Policy': {
                'required': True,
                'good': "default-src 'self'",
                'description': 'Prevents XSS by controlling resource loading'
            },
            'Strict-Transport-Security': {
                'required': True,
                'good': 'max-age',
                'description': 'Enforces HTTPS'
            },
            'X-Content-Type-Options': {
                'required': True,
                'good': 'nosniff',
                'description': 'Prevents MIME type sniffing'
            },
            'X-Frame-Options': {
                'required': True,
                'good': ['DENY', 'SAMEORIGIN'],
                'description': 'Prevents clickjacking'
            },
            'X-XSS-Protection': {
                'required': False,
                'good': '1; mode=block',
                'description': 'Legacy XSS filter (deprecated)'
            },
            'Referrer-Policy': {
                'required': True,
                'good': ['no-referrer', 'same-origin', 'strict-origin'],
                'description': 'Controls referrer information'
            },
            'Permissions-Policy': {
                'required': True,
                'good': '.',
                'description': 'Controls browser features'
            },
            'Set-Cookie': {
                'required': True,
                'good': ['Secure', 'HttpOnly', 'SameSite'],
                'description': 'Cookie security flags'
            },
            'X-Permitted-Cross-Domain-Policies': {
                'required': False,
                'good': 'none',
                'description': 'Controls Adobe Flash cross-domain requests'
            },
            'Cross-Origin-Opener-Policy': {
                'required': False,
                'good': 'same-origin',
                'description': 'Isolates browsing context'
            },
            'Cross-Origin-Resource-Policy': {
                'required': False,
                'good': 'same-origin',
                'description': 'Controls resource sharing'
            },
            'Cross-Origin-Embedder-Policy': {
                'required': False,
                'good': 'require-corp',
                'description': 'Controls embedding'
            },
            'Cache-Control': {
                'required': True,
                'good': ['no-store', 'no-cache', 'private'],
                'description': 'Controls caching of sensitive data'
            },
            'Pragma': {
                'required': False,
                'good': 'no-cache',
                'description': 'Legacy cache control'
            },
            'Server': {
                'required': False,
                'good': 'remove or obscure',
                'description': 'Server version disclosure'
            },
            'X-Powered-By': {
                'required': False,
                'good': 'remove',
                'description': 'Technology disclosure'
            },
        }
        
    def analyze(self):
        """Analyze HTTP headers"""
        print(f"[*] Analyzing headers at {self.target}...")
        
        try:
            r = requests.get(self.target, timeout=10, verify=False)
            self.headers = dict(r.headers)
        except Exception as e:
            print(f"[!] Error: {e}")
            return None
        
        return self.headers
    
    def check_security_headers(self):
        """Check security headers"""
        results = {
            'missing': [],
            'weak': [],
            'good': []
        }
        
        for header, info in self.security_headers.items():
            value = self.headers.get(header)
            
            if value is None:
                if info['required']:
                    results['missing'].append(header)
                    print(f"[!] MISSING: {header} - {info['description']}")
                continue
            
            # Check if value is good
            good_values = info['good']
            if isinstance(good_values, list):
                best = any(g in value for g in good_values)
            else:
                best = good_values in value if good_values else False
            
            if best:
                results['good'].append(header)
                print(f"[+] GOOD: {header} = {value}")
            else:
                results['weak'].append((header, value))
                print(f"[!] WEAK: {header} = {value}")
        
        return results
    
    def check_cors(self):
        """Check CORS configuration"""
        print("\n[*] Checking CORS...")
        
        cors_headers = [
            'Access-Control-Allow-Origin',
            'Access-Control-Allow-Methods',
            'Access-Control-Allow-Headers',
            'Access-Control-Allow-Credentials',
            'Access-Control-Max-Age',
            'Access-Control-Expose-Headers',
        ]
        
        cors_config = {}
        for header in cors_headers:
            value = self.headers.get(header)
            if value:
                cors_config[header] = value
                print(f"[*] {header}: {value}")
        
        # Check for misconfigurations
        origin = cors_config.get('Access-Control-Allow-Origin')
        credentials = cors_config.get('Access-Control-Allow-Credentials')
        
        if origin == '*':
            print("[!] CORS: Wildcard origin allows any site")
            if credentials == 'true':
                print("[!] CORS: Wildcard + credentials = critical vulnerability")
        
        return cors_config
    
    def check_info_disclosure(self):
        """Check for information disclosure"""
        print("\n[*] Checking information disclosure...")
        
        disclosure = []
        
        # Check server header
        server = self.headers.get('Server')
        if server and server != 'Cloudflare':
            disclosure.append(f"Server: {server}")
            print(f"[!] Server disclosure: {server}")
        
        # Check powered by
        powered = self.headers.get('X-Powered-By')
        if powered:
            disclosure.append(f"X-Powered-By: {powered}")
            print(f"[!] Technology disclosure: {powered}")
        
        # Check for debug headers
        for header in self.headers:
            if 'debug' in header.lower() or 'trace' in header.lower():
                disclosure.append(header)
                print(f"[!] Debug header: {header} = {self.headers[header]}")
        
        return disclosure
    
    def generate_report(self):
        """Generate full report"""
        self.analyze()
        results = self.check_security_headers()
        cors = self.check_cors()
        disclosure = self.check_info_disclosure()
        
        # Summary
        print("\n" + "="*50)
        print("HEADER SECURITY REPORT")
        print("="*50)
        print(f"\n[+] Good headers: {len(results['good'])}")
        
        if results['missing']:
            print(f"\n[!] Missing required headers: {len(results['missing'])}")
            for h in results['missing']:
                print(f"    - {h}")
        
        if results['weak']:
            print(f"\n[!] Weak headers: {len(results['weak'])}")
            for h, v in results['weak']:
                print(f"    - {h}: {v}")
        
        if disclosure:
            print(f"\n[!] Information disclosure: {len(disclosure)}")
            for d in disclosure:
                print(f"    - {d}")
        
        return {
            'good': results['good'],
            'missing': results['missing'],
            'weak': results['weak'],
            'cors': cors,
            'disclosure': disclosure
        }


def main():
    if len(sys.argv) < 2:
        print("Usage: python header_analyzer.py <target>")
        sys.exit(1)
    
    target = sys.argv[1]
    analyzer = HeaderAnalyzer(target)
    analyzer.generate_report()


if __name__ == "__main__":
    main()