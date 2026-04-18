# Bug Hunter - Recon Tool
# Usage: ./recon.ps1 -Target <domain>

param(
    [Parameter(Mandatory=$true)]
    [string]$Target,
    [string]$OutputDir = "./bug-hunter-output"
)

$ErrorActionPreference = "Stop"

Write-Host "[*] Starting recon for: $Target" -ForegroundColor Cyan

# Create output directory
if (!(Test-Path $OutputDir)) {
    New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null
}

$subsFile = "$OutputDir/subs.txt"
$liveFile = "$OutputDir/live.txt"
$urlsFile = "$OutputDir/urls.txt"

# Step 1: Subdomain enumeration
Write-Host "[*] Step 1: Subdomain enumeration..." -ForegroundColor Yellow

if (Get-Command subfinder -ErrorAction SilentlyContinue) {
    subfinder -d $Target -silent | Sort -Unique | Set-Content $subsFile
    Write-Host "[+] Found $( (Get-Content $subsFile | Measure-Object).Count subdomains"
} else {
    Write-Host "[!] subfinder not found, skipping..." -ForegroundColor Red
}

if (Get-Command assetfinder -ErrorAction SilentlyContinue) {
    assetfinder --subs-only $Target | Sort -Unique | Add-Content $subsFile
}

# Step 2: Live host detection
Write-Host "[*] Step 2: Detecting live hosts..." -ForegroundColor Yellow

if (Get-Command httpx -ErrorAction SilentlyContinue) {
    if (Test-Path $subsFile) {
        Get-Content $subsFile | httpx -silent -status-code -title -tech-detect -o $liveFile
        Write-Host "[+] Found $( (Get-Content $liveFile | Measure-Object).Count live hosts"
    }
} else {
    Write-Host "[!] httpx not found..." -ForegroundColor Red
}

# Step 3: URL collection
Write-Host "[*] Step 3: Collecting URLs..." -ForegroundColor Yellow

if (Get-Command katana -ErrorAction SilentlyContinue) {
    if (Test-Path $liveFile) {
        Get-Content $liveFile | ForEach-Object { ($_ -split ' ')[0] } | katana -d 3 -silent | Sort -Unique | Set-Content $urlsFile
    }
}

# Step 4: Nuclei scan
Write-Host "[*] Step 4: Running Nuclei scan..." -ForegroundColor Yellow

if (Get-Command nuclei -ErrorAction SilentlyContinue) {
    if (Test-Path $liveFile) {
        $nucleiFile = "$OutputDir/nuclei.txt"
        nuclei -l $liveFile -severity critical,high,medium -silent -o $nucleiFile
        Write-Host "[+] Nuclei scan complete"
    }
}

Write-Host "[*] Recon complete! Results in: $OutputDir" -ForegroundColor Green
Write-Host "[*] Files: subs.txt, live.txt, urls.txt, nuclei.txt" -ForegroundColor Cyan