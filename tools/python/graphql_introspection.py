#!/usr/bin/env python3
"""
GraphQL Introspection Disabler
Tests GraphQL introspection security
"""

import requests
import json
import argparse
import warnings
warnings.filterwarnings('ignore')

QUERY = '{"query":"{__schema{types{name}}}"}'

def scan(target):
    print(f"[*] GraphQL Introspection Scanner - {target}")
    print("="*50)
    
    if not target.startswith(('http://', 'https://')):
        target = 'https://' + target
    
    found = []
    gql_paths = ['/graphql', '/api/graphql', '/gql']
    
    for path in gql_paths:
        try:
            r = requests.post(target + path, data=QUERY, 
                           headers={'Content-Type': 'application/json'}, 
                           timeout=10, verify=False)
            if '__schema' in r.text:
                print(f"[!] Introspection enabled: {path}")
                found.append(path)
                
                if 'queryType' in r.text:
                    types = r.json()
                    print(f"    Query types available")
        except:
            pass
    
    print("\n" + "="*50)
    print(f"[*] Found {len(found)} exposed endpoints")
    return found

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='GraphQL Introspection')
    parser.add_argument('target', help='Target URL')
    args = parser.parse_args()
    scan(args.target)