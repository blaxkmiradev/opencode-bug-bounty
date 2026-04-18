# Bug Hunter - Bug Chaining Tool
# Usage: ./chain.ps1 -FindingsFile <file> -OutputDir <dir>

param(
    [string]$FindingsFile = "./bug-hunter-output/findings.txt",
    [string]$OutputDir = "./bug-hunter-output"
)

Write-Host "[*] Bug Chaining Tool" -ForegroundColor Cyan
Write-Host "[*] Finding known chains to escalate impact" -ForegroundColor Yellow

# Read existing findings
$findings = @()

if (Test-Path $FindingsFile) {
    $findings = Get-Content $FindingsFile
} else {
    # Scan for existing findings
    $findingsDir = Get-ChildItem -Path $OutputDir -Filter "*.txt" -ErrorAction SilentlyContinue
    
    foreach ($file in $findingsDir) {
        $content = Get-Content $file.FullName
        if ($content) { $findings += $content }
    }
}

# Known chains
$chains = @{
    # S3 Chain
    "S3 bucket listable" = @("Enumerate JS bundles for OAuth client_secret", "Check for wildcard redirect_uri", "Check cookie domain")
    
    # IDOR Chain
    "IDOR (read)" = @("PUT/DELETE on same endpoint", "Nested IDOR", "GraphQL node bypass")
    
    # XSS Chain
    "XSS (stored)" = @("Session cookie HttpOnly?", "CSRF token theft", "Fake login form", "Service worker")
    
    # Open Redirect Chain
    "Open redirect" = @("OAuth redirect_uri accepts attacker domain", "Use in URL parameter", "CSP bypass")
    
    # SSRF Chain
    "SSRF" = @("Cloud metadata access", "Internal service access", "Port scan internal")
    
    # CORS Chain
    "CORS wildcard" = @("Credentialed requests", "JSONP callback", "PostMessage listener")
    
    # Host Header Chain
    "Host header injection" = @("Password reset poisoning", "Session fixation", "Cache poisoning")
    
    # GraphQL Chain
    "GraphQL introspection" = @("Missing field-level auth", "Batching for rate limit", "Query complexity")
    
    # Race Condition Chain
    "Race condition" = @("Double-spend", "Coupon reuse", "OTP bypass")
}

Write-Host "`n[*] Known Escalation Chains:" -ForegroundColor Green

foreach ($finding in $findings) {
    if ($finding -match "IDOR|XSS|SSRF|Open redirect|S3|CORS|GraphQL|Race|Host header") {
        $type = $matches[0]
        
        Write-Host "`n[*] Found: $finding" -ForegroundColor Cyan
        Write-Host "[*] Chain with:" -ForegroundColor Yellow
        
        if ($chains.ContainsKey($type)) {
            foreach ($chain in $chains[$type]) {
                Write-Host "    -> $chain" -ForegroundColor White
            }
        }
    }
}

# Quick Chain Reference Table
Write-Host "`n[*] Chain Reference Table:" -ForegroundColor Green

$chainTable = @"

| Bug A (Signal) | Hunt for Bug B | Escalate to C |
|-------------|--------------|------------|
| IDOR (read) | PUT/DELETE same endpoint | Full account manipulation |
| SSRF | Cloud metadata | IAM credential exfil -> RCE |
| XSS (stored) | HttpOnly on cookie | Session hijack -> ATO |
| Open redirect | OAuth redirect_uri | Auth code theft -> ATO |
| S3 listing | JS bundles -> OAuth secret | OAuth chain |
| Rate limit bypass | OTP brute force | Account takeover |
| GraphQL introspec | Missing field auth | Mass PII exfil |
| Debug endpoint | Env vars | Cloud credentials |
| CORS reflects origin | With credentials | Data theft |
| Host header inj | Password reset | ATO |

| Low Finding | + Chain | = Valid Bug |
|-----------|-------|----------|
| Open redirect | + OAuth code theft | ATO |
| Clickjacking | + sensitive action | Account action |
| CORS wildcard | + credentialed exfil | Data theft |
| CSRF | + sensitive state | ATO |
| No rate limit | + OTP brute | ATO |
| SSRF (DNS) | + internal proof | Internal access |
| Host header | + reset poisoning | ATO |
| Self-XSS | + login CSRF | Stored XSS |

"@

Write-Host $chainTable

# Save chain reference
$chainFile = "$OutputDir/chains.txt"
$chainTable | Set-Content $chainFile
Write-Host "[*] Chain reference saved to: $chainFile" -ForegroundColor Green