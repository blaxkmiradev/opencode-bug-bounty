@echo off
:: Bug Hunter Toolkit - Windows Setup
:: Run as Administrator

echo ========================================
echo   Bug Hunter Toolkit - Setup (Windows)
echo ========================================
echo.

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [!] Python not found! Please install Python 3.8+
    pause
    exit /b 1
)

echo [+] Python found

:: Create symbolic link for OpenCode
set OPENCODE_PATH=%USERPROFILE%\.opencode\tools
set BUGHUNTER_PATH=%~dp0

if not exist "%OPENCODE_PATH%" (
    mklink /D "%OPENCODE_PATH%" "%BUGHUNTER_PATH%" >nul 2>&1
    if errorlevel 1 (
        echo [*] Copying tools to OpenCode folder...
        xcopy "%BUGHUNTER_PATH%" "%OPENCODE_PATH%" /E /I /Y >nul
    )
)

echo [+] Tools linked to: %OPENCODE_PATH%

:: Add to PATH (session)
setx PATH "%OPENCODE_PATH%\tools\python;%OPENCODE_PATH%\tools\bug-hunter;%PATH%" >nul 2>&1

echo [+] PATH updated

:: Test tools
echo.
echo ========================================
echo   Testing Tools...
echo ========================================
python "%BUGHUNTER_PATH%\tools\python\full_scan.py" --help >nul 2>&1
if errorlevel 1 (
    echo [!] Tool test failed
) else (
    echo [+] All tools ready!
)

echo.
echo ========================================
echo   Usage Examples:
echo ========================================
echo python tools\python\full_scan.py target.com
echo python tools\python\rce_scanner.py target.com
echo python tools\python\ssrf_scanner.py https://target.com
echo.
pause