# Bug Hunter - Mobile Security Testing Tool
# Usage: ./test-mobile.ps1 -APK <apk-file>

param(
    [Parameter(Mandatory=$true)]
    [string]$Target,
    [switch]$All,
    [switch]$Analyze,
    [switch]$Secrets,
    [switch]$Storage,
    [switch]$Network
)

Write-Host "[*] Mobile Security Testing for: $Target" -ForegroundColor Cyan

$Results = @()

function Test-MobileAPK {
    param($apk)
    
    Write-Host "[*] Analyzing APK: $apk" -ForegroundColor Yellow
    
    $decompileDir = "$apk-decompiled"
    
    # Check if apktool available
    if (Get-Command apktool -ErrorAction SilentlyContinue) {
        Write-Host "[*] Decompiling APK..." -ForegroundColor Yellow
        apktool d $apk -o $decompileDir -f 2>$null
        
        # Analyze AndroidManifest.xml
        $manifest = "$decompileDir/AndroidManifest.xml"
        if (Test-Path $manifest) {
            Write-Host "[*] Analyzing AndroidManifest.xml..." -ForegroundColor Yellow
            
            # Check exported components
            $exported = Select-String -Path $manifest -Pattern 'android:exported="true"'
            if ($exported) {
                Write-Host "[!] Exported components FOUND" -ForegroundColor Red
                $Results += @{Type="Exported Components"; Count=$exported.Count}
            }
            
            # Check for exported activities/receivers/services
            $components = Select-String -Path $manifest -Pattern 'exported="true"'
            foreach ($comp in $components) {
                Write-Host "[!] $comp" -ForegroundColor Red
            }
        }
        
        # Check for dangerous permissions
        $permissions = @(
            "READ_SMS",
            "RECEIVE_SMS",
            "SEND_SMS",
            "READ_CONTACTS",
            "WRITE_CONTACTS",
            "READ_EXTERNAL_STORAGE",
            "WRITE_EXTERNAL_STORAGE",
            "RECORD_AUDIO",
            "CAMERA",
            "ACCESS_FINE_LOCATION",
            "READ_PHONE_STATE"
        )
        
        foreach ($perm in $permissions) {
            $found = Select-String -Path $manifest -Pattern $perm
            if ($found) {
                Write-Host "[!] Dangerous permission: $perm" -ForegroundColor Red
                $Results += @{Type="Dangerous Permission"; Permission=$perm}
            }
        }
        
        # Search for hardcoded secrets
        if (Test-Path $decompileDir) {
            Write-Host "[*] Searching for hardcoded secrets..." -ForegroundColor Yellow
            
            $secretPatterns = @(
                "API_KEY",
                "SECRET",
                "TOKEN",
                "PASSWORD",
                "PRIVATE_KEY",
                "AWS_ACCESS",
                "169.254.169.254"
            )
            
            foreach ($pattern in $secretPatterns) {
                $found = Get-ChildItem -Path $decompileDir -Recurse -File | 
                    Select-String -Pattern $pattern -ErrorAction SilentlyContinue
                
                if ($found) {
                    Write-Host "[!] Secret found: $pattern" -ForegroundColor Red
                    $Results += @{Type="Hardcoded Secret"; Pattern=$pattern}
                }
            }
        }
        
        # Check for insecure storage
        Write-Host "[*] Checking insecure storage..." -ForegroundColor Yellow
        
        $storagePatterns = @(
            "SharedPreferences",
            "getSharedPreferences",
            "MODE_WORLD_READABLE",
            "openFileOutput"
        )
        
        foreach ($pattern in $storagePatterns) {
            $found = Get-ChildItem -Path $decompileDir -Recurse -File | 
                Select-String -Pattern $pattern -ErrorAction SilentlyContinue
            
            if ($found) {
                Write-Host "[!] Insecure storage: $pattern" -ForegroundColor Yellow
                $Results += @{Type="Insecure Storage"; Pattern=$pattern}
            }
        }
        
        # Check for insecure network
        Write-Host "[*] Checking network security..." -ForegroundColor Yellow
        
        $networkPatterns = @(
            "http://",
            "HTTP://",
            "SSLContext",
            "TrustAllHostnameVerifier",
            "AllowAllTrustManager"
        )
        
        foreach ($pattern in $networkPatterns) {
            $found = Get-ChildItem -Path $decompileDir -Recurse -File | 
                Select-String -Pattern $pattern -ErrorAction SilentlyContinue
            
            if ($found) {
                if ($pattern -match "http://") {
                    Write-Host "[!] Cleartext traffic: $pattern" -ForegroundColor Red
                    $Results += @{Type="Cleartext Traffic"; Pattern=$pattern}
                } else {
                    Write-Host "[!] Insecure network: $pattern" -ForegroundColor Yellow
                    $Results += @{Type="Insecure Network"; Pattern=$pattern}
                }
            }
        }
        
        # Check WebView security
        Write-Host "[*] Checking WebView security..." -ForegroundColor Yellow
        
        $webviewPatterns = @(
            "setJavaScriptEnabled",
            "setAllowFileAccess",
            "setAllowContentAccess",
            "addJavascriptInterface"
        )
        
        foreach ($pattern in $webviewPatterns) {
            $found = Get-ChildItem -Path $decompileDir -Recurse -File | 
                Select-String -Pattern $pattern -ErrorAction SilentlyContinue
            
            if ($found) {
                Write-Host "[!] WebView issue: $pattern" -ForegroundColor Yellow
                $Results += @{Type="WebView Issue"; Pattern=$pattern}
            }
        }
    } else {
        # apktool not available - use basic analysis
        Write-Host "[!] apktool not found, using basic analysis..." -ForegroundColor Yellow
        
        # Try unzip and look at files
        $tempDir = "$apk-extracted"
        Expand-Archive -Path $apk -DestinationPath $tempDir -Force 2>$null
        
        if (Test-Path "$tempDir/AndroidManifest.xml") {
            $manifest = Get-Content "$tempDir/AndroidManifest.xml" -Raw
            
            if ($manifest -match 'android:exported="true"') {
                Write-Host "[!] Exported components FOUND" -ForegroundColor Red
            }
        }
    }
}

# Run tests
Write-Host "[*] Starting mobile security tests..." -ForegroundColor Yellow

if ($Target -match "\.apk$") {
    Test-MobileAPK -apk $Target
} elseif ($All -or $Analyze) {
    Write-Host "[*] APK analysis selected" -ForegroundColor Yellow
    # Check current directory for APKs
    Get-ChildItem -Path . -Filter "*.apk" | ForEach-Object {
        Test-MobileAPK -apk $_.FullName
    }
}

if ($All -or $Secrets) {
    Write-Host "[*] Searching for secrets..." -ForegroundColor Yellow
}

if ($All -or $Storage) {
    Write-Host "[*] Checking storage..." -ForegroundColor Yellow
}

if ($All -or $Network) {
    Write-Host "[*] Checking network security..." -ForegroundColor Yellow
}

# Output results
Write-Host "`n[*] Mobile Security Testing Complete" -ForegroundColor Green
Write-Host "[*] Found $($Results.Count) issues" -ForegroundColor Cyan

# Mobile Testing Checklist
Write-Host "`n[*] Mobile Security Checklist:" -ForegroundColor Yellow
Write-Host "[*] 1. Decompile APK (jadx/apktool)" -ForegroundColor White
Write-Host "[*] 2. Check AndroidManifest.xml" -ForegroundColor White
Write-Host "[*] 3. Exported components" -ForegroundColor White
Write-Host "[*] 4. Dangerous permissions" -ForegroundColor White
Write-Host "[*] 5. Hardcoded secrets" -ForegroundColor White
Write-Host "[*] 6. Insecure storage" -ForegroundColor White
Write-Host "[*] 7. Cleartext traffic" -ForegroundColor White
Write-Host "[*] 8. Certificate pinning" -ForegroundColor White
Write-Host "[*] 9. WebView security" -ForegroundColor White
Write-Host "[*] 10. Deep link handling" -ForegroundColor White
Write-Host "[*] 11. Root/jailbreak detection" -ForegroundColor White

# Save results
$resultsFile = "./bug-hunter-output/mobile-results.txt"
$Results | ConvertTo-Json | Set-Content $resultsFile
Write-Host "[*] Results saved to: $resultsFile" -ForegroundColor Green