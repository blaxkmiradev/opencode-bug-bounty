#!/usr/bin/env python3
"""
Backup File Finder
Discovers exposed backup files
"""

import requests
import argparse
import warnings
warnings.filterwarnings('ignore')

BACKUP_EXTENSIONS = [
    '.zip', '.tar', '.gz', '.rar', '.7z',
    '.bak', '.backup', '.old', '.orig',
    '.sql', '.db', '.sqlite', '.sqlite3',
    '.tar.gz', '.tgz',
]

def scan(target):
    print(f"[*] Backup File Finder - {target}")
    print("="*50)
    
    if not target.startswith(('http://', 'https://')):
        target = 'https://' + target
    
    found = []
    common_names = ['backup', 'dump', 'database', 'db', 'backup.sql', 'dump.sql']
    
    for name in common_names:
        for ext in BACKUP_EXTENSIONS[:5]:
            path = f"/{name}{ext}"
            try:
                r = requests.get(target + path, timeout=10, verify=False)
                if r.status_code == 200 and len(r.text) > 100:
                    print(f"[!] Found: {path}")
                    found.append(path)
            except:
                pass
    
    print("\n" + "="*50)
    print(f"[*] Found {len(found)} backup files")
    
    return found

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Backup Finder')
    parser.add_argument('target', help='Target URL')
    args = parser.parse_args()
    scan(args.target)