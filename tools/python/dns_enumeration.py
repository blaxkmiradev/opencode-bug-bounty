#!/usr/bin/env python3
"""
DNS Enumeration Tool
Discovers DNS records for a domain
"""

import socket
import argparse
import warnings
warnings.filterwarnings('ignore')

RECORD_TYPES = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME', 'SOA', 'PTR', 'SPF']

def lookup(domain, record_type):
    try:
        import dns.resolver
        answers = dns.resolver.resolve(domain, record_type)
        return [str(r) for r in answers]
    except:
        return []

def scan(domain):
    print(f"[*] DNS Enumeration - {domain}")
    print("="*50)
    
    found = {}
    for rtype in RECORD_TYPES:
        try:
            result = lookup(domain, rtype)
            if result:
                found[rtype] = result
                print(f"[+] {rtype}: {result}")
        except Exception as e:
            pass
    
    print("\n" + "="*50)
    print(f"[*] Found {len(found)} record types")
    
    return found

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='DNS Enumeration')
    parser.add_argument('domain', help='Target domain')
    args = parser.parse_args()
    scan(args.domain)