name: network-security
description: Network penetration testing — port scanning, service enumeration, SNMP, SMB, FTP, SSH, LDAP, DNS, VPN, WiFi hacking
trigger:
  - network security
  - network pentest
  - port scanning
  - service enumeration
  - SMB testing
  - FTP testing
  - DNS
  - SNMP
  - VPN hacking
  - WiFi hacking

---

# NETWORK PENETRATION TESTING

## PORT SCANNING

### TCP Scan Types
```bash
# SYN Scan (requires root)
nmap -sS target

# Connect Scan
nmap -sT target

# UDP Scan
nmap -sU target

# Comprehensive Scan
nmap -sS -sV -sC -O -oA output target
```

### Common Ports
| Port | Service | Test |
| 21 | FTP | Anonymous login, Anonymous upload |
| 22 | SSH | Weak keys, Brute force |
| 23 | Telnet | Cleartext, Brute force |
| 25 | SMTP | Open relay, User enum |
| 53 | DNS | Zone transfer, AXFR |
| 67/68 | DHCP | Rogue server |
| 69 | TFTP | Read/Write files |
| 80 | HTTP | Web vulns |
| 110 | POP3 | Brute force |
| 111 | RPC | rpcbind |
| 135 | MSRPC | Enum users |
| 139/445 | SMB | Null sessions, Enum |
| 143 | IMAP | Brute force |
| 161/162 | SNMP | Community strings |
| 389 | LDAP | Anonymous bind |
| 443 | HTTPS | SSL vulns |
| 445 | SMB | EternalBlue |
| 465 | SMTPS | SSL vulns |
| 514 | Syslog | Log injection |
| 515 | LPD | Print spooler |
| 636 | LDAPS | SSL vulns |
| 993 | IMAPS | SSL vulns |
| 995 | POP3S | SSL vulns |
| 1433 | MSSQL | Brute force |
| 1521 | Oracle | TNS listener |
| 3306 | MySQL | Brute force |
| 3389 | RDP | BlueKeep, Brute |
| 5432 | PostgreSQL | Brute force |
| 5900 | VNC | Brute force |
| 5985/6 | WinRM | Brute force |
| 6379 | Redis | No auth |
| 8080 | HTTP-Alt | Proxy |
| 8443 | HTTPS-Alt | SSL vulns |
| 27017 | MongoDB | No auth |

---

# SERVICE ENUMERATION

## FTP
```bash
# Anonymous login
ftp target
anonymous:anonymous

# Test
ls
get file
put file

# Brute force
hydra -L users.txt -P passwords.txt ftp://target
```

## SSH
```bash
# Banner grab
nc target 22

# Test weak keys
nmap -p 22 --script ssh-hostkey target

# Test weak algorithms
nmap -p 22 --script ssh2-enum-algos target

# Brute force
hydra -L users.txt -P passwords.txt ssh://target
```

## SMB
```bash
# Null session
enum4linux target
rpcclient -U "" target

# List shares
smbclient -L //target -N

# Enum users
ridenum target 5000

# Test exploits
nmap -p 445 --script smb-vuln-* target
```

## DNS
```bash
# Zone transfer
dig axfr @dns-server target

# Try all ns
for ns in $(dig +short target NS); do
  dig axfr @ns target
done

# Reverse lookup
for ip in $(seq 1 254); do
  dig +short $ip.$net.in-addr.arpa PTR
done
```

## LDAP
```bash
# Anonymous bind
ldapsearch -x -h target -s base "(objectclass=*)"

# List users
ldapsearch -x -h target -b "dc=example,dc=com" 

# Enum users
ldap-brute target
```

## SNMP
```bash
# Enumerate
snmpwalk -v1 -c public target

# Test community strings
onesixtyone -c public target

# Walk specific OIDs
snmpwalk -v1 -c public target .1.3.6.1.4.1.77
```

## SMTP
```bash
# Connect
nc target 25

# Test relay
HELO test.com
MAIL FROM:<test@test.com>
RCPT TO:<admin@target.com>
DATA
.

# User enum
VRFY user
EXPN root
```

---

# COMMON NETWORK VULNERABILITIES

## SMB
- **Null sessions** - Information disclosure
- **SMB signing not required** - NTLM relay
- **SMBv1 enabled** - EternalBlue
- **Weak password** - Brute force

## FTP
- **Anonymous access** - Read/Write files
- **Cleartext** - Sniff credentials
- **Directory traversal** - File access

## SSH
- **Weak keys** - Key compromise
- **Old protocols** - SSH1
- **Weak ciphers** - Downgrade

## Telnet
- **Cleartext** - Sniff credentials
- **No auth** - Direct access

## SMTP
- **Open relay** - Spam
- **User enum** - VRFY/EXPN

## DNS
- **Zone transfer** - Full zone
- **Cache poisoning** - Redirect
- **DNSSEC not enabled** - Spoofing

## SNMP
- **Default community** - Info disclosure
- **RW community** - Config change

---

# NETWORK ATTACKS

## NTLM Relay
```bash
# Setup relay
responder -I eth0
impacket-ntrelay -t smb://target

# Capture
hashcat -m 5600 hash.txt wordlist.txt
```

## ARP Spoofing
```bash
# MITM
ettercap -T -M ARP //target1 //target2

# ARP spoof
arpspoof -i eth0 -t target gateway
```

## VLAN Hopping
```bash
# Switch spoofing
vtpdump -i eth0
doslug -i eth0
```

---

# WIFI HACKING

## WEP
```bash
# Monitor mode
airmon-ng start wlan0

# Capture
airodump-ng -c channel --bssid MAC -w output wlan0mon

# Inject
aireplay-ng --arpreplay -b MAC -h MYMAC wlan0mon

# Crack
aircrack-ng output.cap
```

## WPA/WPA2
```bash
# Capture handshake
airodump-ng -c channel --bssid MAC -w output wlan0mon

# Deauth attack
aireplay-ng --deauth 5 -a MAC wlan0mon

# Crack
aircrack-ng -w wordlist.txt output.cap

# PMKID
hashcat -m 16800 hash.txt wordlist.txt
```

## WPA3
```bash
# PMKID client
hcxdumptool -i wlan0mon -o output.pcap

# Extract PMKID
hcxpcaptool output.pcap -o hash.txt

# Crack
hashcat -m 16800 hash.txt wordlist.txt

# Dragonblood attacks
# Offline dictionary, Timing, SAE
```

## Evading WiFi Security
```bash
# WPS pixie dust
reaver -i wlan0mon -b MAC -vv

# WPS PIN brute
reaver -i wlan0mon -b MAC -vv -p 12345670

# Rogue AP
hostapd-wpe config
```

---

# NETWORK CHECKLIST

## Scanning
- [ ] TCP SYN scan
- [ ] UDP scan
- [ ] Service version detection
- [ ] OS detection

## Enumeration
- [ ] FTP anonymous
- [ ] SMB null session
- [ ] SNMP community
- [ ] DNS zone transfer
- [ ] SMTP relay

## Testing
- [ ] Test default credentials
- [ ] Test weak passwords
- [ ] Test unencrypted protocols
- [ ] Test service exploits

## Wireless
- [ ] Discover networks
- [ ] Capture handshake
- [ ] Test WEP
- [ ] Test WPS
- [ ] Test WPA3