#!/usr/bin/env python3
"""
Web Crawler
Crawls website for links and pages
"""

import requests
import re
from urllib.parse import urljoin
import argparse
import warnings
warnings.filterwarnings('ignore')

def crawl(url, depth=2):
    print(f"[*] Web Crawler - {url}")
    print("="*50)
    
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    visited = set()
    found = []
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    def visit(page):
        if page in visited or len(visited) > 50:
            return
        visited.add(page)
        
        try:
            r = requests.get(page, timeout=10, verify=False, headers=headers)
            links = re.findall(r'href=["\']([^"\']+)["\']', r.text)
            
            for link in links[:20]:
                if link.startswith('/') or link.startswith(url):
                    full_url = urljoin(page, link)
                    if url in full_url and full_url not in found:
                        found.append(full_url)
                        print(f"[+] {full_url}")
        except:
            pass
    
    visit(url)
    
    print("\n" + "="*50)
    print(f"[*] Found {len(found)} pages")
    
    return found

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Web Crawler')
    parser.add_argument('target', help='Target URL')
    args = parser.parse_args()
    crawl(args.target)