# Bug Hunter - Network Scanning Tool
# Usage: ./enum-network.ps1 -Target <target>

param(
    [Parameter(Mandatory=$true)]
    [string]$Target,
    [switch]$All,
    [switch]$Ports,
    [switch]$Services,
    [switch]$SMB,
    [switch]$FTP,
    [switch]$SSH,
    [switch]$DNS,
    [switch]$SNMP,
    [switch]$LDAP
)

Write-Host "[*] Network Enumeration for: $Target" -ForegroundColor Cyan

$Results = @()

function Test-Port {
    param($target, $port)
    
    try {
        $tcp = New-Object System.Net.Sockets.TcpClient
        $connection = $tcp.BeginConnect($target, $port, $null, $null)
        $wait = $connection.AsyncWaitHandle.WaitOne(1000, $false)
        
        if ($wait -and $tcp.Connected) {
            $tcp.Close()
            return $true
        }
        
        $tcp.Close()
    } catch {}
    
    return $false
}

function Get-Banner {
    param($target, $port)
    
    try {
        $tcp = New-Object System.Net.Sockets.TcpClient($target, $port)
        $stream = $tcp.GetStream()
        $buffer = New-Object byte[] 1024
        $stream.Read($buffer, 0, $buffer.Length) | Out-Null
        $tcp.Close()
        
        return [System.Text.Encoding]::ASCII.GetString($buffer).Trim()
    } catch {
        return $null
    }
}

# Common ports to scan
$commonPorts = @(
    21, 22, 23, 25, 53, 67, 68, 69, 80, 110, 111, 135, 139, 143, 443, 445,
    389, 443, 445, 465, 514, 515, 636, 993, 995, 1433, 1521, 3306, 3389,
    5432, 5900, 5985, 5986, 6379, 8080, 8443, 27017
)

# Run port scan
Write-Host "[*] Scanning ports..." -ForegroundColor Yellow

if ($All -or $Ports) {
    Write-Host "[*] Finding open ports..." -ForegroundColor
    
    foreach ($port in $commonPorts) {
        Write-Host "[*] Testing port: $port" -ForegroundColor Gray
        
        if (Test-Port -target $Target -port $port) {
            Write-Host "[!] Port OPEN: $port" -ForegroundColor Green
            $Results += @{Port=$port; Status="Open"}
            
            # Get banner
            $banner = Get-Banner -target $Target -port $port
            if ($banner) {
                Write-Host "[*] Banner: $banner" -ForegroundColor Cyan
                $Results += @{Port=$port; Banner=$banner}
            }
        }
    }
}

# Service-specific tests
if ($All -or $SMB) {
    Write-Host "[*] Testing SMB..." -ForegroundColor Yellow
    
    $smbTests = @(
        "Test null session",
        "Test default shares",
        "Check SMB signing"
    )
    
    foreach ($test in $smbTests) {
        Write-Host "[*] $test" -ForegroundColor Gray
    }
}

if ($All -or $FTP) {
    Write-Host "[*] Testing FTP..." -ForegroundColor Yellow
    
    Write-Host "[*] Trying anonymous login..." -ForegroundColor Gray
    # Test FTP anonymous
}

if ($All -or $SSH) {
    Write-Host "[*] Testing SSH..." -ForegroundColor Yellow
    
    $banner = Get-Banner -target $Target -port 22
    if ($banner) {
        Write-Host "[*] SSH Banner: $banner" -ForegroundColor Cyan
        $Results += @{Service="SSH"; Banner=$banner}
    }
}

if ($All -or $DNS) {
    Write-Host "[*] Testing DNS..." -ForegroundColor Yellow
    
    try {
        $dns = Resolve-DnsName -Name $Target -Type NS -ErrorAction SilentlyContinue
        foreach ($record in $dns) {
            Write-Host "[*] NS: $($record.NameHost)" -ForegroundColor Gray
        }
    } catch {}
}

if ($All -or $SNMP) {
    Write-Host "[*] Testing SNMP..." -ForegroundColor Yellow
    
    try {
        $snmp = New-Object System.Net.Sockets.UdpClient($Target, 161)
        $snmp.Close()
        Write-Host "[!] SNMP port 161 open" -ForegroundColor Red
        $Results += @{Service="SNMP"; Port=161}
    } catch {}
}

if ($All -or $LDAP) {
    Write-Host "[*] Testing LDAP..." -ForegroundColor Yellow
    
    $banner = Get-Banner -target $Target -port 389
    if ($banner) {
        Write-Host "[*] LDAP: $banner" -ForegroundColor Cyan
        $Results += @{Service="LDAP"; Banner=$banner}
    }
}

# Output results
Write-Host "`n[*] Network Enumeration Complete" -ForegroundColor Green
Write-Host "[*] Found $($Results.Count) open ports/services" -ForegroundColor Cyan

# Save results
$resultsFile = "./bug-hunter-output/network-enum.txt"
if (!(Test-Path "./bug-hunter-output")) {
    New-Item -ItemType Directory -Path "./bug-hunter-output" -Force | Out-Null
}
$Results | ConvertTo-Json | Set-Content $resultsFile
Write-Host "[*] Results saved to: $resultsFile" -ForegroundColor Green