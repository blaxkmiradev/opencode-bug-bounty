#!/usr/bin/env python3
"""
Email/Username Enumerator
Usage: python enum_users.py target.com
"""

import sys
import requests
import concurrent.futures

class UserEnumerator:
    def __init__(self, target):
        self.target = target
        self.found = []
        
        # Common usernames/emails
        self.guesses = [
            'admin', 'root', 'test', 'user', 'guest', 'administrator',
            'support', 'helpdesk', 'sales', 'billing', 'contact',
            'info', 'webmaster', 'noreply', 'no-reply',
            'admin@', 'root@', 'test@', 'admin@target.com',
        ]
        
    def check_email(self, email):
        """Check if email exists"""
        url = f"https://{self.target}/password-reset"
        data = {'email': email}
        try:
            r = requests.post(url, data=data, timeout=5, allow_redirects=True)
            if 'not found' in r.text.lower() or 'invalid' in r.text.lower():
                return None
            return email
        except:
            pass
        return None
    
    def check_username(self, username):
        """Check if username exists"""
        url = f"https://{self.target}/signup"
        data = {'username': username}
        try:
            r = requests.post(url, data=data, timeout=5, allow_redirects=True)
            if 'taken' in r.text.lower() or 'exists' in r.text.lower():
                return username
        except:
            pass
        return None
    
    def enumerate(self, threads=10):
        """Enumerate users"""
        print(f"[*] Enumerating users on {self.target}...")
        
        # Generate email guesses
        emails = [f"{u}@{self.target}" for u in self.guesses]
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            futures = {executor.submit(self.check_email, e): e for e in emails}
            
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result:
                    print(f"[!] Possible user: {result}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python enum_users.py <domain>")
        sys.exit(1)
    
    enumerator = UserEnumerator(sys.argv[1])
    enumerator.enumerate()


if __name__ == "__main__":
    main()