@echo off
:: Quick Scanner Launcher for Windows
:: Usage: run-scan.bat <tool> <target>

if "%1"=="" (
    echo Bug Hunter Toolkit Launcher
    echo.
    echo Usage: run-scan.bat [tool] [target]
    echo.
    echo Tools:
    echo   full    - Full security scan
    echo   quick   - Quick scan
    echo   rce     - RCE scanner
    echo   ssrf    - SSRF scanner
    echo   xss     - XSS scanner
    echo   sqli    - SQLi scanner
    echo   web     - Web scanner
    echo   wp      - WordPress scanner
    echo   waf     - WAF detector
    echo   headers - Security headers
    echo.
    echo Examples:
    echo   run-scan.bat full target.com
    echo   run-scan.bat xss https://target.com
    exit /b 1
)

set TOOL=%1
set TARGET=%2

if "%TARGET%"=="" set TARGET=%COMPUTERNAME%

echo [Running %TOOL% on %TARGET%]...

python "%~dp0tools\python\%TOOL%_scanner.py" %TARGET%
if errorlevel 1 (
    python "%~dp0tools\python\%TOOL%.py" %TARGET%
)

pause