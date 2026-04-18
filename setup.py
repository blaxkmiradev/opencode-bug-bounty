#!/usr/bin/env python3
"""
Bug Hunter Toolkit - Complete Setup for OpenCode
One file to install all tools + skills
"""

import sys
import os
import shutil
import platform
import json
from pathlib import Path

TOOL_NAME = "bug-hunter"
VERSION = "1.0.0"

OPENCODE_SKILLS = {
    "bug-bounty": {
        "description": "Comprehensive bug bounty hunting and vulnerability assessment",
        "triggers": ["bug bounty", "vulnerability", "pentest", "security scan", "hack"],
        "commands": ["/scan", "/recon", "/enum", "/vuln"],
        "tools": ["full_scan.py", "pro_scanner.py", "subdomain_enum.py", "web_scanner.py"]
    },
    "web-audit": {
        "description": "Web application security audit and testing",
        "triggers": ["web audit", "web security", "website scan", "http"],
        "commands": ["/web-scan", "/headers", "/xss", "/sqli"],
        "tools": ["xss_scanner.py", "sqli_scanner.py", "header_analyzer.py", "web_scanner.py"]
    },
    "api-security": {
        "description": "REST API and GraphQL security testing",
        "triggers": ["api", "rest", "graphql", "endpoint", "json"],
        "commands": ["/api-scan", "/graphql", "/rest-test"],
        "tools": ["graphql_scanner.py", "api_scanner.py", "json_injection.py"]
    },
    "cloud-security": {
        "description": "Cloud security assessment (AWS/GCP/Azure)",
        "triggers": ["cloud", "aws", "gcp", "azure", "s3", "cloudformation"],
        "commands": ["/cloud-scan", "/aws-scan", "/s3"],
        "tools": ["s3_scanner.py", "aws_enum.py", "cloud_scanner.py"]
    },
    "network-security": {
        "description": "Network penetration testing",
        "triggers": ["network", "port", "nmap", "scan"],
        "commands": ["/port-scan", "/network-scan"],
        "tools": ["nmap_scan.py", "port_scanner.py"]
    },
    "mobile-security": {
        "description": "Mobile application security (Android/iOS)",
        "triggers": ["mobile", "android", "apk", "ios"],
        "commands": ["/mobile-scan", "/apk-analyze"],
        "tools": ["android_apk.py", "mobile_scanner.py"]
    },
    "red-team": {
        "description": "Red team operations and advanced pentesting",
        "triggers": ["red team", "advanced", "exploit"],
        "commands": ["/red-team", "/exploit"],
        "tools": ["rce_scanner.py", "exploit_scanner.py"]
    },
    "osint": {
        "description": "OSINT and reconnaissance",
        "triggers": ["osint", "recon", "information", "gather"],
        "commands": ["/osint", "/recon", "/whois"],
        "tools": ["subdomain_enum.py", "dns_enumeration.py", "enum_users.py"]
    },
    "report-writing": {
        "description": "Security assessment report generation",
        "triggers": ["report", "findings", "documentation"],
        "commands": ["/report", "/generate"],
        "tools": ["cve_writer.py", "report_generator.py"]
    },
    "exploit-dev": {
        "description": "Exploit development and fuzzing",
        "triggers": ["exploit", "fuzz", "shellcode"],
        "commands": ["/exploit", "/fuzz"],
        "tools": ["fuzz.py", "rce_scanner.py"]
    },
    "malware-analysis": {
        "description": "Malware and APK analysis",
        "triggers": ["malware", "apk", "analyze"],
        "commands": ["/analyze", "/apk"],
        "tools": ["android_apk.py", "sensitive_finder.py"]
    },
    "social-eng": {
        "description": "Social engineering and phishing reconnaissance",
        "triggers": ["phishing", "social", "email harvest"],
        "commands": ["/phish", "/email-harvest"],
        "tools": ["subdomain_enum.py", "email_finder.py"]
    },
    "devops-sec": {
        "description": "DevOps and CI/CD security",
        "triggers": ["devops", "ci/cd", "k8s", "docker"],
        "commands": ["/k8s-scan", "/docker-scan"],
        "tools": ["docker_scanner.py"]
    },
    "iot-sec": {
        "description": "IoT device security",
        "triggers": ["iot", "firmware", "embedded"],
        "commands": ["/firmware", "/device-scan"],
        "tools": ["nmap_scan.py", "firmware_scanner.py"]
    }
}

def get_opencode_dir():
    """Get OpenCode config directory"""
    home = Path.home()
    if platform.system() == "Windows":
        return home / ".opencode"
    return home / ".opencode"

def get_tools_dir():
    """Get tools directory"""
    return Path(__file__).parent / "tools" / "python"

def get_skills_source_dir():
    """Get skills source directory"""
    return Path(__file__).parent / "skills"

def create_skill_file(skill_name, skill_data, target_dir):
    """Create a skill file for OpenCode"""
    skill_dir = target_dir / skill_name
    skill_dir.mkdir(parents=True, exist_ok=True)
    
    yaml_file = skill_dir / "skills.yaml"
    md_file = skill_dir / "SKILL.md"
    
    yaml_content = f'''name: {skill_name}
description: {skill_data["description"]}
triggers:
'''
    for trigger in skill_data.get("triggers", []):
        yaml_content += f'  - {trigger}\n'
    
    yaml_content += '''commands:
'''
    for cmd in skill_data.get("commands", []):
        yaml_content += f'  - {cmd}\n'
    
    yaml_content += "tools:\n"
    for tool in skill_data.get("tools", []):
        yaml_content += f'  - {tool}\n'
    
    md_content = f'''# {skill_name.title()} Skill

## Description
{skill_data["description"]}

## Triggers
'''
    for trigger in skill_data.get("triggers", []):
        md_content += f"- {trigger}\n"
    
    md_content += "\n## Commands\n"
    for cmd in skill_data.get("commands", []):
        md_content += f"- {cmd}\n"
    
    md_content += "\n## Tools\n"
    for tool in skill_data.get("tools", []):
        md_content += f"- {tool}\n"
    
    md_content += "\n## Usage\n```\n"
    md_content += f"{skill_data['commands'][0]} target.com\n"
    md_content += "```\n"
    
    with open(yaml_file, "w") as f:
        f.write(yaml_content)
    
    with open(md_file, "w") as f:
        f.write(md_content)
    
    return skill_dir

def create_unified_skill(target_dir):
    """Create unified bug-hunter skill"""
    skill_dir = target_dir / TOOL_NAME
    skill_dir.mkdir(parents=True, exist_ok=True)
    
    tools_list = list(get_tools_dir().glob("*.py"))
    tool_names = [f.name for f in tools_list[:50]]
    
    yaml_content = f'''name: {TOOL_NAME}
description: Complete Security Testing Toolkit - {len(tool_names)}+ vulnerability scanners and security tools
version: {VERSION}

triggers:
  - security
  - vulnerability
  - pentest
  - bug bounty
  - scan
  - hack
  - exploit
  - audit
  - penetration
  - vuln
  - xss
  - sqli
  - rce
  - ssrf

commands:
  - /scan
  - /full-scan
  - /quick-scan
  - /recon
  - /enum
  - /vuln
  - /xss
  - /sqli
  - /rce
  - /ssrf
  - /headers
  - /waf
  - /subdomain
  - /web
  - /api
  - /cloud
  - /network
  - /mobile
  - /report

tools:
'''
    for tool in tool_names:
        yaml_content += f'  - {tool}\n'
    
    md_content = f'''# Bug Hunter Toolkit - Complete Security Suite

## Overview
Comprehensive security testing toolkit with {len(tool_names)}+ specialized tools for:
- Web vulnerability scanning
- API security testing
- Cloud infrastructure assessment
- Network penetration testing
- Mobile security analysis
- OSINT reconnaissance

## Version
{VERSION}

## Quick Commands

### Scanning
```
/scan <target>          - Full security scan
/quick-scan <target>  - Quick scan
/recon <target>       - Reconnaissance
/enum <target>        - Enumeration
```

### Vulnerability Testing
```
/xss <target>         - XSS scanner
/sqli <target>       - SQL injection
/rce <target>        - RCE scanner
/ssrf <target>       - SSRF scanner
/headers <target>    - Security headers
```

### Special Scans
```
/waf <target>         - WAF detector
/subdomain <target>   - Subdomain enum
/web <target>         - Web scanner
/api <target>        - API scanner
/cloud <target>      - Cloud scanner
/network <target>    - Network scanner
```

### Reporting
```
/report               - Generate report
/vuln <target>       - Vulnerability assessment
```

## Available Tools ({len(tool_names)}+)

### Web Vulnerabilities
- XSS Scanner
- SQLi Scanner  
- RCE Scanner
- SSRF Scanner
- LFI Scanner
- XXE Scanner
- IDOR Scanner
- SSTI Scanner
- Open Redirect Scanner
- CSRF Scanner
- CORS Scanner

### API Testing
- REST API Scanner
- GraphQL Scanner
- JWT Analyzer
- OAuth Scanner

###Recon/Enum
- Subdomain Enumeration
- Directory Scanner
- Parameter Scanner
- User Enumeration
- DNS Enumeration

### Infrastructure
- Port Scanner
- Nmap Integration
- WAF Detector
- SSL Analyzer

### Cloud
- AWS Scanner
- S3 Bucket Scanner
- Cloud Metadata Scanner

### Specialized
- WordPress Scanner
- Git/Backup Finder
- Sensitive Data Finder
- DoS Tester

## Usage Examples

```bash
# Full scan
python tools/python/full_scan.py target.com

# Quick scan
python tools/python/fast_scanner.py target.com

# Specific vulnerability
python tools/python/xss_scanner.py https://target.com
python tools/python/ssrf_scanner.py https://target.com
python tools/python/rce_scanner.py https://target.com

# Security headers
python tools/python/header_analyzer.py target.com

# Reconnaissance
python tools/python/subdomain_enum.py target.com

# WAF detection
python tools/python/waf_detector.py target.com
```

## Installation

### Python
```bash
pip install -r requirements.txt
python install.py
```

### Windows
```cmd
setup-windows.bat
```

### Linux
```bash
chmod +x setup-linux.sh
./setup-linux.sh
```

## Reports
Generated reports are saved in `output/` directory.
'''
    
    with open(skill_dir / "skills.yaml", "w") as f:
        f.write(yaml_content)
    
    with open(skill_dir / "SKILL.md", "w") as f:
        f.write(md_content)
    
    return skill_dir

def install():
    """Main installation function"""
    print("="*60)
    print(f"  Bug Hunter Toolkit - OpenCode Setup v{VERSION}")
    print("="*60)
    
    opencode_dir = get_opencode_dir()
    tools_dir = get_tools_dir()
    skills_src = get_skills_source_dir()
    
    print(f"\n[*] Platform: {platform.system()}")
    print(f"[*] OpenCode dir: {opencode_dir}")
    print(f"[*] Tools dir: {tools_dir}")
    
    opencode_dir.mkdir(parents=True, exist_ok=True)
    
    tools_target = opencode_dir / "tools"
    tools_target.mkdir(parents=True, exist_ok=True)
    
    print("\n[*] Installing Python tools...")
    py_target = tools_target / "python"
    py_target.mkdir(parents=True, exist_ok=True)
    
    count = 0
    for py_file in tools_dir.glob("*.py"):
        shutil.copy2(py_file, py_target / py_file.name)
        count += 1
    
    print(f"    [+] {count} Python tools installed")
    
    print("\n[*] Installing PowerShell tools...")
    ps_src = Path(__file__).parent / "tools" / "bug-hunter"
    ps_target = tools_target / "bug-hunter"
    ps_target.mkdir(parents=True, exist_ok=True)
    
    count = 0
    if ps_src.exists():
        for ps_file in ps_src.glob("*.ps1"):
            shutil.copy2(ps_file, ps_target / ps_file.name)
            count += 1
    
    print(f"    [+] {count} PowerShell tools installed")
    
    print("\n[*] Installing Skills for OpenCode...")
    skills_target = opencode_dir / "skills"
    skills_target.mkdir(parents=True, exist_ok=True)
    
    for skill_name, skill_data in OPENCODE_SKILLS.items():
        create_skill_file(skill_name, skill_data, skills_target)
    
    print(f"    [+] {len(OPENCODE_SKILLS)} individual skills")
    
    print("\n[*] Creating unified skill...")
    create_unified_skill(skills_target)
    print("    [+] bug-hunter skill created")
    
    print("\n" + "="*60)
    print(f"[+] Setup complete!")
    print("="*60)
    
    print("\n[+] Tool location:")
    print(f"    {py_target}")
    
    print("\n[+] Available commands in OpenCode:")
    print("    /scan <target>     - Full security scan")
    print("    /quick-scan <target> - Quick scan")
    print("    /recon <target>  - Reconnaissance")
    print("    /xss <target>    - XSS scanner")
    print("    /sqli <target>   - SQLi scanner")
    print("    /rce <target>    - RCE scanner")
    print("    /ssrf <target>   - SSRF scanner")
    print("    /waf <target>    - WAF detector")
    
    print("\n[+] Python usage:")
    print(f"    python {py_target}/full_scan.py target.com")
    print(f"    python {py_target}/rce_scanner.py target.com")
    print(f"    python {py_target}/waf_detector.py target.com")
    
    config_file = opencode_dir / "config.json"
    config = {
        "tool_name": TOOL_NAME,
        "version": VERSION,
        "tools_dir": str(py_target),
        "skills_count": len(OPENCODE_SKILLS) + 1,
        "tools_count": count
    }
    with open(config_file, "w") as f:
        json.dump(config, f, indent=2)
    
    print("\n[+] Config saved to:", config_file)
    
    return opencode_dir

if __name__ == "__main__":
    install()