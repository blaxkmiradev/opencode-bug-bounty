#!/usr/bin/env python3
"""
GraphQL Introspection Scanner
Tests GraphQL for vulnerabilities
"""

import requests
import argparse
import warnings
warnings.filterwarnings('ignore')

INTROSPECTION_QUERY = '{"query":"{__schema{types{name}}}"}'

def scan(target):
    print(f"[*] GraphQL Scanner - {target}")
    print("="*50)
    
    if not target.startswith(('http://', 'https://')):
        target = 'https://' + target
    
    found = []
    gql_paths = ['/graphql', '/api/graphql', '/gql', '/query']
    
    for path in gql_paths:
        try:
            r = requests.post(target + path, data=INTROSPECTION_QUERY, 
                         headers={'Content-Type': 'application/json'}, timeout=10, verify=False)
            if '"data"' in r.text or '__schema' in r.text:
                print(f"[!] GraphQL enabled: {path}")
                found.append(path)
                
                if '"queryType"' in r.text:
                    print(f"    [!] Introspection enabled")
        except:
            pass
    
    print("\n" + "="*50)
    print(f"[*] Found {len(found)} GraphQL endpoints")
    
    return found

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='GraphQL Scanner')
    parser.add_argument('target', help='Target URL')
    args = parser.parse_args()
    scan(args.target)