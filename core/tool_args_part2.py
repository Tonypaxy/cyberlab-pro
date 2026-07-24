BUILTIN_ARGS = {
    "ffuf": [
        ("-u http://target.com/FUZZ -w wordlist.txt", "Directory fuzz"),
        ("-u http://target.com/FUZZ -w wordlist.txt -mc 200,301", "Match codes"),
        ("-u http://target.com/FUZZ -w wordlist.txt -fc 404", "Filter 404"),
        ("-u http://target.com/FUZZ -w wordlist.txt -t 200", "200 threads"),
        ("-u http://FUZZ.target.com -w subdomains.txt", "Subdomain fuzz"),
    ],
    "curl": [
        ("-I https://target.com", "Headers only"),
        ("-v https://target.com", "Verbose"),
        ("-L https://target.com", "Follow redirects"),
        ("-X POST -d user=admin https://target.com/login", "POST data"),
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
    ],
}
