#!/usr/bin/env python3
"""
Subdomain Takeover Scanner
Detects potential subdomain takeover vulnerabilities
"""

import requests
import argparse
import warnings
warnings.filterwarnings('ignore')

SERVICE_SIGNATURES = {
    'aws': ['AWS', 'amazon', 'cloudfront', 's3'],
    'github': ['github.io', 'github.dev', 'github.com'],
    'heroku': ['herokuapp.com', 'heroku.com'],
    'gitlab': ['gitlab.io'],
    'bitbucket': ['bitbucket.io'],
    'netlify': ['netlify.app', 'netlify.com'],
    'vercel': ['vercel.app', 'now.sh'],
    'azure': ['azurewebsites.net', 'cloudapp.net'],
    'digitalocean': ['digitalocean.com', 'digitalocean'],
    'fastly': ['fastly.net', 'fastly'],
    'cloudflare': ['cloudflare.net'],
    'wordpress': ['wordpress.com'],
    'wix': ['wixsite.com'],
    'squarespace': ['squarespace.com'],
}

def check_takeover(subdomain):
    for service, signatures in SERVICE_SIGNATURES.items():
        for sig in signatures:
            if sig.lower() in subdomain.lower():
                return service
    return None

def scan(domain):
    print(f"[*] Subdomain Takeover Scanner - {domain}")
    print("="*50)
    
    if not domain.startswith(('http://', 'https://')):
        target = 'https://' + domain
    else:
        target = domain
    
    found = []
    common_subs = ['www', 'blog', 'dev', 'staging', 'test', 'api', 'admin', 'mail', 'ftp', 'mysql', 'smtp', 'pop', 'ns1', 'webmail', 'cpanel', 'whm', 'autodiscover', 'autoconfig']
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    for sub in common_subs:
        subdomain = f"{sub}.{domain}"
        try:
            r = requests.get(f"http://{subdomain}", timeout=5, verify=False, headers=headers, allow_redirects=False)
            
            if r.status_code in [404, 400] or 'does not exist' in r.text.lower() or 'not found' in r.text.lower():
                service = check_takeover(subdomain)
                if service:
                    print(f"[!] Possible takeover: {subdomain} ({service})")
                    found.append({'subdomain': subdomain, 'service': service})
            elif r.status_code == 422:
                print(f"[!] Possible takeover: {subdomain} (422 Error)")
                found.append({'subdomain': subdomain, 'service': 'unknown'})
        except requests.exceptions.ConnectionError:
            pass
        except:
            pass
    
    print("\n" + "="*50)
    if found:
        print(f"[!] Found {len(found)} potential takeover targets")
    else:
        print("[*] No subdomain takeover vulnerabilities found")
    
    return found

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Subdomain Takeover Scanner')
    parser.add_argument('domain', help='Target domain')
    args = parser.parse_args()
    scan(args.domain)