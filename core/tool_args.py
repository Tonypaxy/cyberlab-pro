"""CyberLab Pro - Dynamic Tool Arguments Database"""
import subprocess
import json
import os

class ToolArgsDatabase:
    """Auto-generates and caches common arguments for each tool"""
    
    # Built-in known arguments for common tools
    BUILTIN_ARGS = {
        "nmap": [
            ("-sS", "SYN scan"), ("-sT", "TCP scan"), ("-sU", "UDP scan"),
            ("-sV", "Version detect"), ("-sC", "Default scripts"), ("-O", "OS detect"),
            ("-p-", "All ports"), ("-p 80,443", "Web ports"), ("-F", "Fast scan"),
            ("-A", "Aggressive"), ("--script vuln", "Vuln scan"), ("-Pn", "No ping"),
            ("-T4", "Speed T4"), ("-oN", "Output file")
        ],
        "gobuster": [
            ("dir -u", "Directory scan"), ("dns -d", "DNS subdomain"),
            ("vhost -u", "Virtual host"), ("-w /usr/share/wordlists/dirb/common.txt", "Common wordlist"),
            ("-x php,html,txt", "Extensions"), ("-t 50", "50 threads")
        ],
        "sqlmap": [
            ("-u", "URL target"), ("--dbs", "List databases"), ("--tables", "List tables"),
            ("--columns", "List columns"), ("--dump", "Dump data"), ("--os-shell", "OS shell"),
            ("--batch", "Auto answers"), ("--risk=3", "High risk"), ("--level=5", "Level 5"),
            ("--random-agent", "Random UA"), ("--tamper=space2comment", "WAF bypass")
        ],
        "hydra": [
            ("-l admin -P", "Single user"), ("-L users.txt -P", "User list"),
            ("-t 16", "16 tasks"), ("-V", "Verbose"), ("-f", "Stop on first"),
            ("ssh://", "SSH target"), ("ftp://", "FTP target"), ("http-post-form", "HTTP POST")
        ],
        "nikto": [
            ("-h", "Host target"), ("-ssl", "Force SSL"), ("-port 443", "Port 443"),
            ("-Tuning 1", "Interesting files"), ("-Tuning x", "XSS checks"),
            ("-o report.html", "HTML output"), ("-Format htm", "HTML format")
        ],
        "curl": [
            ("-I", "Headers only"), ("-v", "Verbose"), ("-L", "Follow redirects"),
            ("-X POST", "POST method"), ("-X PUT", "PUT method"), ("-d 'data'", "POST data"),
            ("-H 'Content-Type: application/json'", "JSON header"), ("-o file", "Save output"),
            ("-A 'Mozilla/5.0'", "User agent"), ("-k", "Insecure SSL")
        ],
        "dig": [
            ("ANY", "All records"), ("A", "A record"), ("MX", "Mail records"),
            ("NS", "Nameservers"), ("TXT", "TXT records"), ("+short", "Short output"),
            ("+trace", "Trace DNS"), ("-x", "Reverse lookup")
        ],
        "dirb": [
            ("/usr/share/wordlists/dirb/common.txt", "Common"), ("/usr/share/wordlists/dirb/big.txt", "Big"),
            ("-X .php,.html", "Extensions"), ("-w", "No warnings"),
            ("-r", "Non-recursive"), ("-z 100", "Delay 100ms")
        ],
        "wpscan": [
            ("--url", "Target URL"), ("--enumerate p", "Plugins"), ("--enumerate t", "Themes"),
            ("--enumerate u", "Users"), ("--enumerate vp", "Vuln plugins"),
            ("--api-token", "API token"), ("--force", "Force scan")
        ],
        "whatweb": [
            ("-v", "Verbose"), ("-a 3", "Aggression 3"), ("--color=never", "No color"),
            ("--log-json=out.json", "JSON output")
        ],
        "ffuf": [
            ("-u", "URL with FUZZ"), ("-w /usr/share/wordlists/dirb/common.txt", "Wordlist"),
            ("-mc 200,301", "Match codes"), ("-fc 404", "Filter 404"),
            ("-t 100", "100 threads"), ("-o out.json", "JSON output")
        ],
        "john": [
            ("--wordlist=/usr/share/wordlists/rockyou.txt", "Rockyou"), ("--format=raw-md5", "MD5"),
            ("--format=raw-sha256", "SHA256"), ("--show", "Show cracked")
        ],
        "hashcat": [
            ("-m 0", "MD5 mode"), ("-m 100", "SHA1 mode"), ("-a 0", "Dictionary attack"),
            ("-a 3", "Brute force"), ("-O", "Optimized"), ("--show", "Show cracked")
        ],
        "tcpdump": [
            ("-i any", "All interfaces"), ("-n", "No DNS resolve"), ("-v", "Verbose"),
            ("-w capture.pcap", "Save to file"), ("-r capture.pcap", "Read file"),
            ("port 80", "HTTP only"), ("host 192.168.1.1", "Filter host")
        ],
        "msfconsole": [
            ("-q", "Quiet mode"), ("-x 'use auxiliary/scanner/portscan/tcp; run'", "Run command"),
            ("-r script.rc", "Resource script")
        ],
        "aircrack-ng": [
            ("-w /usr/share/wordlists/rockyou.txt", "Wordlist"), ("-b", "BSSID target"),
            ("capture.cap", "Capture file")
        ],
        "netcat": [
            ("-lvp 4444", "Listen port"), ("-v 192.168.1.1 80", "Connect"),
            ("-e /bin/bash", "Bind shell"), ("-z 192.168.1.1 1-1000", "Port scan")
        ],
        "exiftool": [
            ("-a", "All tags"), ("-g", "Group output"), ("-csv", "CSV output"),
            ("-overwrite_original", "Overwrite")
        ],
        "strings": [
            ("-n 8", "Min length 8"), ("-t x", "Hex offset"), ("-e l", "16-bit LE")
        ],
        "ping": [
            ("-c 4", "Count 4"), ("-c 100", "Count 100"), ("-s 1000", "Packet size"),
            ("-i 0.2", "Interval 0.2s"), ("-f", "Flood")
        ],
        "traceroute": [
            ("-n", "No DNS"), ("-m 30", "Max hops 30"), ("-p 80", "Port 80"),
            ("-I", "ICMP"), ("-T", "TCP")
        ],
        "whois": [
            ("-H", "No legal"), ("-p 43", "Port"), ("-a", "ARIN lookup")
        ],
    }
    
    def __init__(self, cache_dir=None):
        self.cache_dir = cache_dir or os.path.join(os.path.dirname(__file__), '..', 'cache')
        os.makedirs(self.cache_dir, exist_ok=True)
        self.cache_file = os.path.join(self.cache_dir, 'tool_args.json')
        self._load_cache()
    
    def _load_cache(self):
        """Load cached arguments"""
        self.cache = dict(self.BUILTIN_ARGS)
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file) as f:
                    cached = json.load(f)
                    self.cache.update(cached)
            except:
                pass
    
    def _save_cache(self):
        """Save discovered arguments to cache"""
        try:
            with open(self.cache_file, 'w') as f:
                json.dump(self.cache, f, indent=2)
        except:
            pass
    
    def get_args(self, tool_name):
        """Get common arguments for a tool"""
        tool_name = tool_name.lower()
        
        # Return from cache if available
        if tool_name in self.cache:
            return self.cache[tool_name]
        
        # Auto-discover from --help
        discovered = self._discover_args(tool_name)
        if discovered:
            self.cache[tool_name] = discovered
            self._save_cache()
            return discovered
        
        return []
    
    def _discover_args(self, tool_name):
        """Try to discover arguments from tool's help output"""
        try:
            result = subprocess.run(
                f"{tool_name} --help 2>&1 | head -60",
                shell=True, capture_output=True, text=True, timeout=5
            )
            output = result.stdout.lower()
            
            args = []
            # Common patterns in help output
            import re
            
            # Find flags like -v, --verbose, -p PORT, --port PORT
            patterns = [
                r'(-\w{1,3})\s+(\w[\w\s]{2,30}?)',  # -f Description
                r'(--[\w-]+)\s+(\w[\w\s]{2,30}?)',    # --flag Description
            ]
            
            seen = set()
            for pattern in patterns:
                matches = re.findall(pattern, output)
                for flag, desc in matches[:10]:
                    if flag not in seen and len(flag) > 1:
                        args.append((flag, desc.strip()[:30]))
                        seen.add(flag)
            
            return args[:15]  # Max 15 args
        except:
            return []
    
    def refresh_tool(self, tool_name):
        """Force rediscover arguments for a tool"""
        if tool_name in self.cache:
            del self.cache[tool_name]
        return self.get_args(tool_name)
    
    def get_all_tools(self):
        """Get list of tools with cached args"""
        return list(self.cache.keys())
