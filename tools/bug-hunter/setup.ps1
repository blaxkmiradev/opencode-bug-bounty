# Bug Hunter - Setup Script
# Installs all required tools for bug bounty hunting

param(
    [switch]$Tools,
    [switch]$All,
    [switch]$Update
)

Write-Host "[*] Bug Hunter Toolkit Setup" -ForegroundColor Cyan
Write-Host "[*] =============================" -ForegroundColor Cyan

$installDir = "$PSScriptRoot"
$binDir = "$installDir/bin"
$wordlistsDir = "$installDir/wordlists"

# Create directories
Write-Host "[*] Creating directories..." -ForegroundColor Yellow
New-Item -ItemType Directory -Path $binDir -Force -ErrorAction SilentlyContinue | Out-Null
New-Item -ItemType Directory -Path $wordlistsDir -Force -ErrorAction SilentlyContinue | Out-Null
New-Item -ItemType Directory -Path "$installDir/output" -Force -ErrorAction SilentlyContinue | Out-Null

# Install Go tools
if ($Tools -or $All) {
    Write-Host "[*] Installing Go tools..." -ForegroundColor Yellow
    
    $goTools = @(
        "github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest",
        "github.com/projectdiscovery/httpx/cmd/httpx@latest",
        "github.com/projectdiscovery/dnsx/cmd/dnsx@latest",
        "github.com/projectdiscovery/nuclei/cmd/nuclei@latest",
        "github.com/projectdiscovery/katana/cmd/katana@latest",
        "github.com/dw1zard/dalfox/v2/cmd/dalfox@latest",
        "github.com/ffuf/ffuf@latest",
        "github.com/tomnomnom/gf@latest",
        "github.com/tomnomnom/assetfinder@latest",
        "github.com/tomnomnom/waybackurls@latest",
        "github.com/tomnomnom/anew@latest",
        "github.com/projectdiscovery/interactsh/cmd/interactsh-client@latest"
    )
    
    foreach ($tool in $goTools) {
        Write-Host "[*] Installing: $tool" -ForegroundColor Gray
        go install $tool 2>$null
    }
}

# Install Python tools
if ($Tools -or $All) {
    Write-Host "[*] Installing Python tools..." -ForegroundColor Yellow
    
    $pythonTools = @(
        "semgrep",
        "arjun",
        "paramspider",
        " XSStrike",
        "sqlmap",
        "secretfinder"
    )
    
    foreach ($tool in $pythonTools) {
        Write-Host "[*] Installing: $tool" -ForegroundColor Gray
        pip install $tool 2>$null
    }
}

# Download wordlists
if ($Tools -or $All) {
    Write-Host "[*] Downloading wordlists..." -ForegroundColor Yellow
    
    $wordlists = @(
        "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/burp-parameter-names.txt",
        "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/api/api-endpoints.txt",
        "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/DNS/subdomains-top1million-5000.txt",
        "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Injection/SQLi.txt"
    )
    
    foreach ($url in $wordlists) {
        $filename = Split-Path $url -Leaf
        Write-Host "[*] Downloading: $filename" -ForegroundColor Gray
        try {
            Invoke-WebRequest -Uri $url -OutFile "$wordlistsDir/$filename" -ErrorAction Stop
        } catch {
            Write-Host "[!] Failed to download: $filename" -ForegroundColor Red
        }
    }
}

# Download Nuclei templates
if ($Tools -or $All) {
    Write-Host "[*] Downloading Nuclei templates..." -ForegroundColor Yellow
    
    $nucleiDir = "$binDir/nuclei-templates"
    New-Item -ItemType Directory -Path $nucleiDir -Force -ErrorAction SilentlyContinue | Out-Null
    
    if (Get-Command nuclei -ErrorAction SilentlyContinue) {
        nuclei -update-templates 2>$null
    }
}

# Create PATH helper
$pathFile = "$installDir/path-helper.ps1"
$pathContent = @"
# Bug Hunter PATH Helper
`$env:PATH = `"$binDir;`$env:PATH`"

# Add current directory to PATH
`$env:PATH = """$installDir/tools;$binDir;""" + `$env:PATH
"@

$pathContent | Out-File -FilePath $pathFile -Encoding UTF8

Write-Host "[*] Setup complete!" -ForegroundColor Green
Write-Host "[*] " -ForegroundColor Green
Write-Host "[*] Usage: " -ForegroundColor Cyan
Write-Host "[*]   ./tools/recon.ps1 -Target example.com" -ForegroundColor White
Write-Host "[*]   ./tools/scan.ps1 -Target https://example.com -Type xss" -ForegroundColor White
Write-Host "[*]   ./tools/test-idor.ps1 -Target https://api.example.com" -ForegroundColor White
Write-Host "[*] " -ForegroundColor Green