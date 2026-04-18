#!/usr/bin/env python3
"""
Bug Hunter Toolkit - Installer
Configures tools for system-wide or OpenCode usage
"""

import sys
import os
import shutil
import platform
from pathlib import Path

def get_opencode_tools_path():
    """Get OpenCode tools directory"""
    home = Path.home()
    opencode_paths = [
        home / ".opencode" / "tools",
        home / "opencode" / "tools",
        home / ".config" / "opencode" / "tools",
    ]
    for path in opencode_paths:
        if path.exists():
            return path
    return opencode_paths[0]

def install_windows():
    """Windows installation"""
    print("[*] Windows Installation")
    
    # Get paths
    script_dir = Path(__file__).parent
    opencode_tools = get_opencode_tools_path()
    
    print(f"[*] Source: {script_dir}")
    print(f"[*] Target: {opencode_tools}")
    
    # Create directories
    opencode_tools.mkdir(parents=True, exist_ok=True)
    (opencode_tools / "python").mkdir(exist_ok=True)
    (opencode_tools / "bug-hunter").mkdir(exist_ok=True)
    
    # Copy tools
    print("[*] Copying Python tools...")
    for py_file in (script_dir / "tools" / "python").glob("*.py"):
        shutil.copy2(py_file, opencode_tools / "python" / py_file.name)
        print(f"    + {py_file.name}")
    
    print("[*] Copying PowerShell tools...")
    for ps_file in (script_dir / "tools" / "bug-hunter").glob("*.ps1"):
        shutil.copy2(ps_file, opencode_tools / "bug-hunter" / ps_file.name)
        print(f"    + {ps_file.name}")
    
    # Create launcher scripts
    print("[*] Creating launchers...")
    
    # Windows batch file
    batch = opencode_tools / "bug-hunter.bat"
    with open(batch, "w") as f:
        f.write("""@echo off
:: Bug Hunter Toolkit Launcher
python "%~dp0tools\python\run.py" %*
""")
    print("    + bug-hunter.bat")
    
    print("[+] Installation complete!")
    return opencode_tools

def install_linux():
    """Linux/macOS installation"""
    print("[*] Linux/macOS Installation")
    
    script_dir = Path(__file__).parent
    opencode_tools = get_opencode_tools_path()
    
    print(f"[*] Source: {script_dir}")
    print(f"[*] Target: {opencode_tools}")
    
    # Create symlink or copy
    opencode_tools.mkdir(parents=True, exist_ok=True)
    
    if opencode_tools.exists() and opencode_tools.is_symlink():
        opencode_tools.unlink()
    
    if not opencode_tools.exists():
        os.symlink(script_dir / "tools", opencode_tools)
        print("[+] Symlink created")
    else:
        print("[*] Tools already installed")
    
    # Make launchers executable
    for launcher in ["run-scan.sh", "bug-hunter"]:
        path = script_dir / launcher
        if path.exists():
            path.chmod(0o755)
            print(f"    + {launcher}")
    
    print("[+] Installation complete!")
    return opencode_tools

def main():
    print("="*50)
    print("  Bug Hunter Toolkit - Installer")
    print("="*50)
    
    system = platform.system()
    
    if system == "Windows":
        path = install_windows()
    else:
        path = install_linux()
    
    print("\n" + "="*50)
    print("  Usage:")
    print("="*50)
    print(f"python {path}/python/full_scan.py target.com")
    print(f"python {path}/python/rce_scanner.py target.com")
    print(f"python {path}/python/waf_detector.py target.com")
    print("\nOr use launchers:")
    print(f"./bug-hunter full target.com")
    print(f"./bug-hunter xss target.com")

if __name__ == "__main__":
    main()