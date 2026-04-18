#!/usr/bin/env python3
"""
Bug Hunter - Ultimate Python Toolkit
Run all tools with one command

Usage:
  python ALL.py scan example.com        # Full scan
  python ALL.py quick example.com   # Quick scan
  python ALL.py vuln example.com   # Vulnerability scan
  python ALL.py recon example.com # Recon only
"""

import sys
import os
import subprocess
import argparse

TOOLS = {
    # Recon
    'fast': 'fast_scanner.py',
    'subdomain': 'subdomain_enum.py',
    'port': 'nmap_scan.py',
    'tech': 'fingerprint.py',
    'fingerprint': 'fingerprint.py',
    'dirs': 'dir_scanner.py',
    'param': 'parameter_scanner.py',
    
    # Vuln Scanners
    'web': 'web_scanner.py',
    'xss': 'xss_scanner.py',
    'sqli': 'sqli_scanner.py',
    'ssrf': 'ssrf_scanner.py',
    'lfi': 'lfi_scanner.py',
    'cmdi': 'cmdi_scanner.py',
    'ssti': 'json_injection.py',
    'xml': 'xml_injection.py',
    'open_redirect': 'open_redirect.py',
    'proto': 'proto_pollution.py',
    
    # Analysis
    'header': 'header_analyzer.py',
    'cors': 'cors_scanner.py',
    'csp': 'csrf_poc.py',
    'secret': 'secret_scanner.py',
    'jwt': 'jwt_analyzer.py',
    
    # Special
    'graphql': 'graphql_scanner.py',
    'oauth': 'oauth_scanner.py',
    'upload': 'upload_tester.py',
    's3': 's3_scanner.py',
    'race': 'race_tester.py',
    
    # CVE
    'shellshock': 'shellshock.py',
    'heartbleed': 'heartbleed.py',
}

QUICK = ['fast']
RECON = ['subdomain', 'port', 'tech', 'fingerprint', 'dirs']
VULN = ['web', 'xss', 'sqli', 'ssrf', 'lfi', 'cmdi', 'ssti', 'header', 'cors']


def run_tool(tool, target, python):
    """Run a single tool"""
    tool_path = os.path.join(os.path.dirname(__file__), TOOLS[tool])
    if target:
        subprocess.run([python, tool_path, target])
    else:
        subprocess.run([python, tool_path])


def run_all(target, mode, python='python'):
    """Run all tools in a category"""
    tools = []
    if mode == 'quick':
        tools = QUICK
    elif mode == 'recon':
        tools = RECON
    elif mode == 'vuln':
        tools = VULN
    elif mode == 'scan':
        tools = list(TOOLS.keys())
    else:
        tools = [mode]
    
    print(f"\n{'='*50}")
    print(f"Bug Hunter - Running {mode} scan on {target}")
    print('='*50 + '\n')
    
    for tool in tools:
        if tool in TOOLS:
            print(f"\n[*] Running {tool}...")
            try:
                run_tool(tool, target, python)
            except Exception as e:
                print(f"[!] Error: {e}")
    
    print(f"\n{'='*50}")
    print(f"[+] Scan complete!")
    print('='*50)


def main():
    parser = argparse.ArgumentParser(description='Ultimate Bug Hunter Toolkit')
    parser.add_argument('mode', nargs='?', default='help', help='Scan mode')
    parser.add_argument('target', nargs='?', help='Target')
    parser.add_argument('-m', '--mode', default='scan', help='Mode: quick/recon/vuln/scan')
    parser.add_argument('-p', '--python', default='python', help='Python interpreter')
    args = parser.parse_args()
    
    if args.mode == 'help':
        print("""
Bug Hunter - Ultimate Python Toolkit
============================

USAGE:
  python ALL.py scan <target>      # Full scan (all tools)
  python ALL.py quick <target>     # Quick scan
  python ALL.py recon <target>    # Recon only
  python ALL.py vuln <target>    # Vuln scan only
  
  python ALL.py xss <url>        # Run specific tool
  python ALL.py sqli <url>
  python ALL.py header <url>
  
MODES:
  quick  - Fast scan (1 tool)
  recon  - Recon (port, subdomain, tech)
  vuln   - Vulnerability scan (XSS, SQLi, etc)
  scan   - All tools (full scan)
  
SPECIFIC:
  xss, sqli, ssrf, lfi, cmdi, ssti, xml, open_redirect
  header, cors, csp, secret, jwt
  graphql, oauth, upload, s3, race
  shellshock, heartbleed
""")
        return
    
    target = args.target or args.target
    
    mode = args.mode
    if args.mode not in ['quick', 'recon', 'vuln', 'scan']:
        mode = 'scan'
        if args.target:
            target = args.target
        else:
            target = sys.argv[1] if len(sys.argv) > 1 else sys.argv[1]
            if target in TOOLS:
                mode = target
                target = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not target:
        print("[!] Target required")
        print("Usage: python ALL.py scan <target>")
        sys.exit(1)
    
    run_all(target, mode if mode in ['quick', 'recon', 'vuln'] else 'scan', args.python)


if __name__ == "__main__":
    main()