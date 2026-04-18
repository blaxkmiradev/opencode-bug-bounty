#!/usr/bin/env python3
"""
Subdomain Takeover Checker
Usage: python subdomain_takeover.py target.com
"""

import sys
import socket
import requests

class SubdomainTakeover:
    def __init__(self, target):
        self.target = target
        self.findings = []
        
        self.services = {
            'github.io': ('github.io', 'There isn\'t a GitHub Pages site here'),
            'herokuapp.com': ('heroku.com', 'no such app'),
            'cloudfront.net': ('cloudfront.net', 'Bad Gateway'),
            'azurewebsites.net': ('azurewebsites.net', '404 Web Site not found'),
            's3.amazonaws.com': ('s3.amazonaws.com', 'NoSuchBucket'),
            'elasticbeanstalk.com': ('elasticbeanstalk.com', 'Bad Gateway'),
            'github.com': ('github.io', 'There isn\'t a GitHub Pages site here'),
            'bitbucket.io': ('bitbucket.io', 'Repo not found'),
            'netlify.app': ('netlify.app', 'Not found'),
            'vercel.app': ('vercel.app', 'not found'),
            '_app.getcruise.com': ('herokuapp.com', 'no such app'),
        }
    
    def check_subdomain(self, subdomain):
        """Check subdomain"""
        try:
            resolved = socket.gethostbyname(subdomain)
            print(f"[*] {subdomain} -> {resolved}")
            
            # Check for takeover fingerprints
            for service, (domain, fingerprint) in self.services.items():
                if domain in subdomain:
                    # Try HTTP request
                    try:
                        r = requests.get(f'http://{subdomain}', timeout=5)
                        if fingerprint.lower() in r.text.lower():
                            print(f"[!] Possible takeover: {subdomain} ({service})")
                            self.findings.append({'subdomain': subdomain, 'service': service})
                    except:
                        pass
            
        except socket.gaierror:
            pass
        
        return None
    
    def scan(self, subdomains):
        """Scan subdomains"""
        print(f"[*] Checking {len(subdomains)} subdomains...")
        
        for sub in subdomains:
            self.check_subdomain(sub)
        
        return self.findings


def main():
    if len(sys.argv) < 2:
        print("Usage: python subdomain_takeover.py <subdomains_file>")
        sys.exit(1)
    
    with open(sys.argv[1]) as f:
        subs = [line.strip() for line in f if line.strip()]
    
    checker = SubdomainTakeover('')
    checker.scan(subs)


if __name__ == "__main__":
    main()