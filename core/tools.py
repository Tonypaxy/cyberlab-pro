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

        
        "advanced_c2": {
            "sliver": ["sliver-client", "sliver-server"], "havoc": ["havoc"], "mythic": ["mythic-cli"],
            "cobalt_strike": ["teamserver"], "brute_ratel": ["badger"], "nimplant": ["nimplant"],
            "ares": ["ares"], "shad0w": ["shad0w"], "villain": ["villain"],
            "hoaxshell": ["hoaxshell"], "godoh": ["godoh"], "merlin": ["merlinServer"],
            "covenant": ["covenant"], "apfell": ["apfell"], "poseidon": ["poseidon"],
            "empire": ["empire"], "star_killer": ["star-killer"], "metasploit": ["msfconsole"]
        },
        "evasion_bypass": {
            "scarecrow": ["scarecrow"], "freeze": ["freeze"], "shellcode_runner": ["shellcode_runner"],
            "limelighter": ["limelighter"], "invisishell": ["invisishell"], "powershell_obfuscator": ["posh-obfuscate"],
            "xencrypt": ["xencrypt"], "confuser_ex": ["confuser"], "enigma_protector": ["enigma"],
            "vmprotect": ["vmprotect"], "the_fucking_bypasser": ["tfb"], "av_evasion_craft": ["av_evasion_craft"],
            "phantom_evasion": ["phantom-evasion"], "hyperion": ["hyperion"], "pe_cloak": ["pecloak"],
            "donut": ["donut"], "sgn": ["sgn"], "shikata_ga_nai": ["msfvenom"]
        },
        "red_team_infra": {
            "red_elk": ["red_elk"], "c2_jwso": ["c2-jwso"], "malleable_c2": ["malleable-c2"],
            "redirect_rules": ["redirect-rules"], "domain_fronting": ["domain-fronting"],
            "azure_c2": ["azure-c2"], "gcp_c2": ["gcp-c2"], "aws_c2": ["aws-c2"],
            "cloudfront_c2": ["cloudfront-c2"], "cdn_c2": ["cdn-c2"], "fastly_c2": ["fastly-c2"],
            "terraform_red": ["terraform-red"], "ansible_red": ["ansible-red"],
            "docker_red": ["docker-red"], "k8s_red": ["k8s-red"]
        },
        "initial_access": {
            "phishing_framework": ["gophish", "evilginx2", "modlishka"], "spear_phish": ["spear-phish"],
            "macro_pack": ["macro_pack"], "hack_browser_data": ["hack-browser-data"],
            "lazagne": ["lazagne"], "mimikatz": ["mimikatz"], "sharp_hound": ["sharp-hound"],
            "seatbelt": ["seatbelt"], "stand_in": ["stand-in"], "rubeus": ["rubeus"],
            "certify": ["certify"], "certipy": ["certipy"], "impacket": ["impacket"],
            "crackmapexec": ["crackmapexec"], "evil_winrm": ["evil-winrm"],
            "chisel": ["chisel"], "ligolo_ng": ["ligolo-ng"], "ngrok": ["ngrok"]
        },
        "privilege_escalation": {
            "linpeas": ["linpeas"], "winpeas": ["winpeas"], "peass_ng": ["peass-ng"],
            "linux_exploit_suggester": ["linux-exploit-suggester", "les"], "windows_exploit_suggester": ["windows-exploit-suggester"],
            "linenum": ["linenum"], "linux_priv_checker": ["linux-priv-checker"],
            "powerup": ["powerup"], "jaws": ["jaws"], "sherlock": ["sherlock"],
            "watson": ["watson"], "sweet_potato": ["sweet-potato"], "juicy_potato": ["juicy-potato"],
            "rogue_potato": ["rogue-potato"], "print_spoofer": ["print-spoofer"],
            "god_potato": ["god-potato"], "efs_potato": ["efs-potato"]
        },
        "lateral_movement": {
            "psexec": ["psexec", "psexec.py"], "wmiexec": ["wmiexec", "wmiexec.py"],
            "smbexec": ["smbexec", "smbexec.py"], "atexec": ["atexec", "atexec.py"],
            "dcomexec": ["dcomexec", "dcomexec.py"], "winrm": ["evil-winrm"],
            "rdp": ["xfreerdp"], "ssh": ["ssh"], "scp": ["scp"],
            "rsync": ["rsync"], "netsh": ["netsh"], "proxychains": ["proxychains"]
        },
        "exfiltration": {
            "dnscat2": ["dnscat2"], "iodine": ["iodine"], "dns_exfiltrator": ["dns-exfiltrator"],
            "icmp_exfil": ["icmp-exfil"], "http_exfil": ["http-exfil"], "cloakify": ["cloakify"],
            "steg_exfil": ["steg-exfil"], "dropbox_c2": ["dropbox-c2"], "gdrive_c2": ["gdrive-c2"],
            "slack_c2": ["slack-c2"], "teams_c2": ["teams-c2"], "discord_c2": ["discord-c2"],
            "twitter_c2": ["twitter-c2"], "github_c2": ["github-c2"], "pastebin_c2": ["pastebin-c2"]
        },
        "persistence": {
            "sharpersist": ["sharppersist"], "persistence_sniper": ["persistence-sniper"],
            "backdoor_factory": ["backdoor-factory"], "veil_evasion": ["veil-evasion"],
            "rootkit": ["rootkit"], "kernel_module": ["kernel-module"], "ld_preload": ["ld-preload"],
            "cron": ["crontab"], "systemd": ["systemctl"], "rc_local": ["rc-local"],
            "bashrc": ["bashrc"], "ssh_key": ["ssh-keygen"], "wmi": ["wmic"],
            "scheduled_tasks": ["schtasks"], "registry": ["reg"], "startup_folder": ["startup"]
        },
        "defense_evasion": {
            "firewall_bypass": ["firewall-bypass"], "applocker_bypass": ["applocker-bypass"],
            "amsi_bypass": ["amsi-bypass"], "etw_bypass": ["etw-bypass"],
            "wdac_bypass": ["wdac-bypass"], "uac_bypass": ["uac-bypass"],
            "dep_bypass": ["dep-bypass"], "aslr_bypass": ["aslr-bypass"],
            "cf_bypass": ["cf-bypass"], "smep_bypass": ["smep-bypass"],
            "disable_defender": ["disable-defender"], "disable_firewall": ["disable-firewall"],
            "clear_logs": ["clear-logs"], "timestomp": ["timestomp"]
        },
        "credential_access": {
            "mimikatz": ["mimikatz"], "lsassy": ["lsassy"], "nanodump": ["nanodump"],
            "procdump": ["procdump"], "sqldumper": ["sqldumper"], "sam_dump": ["sam-dump"],
            "ntds_dump": ["ntds-dump"], "kerberoast": ["kerberoast"], "asreproast": ["asreproast"],
            "hashcat": ["hashcat"], "john": ["john"], "ophcrack": ["ophcrack"],
            "rainbow_crack": ["rcrack"], "cain": ["cain"], "abel": ["abel"],
            "fgdump": ["fgdump"], "pwdump": ["pwdump"], "gsecdump": ["gsecdump"]
        },
        "collection": {
            "keylogger": ["keylogger"], "screen_capture": ["screen-capture"],
            "clipboard_monitor": ["clipboard-monitor"], "audio_capture": ["audio-capture"],
            "video_capture": ["video-capture"], "email_collector": ["email-collector"],
            "file_finder": ["file-finder"], "data_miner": ["data-miner"],
            "sensitive_file_scanner": ["sensitive-file-scanner"]
        },
        "impact_ransomware": {
            "ransomware_sim": ["ransomware-sim"], "wipers": ["wipers"],
            "disk_encryptor": ["disk-encryptor"], "mbr_wiper": ["mbr-wiper"],
            "shadow_copy_delete": ["vssadmin"], "backup_delete": ["backup-delete"],
            "service_stopper": ["service-stopper"], "process_killer": ["process-killer"]
        },
        "cloud_attacks": {
            "pacu": ["pacu"], "cloudmapper": ["cloudmapper"], "cloudsplaining": ["cloudsplaining"],
            "scoutsuite": ["scoutsuite"], "prowler": ["prowler"], "enumerate_iam": ["enumerate-iam"],
            "weird_aal": ["weirdAAL"], "s3_scanner": ["s3scanner"], "bucket_finder": ["bucket-finder"],
            "microburst": ["microburst"], "stormspotter": ["stormspotter"], "azucar": ["azucar"],
            "gcp_scanner": ["gcp-scanner"], "trivy": ["trivy"], "kube_hunter": ["kube-hunter"],
            "kube_bench": ["kube-bench"], "falco": ["falco"], "kyverno": ["kyverno"]
        },
        "ai_ml_tools": {
            "deep_exploit": ["deep-exploit"], "gym_malware": ["gym-malware"],
            "malware_rl": ["malware-rl"], "ai_fuzzer": ["ai-fuzzer"],
            "neural_crypt": ["neural-crypt"], "llm_pentest": ["llm-pentest"],
            "gpt_attack": ["gpt-attack"], "claude_exploit": ["claude-exploit"],
            "deep_phish": ["deep-phish"], "ai_voice_clone": ["ai-voice-clone"],
            "deepfake_gen": ["deepfake-gen"], "face_swap": ["face-swap"]
        },
        "quantum_crypto": {
            "pqcrypto": ["pqcrypto"], "lattice_crypt": ["lattice-crypt"],
            "hash_based_sig": ["hash-based-sig"], "code_based_crypt": ["code-based-crypt"],
            "multivariate_crypt": ["multivariate-crypt"], "isogeny_crypt": ["isogeny-crypt"],
            "quantum_key_dist": ["quantum-key-dist"], "qrng": ["qrng"]
        },
        "blockchain_web3": {
            "mythril": ["mythril"], "slither": ["slither"], "manticore": ["manticore"],
            "echidna": ["echidna"], "foundry": ["foundry"], "hardhat": ["hardhat"],
            "truffle": ["truffle"], "ganache": ["ganache"], "web3_hack": ["web3-hack"],
            "smart_contract_fuzzer": ["smart-contract-fuzzer"], "defi_exploit": ["defi-exploit"],
            "nft_exploit": ["nft-exploit"], "bridge_exploit": ["bridge-exploit"],
            "flash_loan": ["flash-loan"], "mev_bot": ["mev-bot"]
        },
        "satellite_space": {
            "satellite_tracker": ["satellite-tracker"], "ground_station": ["ground-station"],
            "sdr_receiver": ["sdr-receiver"], "signal_decoder": ["signal-decoder"],
            "telemetry_parser": ["telemetry-parser"], "space_link": ["space-link"],
            "sat_com": ["sat-com"], "orbital_hack": ["orbital-hack"],
            "iss_tracker": ["iss-tracker"], "gps_spoof": ["gps-spoof"]
        },
        
        "social_brute": {
            "sherlock": ["sherlock"], "holehe": ["holehe"], "instashell": ["instashell"],
            "instagram-brute": ["instagram-brute"], "facebook-brute": ["facebook-brute"],
            "twitter-brute": ["twitter-brute"], "tiktok-brute": ["tiktok-brute"],
            "snapchat-brute": ["snapchat-brute"], "linkedin-brute": ["linkedin-brute"],
            "github-brute": ["github-brute"], "reddit-brute": ["reddit-brute"],
            "pinterest-brute": ["pinterest-brute"], "tumblr-brute": ["tumblr-brute"],
            "spotify-brute": ["spotify-brute"], "netflix-brute": ["netflix-brute"],
            "hulu-brute": ["hulu-brute"], "amazon-brute": ["amazon-brute"],
            "paypal-brute": ["paypal-brute"], "ebay-brute": ["ebay-brute"],
            "wordpress-brute": ["wordpress-brute"], "joomla-brute": ["joomla-brute"],
            "drupal-brute": ["drupal-brute"], "magento-brute": ["magento-brute"],
            "prestashop-brute": ["prestashop-brute"],
        },

        "biometric_hack": {
            "fingerprint_spoof": ["fingerprint-spoof"], "face_recog_bypass": ["face-recog-bypass"],
            "iris_spoof": ["iris-spoof"], "voice_spoof": ["voice-spoof"],
            "gait_bypass": ["gait-bypass"], "vein_spoof": ["vein-spoof"],
            "dna_spoof": ["dna-spoof"], "heartbeat_spoof": ["heartbeat-spoof"]
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
