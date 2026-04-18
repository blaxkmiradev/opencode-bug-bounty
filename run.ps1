# Bug Hunter - Master Launcher
# Unified interface for all bug bounty operations

param(
    [Parameter(Mandatory=$false)]
    [string]$Command = "help",
    
    [string]$Target,
    [string]$Type,
    [string]$Param,
    [string]$Endpoint,
    [string]$VulnClass,
    [string]$Impact,
    [string]$Severity,
    [switch]$All,
    [switch]$Verbose
)

$ErrorActionPreference = "Continue"

$toolsDir = Split-Path -Parent $PSCommandPath
$outputDir = "$toolsDir/output"

# Colors
function Write-BugHunterOutput {
    param([string]$Message, [string]$Color = "White")
    Write-Host $Message -ForegroundColor $Color
}

# Main menu
function Show-Help {
    Write-BugHunterOutput "`n========================================" -Color Cyan
    Write-BugHunterOutput "    BUG HUNTER - Master Launcher" -Color Cyan
    Write-BugHunterOutput "========================================`n" -Color Cyan
    
    Write-BugHunterOutput "Usage: .\run.ps1 <command> [options]`n" -Color White
    
    Write-BugHunterOutput "RECON COMMANDS:" -Color Yellow
    Write-BugHunterOutput "  recon <target>           - Full recon on target" -Color White
    Write-BugHunterOutput "  subdomains <target>      - Enumerate subdomains" -Color White
    Write-BugHunterOutput "  live <target>         - Find live hosts" -Color White
    Write-BugHunterOutput "  urls <target>         - Collect URLs" -Color White
    
    Write-BugHunterOutput "`nSCAN COMMANDS:" -Color Yellow
    Write-BugHunterOutput "  scan <target>           - Full vulnerability scan" -Color White
    Write-BugHunterOutput "  scan <target> -type xss - XSS scan" -Color White
    Write-BugHunterOutput "  scan <target> -type sqli - SQLi scan" -Color White
    Write-BugHunterOutput "  scan <target> -type ssrf - SSRF scan" -Color White
    Write-BugHunterOutput "  scan <target> -type nuclei - Nuclei scan" -Color White
    
    Write-BugHunterOutput "`nTEST COMMANDS:" -Color Yellow
    Write-BugHunterOutput "  test idor <target>    - Test IDOR" -Color White
    Write-BugHunterOutput "  test ssrf <target>   - Test SSRF" -Color White
    Write-BugHunterOutput "  test xss <target>    - Test XSS" -Color White
    Write-BugHunterOutput "  test sqli <target>    - Test SQLi" -Color White
    Write-BugHunterOutput "  test ssti <target>   - Test SSTI" -Color White
    Write-BugHunterOutput "  test ai <target>     - Test AI/LLM" -Color White
    
    Write-BugHunterOutput "`nCHAIN COMMANDS:" -Color Yellow
    Write-BugHunterOutput "  chain                 - Bug chaining" -Color White
    Write-BugHunterOutput "  chain <finding>       - Chain specific finding" -Color White
    
    Write-BugHunterOutput "`nREPORT COMMANDS:" -Color Yellow
    Write-BugHunterOutput "  report <target> <vuln> - Generate report" -Color White
    
    Write-BugHunterOutput "`nOTHER COMMANDS:" -Color Yellow
    Write-BugHunterOutput "  setup                 - Install tools" -Color White
    Write-BugHunterOutput "  clean                 - Clean output" -Color White
    Write-BugHunterOutput "  results              - View results" -Color White
    Write-BugHunterOutput "  help                - Show this help" -Color White
    
    Write-BugHunterOutput "`nSPECIALIZED COMMANDS:" -Color Yellow
    Write-BugHunterOutput "  test oauth <url>          - OAuth/OIDC testing" -Color White
    Write-BugHunterOutput "  test api <url>            - API security testing" -Color White
    Write-BugHunterOutput "  test mobile <apk>        - Mobile app testing" -Color White
    Write-BugHunterOutput "  enum network <target>    - Network enumeration" -Color White
    Write-BugHunterOutput "  chain                     - Bug chaining" -Color White
    
    Write-BugHunterOutput "`nSKILLS:" -Color Yellow
    Write-BugHunterOutput "  bug-bounty       - Bug bounty hunting" -Color White
    Write-BugHunterOutput "  web-audit        - Web application audit" -Color White
    Write-BugHunterOutput "  mobile-security - Android/iOS security" -Color White
    Write-BugHunterOutput "  cloud-security  - AWS/GCP/Azure/K8s" -Color White
    Write-BugHunterOutput "  network-security - Network pentesting" -Color White
    Write-BugHunterOutput "  red-team        - Red teaming" -Color White
    
    Write-BugHunterOutput "`nEXAMPLES:" -Color Yellow
    Write-BugHunterOutput '  .\run.ps1 recon example.com' -Color Gray
    Write-BugHunterOutput '  .\run.ps1 scan example.com -type xss' -Color Gray
    Write-BugHunterOutput '  .\run.ps1 test xss https://example.com/search?q=test' -Color Gray
    Write-BugHunterOutput '  .\run.ps1 test api https://api.example.com' -Color Gray
    Write-BugHunterOutput '  .\run.ps1 test oauth https://example.com/oauth/authorize' -Color Gray
    Write-BugHunterOutput '  .\run.ps1 test mobile app.apk' -Color Gray
    Write-BugHunterOutput '  .\run.ps1 report example.com IDOR /api/users "read all user data"' -Color Gray
    Write-BugHunterOutput "`n" -Color Cyan
}

# Create output directory
if (!(Test-Path $outputDir)) {
    New-Item -ItemType Directory -Path $outputDir -Force | Out-Null
}

# Parse command
$cmd = $Command.ToLower()
$scriptDir = Split-Path -Parent $PSCommandPath

# Execute command
switch -regex ($cmd) {
    "^recon$|^subdomains$|^live$|^urls$" {
        if (-not $Target) {
            Write-BugHunterOutput "[!] Target required" -Color Red
            exit 1
        }
        
        Write-BugHunterOutput "[*] Running recon on: $Target" -Color Cyan
        
        if ($cmd -eq "recon" -or $cmd -eq "subdomains") {
            & "$scriptDir\tools\bug-hunter\recon.ps1" -Target $Target -OutputDir $outputDir
        }
    }
    
    "^scan$" {
        if (-not $Target) {
            Write-BugHunterOutput "[!] Target required" -Color Red
            exit 1
        }
        
        $scanType = if ($Type) { $Type } else { "all" }
        Write-BugHunterOutput "[*] Running $scanType scan on: $Target" -Color Cyan
        
        & "$scriptDir\tools\bug-hunter\scan.ps1" -Target $Target -Type $scanType -OutputDir $outputDir
    }
    
"^test\s+(.*)$" {
        $testType = $matches[1]
        
        if (-not $Target) {
            Write-BugHunterOutput "[!] Target required" -Color Red
            exit 1
        }
        
        Write-BugHunterOutput "[*] Running $testType test on: $Target" -ForegroundColor Cyan
        
        switch ($testType) {
            "idor" {
                & "$scriptDir\tools\bug-hunter\test-idor.ps1" -Target $Target
            }
            "ssrf" {
                & "$scriptDir\tools\bug-hunter\test-ssrf.ps1" -Target $Target -All
            }
            "xss" {
                & "$scriptDir\tools\bug-hunter\test-xss.ps1" -Target $Target -Param ($Param -or "q") -All
            }
            "sqli" {
                & "$scriptDir\tools\bug-hunter\test-sqli.ps1" -Target $Target -Param ($Param -or "id") -All
            }
            "ssti" {
                & "$scriptDir\tools\bug-hunter\test-ssti.ps1" -Target $Target -Param ($Param -or "input") -All
            }
            "ai" {
                & "$scriptDir\tools\bug-hunter\test-ai.ps1" -Target $Target -All
            }
            "oauth" {
                & "$scriptDir\tools\bug-hunter\test-oauth.ps1" -Target $Target -All
            }
            "api" {
                & "$scriptDir\tools\bug-hunter\test-api.ps1" -Target $Target -All
            }
            "mobile" {
                & "$scriptDir\tools\bug-hunter\test-mobile.ps1" -Target $Target -All
            }
            "network" {
                & "$scriptDir\tools\bug-hunter\enum-network.ps1" -Target $Target -All
            }
            default {
                Write-BugHunterOutput "[!] Unknown test type: $testType" -Color Red
                Write-BugHunterOutput "[*] Available: idor, ssrf, xss, sqli, ssti, ai, oauth, api, mobile" -Color Yellow
            }
        }
    }
        
        Write-BugHunterOutput "[*] Running $testType test on: $Target" -Color Cyan
        
        switch ($testType) {
            "idor" {
                & "$scriptDir\tools\bug-hunter\test-idor.ps1" -Target $Target
            }
            "ssrf" {
                & "$scriptDir\tools\bug-hunter\test-ssrf.ps1" -Target $Target -All
            }
            "xss" {
                & "$scriptDir\tools\bug-hunter\test-xss.ps1" -Target $Target -Param ($Param -or "q") -All
            }
            "sqli" {
                & "$scriptDir\tools\bug-hunter\test-sqli.ps1" -Target $Target -Param ($Param -or "id") -All
            }
            "ssti" {
                & "$scriptDir\tools\bug-hunter\test-ssti.ps1" -Target $Target -Param ($Param -or "input") -All
            }
            "ai" {
                & "$scriptDir\tools\bug-hunter\test-ai.ps1" -Target $Target -All
            }
            default {
                Write-BugHunterOutput "[!] Unknown test type: $testType" -Color Red
                Write-BugHunterOutput "[*] Available: idor, ssrf, xss, sqli, ssti, ai" -Color Yellow
            }
        }
    }
    
    "^chain$" {
        & "$scriptDir\tools\bug-hunter\chain.ps1" -OutputDir $outputDir
    }
    
    "^report$" {
        if (-not $Target -or -not $VulnClass) {
            Write-BugHunterOutput "[!] Target and VulnClass required" -Color Red
            Write-BugHunterOutput "[*] Usage: .\run.ps1 report <target> <vulnclass> [endpoint] [impact]" -Color Yellow
            exit 1
        }
        
        & "$scriptDir\tools\bug-hunter\report.ps1" -Target $Target -VulnClass $VulnClass -Endpoint ($Endpoint -or "/") -Impact ($Impact -or "exploit") -OutputDir $outputDir
    }
    
    "^setup$" {
        & "$scriptDir\tools\bug-hunter\setup.ps1" -All
    }
    
    "^results$" {
        Write-BugHunterOutput "[*] Results in: $outputDir" -Color Cyan
        Get-ChildItem -Path $outputDir | Format-Table Name, Length, LastWriteTime
    }
    
    "^clean$" {
        Write-BugHunterOutput "[*] Cleaning output directory..." -Color Yellow
        Remove-Item -Path "$outputDir\*" -Recurse -Force -ErrorAction SilentlyContinue
        Write-BugHunterOutput "[*] Clean complete" -Color Green
    }
    
    "^help$|default" {
        Show-Help
    }
}

Write-BugHunterOutput "`n[*] Done!" -Color Green