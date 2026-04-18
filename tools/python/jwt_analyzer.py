#!/usr/bin/env python3
"""
JWT (JSON Web Token) Analyzer
Analyzes JWT tokens for vulnerabilities
"""

import base64
import json
import argparse
import warnings
import hashlib
import hmac
warnings.filterwarnings('ignore')

def decode_jwt(token):
    parts = token.split('.')
    if len(parts) != 3:
        return None
    
    def decode_part(p):
        padding = 4 - (len(p) % 4)
        if padding != 4:
            p += '=' * padding
        try:
            return json.loads(base64.urlsafe_b64decode(p))
        except:
            return None
    
    return {
        'header': decode_part(parts[0]),
        'payload': decode_part(parts[1]),
        'signature': parts[2]
    }

def analyzeJwt(token):
    print(f"[*] JWT Analyzer")
    print("="*50)
    
    decoded = decode_jwt(token)
    if not decoded:
        print("[!] Invalid JWT format")
        return
    
    print(f"\n[Header]:")
    print(json.dumps(decoded['header'], indent=2))
    
    print(f"\n[Payload]:")
    print(json.dumps(decoded['payload'], indent=2))
    
    print(f"\n[Vulnerabilities]:")
    alg = decoded['header'].get('alg', '')
    issues = []
    
    if alg in [None, 'none', '']:
        issues.append("Algorithm 'none' - signature bypass!")
    if alg == 'HS256':
        issues.append("Check for weak secret key")
    if alg in ['RS256', 'ES256']:
        issues.append("Check for key confusion attack")
    
    payload = decoded['payload']
    if 'exp' not in payload:
        issues.append("No expiration - token never expires")
    if 'iat' not in payload:
        issues.append("No issued-at timestamp")
    if 'nbf' not in payload:
        issues.append("No not-before timestamp")
    
    if payload.get('admin') or payload.get('role') == 'admin':
        issues.append("Contains admin role - check privilege escalation")
    
    if issues:
        for iss in issues:
            print(f"  [!] {iss}")
    else:
        print("  [*] No obvious issues found")
    
    return decoded

def scan(target):
    print(f"[*] JWT Scanner - {target}")
    print("="*50)
    
    if not target.startswith(('http://', 'https://')):
        target = 'https://' + target
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    jwt_paths = ['/api/auth', '/api/login', '/api/token', '/auth', '/login', '/token', '/jwt', '/api/jwt']
    
    found = []
    for path in jwt_paths:
        try:
            r = requests.get(target + path, timeout=10, verify=False, headers=headers)
            if 'jwt' in r.text.lower() or 'token' in r.headers.get('Authorization', '').lower():
                print(f"[!] JWT found: {path}")
                found.append(path)
        except:
            pass
    
    print("\n" + "="*50)
    if found:
        print(f"[!] Found {len(found)} JWT endpoints")
    else:
        print("[*] No JWT endpoints found")
    
    return found

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='JWT Analyzer')
    parser.add_argument('target', help='Target URL or JWT token')
    args = parser.parse_args()
    
    if '.' in args.target and len(args.target) > 50:
        analyzeJwt(args.target)
    else:
        scan(args.target)