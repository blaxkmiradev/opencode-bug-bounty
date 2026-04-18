@echo off
:: Bug Hunter Toolkit - Main Launcher (Windows)
:: Save as bug-hunter.bat in PATH

setlocal enabledelayedexpansion

:: Get script path
set "SCRIPT_DIR=%~dp0"
set "TOOLS_DIR=%SCRIPT_DIR%tools\python"

if "%1"=="" (
    goto help
)

set "TOOL=%1"
set "TARGET=%2"

:: Map aliases
if "%TOOL%"=="full" set TOOL=full_scan.py
if "%TOOL%"=="quick" set TOOL=fast_scanner.py
if "%TOOL%"=="pro" set TOOL=pro_scanner.py
if "%TOOL%"=="scan" set TOOL=full_scan.py
if "%TOOL%"=="list" goto list
if "%TOOL%"=="-h" goto help
if "%TOOL%"=="--help" goto help

if not exist "%TOOLS_DIR%\%TOOL%" (
    if not exist "%TOOLS_DIR%\%TOOL%.py" (
        echo [!] Tool not found: %TOOL%
        exit /b 1
    )
)

echo ========================================
echo   Bug Hunter Toolkit
echo   Tool: %TOOL%  Target: %TARGET%
echo ========================================

python "%TOOLS_DIR%\%TOOL%.py" %TARGET%

exit /b 0

:help
echo ========================================
echo   Bug Hunter Toolkit - Help
echo ========================================
echo.
echo Usage: bug-hunter [tool] [target]
echo.
echo Tools:
echo   full      - Full security scan
echo   quick     - Quick scan
echo   pro       - Professional scan
echo   xss       - XSS scanner
echo   sqli      - SQLi scanner
echo   rce       - RCE scanner
echo   ssrf      - SSRF scanner
echo   lfi       - LFI scanner
echo   xxe       - XXE scanner
echo   idor      - IDOR scanner
echo   ssti      - SSTI scanner
echo   waf       - WAF detector
echo   headers   - Security headers
echo   wp        - WordPress scanner
echo   subdomain - Subdomain enum
echo   git       - Git scanner
echo   backup    - Backup finder
echo   waf       - WAF detector
echo   cors      - CORS scanner
echo   jwt       - JWT analyzer
echo   sensitive - Sensitive data
echo.
echo Examples:
echo   bug-hunter full target.com
echo   bug-hunter xss https://target.com
echo   bug-hunter waf target.com
echo   bug-hunter subdomain target.com
exit /b 0

:list
echo ========================================
echo   Available Tools
echo ========================================
echo.
for %%f in (%TOOLS_DIR%\*.py) do (
    echo   %%~nf
)
exit /b 0