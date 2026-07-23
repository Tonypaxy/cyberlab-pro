import subprocess
import shutil
import os

class ToolDetector:
    KNOWN_TOOLS = {
        "recon": {
            "nmap": ["nmap"], "gobuster": ["gobuster"], "httpx": ["httpx"],
            "subfinder": ["subfinder"], "assetfinder": ["assetfinder"],
            "gau": ["gau"], "waybackurls": ["waybackurls"],
            "massdns": ["massdns"], "sublist3r": ["sublist3r"],
            "dig": ["dig"], "whois": ["whois"], "traceroute": ["traceroute"],
            "ping": ["ping"], "sqlmap": ["sqlmap"], "dnsenum": ["dnsenum"],
            "fierce": ["fierce"], "amass": ["amass"], "ffuf": ["ffuf"],
            "dirsearch": ["dirsearch"]
        },
        "web": {
            "curl": ["curl"], "sqlmap": ["sqlmap"], "nikto": ["nikto"],
            "dirb": ["dirb"], "whatweb": ["whatweb"], "wpscan": ["wpscan"],
            "wfuzz": ["wfuzz"], "commix": ["commix"], "xsser": ["xsser"]
        },
        "network": {
            "netcat": ["nc", "netcat"], "nmap": ["nmap"], "tcpdump": ["tcpdump"],
            "tshark": ["tshark"], "ettercap": ["ettercap"], "bettercap": ["bettercap"],
            "arp-scan": ["arp-scan"], "masscan": ["masscan"], "rustscan": ["rustscan"]
        },
        "credentials": {
            "hydra": ["hydra"], "john": ["john"], "hashcat": ["hashcat"],
            "crunch": ["crunch"], "cewl": ["cewl"], "medusa": ["medusa"]
        },
        "wireless": {
            "aircrack-ng": ["aircrack-ng"], "airmon-ng": ["airmon-ng"],
            "airodump-ng": ["airodump-ng"], "reaver": ["reaver"], "pixiewps": ["pixiewps"]
        },
        "forensics": {
            "binwalk": ["binwalk"], "foremost": ["foremost"], "strings": ["strings"],
            "exiftool": ["exiftool"], "steghide": ["steghide"], "zsteg": ["zsteg"]
        },
        
        
        "phishing_social": {
            "setoolkit": ["setoolkit"], "socialfish": ["socialfish"], "zphisher": ["zphisher"],
            "blackeye": ["blackeye"], "gophish": ["gophish"], "evilginx2": ["evilginx2"],
            "modlishka": ["modlishka"], "muraena": ["muraena"], "king-phisher": ["king-phisher"]
        },
        "osint": {
            "sherlock": ["sherlock"], "holehe": ["holehe"], "theHarvester": ["theHarvester"],
            "recon-ng": ["recon-ng"], "spiderfoot": ["spiderfoot"], "twint": ["twint"],
            "instaloader": ["instaloader"], "facebook-scraper": ["facebook-scraper"],
            "tiktok-scraper": ["tiktok-scraper"]
        },
        "wifi_bluetooth": {
            "bettercap": ["bettercap"], "kismet": ["kismet"], "fluxion": ["fluxion"],
            "wifite": ["wifite"], "pixiewps": ["pixiewps"], "reaver": ["reaver"],
            "bluetoothctl": ["bluetoothctl"], "hcitool": ["hcitool"]
        },
        "web_exploit": {
            "burpsuite": ["burpsuite"], "zap": ["zap"], "commix": ["commix"],
            "xsser": ["xsser"], "xsstrike": ["xsstrike"], "nosqlmap": ["nosqlmap"]
        },
        "android_hacking": {
            "msfvenom": ["msfvenom"], "apktool": ["apktool"], "jadx": ["jadx"],
            "dex2jar": ["dex2jar"], "androguard": ["androguard"]
        },
        "voip": {
            "sipvicious": ["sipvicious", "svmap", "svwar", "svcrack"],
            "voiphopper": ["voiphopper"]
        },
        "hash_crypto": {
            "md5sum": ["md5sum"], "sha256sum": ["sha256sum"], "sha1sum": ["sha1sum"],
            "base64": ["base64"], "xxd": ["xxd"], "openssl": ["openssl"]
        },
        "stegano": {
            "steghide": ["steghide"], "zsteg": ["zsteg"], "stegsolve": ["stegsolve"],
            "stegcracker": ["stegcracker"], "binwalk": ["binwalk"], "foremost": ["foremost"],
            "strings": ["strings"], "exiftool": ["exiftool"], "bulk_extractor": ["bulk_extractor"]
        },
        "dos": {
            "hping3": ["hping3"], "slowloris": ["slowloris"], "goldeneye": ["goldeneye"],
            "ab": ["ab"], "siege": ["siege"]
        },
        "secure_delete": {
            "shred": ["shred"], "wipe": ["wipe"], "dd": ["dd"], "srm": ["srm"]
        },
        "malware_analysis": {
            "clamscan": ["clamscan"], "lynis": ["lynis"], "chkrootkit": ["chkrootkit"],
            "rkhunter": ["rkhunter"], "testssl.sh": ["testssl.sh"], "sslscan": ["sslscan"],
            "sslyze": ["sslyze"]
        },
        
        "social_engineering": {
            "setoolkit": ["setoolkit"], "zphisher": ["zphisher"], "blackeye": ["blackeye"],
            "socialfish": ["socialfish"], "gophish": ["gophish"], "evilginx2": ["evilginx2"],
            "modlishka": ["modlishka"], "muraena": ["muraena"], "king-phisher": ["king-phisher"],
            "swaks": ["swaks"], "sendemail": ["sendEmail", "sendemail"], "mail": ["mail"]
        },
        "osint": {
            "sherlock": ["sherlock"], "holehe": ["holehe"], "theHarvester": ["theHarvester"],
            "recon-ng": ["recon-ng"], "spiderfoot": ["spiderfoot"], "twint": ["twint"],
            "instaloader": ["instaloader"], "facebook-scraper": ["facebook-scraper"],
            "tiktok-scraper": ["tiktok-scraper"], "subfinder": ["subfinder"],
            "assetfinder": ["assetfinder"], "gau": ["gau"], "waybackurls": ["waybackurls"],
            "amass": ["amass"], "dnsrecon": ["dnsrecon"], "whois": ["whois"]
        },
        "crypto_stego": {
            "steghide": ["steghide"], "zsteg": ["zsteg"], "stegcracker": ["stegcracker"],
            "outguess": ["outguess"], "openstego": ["openstego"], "stegsolve": ["stegsolve"],
            "binwalk": ["binwalk"], "foremost": ["foremost"], "exiftool": ["exiftool"],
            "strings": ["strings"], "qrencode": ["qrencode"], "gpg": ["gpg"],
            "openssl": ["openssl"], "base64": ["base64"]
        },
        "reverse_engineering": {
            "objdump": ["objdump"], "radare2": ["r2"], "rizin": ["rizin"],
            "ghidra": ["ghidra"], "jadx": ["jadx"], "apktool": ["apktool"],
            "dex2jar": ["dex2jar", "d2j-dex2jar"], "readelf": ["readelf"],
            "strace": ["strace"], "ltrace": ["ltrace"], "nm": ["nm"],
            "ldd": ["ldd"], "strings": ["strings"], "xxd": ["xxd"],
            "hexdump": ["hexdump"], "file": ["file"]
        },
        "api_testing": {
            "curl": ["curl"], "wget": ["wget"], "ffuf": ["ffuf"], "arjun": ["arjun"],
            "kiterunner": ["kiterunner"], "nmap": ["nmap"], "sqlmap": ["sqlmap"]
        },

        "programming": {
            "python": ["python3"], "go": ["go"], "git": ["git"], "ruby": ["ruby"],
            "perl": ["perl"], "php": ["php"], "node": ["node"], "gcc": ["gcc"], "make": ["make"]
        },
        "exploitation": {
            "metasploit": ["msfconsole"], "searchsploit": ["searchsploit"],
            "setoolkit": ["setoolkit"], "beef": ["beef-xss"]
        }
    }
    
    def __init__(self):
        self.detected = {}
        # Add go/bin to search paths
        go_path = os.path.expanduser('~/go/bin')
        self._search_paths = [
            '/data/data/com.termux/files/usr/bin',
            '/data/data/com.termux/files/home/go/bin',
            go_path,
            '/usr/bin', '/usr/local/bin', '/usr/sbin'
        ]
        # Also add to system PATH for subprocess
        os.environ['PATH'] = ':'.join(self._search_paths) + ':' + os.environ.get('PATH', '')
    
    def detect_all(self):
        for category, tools in self.KNOWN_TOOLS.items():
            self.detected[category] = []
            for name, commands in tools.items():
                tool_info = self._detect_tool(name, commands)
                if tool_info:
                    self.detected[category].append(tool_info)
        return self.detected
    
    def _detect_tool(self, name, commands):
        for cmd in commands:
            path = shutil.which(cmd)
            if not path:
                for base in self._search_paths:
                    full = os.path.join(base, cmd)
                    if os.path.isfile(full) and os.access(full, os.X_OK):
                        path = full
                        break
            if not path:
                try:
                    result = subprocess.run(['command', '-v', cmd], capture_output=True, text=True, timeout=3)
                    if result.returncode == 0 and result.stdout.strip():
                        path = result.stdout.strip()
                except:
                    pass
            if path:
                version = self._get_version(cmd)
                return {'name': name, 'command': cmd, 'path': path, 'version': version or 'installed'}
        return None
    
    def _get_version(self, command):
        for flag in ['--version', '-v', '-V', 'version']:
            try:
                result = subprocess.run(f"{command} {flag} 2>&1 | head -1", shell=True,
                        capture_output=True, text=True, timeout=5)
                output = result.stdout.strip() or result.stderr.strip()
                if output and len(output) > 2 and len(output) < 100:
                    return output[:80]
            except:
                pass
        return None
    
    def get_total_count(self):
        return sum(len(v) for v in self.detected.values())
    
    def get_installed_tools(self):
        tools = []
        for cat_tools in self.detected.values():
            for t in cat_tools:
                tools.append(t['name'])
        return sorted(tools)
    
    def is_installed(self, tool_name):
        for cat_tools in self.detected.values():
            for t in cat_tools:
                if t['name'] == tool_name:
                    return True
        return False
    
    def get_missing_tools(self):
        missing = []
        for category, tools in self.KNOWN_TOOLS.items():
            installed_names = [t['name'] for t in self.detected.get(category, [])]
            for name in tools:
                if name not in installed_names:
                    missing.append({'name': name, 'category': category})
        return missing

    def refresh_args_for_new_tools(self):
        """Auto-discover arguments for newly installed tools"""
        try:
            from core.tool_args import ToolArgsDatabase
            args_db = ToolArgsDatabase()
            all_tools = self.get_installed_tools()
            discovered = args_db.discover_all_installed(all_tools)
            return discovered
        except:
            return 0
