#!/usr/bin/env python3
"""
Directory and File Scanner
Usage: python dir_scanner.py https://target.com
"""

import sys
import requests
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed

class DirScanner:
    def __init__(self, target):
        self.target = target.rstrip('/')
        self.found = []
        
        # Basic wordlist
        self.wordlist = [
            'admin', 'login', 'dashboard', 'admin.php', 'login.php', 'admin.html',
            'wp-admin', 'administrator', 'config', 'configuration', 'config.php',
            'settings', 'setup', 'upload', 'uploads', 'file', 'files',
            'images', 'image', 'img', 'css', 'js', 'javascript',
            'api', 'v1', 'v2', 'v3', 'rest', 'graphql',
            'backup', 'backups', 'backup.zip', 'backup.tar', 'backup.gz',
            'old', 'new', 'dev', 'test', 'staging', 'beta',
            '~', '~', '.bak', '.old', '.tar', '.gz',
            '.git', '.svn', '.hg', '.DS_Store', '.env',
            'phpinfo', 'info', 'server-status', 'server-info',
            'control', 'panel', 'cpanel', 'whm', 'webmail',
            'phpmyadmin', 'pma', 'myadmin', 'mysql', 'database',
            'sql', 'db', 'database.sql', 'dump.sql',
            'sitemap.xml', 'sitemap', 'robots.txt',
            '.htaccess', '.htpasswd',
            'logs', 'log', 'error.log', 'access.log',
            'tmp', 'temp', 'cache',
            'download', 'downloads',
            'search', 'find', 'query',
            'user', 'users', 'user.php',
            'profile', 'profiles', 'account', 'account.php',
            'register', 'signup', 'signin', 'logout',
            'auth', 'authentication', 'authorize',
            'feed', 'rss', 'atom',
            'document', 'docs', 'documentation',
            'help', 'faq', 'terms', 'privacy', 'policy',
            'contact', 'about', 'home', 'index',
            'main', 'root', 'apache', 'nginx',
            'shell', 'webshell', 'backdoor',
            'console', 'terminal', 'bash', 'sh',
            'cgi', 'cgi-bin', 'perl',
            'java', 'jsp', 'asp', 'aspx', 'php',
            'editor', 'CKeditor', 'tinymce',
            'chat', 'message', 'messages',
            'mail', 'email', 'inbox', 'sent',
            'calendar', 'event', 'events',
            'shop', 'store', 'product', 'products',
            'cart', 'checkout', 'order', 'orders',
            'pay', 'payment', 'payments', 'billing',
            'invoice', 'invoices', 'receipt',
            'subscription', 'plan', 'pricing',
            'video', 'audio', 'media', 'player',
            'download', 'streaming', 'stream',
            'gallery', 'photo', 'photos', 'picture',
            'blog', 'post', 'posts', 'news', 'article',
            'comment', 'comments', 'forum',
            'social', 'share', 'friends', 'followers',
        ]
    
    def test_path(self, path):
        """Test a path"""
        url = f"{self.target}/{path}"
        try:
            r = requests.get(url, timeout=5, allow_redirects=False)
            if r.status_code != 404:
                return {'path': path, 'status': r.status_code, 'length': len(r.text)}
        except:
            pass
        return None
    
    def scan(self, threads=20):
        """Scan directories"""
        print(f"[*] Scanning {self.target}...")
        
        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = {executor.submit(self.test_path, p): p for p in self.wordlist}
            
            for future in as_completed(futures):
                result = future.result()
                if result and result['status'] != 403:
                    print(f"[{result['status']}] {result['path']}")
                    self.found.append(result)
        
        return self.found


def main():
    if len(sys.argv) < 2:
        print("Usage: python dir_scanner.py <target>")
        sys.exit(1)
    
    target = sys.argv[1]
    scanner = DirScanner(target)
    scanner.scan()


if __name__ == "__main__":
    main()