#!/usr/bin/env python3
"""
Report Generator - Generate Markdown Report
Usage: python generate_csv.py --vuln XSS --target target.com --endpoint /search?q= --poc "GET /search?q=<script>alert(1)</script>"
"""

import sys
import json
import argparse
from datetime import datetime

class ReportGenerator:
    def __init__(self):
        self.template = '''---
title: '[Vuln] in [Endpoint] allows [Impact]'
created: {date}
target: {target}
vulnerability_class: {vuln}
severity: {severity}

## Summary

A {vuln} vulnerability was discovered in {endpoint} on {target}.
An attacker can {impact}.

## Steps To Reproduce

1. Navigate to {target}{endpoint}
2. Send the following request:
   ```
   {poc}
   ```

3. Observe: {response}

## Impact

An attacker can {impact}.
{quantify}

## Severity Assessment

CVSS 3.1 Score: {cvss}
- Attack Vector: Network
- Complexity: Low
- Privileges: None
- User Interaction: None
- Confidentiality: {conf}
- Integrity: {integr}
- Availability: {avail}

## Remediation

{remediation}

---

'''
        
    def generate(self, vuln, target, endpoint, poc, severity='High', impact='exploit', cvss='7.5'):
        """Generate report"""
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        cvss_map = {
            'Critical': ('High', 'High', 'High'),
            'High': ('High', 'High', 'None'),
            'Medium': ('None', 'None', 'None'),
            'Low': ('None', 'None', 'None'),
        }
        conf, integr, avail = cvss_map.get(severity, ('None', 'None', 'None'))
        
        report = self.template.format(
            date=date,
            target=target,
            vuln=vuln,
            endpoint=endpoint,
            poc=poc,
            impact=impact,
            cvss=cvss,
            severity=severity,
            conf=conf,
            integr=integr,
            avail=avail,
            quantify='This affects all users of the application.',
            response='The XSS payload executes',
            remediation='Sanitize and escape user input. Use CSP header.'
        )
        
        filename = f"report-{vuln.lower()}-{datetime.now().strftime('%Y%m%d')}.md"
        with open(filename, 'w') as f:
            f.write(report)
        
        print(f"[+] Report saved to {filename}")
        return filename


def main():
    parser = argparse.ArgumentParser(description='Bug Report Generator')
    parser.add_argument('--vuln', required=True, help='Vulnerability class')
    parser.add_argument('--target', required=True, help='Target hostname')
    parser.add_argument('--endpoint', help='Affected endpoint')
    parser.add_argument('--poc', help='Proof of Concept')
    parser.add_argument('--severity', default='High', help='Severity')
    parser.add_argument('--impact', default='exploit', help='Impact')
    parser.add_argument('--cvss', default='7.5', help='CVSS score')
    args = parser.parse_args()
    
    gen = ReportGenerator()
    gen.generate(args.vuln, args.target, args.endpoint, args.poc, args.severity, args.impact, args.cvss)


if __name__ == "__main__":
    main()