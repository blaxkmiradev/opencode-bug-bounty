#!/usr/bin/env python3
"""
CVE Finder - Search for CVEs in software
Usage: python cve_finder.py nginx
Usage: python cve_finder.py "WordPress 5.8"
Usage: python cve_finder.py --cve CVE-2021-44228
"""

import sys
import requests
import json
import argparse

class CVEFinder:
    def __init__(self):
        self.nvd_api = "https://services.nvd.nist.gov/rest/json/cves/2.0"
        self.cve_list = []
        
    def search_by_product(self, product):
        """Search CVEs by product name"""
        print(f"[*] Searching CVEs for: {product}")
        
        params = {
            'keywordSearch': product,
            'resultsPerPage': 50
        }
        
        try:
            r = requests.get(self.nvd_api, params=params, timeout=30)
            data = r.json()
            
            if 'vulnerabilities' in data:
                for vuln in data['vulnerabilities']:
                    cve_id = vuln.get('cve', {}).get('id', 'N/A')
                    desc = vuln.get('cve', {}).get('descriptions', [{}])[0].get('value', 'No description')
                    print(f"\n[+] {cve_id}")
                    print(f"    {desc[:200]}...")
                    self.cve_list.append(cve_id)
                    
        except Exception as e:
            print(f"[!] Error: {e}")
    
    def search_by_cve(self, cve_id):
        """Get specific CVE details"""
        print(f"[*] Fetching {cve_id}...")
        
        try:
            r = requests.get(f"{self.nvd_api}/{cve_id}", timeout=30)
            data = r.json()
            
            if 'vulnerabilities' in data:
                vuln = data['vulnerabilities'][0]
                cve = vuln.get('cve', {})
                
                print(f"\n{'='*60}")
                print(f"CVE: {cve.get('id')}")
                print('='*60)
                
                # Description
                for desc in cve.get('descriptions', []):
                    if desc.get('lang') == 'en':
                        print(f"\nDescription:")
                        print(f"  {desc.get('value')}")
                
                # Metrics
                metrics = cve.get('metrics', {}).get('cvssMetricV31', [{}])
                if metrics:
                    cvss = metrics[0].get('cvssData', {})
                    print(f"\nCVSS Score: {cvss.get('baseScore')}")
                    print(f"Severity: {cvss.get('baseSeverity')}")
                    print(f"Attack Vector: {cvss.get('attackVector')}")
                
                # References
                refs = cve.get('references', [])
                if refs:
                    print(f"\nReferences:")
                    for ref in refs[:5]:
                        print(f"  - {ref.get('url')}")
                
        except Exception as e:
            print(f"[!] Error: {e}")
    
    def search_cwe(self, cwe_id):
        """Search by CWE"""
        print(f"[*] Searching for {cwe_id}...")
        
        params = {
            'cwe': cwe_id,
            'resultsPerPage': 20
        }
        
        try:
            r = requests.get(self.nvd_api, params=params, timeout=30)
            data = r.json()
            
            if 'vulnerabilities' in data:
                print(f"\n[+] Found {len(data['vulnerabilities'])} CVEs with {cwe_id}:")
                for vuln in data['vulnerabilities']:
                    cve_id = vuln.get('cve', {}).get('id')
                    print(f"  - {cve_id}")
                    
        except Exception as e:
            print(f"[!] Error: {e}")
    
    def get_recent(self, days=30):
        """Get recent CVEs"""
        print(f"[*] Getting CVEs from last {days} days...")
        
        params = {
            'pubStartDate': f'2024-01-01',  # Would use datetime in production
            'resultsPerPage': 30
        }
        
        try:
            r = requests.get(self.nvd_api, params=params, timeout=30)
            data = r.json()
            
            if 'vulnerabilities' in data:
                for vuln in data['vulnerabilities'][:20]:
                    cve_id = vuln.get('cve', {}).get('id')
                    print(f"  {cve_id}")
                    
        except Exception as e:
            print(f"[!] Error: {e}")


def main():
    parser = argparse.ArgumentParser(description='CVE Finder')
    parser.add_argument('product', nargs='?', help='Product name')
    parser.add_argument('--cve', help='Search specific CVE')
    parser.add_argument('--cwe', help='Search by CWE')
    parser.add_argument('--recent', type=int, help='Get recent CVEs (days)')
    args = parser.parse_args()
    
    finder = CVEFinder()
    
    if args.cve:
        finder.search_by_cve(args.cve)
    elif args.cwe:
        finder.search_cwe(args.cwe)
    elif args.recent:
        finder.get_recent(args.recent)
    elif args.product:
        finder.search_by_product(args.product)
    else:
        print("""
CVE Finder
=========

Usage:
  python cve_finder.py nginx                    # Search by product
  python cve_finder.py --cve CVE-2021-44228  # Get CVE details
  python cve_finder.py --cwe CWE-79        # Search by CWE
  python cve_finder.py --recent 30          # Recent CVEs

Examples:
  python cve_finder.py WordPress
  python cve_finder.py "Drupal 9"
  python cve_finder.py --cve CVE-2021-44228
  python cve_finder.py --cwe CWE-89
""")


if __name__ == "__main__":
    main()