# Bug Hunter Toolkit
## Professional Bug Bounty & Security Testing Framework

**Created by:** [rikixz](https://github.com/blaxkmiradev) | [blaxkmiradev](https://github.com/blaxkmiradev)
**Version:** 2.0.0
**License:** MIT

---

## Table of Contents

1. [Introduction](#introduction)
2. [Setup](#setup)
3. [How to Use](#how-to-use)
4. [Skills](#skills)
5. [Tools](#tools)
6. [Vulnerability Levels](#vulnerability-levels)
7. [CVE Finding & Writing](#cve-finding--writing)
8. [Report Writing](#report-writing)
9. [Adding New Skills](#adding-new-skills)
10. [Commands Reference](#commands-reference)
11. [Credits](#credits)

---

## Introduction

Bug Hunter Toolkit is a comprehensive security testing framework for bug bounty hunters, penetration testers, and security professionals. It includes:

- **9 Specialized Skills** for different security areas
- **40+ Python Tools** for vulnerability scanning
- **15+ PowerShell Tools** for Windows automation
- **Complete Workflow** from recon to report

---

## Setup

### Requirements

#### Python (Required)
```bash
# Install Python dependencies
pip install -r requirements.txt

# Or install individually
pip install requests urllib3 dnspython colorama
```

#### Go (Optional - for advanced tools)
```bash
# Install Go tools
go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install github.com/projectdiscovery/httpx/cmd/httpx@latest
go install github.com/projectdiscovery/nuclei/cmd/nuclei@latest
go install github.com/projectdiscovery/katana/cmd/katana@latest
go install github.com/dw1zard/dalfox/v2/cmd/dalfox@latest
go install github.com/ffuf/ffuf@latest
```

#### PowerShell (Windows)
```powershell
# Run setup
.\tools\bug-hunter\setup.ps1 -All

# Or use individual tools
.\run.ps1 setup
```

### Quick Setup

```bash
# Clone or download the toolkit
git clone https://github.com/blaxkmiradev/bug-hunter.git

# Install dependencies
cd bug-hunter
pip install -r scripts/requirements.txt

# Test installation
python tools/python/fast_scanner.py example.com
```

---

## How to Use

### Master Launcher (PowerShell)

```powershell
# Show help
.\run.ps1

# Recon
.\run.ps1 recon example.com

# Scan for vulnerabilities
.\run.ps1 scan example.com -type xss

# Test specific vulnerability
.\run.ps1 test xss https://example.com/search?q=test
.\run.ps1 test ssrf https://example.com/webhook
.\run.ps1 test idor https://api.example.com
.\run.ps1 test oauth https://example.com/oauth/authorize

# Network enumeration
.\run.ps1 test network 192.168.1.1

# Mobile testing
.\run.ps1 test mobile app.apk

# Generate report
.\run.ps1 report example.com IDOR /api/users "read all user data"
```

### Master Launcher (Python)

```bash
# Show help
python scripts/run.py

# Quick scan
python scripts/run.py fast example.com

# Subdomain enumeration
python scripts/run.py subdomain example.com

# Port scan
python scripts/run.py port target.com

# Directory scan
python scripts/run.py dirs https://example.com

# Vulnerability scan
python scripts/run.py xss https://example.com/search?q=test
python scripts/run.py sqli https://example.com/product?id=1
python scripts/run.py ssrf https://example.com/webhook

# Header analysis
python scripts/run.py header https://example.com

# CORS scanner
python scripts/run.py cors https://api.example.com

# JWT analyzer
python scripts/run.py jwt eyJhbGciOi...

# Run all tools
python tools/python/ALL.py scan example.com
```

### Individual Tools

```bash
# Recon
python tools/python/fast_scanner.py target.com
python tools/python/subdomain_enum.py target.com
python tools/python/parameter_scanner.py https://example.com
python tools/python/fingerprint.py https://example.com
python tools/python/nmap_scan.py target.com

# Vulnerability Scanning
python tools/python/xss_scanner.py "https://example.com/search?q=test"
python tools/python/sqli_scanner.py "https://example.com/product?id=1"
python tools/python/ssrf_scanner.py https://example.com/urlfetch
python tools/python/lfi_scanner.py "https://example.com/view?page="
python tools/python/cmdi_scanner.py "https://example.com/ping?ip="
python tools/python/open_redirect.py "https://example.com/redirect?url="

# Analysis
python tools/python/header_analyzer.py https://example.com
python tools/python/cors_scanner.py https://example.com/api
python tools/python/secret_scanner.py https://example.com
python tools/python/jwt_analyzer.py eyJhbGciOi...
python tools/python/graphql_scanner.py https://example.com/graphql

# Special
python tools/python/race_tester.py https://example.com/redeem -c 20
python tools/python/bruteforce.py https://example.com /login users.txt passwords.txt
python tools/python/generate_csv.py --vuln XSS --target example.com --endpoint /search
python tools/python/cvss.py
```

---

## Skills

### Skill Structure

Each skill is a directory in `skills/` with:
- `SKILL.md` - Main skill content
- `skills.yaml` - Skill metadata

### Available Skills

| Skill | Description | Trigger |
|-------|------------|---------|
| **bug-bounty** | Main bug bounty workflow | bug bounty, recon, 漏洞赏金 |
| **web-audit** | Web app security audit | web audit, code review, API |
| **mobile-security** | Android/iOS security | mobile security, Android, Frida |
| **cloud-security** | AWS/GCP/Azure/K8s | cloud security, S3, K8s |
| **network-security** | Network pentesting | network, port scan, SMB |
| **api-security** | REST/GraphQL testing | API, REST, GraphQL |
| **red-team** | Red team operations | red team, C2, AD |
| **report-writing** | Report templates, CVSS | report, cvss, 漏洞报告 |
| **osint** | OSINT reconnaissance | OSINT, Google hacking |

### Activating Skills

Skills auto-activate based on keywords in your prompt:

```text
# Bug bounty related
漏洞赏金, 安全测试, 渗透测试, bug bounty, recon, pentest
IDOR, SSRF, XSS, SQLi, vulnerability hunting

# Web audit
web audit, code review, source audit, API security

# Mobile  
mobile security, Android, iOS, APK analysis, Frida

# Cloud
cloud security, AWS, S3 bucket, Kubernetes, K8s

# Reports
report writing, cvss, severity, triage response
```

---

## Tools

### Python Tools (40+)

#### Recon Tools
| Tool | Description | Usage |
|------|------------|--------|
| `fast_scanner.py` | Quick all-in-one scan | `python fast_scanner.py target.com` |
| `subdomain_enum.py` | Subdomain enumeration | `python subdomain_enum.py target.com` |
| `nmap_scan.py` | Port scanner | `python nmap_scan.py target.com` |
| `fingerprint.py` | Tech detection | `python fingerprint.py https://target.com` |
| `parameter_scanner.py` | Parameter discovery | `python parameter_scanner.py https://target.com` |
| `dir_scanner.py` | Directory scanner | `python dir_scanner.py https://target.com` |

#### Vulnerability Scanners
| Tool | Description | Usage |
|------|------------|--------|
| `xss_scanner.py` | XSS detection | `python xss_scanner.py https://target.com/search?q=test` |
| `sqli_scanner.py` | SQL injection | `python sqli_scanner.py https://target.com/product?id=1` |
| `ssrf_scanner.py` | SSRF detection | `python ssrf_scanner.py https://target.com/urlfetch` |
| `lfi_scanner.py` | LFI/RFI detection | `python lfi_scanner.py https://target.com/view?page=` |
| `cmdi_scanner.py` | Command injection | `python cmdi_scanner.py https://target.com/ping?ip=` |
| `ssti_scanner.py` | SSTI detection | `python ssti_scanner.py https://target.com/template` |
| `xml_injection.py` | XXE detection | `python xml_injection.py https://target.com/upload` |
| `open_redirect.py` | Open redirect | `python open_redirect.py https://target.com/redirect?url=` |
| `proto_pollution.py` | Proto pollution | `python proto_pollution.py https://target.com/api` |
| `race_tester.py` | Race conditions | `python race_tester.py https://target.com/redeem -c 20` |
| `upload_tester.py` | File upload | `python upload_tester.py https://target.com/upload` |

#### Analysis Tools
| Tool | Description | Usage |
|------|------------|--------|
| `header_analyzer.py` | Security headers | `python header_analyzer.py https://target.com` |
| `cors_scanner.py` | CORS misconfig | `python cors_scanner.py https://target.com/api` |
| `csp_bypass.py` | CSP bypass | `python csp_bypass.py https://target.com` |
| `jwt_analyzer.py` | JWT attacks | `python jwt_analyzer.py eyJ...` |
| `secret_scanner.py` | Find secrets | `python secret_scanner.py https://target.com` |
| `graphql_scanner.py` | GraphQL testing | `python graphql_scanner.py https://target.com/graphql` |
| `oauth_scanner.py` | OAuth testing | `python oauth_scanner.py https://target.com/oauth` |
| `web_scanner.py` | Web vulns | `python web_scanner.py https://target.com` |

#### Special Tools
| Tool | Description | Usage |
|------|------------|--------|
| `s3_scanner.py` | S3 buckets | `python s3_scanner.py bucket-name` |
| `bruteforce.py` | HTTP brute | `python bruteforce.py target /login users.txt passwords.txt` |
| `heartbleed.py` | Heartbleed | `python heartbleed.py target.com 443` |
| `shellshock.py` | Shellshock | `python shellshock.py https://target.com/cgi-bin/test` |
| `subdomain_takeover.py` | Takeover | `python subdomain_takeover.py subs.txt` |
| `enum_users.py` | User enum | `python enum_users.py target.com` |
| `fuzz.py` | Fuzzer | `python fuzz.py https://target.com/api?param=FUZZ` |
| `cvss_calculator.py` | CVSS calc | `python cvss_calculator.py` |

#### Report Tools
| Tool | Description | Usage |
|------|------------|--------|
| `generate_csv.py` | Gen report | `python generate_csv.py --vuln XSS --target example.com` |
| `cvss_calculator.py` | CVSS score | `python cvss_calculator.py` |

#### CVE Tools
| Tool | Description | Usage |
|------|------------|--------|
| `cve_finder.py` | Search CVEs | `python cve_finder.py nginx` |
| `cve_writer.py` | Gen CVE report | `python cve_writer.py --product nginx --impact "RCE"` |
| `vuln_level.py` | Vuln severity scan | `python vuln_level.py target.com` |

#### Vuln Level Scanner
| Tool | Description | Usage |
|------|------------|--------|
| `vuln_level.py` | Level-based vuln scan | `python vuln_level.py target.com` |

### PowerShell Tools

```powershell
# Recon
.\tools\bug-hunter\recon.ps1 -Target example.com

# Scan
.\tools\bug-hunter\scan.ps1 -Target example.com -Type all
.\tools\bug-hunter\scan.ps1 -Target example.com -Type xss

# Test vulnerabilities
.\tools\bug-hunter\test-idor.ps1 -Target https://api.example.com
.\tools\bug-hunter\test-ssrf.ps1 -Target https://example.com/webhook
.\tools\bug-hunter\test-xss.ps1 -Target https://example.com -Param q

# Special
.\tools\bug-hunter\test-api.ps1 -Target https://api.example.com -All
.\tools\bug-hunter\test-oauth.ps1 -Target https://example.com/oauth/authorize
.\tools\bug-hunter\test-mobile.ps1 -Target app.apk

# Report
.\tools\bug-hunter\report.ps1 -Target example.com -VulnClass IDOR -Impact "data breach"
```

---

## Vulnerability Levels

### Severity Classification

| Level | Score | Description | Example |
|-------|-------|------------|---------|
| **CRITICAL** | 9.0-10.0 | Complete system compromise | Auth bypass → admin, RCE |
| **HIGH** | 7.0-8.9 | Significant impact | IDOR write, SQLi data theft |
| **MEDIUM** | 4.0-6.9 | Limited impact | IDOR read PII, Stored XSS |
| **LOW** | 0.1-3.9 | Minimal impact | Self-XSS, Info disclosure |
| **INFO** | 0.0 | No vulnerability | Banner disclosure |

### Quick CVSS Reference

| Vulnerability | Typical CVSS | Severity |
|-------------|-------------|----------|
| IDOR (read PII) | 6.5 | Medium |
| IDOR (write/delete) | 7.5 | High |
| Auth bypass → admin | 9.8 | Critical |
| Stored XSS | 5.4-8.8 | Medium-High |
| SQLi (data exfil) | 8.6 | High |
| SSRF (cloud metadata) | 9.1 | Critical |
| Race condition | 7.5 | High |
| GraphQL auth bypass | 8.7 | High |
| JWT none algorithm | 9.1 | Critical |
| Open redirect alone | 3.5 | Low |
| Self-XSS | 3.5 | Low |

### Severity Escalation

Same bug can become higher when chained:

```
Open redirect + OAuth = Account Takeover (High)
Self-XSS + Login CSRF = Stored XSS (Medium)  
SSRF (DNS only) + Internal proof = Internal access (Medium)
CORS wildcard + Credentials = Data theft (Medium)
Clickjacking + Sensitive action = Account action (Medium)
```

---

## CVE Finding & Writing

### Finding CVEs

1. **Version Detection**
   ```bash
   # Find version
   python tools/python/fingerprint.py target.com
   
   # Check for known CVEs
   curl -s "https://services.nvd.nist.gov/rest/json/cves/2.0?keywordSearch=TARGET_SOFTWARE"
   ```

2. **Common CVE Vectors**
   - Outdated software versions
   - Known vulnerable parameters
   - Public exploit databases
   - Change logs and security advisories

3. **Finding New CVEs**
   - Zero-day research
   - Novel attack vectors
   - Business logic flaws
   - Configuration issues

### CVE Writing Format

```markdown
# CVE Submission Format

CVE ID: CVE-YYYY-XXXXX

## Description
[Software name] [version] and earlier contains a [vulnerability type] 
in [component] that allows [attacker] to [impact].

## Affected Versions
[Software name] [start version] through [end version]

## References
https://example.com/advisory
https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-YYYY-XXXXX

## Credits
Discovered by: [Your Name]
Date: [Discovery Date]

## Proof of Concept
[HTTP Request]
GET /vulnerable?param=PAYLOAD HTTP/1.1
Host: target.com

[Response]
HTTP/1.1 200 OK
[Payload executed]

## Timeline
Discovery Date: YYYY-MM-DD
Vendor Notified: YYYY-MM-DD
Patch Released: YYYY-MM-DD
CVE Assigned: YYYY-MM-DD
```

### CVE Resources

- [MITRE CVE](https://cve.mitre.org)
- [NVD](https://nvd.nist.gov)
- [Exploit-DB](https://exploit-db.com)
- [PacketStorm](https://packetstormsecurity.com)
- [Google Project Zero](https://bugs.chromium.org)

---

## Report Writing

### Report Templates

#### HackerOne Format
```markdown
# Title
[ vuln class ] in [ endpoint/feature ] allows [ attacker ] to [ impact ]

## Summary
[ 2-3 sentences: what it is, where it is, what attacker can do ]

## Steps To Reproduce
1. [Step with exact HTTP request]
2. [Step]
3. [Step]

## Supporting Material
[ Screenshot / video / PoC request ]

## Impact
An attacker can [ specific action ] resulting in [ specific harm ].

## Severity Assessment
CVSS 3.1 Score: X.X ( severity )
Attack Vector: Network | Complexity: Low | Privileges: None | User Interaction: None
```

#### Quick Report Generator
```bash
python tools/python/generate_csv.py \
  --vuln XSS \
  --target example.com \
  --endpoint /search?q= \
  --poc "GET /search?q=<script>alert(1)</script>" \
  --severity Medium \
  --impact "Execute JavaScript in user context"
```

### Impact Statement Formula

> An [attacker with X access level] can [exact action] by [method], 
> resulting in [business harm]. This requires [prerequisites] and 
> leaves [detection difficulty].

### Human Tone Rules

✓ Start with impact, not vulnerability name  
✓ Write like explaining to a developer  
✓ Use "I found..." not "A vulnerability was discovered..."  
✓ One concrete example beats three abstract sentences  
✓ No: "comprehensive/leverage/seamless/ensure"  
✓ No em dashes in the middle of sentences

### 60-Second Pre-Submit Checklist

- [ ] Title follows formula: [Class] in [endpoint] allows [actor] to [impact]
- [ ] First sentence states exact impact in plain English
- [ ] Steps to Reproduce has exact HTTP request
- [ ] Response showing the bug is included
- [ ] Two test accounts used
- [ ] CVSS score calculated and included
- [ ] Recommended fix is one sentence
- [ ] No typos in endpoint path
- [ ] Report is < 600 words
- [ ] Severity matches impact described

---

## Adding New Skills

### Skill Structure

```
skills/
├── skill-name/
│   ├── SKILL.md        # Main content
│   ├── skills.yaml     # Metadata
│   └── agent.yaml    # (optional) Agent config
```

### SKILL.md Format

```markdown
name: skill-name
description: Skill description
trigger:
  - trigger_word1
  - trigger_word2
  - trigger_word3

---

# Skill Content

## Section 1
Content here...

## Section 2
More content...
```

### skills.yaml Format

```yaml
name: skill-name
description: Skill description
trigger:
  - trigger_word
  - another_trigger
author: rikixz
version: 1.0.0
```

### Adding New Tools

1. Create Python tool in `tools/python/`:
   ```python
   #!/usr/bin/env python3
   """
   Tool Name
   Usage: python tool.py <target>
   """
   
   import sys
   import requests
   
   def main():
       if len(sys.argv) < 2:
           print("Usage: python tool.py <target>")
           sys.exit(1)
       
       target = sys.argv[1]
       # Tool logic here
       print(f"[*] Testing {target}...")
   
   if __name__ == "__main__":
       main()
   ```

2. Add to `scripts/run.py` for master launcher

---

## Commands Reference

### Quick Reference

```bash
# Quick scan
python tools/python/fast_scanner.py target.com

# Full recon
python scripts/run.py recon target.com

# Scan vulnerabilities
python scripts/run.py xss "https://target.com/search?q=test"
python scripts/run.py sqli "https://target.com/product?id=1"
python scripts/run.py ssrf "https://target.com/urlfetch"

# Analysis
python scripts/run.py header https://target.com
python scripts/run.py cors https://api.target.com
python scripts/run.py jwt eyJhbGciOi...

# Report
python scripts/run.py report target.com IDOR /api/users "read data"
python tools/python/generate_csv.py --vuln XSS --target target.com
python tools/python/cvss_calculator.py
```

---

## 🚀 OpenCode Setup & Usage

### How to Add Skills to OpenCode

OpenCode automatically loads skills from the `skills/` directory. Here's how to use:

#### 1. Skill Directory Structure
```
skills/
├── skill-name/
│   ├── SKILL.md        # Required - Main skill content
│   ├── skills.yaml     # Required - Skill metadata
│   └── agent.yaml     # Optional - Agent configuration
```

#### 2. SKILL.md Format (Required)
```markdown
name: skill-name
description: Your skill description
trigger:
  - trigger_word1
  - trigger_word2
  - 中文触发词

---

# Skill Content

## Section 1
Content here...
```

#### 3. skills.yaml Format (Required)
```yaml
name: skill-name
description: Skill description
trigger:
  - trigger_word
  - another_trigger
author: rikixz
version: 1.0.0
```

### How to Ask OpenCode to Use Tools

#### 🐛 Basic Bug Bounty Questions
```text
"do recon on example.com"
"scan for XSS vulnerabilities"
"test for SQL injection in https://example.com/product?id=1"
"find subdomains"
"check security headers"
```

#### 🎯 Specific Vulnerability Testing
```text
"test for IDOR in https://api.example.com/users"
"test for SSRF in https://example.com/webhook"  
"test for XSS in https://example.com/search?q="
"check for open redirect in https://example.com/redirect"
"analyze JWT tokens"
```

#### 🔍 Recon Questions
```text
"what technologies does example.com use?"
"find all endpoints in https://api.example.com"
"enumerate subdomains"
"scan ports on target.com"
"directory scan"
```

#### 📊 Analysis Questions
```text
"analyze HTTP security headers"
"check CORS configuration"
"find secrets in JavaScript files"
"test GraphQL for vulnerabilities"
```

#### 💻 Commands to Run Tools
```text
"run fast_scanner on example.com"
"run xss_scanner on https://example.com/search?q=test"
"run subdomain enumeration on target.com"
"run port scan on target.com"
```

### Using Skills Automatically

Skills auto-activate based on keywords - just ask naturally:

```text
# Bug bounty related
"我需要做漏洞赏金测试" → Activates bug-bounty skill
"do a security audit" → Activates web-audit skill
"test mobile app security" → Activates mobile-security skill  
"check cloud security" → Activates cloud-security skill

# Specific vulnerabilities
"test for IDOR" → IDOR testing tools
"find XSS" → XSS scanner  
"check for SQLi" → SQLi scanner
```

### OpenCode AI Commands

#### Quick Actions
```text
"run recon on [target]"           → Full recon
"quick scan [target]"           → Fast scanner
"vuln scan [target]"            → All vulns
"subdomain enum [target]"       → Find subdomains

# Specific tests
"test XSS [url]"
"test SQLi [url]"
"test SSRF [url]"
"test IDOR [url]"
"test auth [url]"

# Analysis
"scan headers [target]"
"check CORS [target]"
"analyze JWT [token]"
"fingerprint [target]"
```

### Tool Categories by User Type

#### 👀 Beginner Users
```bash
# Just ask!
"scan example.com"
"find vulnerabilities"
"check security"

# Or use fast scanner
python tools/python/fast_scanner.py target.com
```

#### 🔧 Intermediate Users
```bash
# Specific vulnerability tests
python tools/python/xss_scanner.py "https://target.com/search?q=test"
python tools/python/sqli_scanner.py "https://target.com/product?id=1"
python tools/python/header_analyzer.py https://target.com

# Use master launcher
python scripts/run.py fast example.com
python scripts/run.py xss "https://target.com/search"
```

#### 🚀 Advanced Users
```bash
# Full scanning suite
python tools/python/ALL.py scan target.com
python tools/python/ALL.py vuln target.com

# Run all tools with specific focus
python tools/python/ALL.py xss target.com
python tools/python/ALL.py sqli target.com

# Custom tool combinations
python tools/python/fast_scanner.py target.com && \
python tools/python/xss_scanner.py target.com && \
python tools/python/sqli_scanner.py target.com
```

### CLI Reference for OpenCode

```bash
# PowerShell (Windows)
.\run.ps1 recon example.com
.\run.ps1 scan example.com -type xss
.\run.ps1 test xss https://example.com/search?q=test

# Python
python scripts/run.py fast example.com
python scripts/run.py xss "https://example.com/search?q=test"

# Direct tool
python tools/python/fast_scanner.py example.com
```

### How to Get Help

```text
# Show available commands
python scripts/run.py

# Show tool help
python tools/python/fast_scanner.py

# Show CVSS reference
python tools/python/cvss_calculator.py

# Find CVEs
python tools/python/cve_finder.py --help
```

### Quick Command Cheat Sheet

| Action | Command |
|--------|---------|
| Quick Scan | `python ALL.py quick target.com` |
| Full Scan | `python ALL.py scan target.com` |
| Recon | `python fast_scanner.py target.com` |
| XSS Test | `python xss_scanner.py URL` |
| SQLi Test | `python sqli_scanner.py URL` |
| Headers | `python header_analyzer.py URL` |
| CORS | `python cors_scanner.py URL` |
| JWT | `python jwt_analyzer.py TOKEN` |
| CVE Search | `python cve_finder.py PRODUCT` |
| CVSS | `python cvss_calculator.py` |
| Report | `python generate_csv.py --vuln XSS --target domain` |

### User Scenarios & How to Ask

#### 📌 "I want to scan a target"
```text
Just say: "scan example.com"
→ Runs fast_scanner.py
```

#### 📌 "I found a vulnerability and need to write a report"  
```text
Say: "generate report for XSS in /search on example.com"
→ Uses generate_csv.py
```

#### 📌 "What's the severity of this bug?"
```text
Ask: "what CVSS score for IDOR?"
→ Shows cvss_calculator.py with typical scores
```

#### 📌 "Check if target is vulnerable to [vulnerability]"
```text
Say: "check example.com for XSS"
→ Runs xss_scanner.py
```

#### 📌 "Find information about this software"
```text
Ask: "search CVE for nginx"
→ Uses cve_finder.py
```

#### 📌 "Audit this web application"
```text
Say: "audit web application security"
→ Uses web_scanner.py + header_analyzer.py
```

### Skill Trigger Keywords

| Trigger | Skills Activated |
|---------|----------------|
| 漏洞赏金 / bug bounty / recon | bug-bounty |
| web audit / code review / API | web-audit |
| mobile / Android / iOS | mobile-security |
| cloud / AWS / S3 / K8s | cloud-security |
| network / port / SMB | network-security |
| API / REST / GraphQL | api-security |
| red team / C2 / AD | red-team |
| report / CVSS / severity | report-writing |
| OSINT / Google hacking / email | osint |

### Example Conversations with AI

```
User: "I want to test this URL for SQL injection"
AI: "I'll run sql_injection scanner on that URL. Found 3 potential issues..."

User: "What's the severity of stored XSS in admin panel?"  
AI: "Stored XSS with admin access typically scores 7.5-8.8 (High). CVSS..."

User: "Generate a bug bounty report for this IDOR"
AI: "I'll create a report with CVSS score 6.5 (Medium) using the template..."

User: "Search for known CVEs in WordPress"
AI: "Searching NVD database... Found CVE-2024-XXXX for WordPress..."
```

### Setting Up for OpenCode Integration

1. Clone or copy the bug-hunter directory:
```bash
git clone https://github.com/blaxkmiradev/bug-hunter.git
cd bug-hunter
```

2. Ensure Python dependencies are installed:
```bash
pip install -r scripts/requirements.txt
```

3. Add to your PATH or use absolute paths:
```bash
# Option 1: Add to PATH
export PATH="$PATH:/path/to/bug-hunter/tools/python"

# Option 2: Always use full path
python /path/to/bug-hunter/tools/python/fast_scanner.py target.com
```

4. For Windows PowerShell, use:
```powershell
# Add to PATH
$env:PATH += ";C:\path\to\bug-hunter\tools\python"

# Or run directly
& "C:\path\to\bug-hunter\run.ps1" recon target.com
```

---

## Credits

### Created By

**[rikixz](https://github.com/blaxkmiradev)** - [blaxkmiradev](https://github.com/blaxkmiradev)

GitHub: [github.com/blaxkmiradev](https://github.com/blaxkmiradev)

### Inspired By

- Bug Bounty methodology from top hunters
- OWASP testing guide
- PortSwigger Web Security Academy
- Security community tools

### Tools & Resources Used

- ProjectDiscovery tools (nuclei, httpx, subfinder, katana)
- OWASP
- PortSwigger labs
- HackerOne disclosed reports

---

## Disclaimer

This toolkit is for **authorized security testing only**. Always get proper 
authorization before testing any system you don't own.

Using this toolkit against systems without authorization is illegal and 
may result in legal action.

---

## License

MIT License - Use at your own risk.

---

## Support

- Issues: https://github.com/blaxkmiradev/opencode-bug-bounty/issues
- Stars: ⭐⭐⭐⭐⭐ (If you find it useful!)

---

**Made with 🔥 by [rikixz](https://github.com/blaxkmiradev)** | [blaxkmiradev](https://github.com/blaxkmiradev)

Happy Hunting! 🐛🔍
