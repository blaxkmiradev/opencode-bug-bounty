name: web-audit
description: Web application security audit — source code review, API testing, authentication bypass, authorization flaws, business logic flaws
trigger:
  - web audit
  - code review
  - source audit
  - API security
  - authentication bypass
  - authorization
  - business logic
  - web security audit

---

# WEB APPLICATION SECURITY AUDIT

## Source Code Review Methodology

### Step 1: Tech Stack Identification
```bash
# Detect framework from source
grep -r "require(" --include="*.js" | head -20
grep -r "import " --include="*.py" | head -20
grep -r "using " --include="*.cs" | head -20

# Check package managers
ls package.json  # Node.js
ls requirements.txt  # Python
ls pom.xml  # Java
ls go.mod  # Go
```

### Step 2: Dangerous Pattern Search
```bash
# JavaScript/Node.js
grep -rn "eval(\|exec(\|spawn(" --include="*.js"
grep -rn "child_process" --include="*.js"
grep -rn "dangerouslySetInnerHTML" --include="*.js"
grep -rn "innerHTML\|outerHTML" --include="*.js"
grep -rn "document.write" --include="*.js"

# Python
grep -rn "pickle\.loads\|yaml\.load\|eval(" --include="*.py"
grep -rn "subprocess\|os\.system\|os\.popen" --include="*.py"
grep -rn "format()\|fstring" --include="*.py"

# PHP
grep -rn "eval(\|exec(\|system(" --include="*.php"
grep -rn "unserialize" --include="*.php"
grep -rn "preg_replace.*e" --include="*.php"
grep -rn "\$\_(GET|POST|REQUEST)" --include="*.php"

# Java
grep -rn "exec\|Runtime.getRuntime" --include="*.java"
grep -rn "JNDI\|ldap" --include="*.java"
grep -rn "SQL\|PreparedStatement" --include="*.java"
```

### Step 3: Auth Check
```bash
# Find auth implementation
grep -rn "password\|hash\|bcrypt" --include="*.py"
grep -rn "jwt\|token\|session" --include="*.js"
grep -rn "token\|authorize\|security" --include="*.java"

# Find auth validation middleware
grep -rn "authenticate\|verify\|checkAuth" --include="*"
```

---

# API SECURITY TESTING

## REST API Testing
```bash
# Enumerate endpoints
ffuf -u https://api.target.com/FUZZ -w wordlist.txt -mc 200,201,401,403

# Test HTTP methods
for method in GET POST PUT DELETE PATCH OPTIONS; do
  curl -X $method https://api.target.com/endpoint -v
done

# Test authentication
curl -H "Authorization: Bearer TOKEN" https://api.target.com/endpoint
curl -H "Cookie: session=TOKEN" https://api.target.com/endpoint

# Test IDOR in API
curl https://api.target.com/users/1
curl https://api.target.com/users/2  # Compare responses
```

## GraphQL Testing
```bash
# Introspection
curl -X POST https://target.com/graphql \
  -H "Content-Type: application/json" \
  -d '{"query":"{ __schema { types { name fields { name type { name } } } } }"}'

# Test query
curl -X POST https://target.com/graphql \
  -H "Content-Type: application/json" \
  -d '{"query":"{ user(id: 1) { email password } }"}'

# Test mutation
curl -X POST https://target.com/graphql \
  -H "Content-Type: application/json" \
  -d '{"query":"mutation { updateUser(id: 1, email: \"attacker@evil.com\") { id } }"}'
```

## API Bypass Techniques
| Technique | Example |
| JSON parameter pollution | {"id": 1, "id": 2} |
| Type confusion | {"id": "1"} vs {"id": 1} |
| Array injection | {"ids": [1,2,3]} |
| Wildcard | {"ids": "*"} |
| Null bypass | {"id": null} |

---

# AUTHENTICATION BYPASS

## Common Auth Bypass
- Missing auth check on endpoint
- Auth check only in some routes
- Token not validated
- Weak token generation
- Session not invalidated
- CSRF token missing

## JWT Vulnerabilities
```bash
# None algorithm
{"alg": "none"}

# Algorithm confusion
{"alg": "HS256"}  # Use public key as HMAC secret

# Key confusion
{"alg": "RS256"} -> {"alg": "HS256"}
```

## Session Fixation
```bash
# Test session fixation
1. Get session cookie
2. Login (session should change)
3. If same = vulnerability
```

---

# AUTHORIZATION FLAWS

## Horizontal Privilege Escalation
```bash
# Access other user's data
GET /api/users/1
GET /api/users/2  # Same privileges, different user
```

## Vertical Privilege Escalation
```bash
# Access admin endpoints with user account
GET /api/admin/users
POST /api/admin/create
```

## Insecure Direct Object Reference (IDOR)
| Test | Request |
| Access other user file | /files/download?id=../otheruser/file.pdf |
| Access other user invoice | /api/invoices/12345 |
| Modify other user profile | PUT /api/users/2 {"email": "attacker@evil.com"} |

---

# BUSINESS LOGIC FLAWS

## Price Manipulation
```bash
# Negative price
POST /api/checkout
{"item_id": 1, "price": -100}

# Price in request (trust client)
POST /api/checkout
{"item_id": 1, "price": 0.01}
```

## Quantity Manipulation
```bash
# Negative quantity
POST /api/cart
{"item_id": 1, "quantity": -999}

# Overflow
POST /api/cart
{"item_id": 1, "quantity": 999999999}
```

## Coupon/Discount Abuse
```bash
# Reuse single-use coupon
# Race condition with multiple requests
# Coupon code enumeration
```

## Workflow Bypass
```bash
# Skip payment step
POST /api/order/complete
{"step1": true, "step2": true, "step3": false}

# Access without subscription
GET /api/premium/content  # Bypass check
```

---

# RACE CONDITIONS

## Testing for Race Conditions
```bash
# Concurrent coupon redemption
seq 20 | xargs -P 20 -I {} curl -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"code": "SAVE20"}' &

# Double spend / balance manipulation
for i in {1..50}; do
  curl -X POST -H "Authorization: Bearer $TOKEN" \
    -d '{"amount": 100}' &
done
```

## Race Condition Payloads
- Parallel transfers
- Coupon reuse
- OTP bypass
- Inventory manipulation
- Rate limit bypass

---

# CRITICAL ENDPOINTS TO TEST

| Endpoint | Test |
| /api/login | Default creds, SQLi, OAuth bypass |
| /api/register | Email enumeration, SQLi |
| /api/password-reset | Token prediction, Host header injection |
| /api/admin/* | Privilege escalation |
| /api/upload | File upload, extension bypass |
| /api/payment | Price manipulation, integer overflow |
| /api/graphql | Introspection, query complexity |
| /api/debug | Information disclosure |

---

# ALWAYS TEST

1. **Change HTTP method** - GET -> POST -> PUT -> DELETE
2. **Add/remove headers** - Content-Type, Authorization, X-Forwarded-For
3. **Change Content-Type** - JSON -> XML -> form-data
4. **IDOR on all endpoints** - Change IDs
5. **Auth on all endpoints** - Access with/without token
6. **Rate limiting** - Brute force enumeration
7. **Error handling** - Force errors, check disclosure