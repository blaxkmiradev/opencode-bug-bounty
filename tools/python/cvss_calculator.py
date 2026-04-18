#!/usr/bin/env python3
"""
CVSS 3.1 Calculator
Usage: python cvss.py
Interactive mode or specify metrics
"""

import sys

class CVSSCalculator:
    def __init__(self):
        self.metrics = {
            'AV': {'N': 0.85, 'A': 0.62, 'L': 0.55, 'P': 0.20},
            'AC': {'L': 0.77, 'H': 0.44},
            'PR': {'N': 0.85, 'L': 0.62, 'H': 0.27},
            'UI': {'N': 0.85, 'R': 0.62},
            'S':  {'U': 6.42, 'C': 7.52},
            'C':  {'N': 0, 'L': 0.22, 'H': 0.56},
            'I':  {'N': 0, 'L': 0.22, 'H': 0.56},
            'A':  {'N': 0, 'L': 0.22, 'H': 0.56},
        }
        
    def calculate(self, AV='N', AC='L', PR='N', UI='N', S='U', C='N', I='N', A='N'):
        """Calculate CVSS score"""
        # Base score
        impact = self.metrics['S'][S] * (
            (1 - ((1 - self.metrics['C'][C]) * 
                  (1 - self.metrics['I'][I]) * 
                  (1 - self.metrics['A'][A]))
        )
        
        exploitability = 8.22 * self.metrics['AV'][AV] * self.metrics['AC'][AC] * self.metrics['PR'][PR] * self.metrics['UI'][UI]
        
        if impact <= 0:
            base_score = 0
        elif S == 'U':
            base_score = min(impact, 6.42) * exploitability / 6.42
        else:
            base_score = min((impact + impact * 0.62), 10) * exploitability / 6.42
        
        return round(base_score, 1)
    
    def get_severity(self, score):
        """Get severity label"""
        if score >= 9.0:
            return 'CRITICAL'
        elif score >= 7.0:
            return 'HIGH'
        elif score >= 4.0:
            return 'MEDIUM'
        elif score > 0:
            return 'LOW'
        else:
            return 'NONE'
    
    def quick_scores(self):
        """Generate common CVSS scores"""
        scores = [
            ('IDOR read PII', 'N', 'L', 'L', 'N', 'U', 'H', 'N', 'N'),
            ('IDOR write', 'N', 'L', 'L', 'N', 'U', 'H', 'H', 'N'),
            ('Auth bypass admin', 'N', 'L', 'N', 'N', 'C', 'H', 'H', 'H'),
            ('Stored XSS', 'N', 'L', 'N', 'N', 'U', 'N', 'M', 'N'),
            ('SQLi', 'N', 'L', 'L', 'N', 'U', 'H', 'N', 'N'),
            ('SSRF cloud', 'N', 'L', 'N', 'N', 'C', 'H', 'N', 'N'),
            ('Open redirect', 'N', 'L', 'N', 'N', 'U', 'N', 'N', 'N'),
            ('Self-XSS', 'N', 'L', 'N', 'R', 'U', 'N', 'N', 'N'),
        ]
        
        print("\n" + "="*60)
        print("Common CVSS Scores")
        print("="*60)
        print(f"{'Vulnerability':<25} {'Score':<8} {'Severity'}")
        print("-"*60)
        
        for vuln, AV, AC, PR, UI, S, C, I, A in scores:
            score = self.calculate(AV, AC, PR, UI, S, C, I, A)
            severity = self.get_severity(score)
            print(f"{vuln:<25} {score:<8} {severity}")


def main():
    cvss = CVSSCalculator()
    
    if len(sys.argv) < 2:
        print("CVSS 3.1 Calculator")
        print("="*40)
        cvss.quick_scores()
        
        print("\n\nUsage:")
        print("  python cvss.py                          -- Show common scores")
        print("  python cvss.py N L N N U H N N           -- Calculate specific")
        
        print("\n\nMetrics:")
        print("  AV: N (Network), A (Adjacent), L (Local), P (Physical)")
        print("  AC: L (Low), H (High)")
        print("  PR: N (None), L (Low), H (High)")
        print("  UI: N (None), R (Required)")
        print("  S:  U (Unchanged), C (Changed)")
        print("  C/I/A: N (None), L (Low), H (High)")
        sys.exit(1)
    
    if len(sys.argv) >= 9:
        AV, AC, PR, UI, S, C, I, A = sys.argv[1:]
        score = cvss.calculate(AV, AC, PR, UI, S, C, I, A)
        severity = cvss.get_severity(score)
        print(f"\nCVSS Score: {score}")
        print(f"Severity: {severity}")
    else:
        cvss.quick_scores()


if __name__ == "__main__":
    main()