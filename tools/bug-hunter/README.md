# Bug Hunter - Professional Bug Bounty Toolkit
# Usage Guide

## Quick Start

```powershell
# 1. Setup (install tools)
.\setup.ps1 -All

# 2. Recon
.\recon.ps1 -Target example.com

# 3. Scan
.\scan.ps1 -Target https://example.com -Type all

# 4. Test specific vulnerabilities
.\test-idor.ps1 -Target https://api.example.com
.\test-ssrf.ps1 -Target https://example.com/webhook
.\test-xss.ps1 -Target https://example.com/search -Param q
.\test-sqli.ps1 -Target https://example.com/item -Param id
.\test-ssti.ps1 -Target https://example.com/template -Param input

# 5. AI Security Testing
.\test-ai.ps1 -Target https://example.com/chat -All

# 6. Bug Chaining
.\chain.ps1

# 7. Generate Report
.\report.ps1 -Target example.com -VulnClass IDOR -Endpoint /api/users -Impact "read other users data"
```

## Tool Overview

### recon.ps1
Subdomain enumeration and live host detection.

### scan.ps1
General vulnerability scanning (Nuclei, Dalfox, SQLMap).

### test-idor.ps1
Tests for Insecure Direct Object Reference:
- Direct ID manipulation
- Body parameter manipulation
- Header injection
- Method swap
- Version rollback
- GraphQL node bypass

### test-ssrf.ps1
Tests for Server-Side Request Forgery:
- Cloud metadata (AWS, GCP, Azure)
- Internal services
- IP bypass (decimal, hex, octal)
- Protocol bypass (file://, gopher://)

### test-xss.ps1
Tests for Cross-Site Scripting:
- Reflected XSS
- Stored XSS
- DOM XSS
- Filter bypasses

### test-sqli.ps1
Tests for SQL Injection:
- Error-based
- Union-based
- Blind/Time-based
- WAF bypass

### test-ssti.ps1
Tests for Server-Side Template Injection:
- Jinja2, Twig, ERB, Freemarker
- RCE payloads

### test-ai.ps1
Tests for AI/LLM Security (OWASP ASI01-ASI10):
- Prompt injection
- Tool misuse
- Data exfiltration
- Indirect injection

### chain.ps1
Bug chaining to escalate impact.

### report.ps1
Generate structured bug bounty reports.

## Workflow

```
1. RECON
   └─> subfinder, httpx, katana, nuclei

2. LEARN  
   └─> Read disclosed reports, analyze changelog

3. HUNT
   └─> IDOR, SSRF, XSS, SQLi, SSTI, AI

4. VALIDATE
   └─> 7-Question Gate

5. REPORT
   └─> Generate structured report
```

## Output

Results saved to `./bug-hunter-output/`:
- subs.txt
- live.txt
- urls.txt
- nuclei.txt
- xss-results.txt
- sqli-results.txt
- ssrf-results.txt
- ssti-results.txt
- ai-security-results.txt
- chains.txt
- report-*.md

## Required Tools

Go:
- subfinder, httpx, dnsx, nuclei, katana, dalfox, ffuf, gf, assetfinder

Python:
- semgrep, arjun, sqlmap

## License

MIT License - Use at your own risk.