#!/usr/bin/env python3
"""
Android APK Analyzer
Basic APK analysis for common issues
"""

import zipfile
import os
import re
import argparse

DANGEROUS_PERMISSIONS = [
    'android.permission.READ_SMS',
    'android.permission.SEND_SMS',
    'android.permission.RECEIVE_SMS',
    'android.permission.READ_CONTACTS',
    'android.permission.WRITE_CONTACTS',
    'android.permission.CAMERA',
    'android.permission.RECORD_AUDIO',
    'android.permission.ACCESS_FINE_LOCATION',
    'android.permission.READ_PHONE_STATE',
    'android.permission.CALL_PHONE',
]

def analyze_apk(apk_path):
    print(f"[*] Android APK Analyzer - {apk_path}")
    print("="*50)
    
    found = []
    
    try:
        with zipfile.ZipFile(apk_path, 'r') as z:
            manifest = z.read('AndroidManifest.xml')
            
            for perm in DANGEROUS_PERMISSIONS:
                if perm.encode() in manifest:
                    print(f"[!] Dangerous permission: {perm}")
                    found.append(perm)
            
            files = z.namelist()
            print(f"[*] Files in APK: {len(files)}")
            
            for f in files:
                if '.so' in f:
                    print(f"    Native lib: {f}")
                if 'Certificate' in f or 'KeyStore' in f:
                    print(f"    [!] Crypto file: {f}")
    
    except Exception as e:
        print(f"[!] Error: {e}")
    
    print("\n" + "="*50)
    print(f"[*] Found {len(found)} dangerous permissions")
    
    return found

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='APK Analyzer')
    parser.add_argument('apk', help='APK file path')
    args = parser.parse_args()
    analyze_apk(args.apk)