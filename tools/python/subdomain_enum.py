#!/usr/bin/env python3
"""
Subdomain Enumeration Tool
Usage: python subdomain_enum.py target.com
"""

import sys
import requests
import concurrent.futures
import json
from urllib.parse import urlparse

class SubdomainEnumerator:
    def __init__(self, target):
        self.target = target.replace('http://', '').replace('https://', '').split('/')[0]
        self.subdomains = []
        self.wordlists = [
            'www', 'mail', 'ftp', 'localhost', 'webmail', 'smtp', 'pop', 'ns1', 'webdisk',
            'ns', 'mail2', 'cpanel', 'whm', 'autodiscover', 'autoconfig', 'm', 'imap',
            'test', 'ns1', 'dns2', 'static', 'apps', 'google', 'beta', 'shop', 'my',
            'git', 'svn', 'mirror', 'cdn', 'backup', 'staging', 'dev', 'cloud',
            '02', '03', 'new', 'old', 'en', 'store', 'admin', 'login', 'corp',
            'support', 'media', 'i', 'jira', 'git', 'wiki', 'docs', 'forum',
            'news', 'archive', 'www2', 'nginx', 'apache', 'kb', 'images', 'img',
            'test1', 'test2', 'test3', 'mx', 'live', 'map', 'ga', 'beta', 'cp',
            'demo', 'node1', 'sql', 'mysql', 'postgresql', 'mariadb', 'mongo', 'redis',
            'elasticsearch', 'kibana', 'grafana', 'prometheus', 'jenkins', 'tracker',
            'phpmyadmin', 'status', 'ci', 'cd', 'gitlab', 'sonarqube', 'taiga', 'mattermost',
            's3', 's3.amazonaws.com', 'aws', 'gcp', 'azure', 'digitalocean', 'linode',
            'vpc', ' bastion', 'jump', 'gateway', 'vpn', 'proxy', 'lb', 'elb',
        ]
        
    def check_subdomain(self, subdomain):
        """Check if subdomain exists"""
        url = f"http://{subdomain}.{self.target}"
        try:
            r = requests.get(url, timeout=3, allow_redirects=True)
            if r.status_code < 400:
                return {'subdomain': url, 'status': r.status_code, 'title': self.extract_title(r.text)}
        except:
            pass
        
        # Try HTTPS
        url = f"https://{subdomain}.{self.target}"
        try:
            r = requests.get(url, timeout=3, allow_redirects=True, verify=False)
            if r.status_code < 400:
                return {'subdomain': url, 'status': r.status_code, 'title': self.extract_title(r.text)}
        except:
            pass
        return None
    
    def extract_title(self, html):
        """Extract page title"""
        import re
        match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE)
        if match:
            return match.group(1).strip()
        return ''
    
    def enumerate(self, threads=50):
        """Enumerate subdomains"""
        print(f"[*] Enumerating subdomains for {self.target}...")
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            futures = {executor.submit(self.check_subdomain, sub): sub 
                      for sub in self.subdomains}
            
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result:
                    print(f"[+] FOUND: {result['subdomain']} (Status: {result['status']})")
                    self.subdomains.append(result)
        
        return self.subdomains
    
    def check_cname(self):
        """Check for CNAME records"""
        try:
            import dns.resolver
            for sub in self.subdomains[:50]:  # Check first 50
                try:
                    answers = dns.resolver.resolve(sub, 'CNAME')
                    for rdata in answers:
                        print(f"[*] CNAME: {sub} -> {rdata}")
                except:
                    pass
        except ImportError:
            print("[!] dnspython not installed")
    
    def save_results(self, filename=None):
        """Save results to file"""
        if filename is None:
            filename = f"{self.target}-subdomains.txt"
        
        with open(filename, 'w') as f:
            for sub in self.subdomains:
                f.write(f"{sub}\n")
        
        print(f"[+] Results saved to {filename}")
        return filename


def main():
    if len(sys.argv) < 2:
        print("Usage: python subdomain_enum.py <target>")
        print("Example: python subdomain_enum.py example.com")
        sys.exit(1)
    
    target = sys.argv[1]
    enumerator = SubdomainEnumerator(target)
    results = enumerator.enumerate()
    
    if results:
        enumerator.save_results()
        print(f"\n[+] Found {len(results)} subdomains")
    else:
        print("[*] No subdomains found")


if __name__ == "__main__":
    main()