#!/usr/bin/env python3
"""
Bug Hunter - Master Python Runner
Usage: python run.py <command> [options]

Commands:
  recon <target>         - Full recon
  fast <target>          - Fast recon (ports + paths + subs)
  subdomain <target>   - Subdomain enumeration  
  dirs <target>         - Directory scanner
  scan <target>         - Vulnerability scan  
  header <target>       - HTTP header analysis
  jwt <token>           - JWT analyzer
  cors <target>         - CORS scanner
  secret <target>      - Secret scanner
  graphql <target>      - GraphQL scanner
  fuzz <url>            - Fuzzer
  port <target>        - Port scanner
  s3 <bucket>          - S3 scanner
  report               - Generate report
  
EXAMPLES:
  python run.py recon example.com
  python run.py fast example.com  
  python run.py subdomain example.com
  python run.py header https://example.com
  python run.py cors https://api.example.com
  python report --vuln XSS --target example.com --endpoint /search --poc "GET /search?q=<script>"
"""

import sys
import os

def show_help():
    print("""
Bug Hunter - Master Python Runner
=============================

RECON:
  python run.py fast <target>           - Quick scan (ports, paths, subs)
  python run.py subdomain <target>   - Find subdomains
  python run.py dirs <target>        - Directory scanner  
  python run.py port <target>      - Port scanner
  python run.py subdomain_enum.py <target>

ANALYSIS:
  python run.py header <target>    - Security headers
  python run.py cors <target>     - CORS misconfig
  python run.py secret <target>    - Find secrets in JS
  python run.py jwt <token>        - Analyze JWT

VULN SCANNERS:
  python run.py web <target>       - Web vulns
  python run.py xss <url>         - XSS
  python run.py sqli <url>         - SQLi
  python run.py ssrf <url>        - SSRF
  python run.py lfi <url>          - LFI
  python run.py cmdi <url>        - Command injection
  python run.py ssti <url>       - SSTI

SPECIAL:
  python run.py graphql <target>   - GraphQL testing
  python run.py fuzz <url>        - Fuzzer
  python run.py s3 <bucket>       - S3 bucket scanner
  python report --vuln XSS --target example.com --endpoint /search
""")


def main():
    if len(sys.argv) < 2:
        show_help()
        sys.exit(1)
    
    command = sys.argv[1].lower()
    target = sys.argv[2] if len(sys.argv) > 2 else None
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    tools_dir = os.path.join(os.path.dirname(os.path.dirname(base_dir)), 'tools', 'python')
    
    # Map commands to scripts
    commands = {
        'recon': f'{base_dir}/../tools/python/bug_hunter.py',
        'all': f'{base_dir}/../tools/python/bug_hunter.py',
        'sub': f'{base_dir}/../tools/python/subdomain_enum.py',
        'param': f'{base_dir}/../tools/python/parameter_scanner.py',
        'header': f'{base_dir}/../tools/python/header_analyzer.py',
        'jwt': f'{base_dir}/../tools/python/jwt_analyzer.py',
        'csp': f'{base_dir}/../tools/python/csp_bypass.py',
    }
    
    if command == 'help' or command == '--help':
        show_help()
        sys.exit(1)
    
    # Map commands to scripts
    scripts = {
        'recon': lambda t: f'{tools_dir}/bug_hunter.py',
        'fast': lambda t: f'{tools_dir}/fast_scanner.py',
        'quick': lambda t: f'{tools_dir}/fast_scanner.py',
        'subdomain': lambda t: f'{tools_dir}/subdomain_enum.py',
        'subdomain_enum': lambda t: f'{tools_dir}/subdomain_enum.py',
        'dirs': lambda t: f'{tools_dir}/dir_scanner.py',
        'header': lambda t: f'{tools_dir}/header_analyzer.py',
        'header-analysis': lambda t: f'{tools_dir}/header_analyzer.py',
        'cors': lambda t: f'{tools_dir}/cors_scanner.py',
        'secret': lambda t: f'{tools_dir}/secret_scanner.py',
        'jwt': lambda t: f'{tools_dir}/jwt_analyzer.py',
        'csp': lambda t: f'{tools_dir}/csrf_poc.py',
        'param': lambda t: f'{tools_dir}/parameter_scanner.py',
        'web': lambda t: f'{tools_dir}/web_scanner.py',
        'xss': lambda t: f'{tools_dir}/xss_scanner.py',
        'sqli': lambda t: f'{tools_dir}/sqli_scanner.py',
        'ssrf': lambda t: f'{tools_dir}/ssrf_scanner.py',
        'lfi': lambda t: f'{tools_dir}/lfi_scanner.py',
        'cmdi': lambda t: f'{tools_dir}/cmdi_scanner.py',
        'ssti': lambda t: f'{tools_dir}/json_injection.py',
        'xml': lambda t: f'{tools_dir}/xml_injection.py',
        'open-redirect': lambda t: f'{tools_dir}/open_redirect.py',
        'graphql': lambda t: f'{tools_dir}/graphql_scanner.py',
        'oauth': lambda t: f'{tools_dir}/oauth_scanner.py',
        'upload': lambda t: f'{tools_dir}/upload_tester.py',
        'proto-pollution': lambda t: f'{tools_dir}/proto_pollution.py',
        'port': lambda t: f'{tools_dir}/nmap_scan.py',
        's3': lambda t: f'{tools_dir}/s3_scanner.py',
        'tech': lambda t: f'{tools_dir}/fingerprint.py',
        'fingerprint': lambda t: f'{tools_dir}/fingerprint.py',
        'fuzz': lambda t: 'FUZZ_MODE',
        'race': lambda t: f'{tools_dir}/race_tester.py',
        'shellshock': lambda t: f'{tools_dir}/shellshock.py',
        'heartbleed': lambda t: f'{tools_dir}/heartbleed.py',
        'takeover': lambda t: f'{tools_dir}/subdomain_takeover.py',
    }
    
    if command in ['report', 'generate']:
        # Handle report generation
        if command == 'report':
            print("Use: python generate_report.py --vuln XSS --target example.com --endpoint /search")
        return
    
    if command in scripts:
        if not target and command != 'fuzz':
            print("[!] Target required")
            print(f"Available: {', '.join(scripts.keys())}")
            sys.exit(1)
        
        script = scripts[command]
        if callable(script):
            script_path = script(target)
        else:
            script_path = script
        
        # Special case for fuzz
        if command == 'fuzz':
            print("[*] Use: python fuzz.py <url> <wordlist>")
            return
        
        # Run the script
        import subprocess
        try:
            result = subprocess.run([sys.executable, script_path] + ([target] if target else []), 
                              capture_output=False)
        except Exception as e:
            print(f"[!] Error: {e}")
    
    elif command == 'enum':
        # enum network <target>
        if len(sys.argv) < 3:
            print("[!] Target required")
            sys.exit(1)
        
        target = sys.argv[2]
        import subprocess
        result = subprocess.run([
            sys.executable, 
            f'{tools_dir}/header_analyzer.py',
            target
        ])
    
    elif command == 'port':
        import subprocess
        result = subprocess.run([sys.executable, f'{tools_dir}/nmap_scan.py', target])
    
    elif command == 's3':
        import subprocess
        result = subprocess.run([sys.executable, f'{tools_dir}/s3_scanner.py', target])
    
    elif command == 'graphql':
        import subprocess
        result = subprocess.run([sys.executable, f'{tools_dir}/graphql_scanner.py', target])
    
    elif command == 'cve':
        # CVE finder
        import subprocess
        result = subprocess.run([sys.executable, f'{tools_dir}/cve_finder.py'] + ([target] if target else []))
    
    elif command == 'vulnlevel':
        # Vulnerability level scanner
        import subprocess
        result = subprocess.run([sys.executable, f'{tools_dir}/vuln_level.py', target])
    
    elif command == 'cvss':
        # CVSS calculator
        import subprocess
        result = subprocess.run([sys.executable, f'{tools_dir}/cvss_calculator.py'])
    
    elif command == 'test':
        # test <type> <target>
        if len(sys.argv) < 4:
            print("[!] Usage: test <type> <target>")
            sys.exit(1)
        
        test_type = sys.argv[2]
        target = sys.argv[3]
        
        print(f"[*] Running {test_type} on {target}")
        # Add more test types here
    
    elif command == 'bruteforce':
        # bruteforce <target> <users> <passwords>
        if len(sys.argv) < 5:
            print("[!] Usage: bruteforce <target> <users_file> <passwords_file>")
            sys.exit(1)
        
        target = sys.argv[2]
        users = sys.argv[3]
        passwords = sys.argv[4]
        
        import subprocess
        result = subprocess.run([
            sys.executable,
            f'{base_dir}/../tools/python/bruteforce.py',
            target, '/login', users, passwords
        ])
    
    else:
        print(f"[!] Unknown command: {command}")
        show_help()


if __name__ == "__main__":
    main()