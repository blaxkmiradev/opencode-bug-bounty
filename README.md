# Bug Hunter - Professional Bug Bounty Toolkit

Comprehensive security testing toolkit for bug bounty hunters, penetration testers, and security professionals.

## Features

- **7 Specialized Skills** - Each skill focuses on a specific area of security testing
- **20+ Tools** - PowerShell and Python tools for all testing needs
- **Complete Workflow** - From recon to report generation

## Skills

| Skill | Description |
|-------|-------------|
| **bug-bounty** | Main bug bounty workflow, hunting, chaining |
| **web-audit** | Web app security audit, source code review |
| **mobile-security** | Android/iOS APK analysis |
| **cloud-security** | AWS/GCP/Azure cloud testing |
| **network-security** | Network penetration testing |
| **api-security** | REST/GraphQL API testing |
| **red-team** | Red teaming operations |
| **report-writing** | Professional report writing |

## Tools

### PowerShell Tools (tools/bug-hunter/)
```
recon.ps1           - Subdomain enumeration
scan.ps1            - Vulnerability scanner
test-idor.ps1       - IDOR testing
test-ssrf.ps1       - SSRF testing  
test-xss.ps1        - XSS testing
test-sqli.ps1       - SQLi testing
test-ssti.ps1       - SSTI testing
test-ai.ps1         - AI/LLM security
test-oauth.ps1      - OAuth/OIDC testing
test-api.ps1        - API security
test-mobile.ps1     - Mobile app analysis
enum-network.ps1    - Network enumeration
chain.ps1           - Bug chaining
report.ps1          - Report generation
setup.ps1           - Tool installer
```

### Python Tools (tools/python/)
```
subdomain_enum.py   - Subdomain enumeration
parameter_scanner.py - Parameter discovery
header_analyzer.py - HTTP security headers
csp_bypass.py      - CSP bypass scanner
jwt_analyzer.py    - JWT analyzer/attacker
bruteforce.py      - HTTP brute forcer
bug_hunter.py      - All-in-one scanner
```

## Quick Start

### PowerShell (Windows)

```powershell
# Run main launcher
.\run.ps1

# Recon
.\run.ps1 recon example.com

# Scan for vulnerabilities
.\run.ps1 scan example.com -type xss

# Test specific vuln
.\run.ps1 test xss https://example.com/search?q=test
.\run.ps1 test idor https://api.example.com
.\run.ps1 test ssrf https://example.com/webhook
.\run.ps1 test oauth https://example.com/oauth/authorize
```

### Python (Cross-platform)

```bash
# Install requirements
pip install -r scripts/requirements.txt

# Run tools
python tools/python/bug_hunter.py example.com
python tools/python/subdomain_enum.py example.com  
python tools/python/header_analyzer.py https://example.com
python tools/python/jwt_analyzer.py eyJhbGciOi...
python run.py all example.com
```

## Skills Usage

The toolkit auto-activates skills based on keywords:

```text
# Bug bounty related
漏洞赏金, 安全测试, 渗透测试, 漏洞挖掘, bug bounty, recon, IDOR, SSRF, XSS

# Web audit  
web audit, code review, source audit, API security

# Mobile
mobile security, Android, iOS, APK, Frida

# Cloud
cloud security, AWS, S3, Kubernetes, K8s

# Network
network security, port scanning, SMB, DNS

# API
API security, REST, GraphQL

# Reports
report writing, cvss, severity, triage
```

## Testing Workflow

```
1. RECON
   └─> subdomains, live hosts, URLs, tech stack

2. LEARN
   └─> Read disclosed reports, understand app

3. HUNT
   └─> IDOR, SSRF, XSS, SQLi, SSTI, AI

4. VALIDATE
   └─> 7-Question Gate, impact verification

5. REPORT  
   └─> Professional report with CVSS
```

## Output

Results are saved to `./bug-hunter-output/`:

```
├── subs.txt
├── live.txt  
├── urls.txt
├── nuclei.txt
├── xss-results.txt
├── sqli-results.txt
├── ssrf-results.txt
├── ssti-results.txt
├── api-results.txt
├── mobile-results.txt
├── network-enum.txt
└── report-*.md
```

## Requirements

### PowerShell
- PowerShell 5.0+
- Windows or PowerShell Core

### Python
- Python 3.7+
- requests
- urllib3

### Go (optional)
- subfinder, httpx, nuclei, katana, dalfox, ffuf

## Contributing

Improvements welcome! Create issues or PRs at:
https://github.com/bug-hunter

## License

MIT License - Use at your own risk.

## Disclaimer

This toolkit is for authorized security testing only. Always get proper authorization before testing any system you don't own.