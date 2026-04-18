#!/usr/bin/env python3
"""
Weak Password Detector
Checks for weak password policies
"""

import requests
import re
import argparse
import warnings
warnings.filterwarnings('ignore')

def scan(target):
    print(f"[*] Weak Password Detector - {target}")
    print("="*50)
    
    if not target.startswith(('http://', 'https://')):
        target = 'https://' + target
    
    found = []
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        r = requests.get(target, timeout=10, verify=False, headers=headers)
        
        if 'password' in r.text.lower():
            issues = []
            
            if 'minlength' not in r.text.lower() and 'min-length' not in r.text.lower():
                issues.append("No minimum length requirement")
            
            if not re.search(r'[A-Z]', r.text):
                issues.append("No uppercase requirement")
            
            if not re.search(r'[0-9]', r.text):
                issues.append("No number requirement")
            
            if not re.search(r'[!@#$%^&*]', r.text):
                issues.append("No special character requirement")
            
            if issues:
                print("[!] Weak password policy:")
                for iss in issues:
                    print(f"  - {iss}")
                found = issues
            else:
                print("[*] Password policy appears strong")
    except Exception as e:
        print(f"[!] Error: {e}")
    
    print("\n" + "="*50)
    return found

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Weak Password Detector')
    parser.add_argument('target', help='Target URL')
    args = parser.parse_args()
    scan(args.target)