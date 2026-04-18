#!/usr/bin/env python3
"""
GraphQL Scanner
Usage: python graphql_scanner.py https://target.com/graphql
"""

import sys
import requests
import json

class GraphQLScanner:
    def __init__(self, target):
        self.target = target
        self.findings = []
        
    def introspection_query(self):
        """GraphQL introspection query"""
        return {'query': '{ __schema { types { name fields { name type { name } } } } } }'}
    
    def query_introspection(self):
        """Query introspection"""
        try:
            r = requests.post(self.target, json=self.introspection_query(), timeout=10)
            data = r.json()
            
            if 'data' in data and data['data']:
                print("[+] GraphQL introspection enabled")
                return data['data']
        except:
            pass
        return None
    
    def test_query(self, query, description):
        """Test a query"""
        try:
            r = requests.post(self.target, json={'query': query}, timeout=10)
            return r.json()
        except:
            pass
        return None
    
    def scan(self):
        """Scan GraphQL"""
        print(f"[*] Scanning {self.target}...")
        
        # Test introspection
        schema = self.query_introspection()
        if schema:
            self.findings.append({'type': 'Introspection', 'enabled': True})
        
        # Test queries
        queries = [
            ('{ user(id: 1) { id email } }', 'User query'),
            ('{ users { id email } }', 'User list'),
            ('{ __typename }', 'Type query'),
            ('{ me { id email } }', 'Current user'),
        ]
        
        for query, desc in queries:
            result = self.test_query(query, desc)
            if result and 'errors' not in str(result):
                print(f"[+] {desc}: Works")
        
        # Test mutations
        mutations = [
            'mutation { createUser(input: {email: "test@test.com"}) { id } }',
            'mutation { login(email: "admin@admin.com", password: "admin") { token } }',
        ]
        
        for mutation in mutations:
            try:
                r = requests.post(self.target, json={'query': mutation}, timeout=10)
            except:
                pass
        
        return self.findings


def main():
    if len(sys.argv) < 2:
        print("Usage: python graphql_scanner.py <url>")
        sys.exit(1)
    
    target = sys.argv[1]
    scanner = GraphQLScanner(target)
    scanner.scan()


if __name__ == "__main__":
    main()