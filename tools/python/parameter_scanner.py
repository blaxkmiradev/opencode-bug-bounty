#!/usr/bin/env python3
"""
Parameter Discovery Tool
Usage: python parameter_scanner.py https://target.com
"""

import sys
import requests
import urllib.parse
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

class ParameterScanner:
    def __init__(self, target):
        self.target = target.rstrip('/')
        self.found_params = []
        
        self.wordlists = [
            # Common parameters
            'id', 'user', 'user_id', 'account', 'account_id', 'uid', 'uuid',
            'page', 'offset', 'limit', 'sort', 'order', 'dir', 'search', 'q', 'query',
            's', 'keyword', 'filter', 'category', 'cat', 'tag', 'status', 'type',
            'name', 'title', 'email', 'password', 'pass', 'username', 'login',
            'key', 'token', 'secret', 'api_key', 'auth', 'Authorization',
            'file', 'filename', 'filepath', 'path', 'url', 'link', 'redirect', 'next',
            'debug', 'test', 'prod', 'env', 'config', 'setting', 'option',
            'firstname', 'lastname', 'fullname', 'address', 'phone', 'mobile',
            'country', 'city', 'state', 'zip', 'postal', 'zipcode', 'age', 'dob',
            'admin', 'role', 'privilege', 'access', 'level', 'permission',
            'price', 'amount', 'cost', 'fee', 'total', 'currency',
            'id', 'view', 'download', 'upload', 'uploaded', 'file', 'files',
            'v', 'ver', 'version', 'api', 'app', 'client',
            'format', 'output', 'data', 'date', 'start', 'end',
            'from', 'to', 'subject', 'message', 'comment', 'note',
            'news', 'post', 'blog', 'article', 'item', 'product', 'cart',
            'action', 'do', 'execute', 'run', 'func', 'function',
            'back', 'continue', 'return', 'callback', 'jsonp',
            'session', 'sess', 'sid', 'ref', 'referer', 'rf',
            'error', 'err', 'msg', 'code', 'num', 'number',
            'val', 'value', 'values', 'var', 'variable',
            'old', 'new', 'confirm', 'enable', 'disable',
            'username', 'password', 'email', 'token',
            '_', '__',
        ]
        
    def test_param(self, param, payloads=None):
        """Test a parameter"""
        if payloads is None:
            payloads = ['', 'test', '1', 'x', 'null']
        
        for payload in payloads:
            test_url = f"{self.target}?{param}={payload}"
            try:
                r = requests.get(test_url, timeout=5, allow_redirects=False)
                if r.status_code != 404:
                    return param
            except:
                pass
        return None
    
    def test_form_params(self, param):
        """Test parameters in forms"""
        test_data = {param: 'test'}
        try:
            r = requests.post(self.target, data=test_data, timeout=5)
            if r.status_code < 500:
                return param
        except:
            pass
        return None
    
    def discover(self, threads=20):
        """Discover parameters"""
        print(f"[*] Discovering parameters at {self.target}...")
        
        found = []
        
        # Test common parameters
        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = {executor.submit(self.test_param, p): p for p in self.wordlists[:100]}
            
            for future in as_completed(futures):
                result = future.result()
                if result:
                    print(f"[+] Found parameter: {result}")
                    found.append(result)
        
        self.found_params = found
        return found
    
    def fuzz_parameters(self, wordlist_file=None):
        """Fuzz parameters with wordlist"""
        if wordlist_file:
            try:
                with open(wordlist_file) as f:
                    wordlist = [line.strip() for line in f if line.strip()]
            except:
                print(f"[!] Could not read {wordlist_file}")
                wordlist = self.wordlist
        else:
            wordlist = self.wordlist
        
        print(f"[*] Fuzzing {len(wordlist)} parameters...")
        
        found = []
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = {executor.submit(self.test_param, p): p for p in wordlist}
            
            for future in as_completed(futures):
                result = future.result()
                if result:
                    found.append(result)
                    print(f"[+] Found: {result}")
        
        return found
    
    def save_results(self, filename=None):
        """Save results"""
        if filename is None:
            filename = f"params-{urllib.parse.urlparse(self.target).netloc}.txt"
        
        with open(filename, 'w') as f:
            for param in self.found_params:
                f.write(f"{param}\n")
        
        print(f"[+] Saved to {filename}")
        return filename


def main():
    if len(sys.argv) < 2:
        print("Usage: python parameter_scanner.py <url> [wordlist]")
        sys.exit(1)
    
    target = sys.argv[1]
    scanner = ParameterScanner(target)
    results = scanner.discover()
    
    if results:
        scanner.save_results()
        print(f"\n[+] Found {len(results)} parameters")
    else:
        print("[*] No parameters found")


if __name__ == "__main__":
    main()