# Bug Hunter - API Security Testing Tool
# Usage: ./test-api.ps1 -Target <api-url>

param(
    [Parameter(Mandatory=$true)]
    [string]$Target,
    [string]$Token,
    [switch]$All,
    [switch]$Auth,
    [switch]$IDOR,
    [switch]$RateLimit,
    [switch]$GraphQL
)

Write-Host "[*] API Security Testing for: $Target" -ForegroundColor Cyan

$Results = @()

# API Endpoints to test
$apiEndpoints = @(
    "/api/users",
    "/api/user",
    "/api/auth",
    "/api/login",
    "/api/logout",
    "/api/register",
    "/api/profile",
    "/api/account",
    "/api/settings",
    "/api/admin",
    "/api/v1/users",
    "/api/v2/users",
    "/api/graphql",
    "/api/debug",
    "/api/health",
    "/api/status"
)

function Test-APIEndpoint {
    param($url, $method, $headers, $body)
    
    try {
        $params = @{
            Uri = $url
            Method = $method
            UseBasicParsing = $true
            ErrorAction = SilentlyContinue
        }
        
        if ($headers) { $params.Headers = $headers }
        if ($body) { $params.Body = $body }
        if ($Token) { $params.Headers = @{Authorization = "Bearer $Token"} }
        
        $response = Invoke-RestMethod @params
        
        return @{
            Status = $response.StatusCode
            Content = $response
        }
    } catch {
        return @{
            Status = $_.Exception.Response.StatusCode
            Error = $_.Exception.Message
        }
    }
}

# Run tests
Write-Host "[*] Testing API endpoints..." -ForegroundColor Yellow

# Test each endpoint
foreach ($endpoint in $apiEndpoints) {
    $url = $Target.TrimEnd('/') + "/" + $endpoint.TrimStart('/')
    
    # Test GET
    Write-Host "[*] Testing: $endpoint (GET)" -ForegroundColor Gray
    $result = Test-APIEndpoint -url $url -method "GET"
    
    if ($result.Status -eq 200 -or $result.Status -eq 401) {
        Write-Host "[*] Found: $endpoint - $($result.Status)" -ForegroundColor Cyan
        $Results += @{Endpoint=$endpoint; Method="GET"; Status=$result.Status}
    }
    
    # Test POST
    Write-Host "[*] Testing: $endpoint (POST)" -ForegroundColor Gray
    $result = Test-APIEndpoint -url $url -method "POST"
    
    if ($result.Status -eq 200 -or $result.Status -eq 401) {
        Write-Host "[*] Found: $endpoint - $($result.Status)" -ForegroundColor Cyan
        $Results += @{Endpoint=$endpoint; Method="POST"; Status=$result.Status}
    }
}

# Test HTTP Methods
Write-Host "[*] Testing HTTP methods..." -ForegroundColor Yellow

$methods = @("GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD")

if ($Results.Count -gt 0) {
    $firstEndpoint = $Results[0].Endpoint
    $url = $Target + $firstEndpoint
    
    foreach ($method in $methods) {
        Write-Host "[*] Testing: $method on $firstEndpoint" -ForegroundColor Gray
        
        try {
            $response = Invoke-WebRequest -Uri $url -Method $method -UseBasicParsing -ErrorAction SilentlyContinue
            if ($response.StatusCode -ne 405) {  # Not Method Not Allowed
                Write-Host "[*] $method allowed: $($response.StatusCode)" -ForegroundColor Cyan
                $Results += @{Endpoint=$firstEndpoint; Method=$method; Status=$response.StatusCode}
            }
        } catch {}
    }
}

# Test IDOR
if ($All -or $IDOR) {
    Write-Host "[*] Testing IDOR..." -ForegroundColor Yellow
    
    # Test with numeric IDs
    for ($i = 1; $i -le 10; $i++) {
        $url = "$Target/api/users/$i"
        Write-Host "[*] Testing ID: $i" -ForegroundColor Gray
        
        try {
            $response = Invoke-RestMethod -Uri $url -UseBasicParsing -ErrorAction SilentlyContinue
            
            if ($response -and $response.id -eq $i) {
                $Results += @{Type="IDOR"; Endpoint="/api/users/$i"; Status="Accessible"}
            }
        } catch {}
    }
    
    # Test IDOR with headers
    $testHeaders = @(
        @{X-User-ID = "1"},
        @{X-User-ID = "2"},
        @{X-Forwarded-User = "1"}
    )
    
    foreach ($header in $testHeaders) {
        Write-Host "[*] Testing header: $($header.Keys)" -ForegroundColor Gray
        
        try {
            $response = Invoke-RestMethod -Uri "$Target/api/me" -Headers $header -UseBasicParsing -ErrorAction SilentlyContinue
        } catch {}
    }
}

# Test Rate Limiting
if ($All -or $RateLimit) {
    Write-Host "[*] Testing rate limiting..." -ForegroundColor Yellow
    
    $count = 0
    $limited = $false
    
    for ($i = 1; $i -le 50; $i++) {
        try {
            $response = Invoke-WebRequest -Uri "$Target/api/login" -Method POST `
                -Body (@{email = "test$i@test.com"; password = "test"} | ConvertTo-Json) `
                -Headers @{"Content-Type" = "application/json"} `
                -UseBasicParsing -ErrorAction SilentlyContinue
            
            if ($response.StatusCode -eq 429) {
                $limited = $true
                $count = $i
                break
            }
        } catch {
            if ($_.Exception.Message -match "429") {
                $limited = $true
                $count = $i
                break
            }
        }
    }
    
    if ($limited) {
        Write-Host "[!] Rate limited after $count requests" -ForegroundColor Red
        $Results += @{Type="Rate Limit"; After=$count}
    } else {
        Write-Host "[!] No rate limiting detected" -ForegroundColor Yellow
        $Results += @{Type="No Rate Limit"; Risk="High"}
    }
}

# Test GraphQL
if ($All -or $GraphQL -or $Target -match "graphql") {
    Write-Host "[*] Testing GraphQL..." -ForegroundColor Yellow
    
    $url = $Target.TrimEnd('/')
    
    # Introspection query
    $query = '{ __schema { types { name fields { name } } } }'
    $body = @{query = $query} | ConvertTo-Json
    
    try {
        $response = Invoke-RestMethod -Uri $url -Method POST -Body $body `
            -Headers @{"Content-Type" = "application/json"} `
            -UseBasicParsing -ErrorAction SilentlyContinue
        
        if ($response.data) {
            Write-Host "[!] GraphQL introspection enabled" -ForegroundColor Red
            $Results += @{Type="GraphQL Introspection"; Status="Enabled"}
        }
    } catch {}
    
    # Test query
    $query = '{ user(id: 1) { email } }'
    $body = @{query = $query} | ConvertTo-Json
    
    try {
        $response = Invoke-RestMethod -Uri $url -Method POST -Body $body `
            -Headers @{"Content-Type" = "application/json"} `
            -UseBasicParsing -ErrorAction SilentlyContinue
        
        if ($response.data -and $response.data.user) {
            Write-Host "[!] GraphQL query accessible" -ForegroundColor Yellow
        }
    } catch {}
    
    # Test mutation
    $query = 'mutation { updateUser(id: 1, email: "attacker@evil.com") { id } }'
    $body = @{query = $query} | ConvertTo-Json
    
    try {
        $response = Invoke-RestMethod -Uri $url -Method POST -Body $body `
            -Headers @{"Content-Type" = "application/json"} `
            -UseBasicParsing -ErrorAction SilentlyContinue
    } catch {}
}

# JSON Parameter Pollution
Write-Host "[*] Testing JSON parameter pollution..." -ForegroundColor Yellow

$jppTests = @(
    @{id = 1; id = 2},
    @{id = "1"; id = 1},
    @{ids = @("1", "2", "3")},
    @{id = "*"},
    @{id = ""}
)

foreach ($test in $jppTests) {
    Write-Host "[*] Testing: $($test | ConvertTo-Json)" -ForegroundColor Gray
    
    try {
        $response = Invoke-RestMethod -Uri "$Target/api/users" -Method POST -Body ($test | ConvertTo-Json) `
            -Headers @{"Content-Type" = "application/json"} `
            -UseBasicParsing -ErrorAction SilentlyContinue
    } catch {}
}

# Output results
Write-Host "`n[*] API Security Testing Complete" -ForegroundColor Green
Write-Host "[*] Found $($Results.Count) findings" -ForegroundColor Cyan

# API Testing Checklist
Write-Host "`n[*] API Security Checklist:" -ForegroundColor Yellow
Write-Host "[*] 1. Enumerate endpoints" -ForegroundColor White
Write-Host "[*] 2. Test HTTP methods" -ForegroundColor White
Write-Host "[*] 3. Test IDOR" -ForegroundColor White
Write-Host "[*] 4. Test auth bypass" -ForegroundColor White
Write-Host "[*] 5. Test rate limiting" -ForegroundColor White
Write-Host "[*] 6. Test GraphQL" -ForegroundColor White
Write-Host "[*] 7. Test JSON pollution" -ForegroundColor White
Write-Host "[*] 8. Test parameter tampering" -ForegroundColor White
Write-Host "[*] 9. Test versioning" -ForegroundColor White
Write-Host "[*] 10. Test content types" -ForegroundColor White

# Save results
$resultsFile = "./bug-hunter-output/api-results.txt"
$Results | ConvertTo-Json | Set-Content $resultsFile
Write-Host "[*] Results saved to: $resultsFile" -ForegroundColor Green