name: api-security
description: API security testing — REST API, GraphQL, gRPC, WebSocket, rate limiting, authentication bypass, API fuzzing
trigger:
  - API security
  - API testing
  - REST API
  - GraphQL
  - gRPC
  - WebSocket
  - API fuzzing
  - endpoint testing

---

# API SECURITY TESTING

## Common API Vulnerabilities

| Vulnerability | OWASP | Impact |
| IDOR | API1 | Data breach |
| Broken Authentication | API2 | Account takeover |
| Broken Object Level Authorization | API1 | Privilege escalation |
| Excessive Data Exposure | API3 | PII leak |
| Lack of Rate Limiting | API4 | Brute force |
| Injection | API6 | RCE |

---

# REST API TESTING

## HTTP Methods
```bash
# Test all methods
curl -X GET /endpoint
curl -X POST /endpoint
curl -X PUT /endpoint
curl -X DELETE /endpoint
curl -X PATCH /endpoint
curl -X OPTIONS /endpoint
curl -X HEAD /endpoint
```

## Authentication Testing
```bash
# No auth
curl /api/data

# Bearer token
curl -H "Authorization: Bearer TOKEN" /api/data

# Basic auth
curl -u user:pass /api/data

# API key
curl -H "X-API-Key: KEY" /api/data
curl -H "api_key: KEY" /api/data

# Cookie
curl -b "session=TOKEN" /api/data

# JWT
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1Ni..." /api/data
```

## Content Types
```bash
# JSON
curl -H "Content-Type: application/json" -d '{"id":1}'

# XML
curl -H "Content-Type: application/xml" -d '<id>1</id>'

# Form
curl -d "id=1"

# Multipart
curl -F "file=@file.txt" /api/upload
```

## Common API Endpoints
```bash
/api/v1/users
/api/v1/auth
/api/v1/login
/api/v1/logout
/api/v1/profile
/api/v2/...
/api/graphql
/api/swagger
/api/v3/...
/api/debug
/api/internal
/api/admin
/api/beta
```

---

# GRAPHQL TESTING

## Introspection
```graphql
# Query schema
{ __schema { types { name fields { name type { name } } } } }

# Query types
{ __type(name: "User") { name fields { name type { name } } } }

# Query all queries
{ __schema { queryType { name } mutationType { name } } }
```

## Common Queries
```graphql
# User enumeration
{ user(id: 1) { id email name } }
{ users { id email name } }
{ me { id email name } }

# Search
{ search(query: "admin") { ... } }

# Field probing
{user1: user(id:1){email}}
{user2: user(id:2){email}}
```

## GraphQL Mutations
```graphql
# Create
mutation { createUser(input: {email: "x@x.com"}) { id } }

# Update
mutation { updateUser(id: 1, email: "x@x.com") { id } }

# Delete
mutation { deleteUser(id: 1) { success } }
```

## GraphQL Attacks

### Batching (Rate Limit Bypass)
```json
[
  {"query": "mutation { login(email: \"a@a.com\", password: \"pass1\") }"},
  {"query": "mutation { login(email: \"a@a.com\", password: \"pass2\") }"},
  {"query": "mutation { login(email: \"a@a.com\", password: \"pass3\") }"}
]
```

### Query Complexity
```graphql
{
  users {
    posts {
      comments {
        author {
          posts {
            comments { author { posts } }
          }
        }
      }
    }
  }
}
```

### Alias Injection
```graphql
{
  user1: user(id: 1) { email }
  user2: user(id: 2) { email }
  user3: user(id: 3) { email }
  user4: user(id: 4) { email }
  user5: user(id: 5) { email }
}
```

### Introspection + Field Authorization
```graphql
# Works
{ user(id: 1) { email } }

# Bypass through node()
{ node(id: "dXNlcjox") { ... on User { email } }
```

---

# gRPC TESTING

## gRPC Reflection
```bash
# Enable reflection
grpcurl -plaintext target:5001 describe

# List services
grpcurl -plaintext target:5001 list

# Invoke method
grpcurl -plaintext -d '{"user_id": 1}' target:5001 UserService/GetUser
```

## gRPC Interceptor
```bash
# Test unary
grpcurl -d '{"id":1}' target:5001 Service/Method

# Test server streaming
grpcurl -d '{}' target:5001 Service/Method

# Test client streaming
grpcurl -d '{"data":1}' -d '{"data":2}' target:5001 Service/Method
```

---

# WEBSOCKET TESTING

## WebSocket Connection
```javascript
// JavaScript
var ws = new WebSocket("wss://target.com/ws");

ws.onopen = function() {
  ws.send("message");
};

ws.onmessage = function(e) {
  console.log(e.data);
};
```

## WebSocket Attacks
```bash
# Cross-site WebSocket
# WebSocket injection
# Authentication bypass
# Subscribe to channels
```

## Test WebSocket
```bash
# Using wscat
wscat -c wss://target.com/ws

# Send messages
{"type": "message", "content": "test"}
{"type": "subscribe", "channel": "admin"}
```

---

# API FUZZING

## Fuzz Parameters
```bash
# Integer fuzzing
for i in {1..1000}; do curl "/api?id=$i"; done

# String fuzzing
ffuf -w wordlist.txt -u "/api?q=FUZZ"

# Array fuzzing
{"ids": [1]}
{"ids": [1,2,3]}
{"ids": ["1","2","3"]}
```

## Parameter Discovery
```bash
ffuf -w wordlist.txt -u "/api?FUZZ=value"
ffuf -w wordlist.txt -u "/api/FUZZ"
```

---

# RATE LIMITING BYPASS

## Techniques
| Technique | Example |
| Change IP | X-Forwarded-For |
| Change User-Agent | Rotate UA |
| Change Cookie | Rotate session |
| Change Auth | Rotate tokens |
| Accept | Different MIME |
| Origin | Different domain |
| Encoding | Different encoding |

```bash
# Rate limit test
for i in {1..100}; do
  curl -H "X-Forwarded-For: 192.168.1.$i" /api/login &
done

# Using Turbo Intruder
# Concurrent requests
```

---

# IDOR IN APIS

## Test IDOR
```bash
# Replace ID in URL
/api/users/1
/api/users/2

# Replace ID in body
{"user_id": 1}
{"id": 1}

# Replace ID in header
X-User-ID: 1

# Replace ID in JWT claims
{"sub": 1}
```

## Batch IDOR
```bash
# Get multiple
/api/users?ids=1,2,3
/api/users?ids=*

# GraphQL
{users(ids:[1,2,3]){email}}
```

---

# API CHECKLIST

- [ ] Enumerate endpoints
- [ ] Test HTTP methods
- [ ] Test authentication
- [ ] Test authorization (IDOR)
- [ ] Test rate limiting
- [ ] Test GraphQL
- [ ] Test WebSocket
- [ ] Test versioning
- [ ] Test content types
- [ ] Fuzz parameters
- [ ] Test injections
- [ ] Test BOLA