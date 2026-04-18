name: osint
description: OSINT and reconnaissance — target footprinting, email harvesting, social media OSINT, leaks database search, GitHub reconnaissance, domain research
trigger:
  - OSINT
  - reconnaissance
  - email harvesting
  - social media
  - domain research
  - GitHub
  - information gathering
  - google hacking
  - ghdb

---

# OSINT & RECONNAISSANCE

## Target Footprinting

### Domain Information
```bash
# WHOIS
whois target.com

# DNS
dig target.com ANY
dig -x 1.2.3.4

# Subdomains
subfinder -d target.com
assetfinder --subs-only target.com
```

### Email Harvesting
```bash
# TheHarvester
theHarvester -d target.com -b all

# EmailHunter
hunter.io search target.com

# Google search
site:target.com email
site:target.com @gmail.com
```

### Technology Fingerprint
```bash
# BuiltWith
builtwith.com

# Wappalyzer  
wappalyzer.com

# WhatWeb
whatweb target.com
```

## Google Hacking (GHDB)

### Find Login Pages
```
site:target.com inurl:login
site:target.com inurl:admin
site:target.com inurl:dashboard
site:target.com inurl:signin
```

### Find Sensitive Files
```
site:target.com ext:xml
site:target.com ext:yml
site:target.com ext:env
site:target.com ext:json
site:target.com ext:xlsx
site:target.com ext:csv
site:target.com ext:pdf
```

### Find Backups
```
site:target.com ext:bak
site:target.com ext:old
site:target.com ext:zip
site:target.com ext:tar.gz
site:target.com "index of" backup
```

### Find Config Files
```
site:target.com ext:config
site:target.com ext:conf
site:target.com ext:ini
site:target.com ext:cfg
```

### Find Passwords
```
site:target.com "password"
site:target.com "password" filetype:xlsx
site:target.com "password" filetype:txt
site:target.com "password" filetype:csv
```

### Find Databases
```
site:target.com ext:sql
site:target.com ext:sqlite
site:target.com ext:db
site:target.com ext:mdb
```

### Find Exposed Docs
```
site:target.com filetype:pdf
site:target.com filetype:doc
site:target.com filetype:docx
site:target.com filetype:xls
```

### Find Debug Pages
```
site:target.com inurl:debug  
site:target.com inurl:test
site:target.com inurl:phpinfo
site:target.com inurl:env
```

### Find Git
```
site:github.com target.com
site:github.com "target.com"
inurl:.git target.com
site:github.com target fork
```

---

# EMAIL OSINT

## Email Discovery
```
@target.com
firstname.lastname@target.com
admin@target.com
support@target.com
contact@target.com
```

## Email Patterns
- firstname.lastname@target.com
- firstname@target.com
- lastname@target.com
- initials@target.com
- flast@target.com

## Breached Credentials
- HaveIBeenPwned.com
- Dehashed.com
- LeakCheck.io
- IntelX.io

---

# SOCIAL MEDIA OSINT

## Search Techniques
```
site:linkedin.com "target"
site:twitter.com "target"
site:facebook.com "target"
```

## People Search
- LinkedIn
- Twitter
- Facebook
- Instagram

---

# GITHUB OSINT

## Find Repos
```
site:github.com target-org
site:github.com "target company"
```

## Find Secrets
```
repo:target/repo password=
repo:target/repo api_key=
repo:target/repo secret=
repo:target/repo AWS_ACCESS
repo:target/repo private_key
```

## Find Dorks
```
github "target.com" password
github "target.com" api_key
github "target.com" token
github "CF" API key
github "Authorization: Bearer"
```

---

# DOMAIN OSINT

## Find Subdomains
```bash
# DNSenum
dnsenum target.com

# Fierce
fierce --domain target.com

# Sublist3r
sublist3r -d target.com
```

## Find Historical Data
```bash
# SecurityTrails
securitytrails.com

# Wayback Machine
web.archive.org
waybackurls target.com

# CtExposure
```

---

# WIRELESS OSINT

## WiFi Networks
- WiGLE.net
- WirelessMap

---

# PASSWORD OSINT

## Common Patterns
- Password in URL
- Password in configs
- AWS keys
- API keys
- Private keys

---

# OSINT CHECKLIST

## Passive Recon
- [ ] WHOIS lookup
- [ ] DNS enumeration
- [ ] Subdomain enumeration
- [ ] Technology fingerprint
- [ ] Email discovery
- [ ] Cloud storage search

## Active OSINT
- [ ] Google hacking
- [ ] GitHub search
- [ ] Social media search
- [ ] Breached credentials check
- [ ] Wayback machine

## Documentation
- [ ] Screenshot search results
- [ ] Document all findings
- [ ] Cross-reference data