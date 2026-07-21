"""CyberLab Pro - Built-in Tool Arguments Database
This file contains all pre-written bruteforce and attack arguments for 30+ tools.
Future tools auto-discover their arguments from --help output.
"""

BUILTIN_ARGS = {
    "nmap": [
        ("-sS", "SYN stealth scan"), ("-sT", "TCP connect scan"), ("-sU", "UDP scan"),
        ("-sV", "Version detection"), ("-sC", "Default scripts"), ("-O", "OS detection"),
        ("-p-", "All 65535 ports"), ("-p 1-1000", "Top 1000 ports"), ("-F", "Fast top 100"),
        ("-A", "Aggressive all"), ("--script vuln", "Vuln scan"), ("--script exploit", "Exploit scan"),
        ("--script brute", "Brute force"), ("--script auth", "Auth scan"), ("--script discovery", "Discovery"),
        ("-Pn", "Skip ping"), ("-T4", "Speed T4"), ("-T5", "Max speed"),
        ("-sA", "ACK scan"), ("-sW", "Window scan"), ("-sM", "Maimon scan"),
        ("-sN", "NULL scan"), ("-sF", "FIN scan"), ("-sX", "Xmas scan"),
        ("--scanflags URGACKPSHRSTSYNFIN", "Custom flags"), ("-f", "Fragment packets"),
        ("-D RND:10", "Decoy scan"), ("-S 192.168.1.1", "Spoof source"),
        ("-g 53", "Source port 53"), ("--data-length 100", "Extra data"),
        ("-oN output.txt", "Normal output"), ("-oX output.xml", "XML output"), ("-oG output.grep", "Grepable"),
        ("-v", "Verbose"), ("-vv", "Very verbose"), ("--reason", "Show reasons"),
        ("--open", "Only open ports"), ("--packet-trace", "Packet trace")
    ],
    "gobuster": [
        ("dir -u", "Directory mode"), ("dns -d", "DNS subdomain mode"), ("vhost -u", "Virtual host mode"),
        ("-w /usr/share/wordlists/dirb/common.txt", "Common wordlist"),
        ("-w /usr/share/wordlists/dirb/big.txt", "Big wordlist"),
        ("-w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt", "Medium dirbuster"),
        ("-x php,html,txt,js", "Web extensions"), ("-x php,asp,aspx,jsp", "Code extensions"),
        ("-x bak,old,zip,tar,gz", "Backup extensions"), ("-x all", "All extensions"),
        ("-t 50", "50 threads"), ("-t 100", "100 threads"), ("-t 200", "200 threads"),
        ("-k", "Skip SSL verify"), ("--no-error", "No errors"), ("-q", "Quiet mode"),
        ("-o output.txt", "Save output"), ("--delay 100ms", "100ms delay"), ("--random-agent", "Random UA"),
        ("-c http://127.0.0.1:8080", "Proxy"), ("-a 'Mozilla/5.0'", "Custom UA"),
        ("-H 'Authorization: Basic xxx'", "Auth header"), ("--wildcard", "Wildcard check")
    ],
    "sqlmap": [
        ("-u", "Target URL"), ("--data=", "POST data"), ("--cookie=", "Cookie"),
        ("--dbs", "Enumerate databases"), ("--tables", "Enumerate tables"), ("--columns", "Enumerate columns"),
        ("--dump", "Dump all data"), ("--dump-all", "Dump everything"), ("--schema", "Schema only"),
        ("--batch", "Auto answers"), ("--random-agent", "Random UA"), ("--tor", "Use Tor"),
        ("--level=1", "Level 1 safe"), ("--level=3", "Level 3 medium"), ("--level=5", "Level 5 all"),
        ("--risk=1", "Risk 1 safe"), ("--risk=2", "Risk 2 medium"), ("--risk=3", "Risk 3 dangerous"),
        ("--tamper=between", "Between tamper"), ("--tamper=space2comment", "Space2comment"),
        ("--tamper=charencode", "Char encode"), ("--tamper=randomcase", "Random case"),
        ("--os-shell", "OS shell"), ("--os-pwn", "OS pwn"), ("--os-cmd=id", "OS command"),
        ("--sql-shell", "SQL shell"), ("--file-read=/etc/passwd", "Read file"),
        ("--file-write=shell.php", "Write file"), ("--privileges", "Check privileges"),
        ("--users", "Enumerate users"), ("--passwords", "Enumerate passwords"),
        ("--current-user", "Current user"), ("--current-db", "Current database"),
        ("--hostname", "Hostname"), ("--is-dba", "Check DBA"), ("--proxy=http://127.0.0.1:8080", "Proxy")
    ],
    "hydra": [
        ("-l admin -P wordlist.txt", "Single user brute"), ("-L users.txt -P pass.txt", "User list brute"),
        ("-l admin -p password", "Single test"), ("-t 4", "4 tasks"), ("-t 16", "16 tasks"),
        ("-t 64", "64 tasks"), ("-V", "Verbose"), ("-vV", "Very verbose"),
        ("-f", "Stop on first"), ("-F", "Stop on first host"), ("-o output.txt", "Save found"),
        ("-R", "Restore session"), ("-s 2222", "Custom port"), ("-e nsr", "Extra checks"),
        ("-M targets.txt", "Target list"), ("-w 5", "5 second wait"), ("-W 30", "30 second wait"),
        ("ssh://", "SSH brute"), ("ftp://", "FTP brute"), ("http-get://", "HTTP GET"),
        ("http-post-form://", "HTTP POST form"), ("https-get://", "HTTPS GET"),
        ("mysql://", "MySQL brute"), ("mssql://", "MSSQL brute"), ("rdp://", "RDP brute"),
        ("smtp://", "SMTP brute"), ("pop3://", "POP3 brute"), ("imap://", "IMAP brute"),
        ("telnet://", "Telnet brute"), ("vnc://", "VNC brute"), ("snmp://", "SNMP brute"),
        ("smb://", "SMB brute"), ("ldap://", "LDAP brute"), ("postgres://", "PostgreSQL brute")
    ],
    "nikto": [
        ("-h", "Target host"), ("-p 80", "Port 80"), ("-p 443", "Port 443"),
        ("-ssl", "Force SSL"), ("-nossl", "No SSL"), ("-Tuning 1", "Interesting files"),
        ("-Tuning 2", "CGI directories"), ("-Tuning 3", "Server issues"), ("-Tuning 4", "XSS checks"),
        ("-Tuning 5", "Remote file retrieval"), ("-Tuning 6", "Denial of service"),
        ("-Tuning 7", "File upload checks"), ("-Tuning 8", "Command execution"),
        ("-Tuning 9", "SQL injection"), ("-Tuning 0", "All except 6"),
        ("-Tuning x", "All including XSS"), ("-o report.html", "HTML output"),
        ("-Format htm", "HTML format"), ("-Format csv", "CSV format"), ("-Format xml", "XML format"),
        ("-Cgidirs all", "All CGI dirs"), ("-evasion 1", "Random URI encoding"),
        ("-evasion 2", "Directory self ref"), ("-evasion 3", "Premature URL ending"),
        ("-evasion 4", "Long URL"), ("-evasion 5", "Fake parameter"),
        ("-mutate 1", "File extensions"), ("-mutate 2", "Replace slash"), ("-mutate 3", "Add directory"),
        ("-timeout 10", "10 sec timeout"), ("-maxtime 30m", "30 minute max"), ("-Plugins auth", "Auth plugin")
    ],
    "wpscan": [
        ("--url", "Target URL"), ("--enumerate p", "Plugins"), ("--enumerate t", "Themes"),
        ("--enumerate u", "Users"), ("--enumerate vp", "Vulnerable plugins"), ("--enumerate vt", "Vulnerable themes"),
        ("--plugins-detection aggressive", "Aggressive plugin"), ("--password-attack wp-login", "Password attack"),
        ("--usernames admin", "Check admin"), ("--passwords wordlist.txt", "Password list"),
        ("--max-threads 5", "5 threads"), ("--max-threads 20", "20 threads"),
        ("--disable-tls-checks", "No TLS check"), ("--proxy http://127.0.0.1:8080", "Proxy"),
        ("--api-token YOUR_TOKEN", "WPVulnDB API"), ("--stealthy", "Stealthy mode"),
        ("--random-user-agent", "Random UA"), ("--force", "Force scan"), ("--verbose", "Verbose"),
        ("--output output.txt", "Text output"), ("--format json", "JSON output")
    ],
    "ffuf": [
        ("-u", "URL with FUZZ"), ("-w wordlist.txt", "Wordlist"), ("-w wordlist.txt:FUZZ", "Named wordlist"),
        ("-H 'Host: FUZZ'", "Custom header"), ("-H 'User-Agent: Mozilla/5.0'", "User agent"),
        ("-H 'Cookie: session=FUZZ'", "Cookie fuzz"), ("-H 'Authorization: Bearer FUZZ'", "Auth fuzz"),
        ("-X POST", "POST method"), ("-X PUT", "PUT method"), ("-X DELETE", "DELETE method"),
        ("-d 'user=FUZZ&pass=test'", "POST data"), ("-d 'json={\"key\":\"FUZZ\"}'", "JSON data"),
        ("-mc 200,301,302", "Match codes"), ("-mc all", "Match all codes"), ("-fc 404", "Filter 404"),
        ("-fc 403,404,500", "Filter errors"), ("-fw 10", "Filter words"), ("-fs 100", "Filter size"),
        ("-fl 5", "Filter lines"), ("-fr 'error'", "Filter regex"), ("-t 50", "50 threads"),
        ("-t 100", "100 threads"), ("-t 200", "200 threads"), ("-p 0.5", "0.5s delay"),
        ("-timeout 10", "10s timeout"), ("-maxtime 300", "5 min max"), ("-max-time 600", "10 min max"),
        ("-o output.json", "JSON output"), ("-of json", "JSON format"), ("-of html", "HTML format"),
        ("-of csv", "CSV format"), ("-recursion", "Recursive"), ("-recursion-depth 2", "Depth 2"),
        ("-replay-proxy http://127.0.0.1:8080", "Replay proxy"), ("-x http://127.0.0.1:8080", "Proxy"),
        ("-v", "Verbose"), ("-debug-log debug.log", "Debug log"), ("-se", "Stop on errors")
    ],
    "john": [
        ("--wordlist=rockyou.txt", "Rockyou wordlist"), ("--wordlist=wordlist.txt", "Custom wordlist"),
        ("--rules", "Wordlist rules"), ("--rules=Single", "Single rules"), ("--rules=Wordlist", "Wordlist rules"),
        ("--rules=Extra", "Extra rules"), ("--rules=Jumbo", "Jumbo rules"), ("--rules=All", "All rules"),
        ("--incremental", "Incremental mode"), ("--incremental=Lower", "Lowercase incremental"),
        ("--incremental=Alpha", "Alpha incremental"), ("--incremental=Digits", "Digits incremental"),
        ("--incremental=Alnum", "Alphanumeric incremental"), ("--mask=?l?l?l?l?l?l?l?l", "8 lower mask"),
        ("--mask=?u?l?l?l?l?l?d?d", "Password mask"), ("--mask=?a?a?a?a?a?a", "6 char all"),
        ("--format=raw-md5", "Raw MD5"), ("--format=raw-sha1", "Raw SHA1"), ("--format=raw-sha256", "Raw SHA256"),
        ("--format=raw-sha512", "Raw SHA512"), ("--format=nt", "NT hash"), ("--format=lm", "LM hash"),
        ("--format=zip", "ZIP archive"), ("--format=rar", "RAR archive"), ("--format=pdf", "PDF file"),
        ("--format=wpapsk", "WPA PSK"), ("--format=bcrypt", "Bcrypt"),
        ("--show", "Show cracked"), ("--loopback", "Loopback mode"), ("--fork=4", "4 processes"),
        ("--restore", "Restore session"), ("--status", "Show status")
    ],
    "hashcat": [
        ("-m 0", "MD5"), ("-m 100", "SHA1"), ("-m 1400", "SHA256"), ("-m 1700", "SHA512"),
        ("-m 1000", "NTLM"), ("-m 3000", "LM"), ("-m 3200", "Bcrypt"), ("-m 2500", "WPA/WPA2"),
        ("-m 16800", "WPA-PMKID"), ("-m 11600", "7-Zip"), ("-m 12500", "RAR3-hp"),
        ("-m 13000", "RAR5"), ("-m 13600", "ZIP"), ("-m 10700", "PDF"),
        ("-m 9600", "MS Office 2007"), ("-a 0", "Dictionary attack"), ("-a 1", "Combinator attack"),
        ("-a 3", "Brute-force mask"), ("-a 6", "Dict + mask"), ("-a 7", "Mask + dict"),
        ("-O", "Optimized kernel"), ("-w 3", "High workload"), ("-w 4", "Maximum workload"),
        ("--force", "Force ignore warnings"), ("--show", "Show cracked"),
        ("--username", "Username mode"), ("-r rules/best64.rule", "Best64 rules"),
        ("-r rules/dive.rule", "Dive rules"), ("-r rules/rockyou-30000.rule", "Rockyou rules"),
        ("--stdout", "Stdout mode"), ("--restore", "Restore session"), ("--session=name", "Session name"),
        ("-o output.txt", "Output file"), ("--status", "Status")
    ],
    "curl": [
        ("-I", "Headers only"), ("-v", "Verbose"), ("-vv", "Very verbose"), ("-s", "Silent"),
        ("-L", "Follow redirects"), ("-k", "Insecure SSL"), ("-X GET", "GET request"), ("-X POST", "POST request"),
        ("-X PUT", "PUT request"), ("-X DELETE", "DELETE request"), ("-X PATCH", "PATCH request"),
        ("-d 'key=value'", "POST data"), ("-d '{\"json\":\"data\"}'", "JSON POST"), ("-d @file.json", "Data from file"),
        ("-H 'Content-Type: application/json'", "JSON header"), ("-H 'User-Agent: Mozilla/5.0'", "Custom UA"),
        ("-H 'Authorization: Bearer TOKEN'", "Bearer auth"), ("-H 'Authorization: Basic BASE64'", "Basic auth"),
        ("-H 'Cookie: session=xxx'", "Cookie"), ("-H 'X-Forwarded-For: 127.0.0.1'", "Spoof IP"),
        ("-x http://127.0.0.1:8080", "Proxy"), ("--socks5 127.0.0.1:9050", "SOCKS5"),
        ("-o output.txt", "Save output"), ("-O", "Remote filename"),
        ("-u user:pass", "Basic auth"), ("-A 'Mozilla/5.0'", "User agent"), ("-e 'https://referer.com'", "Referer")
    ],
    "dig": [
        ("A", "IPv4 address"), ("AAAA", "IPv6 address"), ("MX", "Mail servers"), ("NS", "Nameservers"),
        ("SOA", "Start of authority"), ("TXT", "Text records"), ("CNAME", "Canonical name"),
        ("PTR", "Reverse DNS"), ("ANY", "All records"), ("+short", "Short output"), ("+noall +answer", "Answer only"),
        ("+trace", "Trace resolution"), ("+recurse", "Recursive"), ("+norecurse", "Non-recursive"),
        ("-x", "Reverse lookup"), ("@8.8.8.8", "Google DNS"), ("@1.1.1.1", "Cloudflare DNS"),
        ("+tcp", "Use TCP"), ("+time=5", "5 sec timeout"), ("+tries=3", "3 tries"),
        ("+dnssec", "DNSSEC"), ("+multiline", "Multi-line")
    ],
    "dirb": [
        ("http://target.com", "Target URL"), ("https://target.com", "HTTPS target"),
        ("/usr/share/wordlists/dirb/common.txt", "Common wordlist"), ("/usr/share/wordlists/dirb/big.txt", "Big wordlist"),
        ("-a 'Mozilla/5.0'", "Custom UA"), ("-c 'session=xxx'", "Cookie"), ("-u user:pass", "Basic auth"),
        ("-p http://127.0.0.1:8080", "Proxy"), ("-w", "No warnings"), ("-r", "Non-recursive"),
        ("-z 100", "100ms delay"), ("-X .php,.html,.txt", "Extensions"), ("-S", "Silent mode"),
        ("-o output.txt", "Output file"), ("-l", "Lowercase"), ("-i", "Case insensitive")
    ],
    "tcpdump": [
        ("-i any", "All interfaces"), ("-i wlan0", "WiFi interface"), ("-i eth0", "Ethernet"),
        ("-n", "No DNS resolve"), ("-nn", "No port names"), ("-v", "Verbose"), ("-vv", "Very verbose"),
        ("-X", "Hex and ASCII"), ("-A", "ASCII only"), ("-c 100", "100 packets only"),
        ("-w capture.pcap", "Save to PCAP"), ("-r capture.pcap", "Read PCAP"),
        ("host 192.168.1.1", "Filter host"), ("port 80", "Port 80"), ("port 443", "Port 443"),
        ("tcp", "TCP only"), ("udp", "UDP only"), ("icmp", "ICMP only"),
        ("net 192.168.1.0/24", "Network"), ("not port 22", "Exclude SSH")
    ],
    "netcat": [
        ("-lvp 4444", "Listen port 4444"), ("-lvp 8080", "Listen port 8080"), ("-lvp 53", "Listen port 53"),
        ("-v 192.168.1.1 80", "Connect port 80"), ("-v target.com 443", "Connect SSL"),
        ("-e /bin/bash", "Execute shell"), ("-e /bin/sh", "Execute SH"),
        ("-z 192.168.1.1 1-1000", "Port scan 1-1000"), ("-z -v 192.168.1.1 1-65535", "Full port scan"),
        ("-u", "UDP mode"), ("-w 5", "5 sec timeout"), ("-k", "Keep listening"),
        ("-n", "No DNS resolve"), ("-s 192.168.1.1", "Source IP"), ("-p 2222", "Source port")
    ],
    "msfconsole": [
        ("-q", "Quiet no banner"), ("-n", "No database"),
        ("-x 'use exploit/multi/handler; set PAYLOAD windows/meterpreter/reverse_tcp; set LHOST 0.0.0.0; set LPORT 4444; run'", "Multi handler"),
        ("-x 'db_nmap -sV 192.168.1.1'", "Nmap scan"),
        ("-x 'use auxiliary/scanner/portscan/tcp; set RHOSTS 192.168.1.0/24; run'", "Network scan"),
        ("-x 'use auxiliary/scanner/smb/smb_version; set RHOSTS 192.168.1.0/24; run'", "SMB scan"),
        ("-x 'use auxiliary/scanner/ssh/ssh_login; set RHOSTS 192.168.1.1; set USERNAME admin; set PASS_FILE pass.txt; run'", "SSH brute"),
        ("-x 'use auxiliary/scanner/ftp/ftp_login; set RHOSTS 192.168.1.1; set USER_FILE users.txt; set PASS_FILE pass.txt; run'", "FTP brute"),
        ("-r script.rc", "Resource script"), ("-o output.txt", "Output file")
    ],
    "exiftool": [
        ("image.jpg", "Read metadata"), ("-a", "Show all tags"), ("-g", "Group output"),
        ("-s", "Short output"), ("-json", "JSON output"), ("-csv", "CSV output"),
        ("-all=", "Delete all metadata"), ("-Comment='test'", "Set comment"),
        ("-Artist='name'", "Set artist"), ("-GPSLatitude=37.7749", "Set GPS lat"),
        ("-overwrite_original", "Overwrite file"), ("-r", "Recursive"),
        ("-ext jpg", "JPG only"), ("-ext png", "PNG only"), ("-tagsfromfile other.jpg", "Copy from file")
    ],
    "aircrack-ng": [
        ("-w rockyou.txt", "Wordlist attack"), ("-b 00:11:22:33:44:55", "Target BSSID"),
        ("-e 'WiFi Name'", "Target ESSID"), ("capture.cap", "Capture file"),
        ("-a 1", "WEP attack"), ("-a 2", "WPA/WPA2 attack"), ("-p 4", "4 threads"),
        ("-P 500", "PTW attack WEP"), ("-K", "KoreK attack WEP"),
        ("-l key.txt", "Save key"), ("-q", "Quiet mode")
    ],
    "strings": [
        ("file.bin", "Read file"), ("-n 4", "Min length 4"), ("-n 8", "Min length 8"),
        ("-n 10", "Min length 10"), ("-n 16", "Min length 16"),
        ("-t o", "Octal offset"), ("-t d", "Decimal offset"), ("-t x", "Hex offset"),
        ("-e s", "7-bit encoding"), ("-e b", "16-bit big-endian"), ("-e l", "16-bit little-endian"),
        ("-e B", "32-bit big-endian"), ("-e L", "32-bit little-endian"), ("-a", "Scan whole file")
    ],
    "binwalk": [
        ("file.bin", "Scan file"), ("-e", "Extract files"), ("-Me", "Extract recursively"),
        ("-D '.*'", "Extract all types"), ("-d 5", "Depth 5"), ("-B", "Signature scan"),
        ("-R 'pattern'", "Raw search"), ("-A", "Opcode scan"), ("-Y", "Capa scan"),
        ("-X", "Hex dump"), ("-E", "Entropy analysis"), ("-J", "JSON output"),
        ("-q", "Quiet"), ("-v", "Verbose")
    ],
    "steghide": [
        ("embed -cf cover.jpg -ef secret.txt", "Embed file"), ("embed -cf cover.jpg -ef secret.txt -p password", "Embed with pass"),
        ("embed -cf cover.jpg -ef secret.txt -e none", "No encryption"), ("embed -cf cover.jpg -ef secret.txt -z 9", "Max compress"),
        ("extract -sf stego.jpg", "Extract file"), ("extract -sf stego.jpg -p password", "Extract with pass"),
        ("extract -sf stego.jpg -xf output.txt", "Output file"), ("info cover.jpg", "Info about file")
    ],
    "ettercap": [
        ("-T", "Text mode"), ("-G", "GUI mode"), ("-q", "Quiet"), ("-i eth0", "Interface"),
        ("-i wlan0", "WiFi interface"), ("-M arp:remote /192.168.1.1/ /192.168.1.0-255/", "ARP poisoning"),
        ("-M arp /192.168.1.0/ /192.168.1.1/", "ARP one-way"),
        ("-P dns_spoof", "DNS spoof"), ("-P repoison_arp", "Repoison ARP"),
        ("-w capture.pcap", "Save PCAP"), ("-L logfile", "Log to file"), ("-B", "Bridge mode")
    ],
    "crunch": [
        ("8 8 -t @@@@%%%% -o output.txt", "8 char pattern"), ("6 8 0123456789 -o num.txt", "Numeric 6-8 length"),
        ("4 6 abcdefghijklmnopqrstuvwxyz -o lower.txt", "Lowercase 4-6"), ("6 10 -o full.txt", "All chars 6-10"),
        ("8 8 -t ,@@@%%%^ -o pass.txt", "Complex pattern"), ("-p word1 word2", "Permutation"),
        ("-p 1234 admin password", "Common combo"), ("-q wordlist.txt", "Read from file"),
        ("-b 1mib", "Split 1MB"), ("-c 10000", "Lines per file")
    ],
    "ping": [
        ("-c 4 192.168.1.1", "4 packets"), ("-c 100 target.com", "100 packets"),
        ("-i 0.2", "0.2 sec interval"), ("-i 1", "1 sec interval"), ("-s 1000", "1000 byte packet"),
        ("-s 65500", "Max packet size"), ("-f", "Flood ping (root)"), ("-t 64", "TTL 64"),
        ("-W 1", "1 sec timeout"), ("-q", "Quiet summary"), ("-D", "Timestamp"), ("-n", "No DNS resolve")
    ],
    "traceroute": [
        ("target.com", "Basic trace"), ("-n", "No DNS"), ("-m 15", "Max 15 hops"),
        ("-m 30", "Max 30 hops"), ("-p 80", "Port 80"), ("-p 443", "Port 443"),
        ("-q 1", "1 probe per hop"), ("-w 2", "2 sec wait"),
        ("-I", "ICMP method"), ("-T", "TCP method"), ("-U", "UDP method"),
        ("-A", "AS path lookup"), ("-f 5", "Start at hop 5"), ("-M", "MTU discovery")
    ],
    "whatweb": [
        ("target.com", "Target URL"), ("-v", "Verbose"), ("-a 1", "Aggression 1 passive"),
        ("-a 3", "Aggression 3 active"), ("-a 4", "Aggression 4 heavy"),
        ("--color=never", "No color"), ("--log-json=out.json", "JSON output"),
        ("--log-xml=out.xml", "XML output"), ("--log-csv=out.csv", "CSV output"),
        ("--proxy http://127.0.0.1:8080", "Proxy"), ("--user-agent 'Mozilla/5.0'", "Custom UA"),
        ("--max-threads 10", "10 threads"), ("--open-timeout 5", "5s timeout"),
        ("--read-timeout 10", "10s read")
    ],
}
