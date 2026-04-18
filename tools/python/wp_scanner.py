#!/usr/bin/env python3
"""
Advanced WordPress Security Scanner
Usage: python wp_scanner.py target.com
"""

import sys
import requests
import concurrent.futures

class WordPressScanner:
    def __init__(self, target):
        self.target = target.replace('https://', '').replace('http://', '').rstrip('/')
        self.findings = {'critical': [], 'high': [], 'medium': [], 'low': [], 'info': []}
        
    def check_xmlrpc(self):
        """Check xmlrpc.php"""
        url = f"https://{self.target}/xmlrpc.php"
        try:
            r = requests.post(url, data={'xml': 'test'}, timeout=5, verify=False)
            if r.status_code in [200, 405]:
                return True
        except:
            pass
        return False
    
    def check_wp_json(self):
        """Check WP REST API"""
        url = f"https://{self.target}/wp-json/"
        try:
            r = requests.get(url, timeout=5, verify=False)
            if r.status_code == 200:
                return True
        except:
            pass
        return False
    
    def check_user_enum(self):
        """Enumerate WordPress users"""
        url = f"https://{self.target}/wp-json/wp/v2/users"
        try:
            r = requests.get(url, timeout=5, verify=False)
            if r.status_code == 200 and 'id' in r.text:
                return True
        except:
            pass
        return False
    
    def check_login(self):
        """Check login page"""
        url = f"https://{self.target}/wp-login.php"
        try:
            r = requests.get(url, timeout=5, verify=False)
            if r.status_code == 200 and 'login' in r.text.lower():
                return True
        except:
            pass
        return False
    
    def check_readme(self):
        """Check readme.html"""
        url = f"https://{self.target}/readme.html"
        try:
            r = requests.get(url, timeout=5, verify=False)
            if r.status_code == 200 and 'wordpress' in r.text.lower():
                return True
        except:
            pass
        return False
    
    def check_install(self):
        """Check installation"""
        url = f"https://{self.target}/wp-admin/install.php"
        try:
            r = requests.get(url, timeout=5, verify=False)
            if r.status_code == 200 and 'install' in r.text.lower():
                return True
        except:
            pass
        return False
    
    def check_debug(self):
        """Check debug log"""
        url = f"https://{self.target}/debug.log"
        try:
            r = requests.get(url, timeout=5, verify=False)
            if r.status_code == 200:
                return True
        except:
            pass
        return False
    
    def check_backup(self):
        """Check backup files"""
        urls = [
            f"https://{self.target}/wp-content/backup.sql",
            f"https://{self.target}/wp-content/uploads/backup.zip",
            f"https://{self.target}/backup.sql",
            f"https://{self.target}/database.sql"
        ]
        for url in urls:
            try:
                r = requests.get(url, timeout=5, verify=False)
                if r.status_code == 200:
                    return url
            except:
                pass
        return None
    
    def scan(self):
        """Run full WordPress scan"""
        print(f"\n{'='*60}")
        print(f"  WordPress Security Scanner - {self.target}")
        print(f"{'='*60}\n")
        
        checks = [
            ("XML-RPC", self.check_xmlrpc),
            ("WP REST API", self.check_wp_json),
            ("User Enumeration", self.check_user_enum),
            ("Login Page", self.check_login),
            ("Readme", self.check_readme),
            ("Install Page", self.check_install),
            ("Debug Log", self.check_debug),
            ("Backup Files", self.check_backup),
        ]
        
        for name, check in checks:
            print(f"[*] Checking {name}...")
            result = check()
            if result:
                if result == True:
                    print(f"  [!] Found: {name}")
                    self.findings['high'].append(name)
                elif isinstance(result, str):
                    print(f"  [!] Found: {result}")
                    self.findings['critical'].append(result)
            else:
                print(f"  [-] Not found: {name}")
        
        # Summary
        print(f"\n{'='*60}")
        print("  SCAN COMPLETE")
        print("="*60)
        total = sum(len(v) for v in self.findings.values())
        print(f"\n  Total: {total} findings")
        
        for level in ['critical', 'high', 'medium', 'low']:
            if self.findings[level]:
                print(f"    {level.upper()}: {len(self.findings[level])}")
        
        return self.findings


def main():
    if len(sys.argv) < 2:
        print("""
WordPress Security Scanner
=========================

Usage: python wp_scanner.py target.com

Examples:
  python wp_scanner.py anajak.cloud
  python wp_scanner.py khmersamnang.com
        """)
        sys.exit(1)
    
    target = sys.argv[1]
    scanner = WordPressScanner(target)
    scanner.scan()


if __name__ == "__main__":
    main()