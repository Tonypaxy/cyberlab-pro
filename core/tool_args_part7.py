BUILTIN_ARGS = {
    "nuclei": [
        ("-u http://target.com", "Basic scan"),
        ("-u http://target.com -severity critical,high", "Critical/High only"),
        ("-l targets.txt -t cves/", "CVE templates"),
        ("-u http://target.com -t exposures/", "Exposure scan"),
        ("-u http://target.com -o report.txt", "Save report"),
    ],
    "httpx": [
        ("-l subs.txt -o live.txt", "Check live hosts"),
        ("-l subs.txt -status-code -title", "Status and title"),
        ("-l subs.txt -tech-detect", "Tech detection"),
    ],
    "rustscan": [
        ("-a target.com", "Fast scan"),
        ("-a target.com -p 1-1000", "Port range"),
        ("-a target.com --ulimit 5000 -t 2000", "Max speed"),
    ],
    "wapiti": [
        ("-u http://target.com", "Basic scan"),
        ("-u http://target.com --scope page", "Page scope"),
    ],
    "testssl": [
        ("https://target.com", "Full test"),
        ("--each-cipher https://target.com", "Each cipher"),
        ("--json https://target.com", "JSON output"),
    ],
    "sslyze": [
        ("--regular target.com", "Regular scan"),
        ("--json_out out.json target.com", "JSON output"),
    ],
    "responder": [
        ("-I eth0", "Start on eth0"),
        ("-I wlan0 -rdwv", "Full mode WiFi"),
    ],
    "bloodhound": [
        ("-d domain -u user -p pass -ns nameserver -c all", "Full collection"),
    ],
    "chisel": [
        ("server -p 8080 --reverse", "Server reverse"),
        ("client server:8080 R:4444:localhost:4444", "Client reverse"),
    ],
    "proxychains": [
        ("nmap -sT target.com", "Nmap via proxy"),
        ("curl target.com", "Curl via proxy"),
    ],
    "wifite": [
        ("-i wlan0", "Basic scan"),
        ("-i wlan0 --wpa", "WPA only"),
        ("-i wlan0 --kill", "Kill interfering"),
    ],
    "reaver": [
        ("-i wlan0mon -b BSSID -vv", "WPS attack"),
        ("-i wlan0mon -b BSSID -c 6 -vv", "Specific channel"),
    ],
    "ab": [
        ("-n 1000 -c 100 http://target.com/", "1000 requests"),
        ("-n 10000 -c 200 -t 30 http://target.com/", "30s stress test"),
    ],
    "siege": [
        ("-c 100 -t 30s http://target.com", "100 users 30s"),
        ("-c 200 -r 50 http://target.com", "200 users 50 reps"),
    ],
    "burpsuite": [
        ("--project=project.burp", "Open project"),
        ("--config=config.json", "Load config"),
    ],
    "commix": [
        ("-u http://target.com/page.php?id=1", "Basic test"),
        ("-u http://target.com/page.php?id=1 --os=unix", "Unix target"),
    ],
    "xsser": [
        ("-u http://target.com/page.php?q=test", "Basic XSS"),
        ("--auto -u http://target.com/page.php?q=test", "Auto mode"),
    ],
    "xsstrike": [
        ("-u http://target.com/page.php?q=test", "Basic scan"),
        ("-u http://target.com/page.php?q=test --crawl", "Crawl mode"),
    ],
    "dalfox": [
        ("url http://target.com/page.php?q=test", "Basic scan"),
        ("file urls.txt", "Bulk URLs"),
    ],
    "nosqlmap": [
        ("-u http://target.com/api", "Basic scan"),
        ("-u http://target.com/api --mongodb", "MongoDB target"),
    ],
    "arjun": [
        ("-u http://target.com/page.php", "Find params"),
        ("-u http://target.com/page.php -t 20", "20 threads"),
    ],
    "feroxbuster": [
        ("-u http://target.com -w wordlist.txt", "Directory brute"),
        ("-u http://target.com -w wordlist.txt -t 100", "100 threads"),
    ],
    "dirsearch": [
        ("-u http://target.com -w wordlist.txt", "Directory scan"),
        ("-u http://target.com -e php,html,txt -t 50", "Extensions"),
    ],
    "grype": [
        ("nginx:latest", "Scan image"),
        ("-o json nginx:latest", "JSON output"),
    ],
    "dockle": [
        ("nginx:latest", "Check image"),
    ],
    "hadolint": [
        ("Dockerfile", "Lint Dockerfile"),
    ],
    "kube-bench": [
        ("--config-dir /etc/kubernetes", "Config dir"),
        ("--version 1.20", "K8s version"),
    ],
    "kubescape": [
        ("scan", "Full scan"),
        ("scan framework nsa", "NSA framework"),
    ],
    "popeye": [
        ("-n dev", "Dev namespace"),
        ("--all-namespaces", "All namespaces"),
    ],
    "checkov": [
        ("-d /terraform", "Terraform scan"),
        ("-d /kubernetes", "K8s scan"),
    ],
    "tfsec": [
        (".", "Current directory"),
        ("--format json .", "JSON output"),
    ],
    "terrascan": [
        ("scan -d /terraform", "Scan directory"),
        ("scan -i terraform", "Terraform only"),
    ],
    "prowler": [
        ("-p custom-profile -r us-east-1", "AWS region"),
        ("-M json -o output", "JSON output"),
    ],
    "scoutsuite": [
        ("aws --profile default", "AWS scan"),
        ("azure --cli", "Azure scan"),
    ],
    "pacu": [
        ("--session mytest", "Create session"),
        ("--list-modules", "List modules"),
    ],
    "cloudmapper": [
        ("collect --account target", "Collect data"),
        ("report --account target", "Generate report"),
    ],
    "scalpel": [
        ("-c scalpel.conf image.dd -o output/", "With config"),
    ],
    "bulk_extractor": [
        ("-o output/ image.dd", "Extract all"),
        ("-e email -o output/ image.dd", "Emails only"),
    ],
    "dex2jar": [
        ("classes.dex -o output.jar", "Convert DEX"),
    ],
    "androguard": [
        ("analyze app.apk", "Analyze"),
    ],
    "rizin": [
        ("-A binary", "Auto analyze"),
        ("-d binary", "Debug mode"),
    ],
    "ltrace": [
        ("command", "Library calls"),
        ("-f command", "Follow forks"),
    ],
    "ss": [
        ("-tunap", "All connections"),
        ("-tlnp", "Listening ports"),
    ],
    "ufw": [
        ("status", "Check status"),
        ("enable", "Enable firewall"),
        ("allow 80/tcp", "Allow port 80"),
    ],
    "wipe": [("-f file.txt", "Force wipe"), ("-r dir/", "Recursive")],
    "srm": [("-v file.txt", "Verbose delete"), ("-r dir/", "Recursive")],
    "scp": [
        ("file.txt user@host:/path/", "Copy to remote"),
        ("user@host:/path/file.txt .", "Copy from remote"),
    ],
    "rsync": [
        ("-av dir/ user@host:/path/", "Sync to remote"),
        ("-av --delete dir/ /backup/", "Mirror sync"),
    ],
    "htop": [("", "Interactive viewer"), ("-u username", "Filter user")],
    "iftop": [("-i wlan0", "Interface traffic"), ("-P", "Show ports")],
    "nethogs": [("wlan0", "Interface bandwidth")],
    "vnstat": [("-i wlan0", "Interface stats"), ("-d", "Daily stats")],
    "base64": [("file.txt", "Encode"), ("-d file.b64", "Decode")],
    "md5sum": [("file.txt", "MD5 hash"), ("-c checksum.md5", "Check")],
    "sha256sum": [("file.txt", "SHA256 hash"), ("-c checksum.sha256", "Check")],
    "go": [("build main.go", "Build"), ("run main.go", "Run")],
    "gem": [("install package", "Install"), ("list", "List")],
    "npm": [("install package", "Install"), ("install -g package", "Global")],
    "ansible": [("all -m ping", "Ping all"), ("-i inventory playbook.yml", "Run playbook")],
    "route": [("-n", "Routing table")],
    "mount": [("-o ro,noexec /dev/sdb1 /mnt", "Read-only mount")],
    "sysctl": [("-a", "All settings")],
    "unzip": [("archive.zip", "Extract"), ("-P password archive.zip", "Password")],
}
