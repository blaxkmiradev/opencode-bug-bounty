#!/usr/bin/env python3
"""
WAF Detector
Detects Web Application Firewalls
"""

import requests
import argparse
import warnings
warnings.filterwarnings('ignore')

WAF_SIGNATURES = {
    'Cloudflare': ['__cfduid', 'cf-ray', 'cloudflare'],
    'AWS WAF': ['aws-waf', 'awswaf'],
    'Akamai': ['akamai', 'akamaighost'],
    'Imperva': ['imperva', 'incapsula'],
    'Sucuri': ['sucuri', 'webshield'],
    'ModSecurity': ['ModSecurity', 'mod_security'],
    'FortiWeb': ['fortiweb', 'fortigate'],
    'Barracuda': ['barracuda', 'barracuda_waf'],
    'F5': ['BIG-IP', 'ASM', 'F5 Networks'],
    'Microsoft': ['Azure', 'Application Gateway'],
}

def scan(target):
    print(f"[*] WAF Detector - {target}")
    print("="*50)
    
    if not target.startswith(('http://', 'https://')):
        target = 'https://' + target
    
    found = []
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        r = requests.get(target, timeout=10, verify=False, headers=headers)
        
        for waf, sigs in WAF_SIGNATURES.items():
            for sig in sigs:
                if sig.lower() in str(r.headers).lower() or sig.lower() in r.text.lower():
                    print(f"[!] WAF Detected: {waf}")
                    found.append(waf)
                    break
        
        if len(r.headers) > 20:
            print(f"[*] Many headers ({len(r.headers)}) - possible proxy/WAF")
            found.append('Unknown Proxy/WAF')
        
    except Exception as e:
        print(f"[!] Error: {e}")
    
    print("\n" + "="*50)
    if found:
        print(f"[!] Detected: {found}")
    else:
        print("[*] No WAF detected")
    
    return found

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='WAF Detector')
    parser.add_argument('target', help='Target URL')
    args = parser.parse_args()
    scan(args.target)