name: mobile-security
description: Mobile application security — Android/iOS app analysis, APK reverse engineering, mobile API testing, Frida hooking, certificate pinning bypass
trigger:
  - mobile security
  - Android security
  - iOS security
  - APK analysis
  - moblie hacking
  - Frida
  - app security
  - mobile pentest

---

# MOBILE SECURITY TESTING

## Android Application Analysis

### APK Structure
```
APK/
├── AndroidManifest.xml
├── classes.dex          # Dalvik bytecode
├── res/                 # Resources
├── assets/             # Assets
├── lib/                # Native libraries
└── META-INF/           # Signatures
```

### Decompile APK
```bash
# Using apktool
apktool d app.apk

# Using jadx
jadx app.apk

# Using androguard
python androguard analyze app.apk
```

### Analyze AndroidManifest.xml
```xml
<!-- Exported components = security risk -->
<activity android:exported="true">
<receiver android:exported="true">
<service android:exported="true">
<provider android:exported="true">
```

### Dangerous Permissions
```xml
<uses-permission android:name="android.permission.INTERNET"/>
<uses-permission android:name="android.permission.READ_SMS"/>
<uses-permission android:name="android.permission.RECEIVE_SMS"/>
<uses-permission android:name="android.permission.READ_CONTACTS"/>
<uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE"/>
<uses-permission android:name="android.permission.CAMERA"/>
<uses-permission android:name="android.permission.RECORD_AUDIO"/>
<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION"/>
<uses-permission android:name="android.permission.READ_PHONE_STATE"/>
```

---

# COMMON VULNERABILITIES

## Insecure Data Storage
```bash
# Check for insecure storage locations
find . -name "*.db" -o -name "*.xml" -o -name "*.shared_prefs"
cat SharedPreferences/file.xml
cat databases/app.db
```

### Vulnerable Storage Patterns
| Storage | Risk | Vulnerability |
| SharedPreferences | Cleartext secrets | No encryption |
| SQLite DB | Cleartext PII | No encryption |
| External Storage | Anyone read | World-readable |
| Log files | Sensitive data | Sensitive in logs |
| Clipboard | Sensitive copy | Cleartext |

## Hardcoded Secrets
```bash
# Search for secrets in code
grep -r "API_KEY\|SECRET\|TOKEN\|PASSWORD" --include="*.java"
grep -r "base64\|encoding" --include="*.java"
grep -r "169.254.169.254" --include="*.java"  # AWS meta
```

## Insecure Network Communication
```bash
# Check for cleartext traffic
grep -r "http://" --include="*.java"
grep -r "SSLContext\|TLS" --include="*.java"

# Check certificate validation
grep -r "HostnameVerifier\|TrustManager" --include="*.java"
```

## Certificate Pinning Bypass (Frida)
```javascript
// Bypass certificate pinning
Java.perform(function() {
    var SSLContext = Java.use("javax.net.ssl.SSLContext");
    var TrustManager = Java.use("javax.net.ssl.X509TrustManager");
    
    SSLContext.init.use(null, [TrustManager.$new()], null);
});

// Bypass specific pinning implementations
// OkHttp, Apache HttpClient, etc.
```

## Deep Link Injection
```xml
<!-- In AndroidManifest -->
<intent-filter>
    <data android:scheme="app"/>
    <data android:host="action"/>
</intent-filter>
```

### Test Deep Links
```bash
adb shell am start -W -a android.intent.action.VIEW -d "app://evil.com"
adb shell am start -W -a android.intent.action.VIEW -d "myapp://host?param=value"
```

## WebView Vulnerabilities
```java
// Dangerous WebView settings
webView.getSettings().setJavaScriptEnabled(true);
webView.getSettings().setAllowFileAccess(true);
webView.getSettings().setAllowContentAccess(true);
webView.getSettings().setPluginEnabled(true);
```

## Exported Components
```xml
<!-- Test exported activities -->
<activity android:name=".AdminActivity" android:exported="true"/>

<!-- Test exported receivers -->
<receiver android:name=".Broadcaster" android:exported="true"/>

<!-- Test exported services -->
<service android:name=".SyncService" android:exported="true"/>
```

---

# MOBILE API TESTING

## Common Mobile API Issues
1. **Older API versions** - Mobile often uses v1/API
2. **Weaker auth** - API keys instead of OAuth
3. **No rate limiting**
4. **IDOR** - User IDs in cleartext
5. **Missing SSL pinning**

## Test Mobile API
```bash
# Intercept traffic
# 1. Install certificate
# 2. Configure proxy
# 3. Monitor requests

# Common endpoints
/api/v1/users
/api/v1/auth/login
/api/v2/feed
/api/mobile/...

# Test auth
curl -H "Authorization: Token XYZ" https://api.target.com/api/v1/data
```

---

# FRIDA SCRIPTS

## Common Frida Hooks
```javascript
// Hook any method
Java.perform(function() {
    var MyClass = Java.use("com.target.MyClass");
    MyClass.method.implementation = function(arg) {
        console.log("Hooked: " + arg);
        return this.method(arg);
    }
});

// Hook native functions
Interceptor.attach(Module.findExportByName("libnative.so", "native_method"), {
    onEnter: function(args) {
        console.log("Native: " + args[0].toString());
    }
});

// Bypass root detection
Java.perform(function() {
    var RootUtil = Java.use("com.target.utils.RootUtil");
    RootUtil.isRooted.implementation = function() {
        return false;
    }
});

// Bypass fingerprint
Java.perform(function() {
    var Fingerprint = Java.use("android.fingerprint.FingerprintManager");
    Fingerprint.isHardwareDetected.implementation = function() {
        return 0;
    }
});
```

## Useful Frida Commands
```bash
# List loaded classes
frida -U -f app.pkg -c "Java.enumerateLoadedClasses()"

# Search for class
frida -U -f app.pkg -c "Java.searchUrls('sensitive')"

# Dump memory
frida -U -f app.pkg --dump-mem output/

# Spawn and attach
frida -U -f com.target.app -l script.js
```

---

# iOS ANALYSIS

## iOS App Structure
```
App.ipa/
├── Payload/
│   └── App.app/
│       ├── App
│       ├── Info.plist
│       ├── Frameworks/
│       └── Resources/
```

## iOS Testing
```bash
# Decrypt IPA (requires jailbreak)
 clutch -d com.target.app
# or
frida-ios-decrypt

# Analysis
otool -L App.app/App  # Libraries
class-dump App.app/App  # Headers
```

## iOS Vulnerabilities
| Vulnerability | Description |
| Keychain storage | Sensitive in keychain |
| NSLog in production | Sensitive in logs |
| World-readable files | Insecure data storage |
| No certificate pinning | MITM attacks |
| Jailbreak detection bypass | Root/bootrom exploits |

---

# MOBILE SECURITY CHECKLIST

## Android
- [ ] Decompile and review code
- [ ] Check exported components
- [ ] Test insecure data storage
- [ ] Test deep link handling
- [ ] Bypass SSL pinning
- [ ] Test WebView security
- [ ] Find hardcoded secrets
- [ ] Test mobile API

## iOS
- [ ] Decrypt and analyze
- [ ] Check Info.plist
- [ ] Test keychain usage
- [ ] Find sensitive data in logs
- [ ] Test network communication
- [ ] Test pasteboard

## API
- [ ] Find mobile API endpoints
- [ ] Test IDOR
- [ ] Test auth bypass
- [ ] Test rate limiting