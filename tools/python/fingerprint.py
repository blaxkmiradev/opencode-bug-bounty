#!/usr/bin/env python3
"""
Technology Fingerprinter
Usage: python fingerprint.py https://target.com
"""

import sys
import requests

class Fingerprinter:
    def __init__(self, target):
        self.target = target
        self.tech = []
        
        self.signatures = {
            'WordPress': ['wp-content', 'wp-includes', 'wp-admin'],
            'Drupal': ['drupal', 'sites/default'],
            'Joomla': ['joomla', 'administrator'],
            'Magento': ['magento', 'skin/frontend'],
            'Shopify': ['cdn.shopify.com', 'shopify'],
            'Wix': ['wixstatic.com', 'wixdns'],
            'React': ['react', 'react-dom', 'reactjs'],
            'Vue': ['vue', 'vuejs', 'vue-router'],
            'Angular': ['@angular', 'ng-app'],
            'Svelte': ['svelte'],
            'Next.js': ['next', '_next/static'],
            'Nuxt': ['_nuxt', '@nuxt'],
            'Express': ['Express', 'node_modules/express'],
            'Django': ['csrfmiddlewaretoken', 'django'],
            'Flask': ['flask', 'jinja2'],
            'Laravel': ['laravel', 'XSRF-TOKEN'],
            'Rails': ['rails', 'actionpack'],
            'ASP.NET': ['__VIEWSTATE', 'asp.net'],
            'Spring': ['spring', 'pivotal'],
            'Nginx': ['nginx'],
            'Apache': ['apache', 'mod_'],
            'IIS': ['iis', 'asp.net'],
            'CloudFlare': ['cloudflare', '__cf_bm'],
            'AWS': ['aws-sdk', 'amazon'],
            'Azure': ['azure', 'windows.net'],
        }
    
    def fingerprint(self):
        """Fingerprint technologies"""
        try:
            r = requests.get(self.target, timeout=10)
            content = r.text.lower()
            headers = {k.lower(): v.lower() for k, v in r.headers.items()}
            
            # Check headers
            server = headers.get('server', '')
            x powered = headers.get('x-powered-by', '')
            
            if server:
                print(f"[+] Server: {server}")
            if x-powered:
                print(f"[+] X-Powered-By: {x-powered}")
            
            # Check content
            for tech, sigs in self.signatures.items():
                for sig in sigs:
                    if sig.lower() in content or sig.lower() in server:
                        if tech not in self.tech:
                            self.tech.append(tech)
            
            # Check cookies
            cookies = r.headers.get('set-cookie', '')
            cookie_sigs = {
                'wordpress': 'wordpress',
                'laravel': 'laravel_session',
                'django': 'csrftoken',
                'express': 'connect.sid',
                'rails': '_rails_session',
            }
            for name, sig in cookie_sigs.items():
                if sig in cookies:
                    if name.title() not in self.tech:
                        self.tech.append(name.title())
            
            if self.tech:
                print(f"\n[+] Technologies: {', '.join(self.tech)}")
            
        except Exception as e:
            print(f"[!] Error: {e}")
        
        return self.tech


def main():
    if len(sys.argv) < 2:
        print("Usage: python fingerprint.py <url>")
        sys.exit(1)
    
    fp = Fingerprinter(sys.argv[1])
    fp.fingerprint()


if __name__ == "__main__":
    main()