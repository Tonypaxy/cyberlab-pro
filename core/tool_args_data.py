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
}
