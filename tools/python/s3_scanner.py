#!/usr/bin/env python3
"""
AWS S3 Bucket Scanner
Usage: python s3_scanner.py bucket-name
"""

import sys
import requests

class S3Scanner:
    def __init__(self, bucket):
        self.bucket = bucket.lower()
        self.findings = []
        
        self.endpoints = [
            '.s3.amazonaws.com',
            '.s3.amazonaws.com/',
            '.s3-us-east-1.amazonaws.com',
            '.s3-us-west-2.amazonaws.com',
            '.s3-eu-west-1.amazonaws.com',
            '.s3.ap-southeast-1.amazonaws.com',
            '.s3.amazonaws.com/',
        ]
        
        self.paths = ['', '/', '/s3/', '/backup/', '/uploads/', '/files/', '/assets/']
    
    def check_bucket(self, endpoint, path):
        """Check if bucket exists"""
        url = f"https://{self.bucket}{endpoint}{path}"
        try:
            r = requests.get(url, timeout=5)
            if r.status_code < 400:
                return {'url': url, 'status': r.status_code, 'exists': True}
        except:
            pass
        return None
    
    def scan(self):
        """Scan for S3 buckets"""
        print(f"[*] Scanning S3 bucket: {self.bucket}...")
        
        for endpoint in self.endpoints:
            for path in self.paths:
                result = self.check_bucket(endpoint, path)
                if result:
                    print(f"[+] Found: {result['url']}")
                    self.findings.append(result)
        
        return self.findings


def main():
    if len(sys.argv) < 2:
        print("Usage: python s3_scanner.py <bucket-name>")
        print("Example: python s3_scanner.py mycompany")
        sys.exit(1)
    
    bucket = sys.argv[1]
    scanner = S3Scanner(bucket)
    scanner.scan()


if __name__ == "__main__":
    main()