#!/usr/bin/env python3
"""
CVE Report Writer - Generate CVE Report
Usage: python write_cve.py --product "nginx" --version "1.18.0" --cwe CWE-79 --score 7.5
"""

import sys
import argparse
from datetime import datetime

class CVEReportWriter:
    def __init__(self):
        self.template = """
================================================================================
                           CVE REPORT TEMPLATE
================================================================================

CVE ID: {cve_id}

Product: {product}
Vendor: {vendor}
Affected Versions: {versions}
Type: {vuln_type}

--------------------------------------------------------------------------------
DESCRIPTION
--------------------------------------------------------------------------------
{description}

--------------------------------------------------------------------------------
VULNERABILITY DETAILS
--------------------------------------------------------------------------------
{details}

--------------------------------------------------------------------------------
PROOF OF CONCEPT
--------------------------------------------------------------------------------
{poc}

--------------------------------------------------------------------------------
IMPACT
--------------------------------------------------------------------------------
{impact}

--------------------------------------------------------------------------------
REFERENCES
--------------------------------------------------------------------------------
{references}

--------------------------------------------------------------------------------
CREDITS
--------------------------------------------------------------------------------
Discovered by: {discoverer}
Date: {date}
Contact: {contact}

--------------------------------------------------------------------------------
TIMELINE
--------------------------------------------------------------------------------
Discovery Date: {discovery_date}
Vendor Notified: {vendor_notify_date}
Patch Released: {patch_date}
CVE Assigned: {cve_assign_date}
Public Disclosure: {public_date}

================================================================================
"""

    def generate(self, product, version, vuln_type, description, impact, cve_id="CVE-YYYY-NNNNN",
              vendor="Unknown", versions="All", details="", poc="", references="", 
              discoverer="", date="", contact=""):
        
        today = datetime.now().strftime('%Y-%m-%d')
        
        report = self.template.format(
            cve_id=cve_id,
            product=product,
            vendor=vendor,
            versions=versions,
            vuln_type=vuln_type,
            description=description,
            details=details or "A " + vuln_type + " vulnerability in " + product + " allows " + impact,
            impact=impact,
            poc=poc or "GET /vulnerable HTTP/1.1\nHost: target.com",
            references=references or "https://example.com/advisory",
            discoverer=discoverer or "Security Researcher",
            date=date or today,
            contact=contact or "research@example.com",
            discovery_date=date or today,
            vendor_notify_date=date or today,
            patch_date="YYYY-MM-DD",
            cve_assign_date=date or today,
            public_date="YYYY-MM-DD"
        )
        
        filename = f"CVE-{product.replace(' ', '_')}.txt"
        with open(filename, 'w') as f:
            f.write(report)
        
        print(f"[+] CVE report saved to: {filename}")
        print(f"[+] CVE ID: {cve_id}")
        
        return filename

    def generate_json(self, product, version, vuln_type, description, impact, **kwargs):
        """Generate JSON report"""
        data = {
            "cve_id": kwargs.get('cve_id', 'CVE-YYYY-NNNNN'),
            "product": product,
            "vendor": kwargs.get('vendor', 'Unknown'),
            "versions": version,
            "type": vuln_type,
            "description": description,
            "impact": impact,
            "cvss": kwargs.get('cvss', 7.5),
            "cwe": kwargs.get('cwe', 'N/A'),
            "references": kwargs.get('references', []),
            "discovered_by": kwargs.get('discoverer', 'Unknown'),
            "date": kwargs.get('date', datetime.now().strftime('%Y-%m-%d'))
        }
        
        filename = f"cve_{product.replace(' ', '_')}.json"
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"[+] JSON report saved to: {filename}")
        
        return filename


def main():
    parser = argparse.ArgumentParser(description='CVE Report Writer')
    parser.add_argument('--product', required=True, help='Product name')
    parser.add_argument('--version', default='All', help='Affected versions')
    parser.add_argument('--vendor', default='Unknown', help='Vendor name')
    parser.add_argument('--type', default='Unknown', help='Vulnerability type')
    parser.add_argument('--cwe', help='CWE ID')
    parser.add_argument('--score', type=float, default=7.5, help='CVSS score')
    parser.add_argument('--impact', required=True, help='Impact description')
    parser.add_argument('--description', help='Detailed description')
    parser.add_argument('--poc', help='Proof of concept')
    parser.add_argument('--output', default='txt', choices=['txt', 'json'], help='Output format')
    args = parser.parse_args()
    
    cve_id = f"CVE-{datetime.now().year}-NNNNN"
    print(f"""
================================================================================
                           CVE Report Generator
================================================================================

This tool generates a CVE report template.
You will need to:
 1. Verify the vulnerability
 2. Get a CVE ID from https://cveform.mitre.org
 3. Submit to vendor
 4. Wait for assignment

NOTE: CVEs must be assigned by MITRE.
================================================================================
""")
    
    writer = CVEReportWriter()
    
    if args.output == 'json':
        import json
        writer.generate_json(
            args.product,
            args.version,
            args.type,
            args.description or args.impact,
            args.impact,
            cwe=args.cwe,
            cvss=args.score,
            vendor=args.vendor
        )
    else:
        writer.generate(
            args.product,
            args.version,
            args.type,
            args.description or args.impact,
            args.impact,
            cve_id=cve_id,
            vendor=args.vendor,
            versions=args.version,
            poc=args.poc
        )


if __name__ == "__main__":
    main()