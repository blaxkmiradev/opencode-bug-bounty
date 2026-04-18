# Bug Hunter - Report Generation Tool
# Usage: ./report.ps1 -Target <target> -VulnClass <class> -Endpoint <endpoint> -Impact <impact>

param(
    [Parameter(Mandatory=$true)]
    [string]$Target,
    [Parameter(Mandatory=$true)]
    [string]$VulnClass,
    [string]$Endpoint = "/",
    [string]$Impact = "data breach",
    [string]$Severity = "High",
    [string]$OutputDir = "./bug-hunter-output"
)

Write-Host "[*] Generating bug bounty report..." -ForegroundColor Cyan

$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

# CVSS Calculator
function Get-CVSS {
    param($vulnClass, $impact)
    
    $cvssScores = @{
        "IDOR-read" = @{Score=6.5; Severity="Medium"}
        "IDOR-write" = @{Score=7.5; Severity="High"}
        "XSS-stored" = @{Score=8.1; Severity="High"}
        "XSS-reflected" = @{Score=6.1; Severity="Medium"}
        "SQLi" = @{Score=8.6; Severity="High"}
        "SSRF-cloud" = @{Score=9.1; Severity="Critical"}
        "SSRF-internal" = @{Score=7.5; Severity="High"}
        "Auth-bypass" = @{Score=9.8; Severity="Critical"}
        "SSTI" = @{Score=9.0; Severity="Critical"}
        "Race-condition" = @{Score=7.5; Severity="High"}
        "ATO" = @{Score=9.8; Severity="Critical"}
    }
    
    if ($cvssScores.ContainsKey($vulnClass.ToLower())) {
        return $cvssScores[$vulnClass.ToLower()]
    }
    
    return @{Score=5.0; Severity="Medium"}
}

$cvss = Get-CVSS -vulnClass $VulnClass -impact $Impact

# Report Template
$report = @"
---
title: '$VulnClass in $Endpoint allows attacker to $Impact'
created: $timestamp
target: $Target
vulnerability_class: $VulnClass
severity: $Severity

## Summary

A $VulnClass vulnerability was discovered in $Endpoint on $Target. 
An attacker can $Impact through this vulnerability.

## Steps To Reproduce

1. Navigate to $Target$Endpoint
2. Send the following request:
   ````
   $(
    if ($VulnClass -eq "IDOR") {
        "GET $Endpoint/1 HTTP/1.1
Host: $Target
Authorization: Bearer [TOKEN]"
    } elseif ($VulnClass -eq "XSS") {
        "GET $Endpoint?q=<script>alert(1)</script> HTTP/1.1
Host: $Target"
    } elseif ($VulnClass -eq "SQLi") {
        "GET $Endpoint?id=' OR '1'='1 HTTP/1.1
Host: $Target"
    } else {
        "GET $Endpoint HTTP/1.1
Host: $Target"
    }
   )
   ````

3. Observe the vulnerable response

## Impact

An attacker can $Impact.
This affects all users who $(
    if ($VulnClass -eq "IDOR") { "access the application" }
    elseif ($VulnClass -eq "XSS") { "visit the affected page" }
    elseif ($VulnClass -eq "SQLi") { "use the affected parameter" }
    else { "use the affected feature" }
).

## Severity Assessment

CVSS 3.1 Score: $($cvss.Score) ($($cvss.Severity))
- Attack Vector: Network
- Complexity: Low
- Privileges: None
- User Interaction: None
- Confidentiality: High
- Integrity: High
- Availability: High

## Remediation

$(
    switch ($VulnClass) {
        "IDOR" { "Implement proper authorization checks on all endpoints. Validate user ownership of requested resources." }
        "XSS" { "Sanitize and escape user input before rendering. Use Content Security Policy (CSP)." }
        "SQLi" { "Use parameterized queries (prepared statements). Validate and sanitize all user input." }
        "SSRF" { "Validate and sanitize all URLs. Block internal IP ranges." }
        "Auth-bypass" { "Implement proper authentication and authorization on all endpoints." }
        default { "Implement proper input validation and output encoding." }
    }
)

---

"@

# Save report
if (!(Test-Path $OutputDir)) {
    New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null
}

$reportFile = "$OutputDir/report-$($VulnClass.ToLower())-$(Get-Date -Format 'yyyyMMdd-HHmmss').md"

$report | Out-File -FilePath $reportFile -Encoding UTF8

Write-Host "[+] Report generated: $reportFile" -ForegroundColor Green
Write-Host "[+] Vuln Class: $VulnClass" -ForegroundColor Cyan
Write-Host "[+] Severity: $($cvss.Severity) (CVSS: $($cvss.Score))" -ForegroundColor Cyan

return $reportFile