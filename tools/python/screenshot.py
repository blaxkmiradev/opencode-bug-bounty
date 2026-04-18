#!/usr/bin/env python3
"""
Screenshot Tool (requires wkhtmltopdf or selenium)
Usage: python screenshot.py https://target.com
"""

import sys
import os

class Screenshot:
    def __init__(self, url):
        self.url = url
        
    def capture_webkit(self):
        """Capture using webkit"""
        if not os.system('which wkhtmltopdf >/dev/null 2>&1'):
            cmd = f"wkhtmltopdf {self.url} screenshot.pdf"
            os.system(cmd)
            print("[+] Screenshot saved to screenshot.pdf")
        else:
            print("[!] wkhtmltopdf not found")
    
    def capture_selenium(self):
        """Capture using selenium"""
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options
            
            opts = Options()
            opts.headless = True
            driver = webdriver.Chrome(options=opts)
            driver.get(self.url)
            
            filename = f"{self.url.replace('https://', '').replace('http://', '').split('/')[0]}.png"
            driver.save_screenshot(filename)
            print(f"[+] Screenshot saved to {filename}")
            
            driver.quit()
        except ImportError:
            print("[!] selenium not installed")
        except Exception as e:
            print(f"[!] Error: {e}")
    
    def capture(self):
        """Capture screenshot"""
        try:
            self.capture_selenium()
        except:
            try:
                self.capture_webkit()
            except:
                print("[!] No screenshot tool available")


def main():
    if len(sys.argv) < 2:
        print("Usage: python screenshot.py <url>")
        sys.exit(1)
    
    url = sys.argv[1]
    sc = Screenshot(url)
    sc.capture()


if __name__ == "__main__":
    main()