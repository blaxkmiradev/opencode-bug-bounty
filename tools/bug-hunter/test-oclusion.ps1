# Bug Hunter - OAuth/OIDC Testing Tool
# Usage: ./test-oauth.ps1 -Target <URL>

param(
    [Parameter(Mandatory=$true)]
    [string]$Target,
    [switch]$All,
    [switch]$Redirect,
    [switch]$State
)

Write-Host "[*] OAuth/OIDC Testing for: $Target" -ForegroundColor Cyan

$results = @()

# OAuth Vulnerabilities
$oauthTests = @{
    # Missing state parameter
    "state" = "CSRF - No state parameter"
    
    # redirect_uri vulnerabilities
    "redirect_uri" = @{payloads=@(
        "https://attacker.com",
        "https://attacker.com/callback",
        "http://127.0.0.1",
        "///attacker.com",
        "https://target.com.attacker.com",
        "https://target.com%2Fattacker.com"
    )}
    
    # PKCE missing
    "pkce" = "Missing PKCE - Code theft"
    
    # Open redirect
    "open_redirect" = @{payloads=@(
        "https://attacker.com",
        "///attacker.com",
        "https://target.com//attacker.com",
        "https://target.com/../attacker.com"
    )}
}

# Test Functions
function Test-OAuthRedirect {
    param($url, $redirectUri)
    
    Write-Host "[*] Testing redirect_uri: $redirectUri" -ForegroundColor Gray
    
    try {
        $response = Invoke-WebRequest -Uri "$url&redirect_uri=$([Uri]::EscapeDataString($redirectUri))" `
            -UseBasicParsing -MaximumRedirection 0 -ErrorAction SilentlyContinue
        
        if ($response.Headers["Location"] -match "attacker|$redirectUri") {
            Write-Host "[!] Open redirect FOUND" -ForegroundColor Red
            return @{Type="Open Redirect"; Payload=$redirectUri; Location=$response.Headers["Location"]}
        }
    } catch {
        if ($_.Exception.Message -match "301|302|303|307|308") {
            $location = $_.Exception.Message -replace ".*Location: ", ""
            if ($location -match "attacker") {
                return @{Type="Open Redirect"; Payload=$redirectUri; Location=$location}
            }
        }
    }
    
    return $null
}

function Test-MissingState {
    param($url)
    
    Write-Host "[*] Testing missing state parameter" -ForegroundColor Gray
    
    # Check if state is required
    if ($url -notmatch "state=") {
        Write-Host "[!] No state parameter FOUND" -ForegroundColor Red
        return @{Type="CSRF"; Issue="No state parameter"}
    }
    
    return $null
}

# Run tests
Write-Host "[*] Starting OAuth tests..." -ForegroundColor Yellow

if ($All -or $Redirect) {
    Write-Host "[*] Testing redirect_uri..." -ForegroundColor Yellow
    
    $redirectPayloads = @(
        "https://attacker.com",
        "https://attacker.com/callback",
        "http://127.0.0.1:8080",
        "///attacker.com",
        "https://target.com.attacker.com",
        "https://target.com/../attacker.com",
        "https://target.com%2Fattacker.com",
        "https://target.com\\attacker.com",
        "https://target.com%5Cattacker.com",
        "https://target.com%E2%80%A6attacker.com"
    )
    
    foreach ($payload in $redirectPayloads) {
        # Append to authorization URL
        $testUrl = "$Target&redirect_uri=$([Uri]::EscapeDataString($payload))"
        
        try {
            $response = Invoke-WebRequest -Uri $testUrl -UseBasicParsing -MaximumRedirection 0 -ErrorAction SilentlyContinue
        } catch {}
    }
}

if ($All -or $State) {
    Write-Host "[*] Testing state parameter..." -ForegroundColor Yellow
    
    if ($Target -notmatch "state=") {
        Write-Host "[!] State parameter missing - CSRF vulnerability" -ForegroundColor Red
        $results += @{Type="CSRF"; Issue="State parameter missing"}
    }
}

# OAuth Flow Test
Write-Host "[*] Testing full OAuth flow..." -ForegroundColor Yellow

$testSteps = @(
    "Step 1: Authorization Request",
    "Step 2: Token Request",
    "Step 3: UserInfo Request"
)

# Output results
Write-Host "`n[*] OAuth Testing Complete" -ForegroundColor Green
Write-Host "[*] Found $($results.Count) issues" -ForegroundColor Cyan

# Always Test checklist
Write-Host "`n[*] OAuth Testing Checklist:" -ForegroundColor Yellow
Write-Host "[*] 1. redirect_uri open redirect" -ForegroundColor White
Write-Host "[*] 2. redirect_uri wildcard" -ForegroundColor White
Write-Host "[*] 3. Missing state parameter" -ForegroundColor White
Write-Host "[*] 4. Missing PKCE" -ForegroundColor White
Write-Host "[*] 5. Implicit flow (no PKCE)" -ForegroundColor White
Write-Host "[*] 6. Token in URL (implicit)" -ForegroundColor White
Write-Host "[*] 7. Token reuse allowed" -ForegroundColor White
Write-Host "[*] 8. Weak client secret" -ForegroundColor White
Write-Host "[*] 9. Token not invalidated on logout" -ForegroundColor White
Write-Host "[*] 10. No token expiration check" -ForegroundColor White

# Save results
$resultsFile = "./bug-hunter-output/oauth-results.txt"
$results | ConvertTo-Json | Set-Content $resultsFile
Write-Host "[*] Results saved to: $resultsFile" -ForegroundColor Green