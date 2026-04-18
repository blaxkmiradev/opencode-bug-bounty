name: report-writing
description: Professional bug bounty report writing — templates, CVSS calculation, impact analysis,Severity assessment, report formatting, triage response
trigger:
  - report writing
  - write report
  - bug report
  - cvss
  - severity
  - impact assessment
  - triage response
  - 漏洞报告
  - 报告撰写

---

# BUG BOUNTY REPORT WRITING

## Report Quality Checklist

A high-quality report has:
- Clear title with vuln class + location + impact
- Concise summary (2-3 sentences)
- Reproducible steps with exact HTTP requests
- Proof of impact (screenshots, data)
- Proper CVSS calculation
- Actionable remediation

A low-quality report has:
- Vague title like "Security issue"
- Long narrative without specifics
- "I found that..." without PoC
- Unsupported impact claims
- No CVSS or wrong calculation

---

# TITLE FORMULA

## Good Titles

```
[Vuln Class] in [Exact Endpoint/Feature] allows [Attacker] to [Impact] [Scope]
```

Examples:
- "IDOR in /api/v2/invoices/{id} allows authenticated user to read any customer's invoice data"
- "Stored XSS in profile bio field executes in admin panel, allows privilege escalation"
- "Missing authentication on POST /api/admin/users allows unauthenticated attacker to create admin accounts"
- "SSRF via image import URL reaches AWS EC2 metadata service"
- "Race condition in coupon redemption allows same code to be used unlimited times"

## Bad Titles

```
Security vulnerability found
Broken access control
XSS in user input
API security issue
Information disclosure
```

---

# SUMMARY FORMULA

**First sentence states exact impact in plain English:**

```
An [attacker with X access level] can [exact action] by [method], resulting in [business harm].
This requires [prerequisites] and leaves [detection difficulty].
```

**Example:**
```
An attacker with a free account can read any user's billing information by modifying the user ID in the API request, resulting in exposure of all customers' PII.
This requires only a standard account and leaves no trace in standard logs.
```

---

# STEPS TO REPRODUCE

## Template

1. Log in as [attacker account]
2. Navigate to [exact endpoint] or send request:
   ```http
   [EXACT HTTP REQUEST]
   ```
3. Observe: [exact response showing the bug]
4. Confirm: [what the attacker gained]

## Make it Copy-Paste Ready

```http
GET /api/v2/invoices/12345 HTTP/1.1
Host: target.com
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...

Response:
{"id": 12345, "customer_email": "victim@company.com", "amount": 499.99}
```

---

# IMPACT STATEMENT

## Quantify When Possible

- "Affects N users" - how many?
- "Exposes $X value" - financial impact?
- "N records" - how much data?
- "All users can..." - scope?

## Business Impact Over Technical

- **Financial**: Money stolen, refund fraud
- **Data**: PII exposed, HIPAA violation
- **Account**: Unauthorized access, takeover
- **Reputation**: Public exposure, embarrassment
- **Legal**: Compliance violation, fines

---

# CVSS 3.1 CALCULATOR

## Base Metrics

| Metric | Values |
|-------|--------|
| Attack Vector (AV) | Network (N), Adjacent (A), Local (L), Physical (P) |
| Attack Complexity (AC) | Low (L), High (H) |
| Privileges Required (PR) | None (N), Low (L), High (H) |
| User Interaction (UI) | None (N), Required (R) |
| Scope (S) | Unchanged (U), Changed (C) |
| Confidentiality (C) | None (N), Low (L), High (H) |
| Integrity (I) | None (N), Low (L), High (H) |
| Availability (A) | None (N), Low (L), High (H) |

## Typical Scores

| Vulnerability | CVSS | Severity |
| IDOR (read PII) | 6.5 | Medium |
| IDOR (write/delete) | 7.5 | High |
| Auth bypass -> admin | 9.8 | Critical |
| Stored XSS | 5.4-8.8 | Medium-High |
| SQLi (data exfil) | 8.6 | High |
| SSRF (cloud metadata) | 9.1 | Critical |
| Race condition | 7.5 | High |
| GraphQL auth bypass | 8.7 | High |
| JWT none algorithm | 9.1 | Critical |
| Reflected XSS | 6.1 | Medium |
| Self-XSS | 3.5-5.4 | Low-Medium |

## Quick CVSS Formulas

**Network + None privileges + Low complexity + None user interaction = Base + 0.85**
**Add scope change = + 0.5**
**Add high confidentiality = + 0.56**

---

# REPORT TEMPLATES

## Template 1: HackerOne

```markdown
# Title
[vuln class] in [endpoint/feature] leads to [Impact]

## Summary
[2-3 sentences: what it is, where it is, what attacker can do]

## Steps To Reproduce
1. [step with exact request]
2. [step with exact request]
3. [step with exact request]

## Supporting Material
[screenshot / video / burp request]

## Impact
[specific action resulting in specific harm]
[quantify if possible]

## Severity Assessment
CVSS 3.1 Score: X.X ([severity])
Attack Vector: Network | Complexity: Low | Privileges: None | User Interaction: None
```

## Template 2: Bugcrowd

```markdown
# Title
[vuln] at [endpoint] -- [Impact in one line]

Bug Type: [vuln class]
Target: [URL or component]
Severity: [P1-P4]

Description:
[root cause + exact location]

Reproduction:
1. [step]
2. [step]
3. [step]

Impact:
[concrete business impact]

Fix Suggestion:
[specific remediation]
```

## Template 3: Intigriti

```markdown
# Summary
| Field | Value |
|-------|-------|
| Target | URL/API |
| Severity | Critical/High/Medium/Low |
| Type | IDOR/XSS/etc |
| Reward | $X |

# Description
[What and where]

# Proof of Concept
[Exact request + response]

# Impact
[Business impact]

# Remediation
[How to fix]
```

---

# TRIAGE RESPONSE TEMP LATES

## Responding to "Not Applicable"

```
This affects [X] users and exposes [specific data type].
The attack requires only a free account - no special privileges.
I've attached a video showing the impact.
[or: This is chained with [finding B] to achieve [impact].
```

## Responding to "Duplicate"

Please provide the report number - I searched hacktivity and did not find this specific vulnerability in [endpoint/method/variant].
If duplicate, I understand. Thank you for the response.

## Responding to "Low Severity"

I understand the CVSS score. However, this affects [N] users and exposes [PII type/financial data].
The practical impact to users is [specific harm].
[or: When chained with [finding B], this becomes [higher severity].

## Responding to "By Design"

Please point me to the documentation that states this behavior is intentionally allowed.
This appears to bypass [security control] without any warning to users.
[or: This contradicts the program's security policy at [URL].

---

# ALWAYS REJECTED LIST

Never submit these without chaining:
- Missing CSP/HSTS
- Missing SPF/DKIM/DMARC  
- GraphQL introspection alone
- Banner disclosure without CVE
- Clickjacking on non-sensitive pages
- Tabnabbing
- CSV injection
- CORS without credential exfil PoC
- Logout CSRF
- Self-XSS
- Open redirect alone
- OAuth client_secret in mobile app
- SSRF DNS-only
- Host header injection alone
- No rate limit on non-critical forms
- Session not invalidated on logout
- Internal IP disclosure
- Mixed content
- Missing HttpOnly/Secure flags alone
- Broken external links
- Autocomplete on password fields

---

# 60-SECOND PRE-SUBMIT CHECKLIST

- [ ] Title follows formula: [Class] in [endpoint] allows [actor] to [impact]
- [ ] First sentence states exact impact in plain English
- [ ] Steps to Reproduce has exact HTTP request (copy-paste ready)
- [ ] Response showing the bug is included
- [ ] Two test accounts used
- [ ] CVSS score calculated and included
- [ ] Recommended fix is one sentence
- [ ] No typos in the endpoint path
- [ ] Report is < 600 words
- [ ] Severity claimed matches impact described

---

# HUMAN TONE RULES

- Start with impact, not vulnerability name
- Write like explaining to a developer, not a textbook
- Use "I found..." not "A vulnerability was discovered..."
- One concrete example beats three abstract sentences
- No: "comprehensive/leverage/seamless/ensure"
- No em dashes in the middle of sentences
- Active voice: "I can read..." not "This allows reading..."