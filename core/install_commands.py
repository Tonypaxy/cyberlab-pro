"""CyberLab Pro - Smart Install Commands by Environment"""
import os
import platform

def detect_environment():
    """Detect current environment"""
    if os.path.exists('/data/data/com.termux/files/usr/bin/bash'):
        return 'termux'
    elif os.path.exists('/usr/bin/apt') or os.path.exists('/usr/bin/apt-get'):
        return 'debian'
    elif os.path.exists('/usr/bin/pacman'):
        return 'arch'
    elif os.path.exists('/usr/bin/dnf'):
        return 'fedora'
    elif os.path.exists('/usr/bin/zypper'):
        return 'suse'
    elif platform.system() == 'Darwin':
        return 'macos'
    else:
        return 'linux'

ENV = detect_environment()

INSTALL_COMMANDS = {
    # === TERMUX ===
    'termux': {
        "nmap": {"pkg": "pkg install nmap -y"},
        "hydra": {"pkg": "pkg install hydra -y"},
        "sqlmap": {"pip": "pip install sqlmap", "git": "git clone --depth 1 https://github.com/sqlmapproject/sqlmap.git ~/sqlmap"},
        "nikto": {"git": "git clone --depth 1 https://github.com/sullo/nikto.git ~/nikto"},
        "gobuster": {"go": "go install github.com/OJ/gobuster/v3@latest"},
        "wpscan": {"gem": "gem install wpscan", "pkg": "pkg install ruby -y && gem install wpscan"},
        "dirb": {"pkg": "pkg install dirb -y"},
        "whatweb": {"pkg": "pkg install whatweb -y"},
        "john": {"pkg": "pkg install john -y"},
        "hashcat": {"pkg": "pkg install hashcat -y"},
        "crunch": {"pkg": "pkg install crunch -y"},
        "aircrack-ng": {"pkg": "pkg install aircrack-ng -y"},
        "tcpdump": {"pkg": "pkg install tcpdump -y"},
        "exiftool": {"pkg": "pkg install exiftool -y"},
        "steghide": {"pkg": "pkg install steghide -y"},
        "binwalk": {"pkg": "pkg install binwalk -y"},
        "foremost": {"pkg": "pkg install foremost -y"},
        "strings": {"pkg": "pkg install binutils -y"},
        "metasploit": {"pkg": "pkg install unstable-repo -y && pkg install metasploit -y"},
        "ettercap": {"pkg": "pkg install ettercap -y"},
        "netcat": {"pkg": "pkg install netcat-openbsd -y"},
        "curl": {"pkg": "pkg install curl -y"},
        "wget": {"pkg": "pkg install wget -y"},
        "git": {"pkg": "pkg install git -y"},
        "python": {"pkg": "pkg install python -y"},
        "go": {"pkg": "pkg install golang -y"},
        "ruby": {"pkg": "pkg install ruby -y"},
        "perl": {"pkg": "pkg install perl -y"},
        "php": {"pkg": "pkg install php -y"},
        "node": {"pkg": "pkg install nodejs -y"},
        "gcc": {"pkg": "pkg install clang -y"},
        "make": {"pkg": "pkg install make -y"},
        "subfinder": {"go": "go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest"},
        "httpx": {"go": "go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest"},
        "assetfinder": {"go": "go install github.com/tomnomnom/assetfinder@latest"},
        "gau": {"go": "go install github.com/lc/gau/v2/cmd/gau@latest"},
        "waybackurls": {"go": "go install github.com/tomnomnom/waybackurls@latest"},
        "ffuf": {"go": "go install github.com/ffuf/ffuf/v2@latest"},
        "amass": {"pkg": "pkg install amass -y"},
        "massdns": {"git": "git clone --depth 1 https://github.com/blechschmidt/massdns.git ~/massdns && cd ~/massdns && make"},
        "sublist3r": {"git": "git clone --depth 1 https://github.com/aboul3la/Sublist3r.git ~/Sublist3r && cd ~/Sublist3r && pip install -r requirements.txt"},
        "dirsearch": {"git": "git clone --depth 1 https://github.com/maurosoria/dirsearch.git ~/dirsearch"},
        "commix": {"git": "git clone --depth 1 https://github.com/commixproject/commix.git ~/commix"},
        "xsser": {"git": "git clone --depth 1 https://github.com/epsylon/xsser.git ~/xsser"},
        "wfuzz": {"pip": "pip install wfuzz"},
        "fierce": {"pip": "pip install fierce"},
        "searchsploit": {"pkg": "pkg install exploitdb -y"},
        "cewl": {"gem": "gem install cewl"},
        "zsteg": {"gem": "gem install zsteg"},
        "bettercap": {"pkg": "pkg install bettercap -y"},
        "rustscan": {"pkg": "pkg install rustscan -y"},
        "masscan": {"pkg": "pkg install masscan -y"},
        "arp-scan": {"pkg": "pkg install arp-scan -y"},
        "tshark": {"pkg": "pkg install tshark -y"},
        "reaver": {"pkg": "pkg install reaver -y"},
        "pixiewps": {"pkg": "pkg install pixiewps -y"},
        "beef": {"gem": "gem install beef-xss"},
        "setoolkit": {"git": "git clone --depth 1 https://github.com/trustedsec/social-engineer-toolkit.git ~/setoolkit"},
        "medusa": {"pkg": "pkg install medusa -y"},
        "dnsenum": {"git": "git clone --depth 1 https://github.com/fwaeytens/dnsenum.git ~/dnsenum"},
    },
    
    # === DEBIAN / UBUNTU / KALI / PARROT ===
    'debian': {
        "nmap": {"apt": "sudo apt install nmap -y"},
        "hydra": {"apt": "sudo apt install hydra -y"},
        "sqlmap": {"apt": "sudo apt install sqlmap -y", "pip": "pip install sqlmap", "git": "git clone --depth 1 https://github.com/sqlmapproject/sqlmap.git ~/sqlmap"},
        "nikto": {"apt": "sudo apt install nikto -y", "git": "git clone --depth 1 https://github.com/sullo/nikto.git ~/nikto"},
        "gobuster": {"apt": "sudo apt install gobuster -y", "go": "go install github.com/OJ/gobuster/v3@latest"},
        "wpscan": {"apt": "sudo apt install wpscan -y", "gem": "gem install wpscan"},
        "dirb": {"apt": "sudo apt install dirb -y"},
        "whatweb": {"apt": "sudo apt install whatweb -y"},
        "john": {"apt": "sudo apt install john -y"},
        "hashcat": {"apt": "sudo apt install hashcat -y"},
        "crunch": {"apt": "sudo apt install crunch -y"},
        "aircrack-ng": {"apt": "sudo apt install aircrack-ng -y"},
        "tcpdump": {"apt": "sudo apt install tcpdump -y"},
        "exiftool": {"apt": "sudo apt install exiftool -y"},
        "steghide": {"apt": "sudo apt install steghide -y"},
        "binwalk": {"apt": "sudo apt install binwalk -y"},
        "foremost": {"apt": "sudo apt install foremost -y"},
        "strings": {"apt": "sudo apt install binutils -y"},
        "metasploit": {"apt": "sudo apt install metasploit-framework -y"},
        "ettercap": {"apt": "sudo apt install ettercap-graphical -y"},
        "netcat": {"apt": "sudo apt install netcat-openbsd -y"},
        "curl": {"apt": "sudo apt install curl -y"},
        "wget": {"apt": "sudo apt install wget -y"},
        "git": {"apt": "sudo apt install git -y"},
        "python": {"apt": "sudo apt install python3 -y"},
        "go": {"apt": "sudo apt install golang -y"},
        "ruby": {"apt": "sudo apt install ruby -y"},
        "perl": {"apt": "sudo apt install perl -y"},
        "php": {"apt": "sudo apt install php -y"},
        "node": {"apt": "sudo apt install nodejs -y"},
        "gcc": {"apt": "sudo apt install gcc -y"},
        "make": {"apt": "sudo apt install make -y"},
        "subfinder": {"go": "go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest"},
        "httpx": {"go": "go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest"},
        "assetfinder": {"go": "go install github.com/tomnomnom/assetfinder@latest"},
        "gau": {"go": "go install github.com/lc/gau/v2/cmd/gau@latest"},
        "waybackurls": {"go": "go install github.com/tomnomnom/waybackurls@latest"},
        "ffuf": {"apt": "sudo apt install ffuf -y", "go": "go install github.com/ffuf/ffuf/v2@latest"},
        "amass": {"apt": "sudo apt install amass -y"},
        "wfuzz": {"apt": "sudo apt install wfuzz -y", "pip": "pip install wfuzz"},
        "fierce": {"apt": "sudo apt install fierce -y", "pip": "pip install fierce"},
        "searchsploit": {"apt": "sudo apt install exploitdb -y"},
        "cewl": {"apt": "sudo apt install cewl -y", "gem": "gem install cewl"},
        "zsteg": {"gem": "gem install zsteg"},
        "bettercap": {"apt": "sudo apt install bettercap -y"},
        "masscan": {"apt": "sudo apt install masscan -y"},
        "arp-scan": {"apt": "sudo apt install arp-scan -y"},
        "tshark": {"apt": "sudo apt install tshark -y"},
        "reaver": {"apt": "sudo apt install reaver -y"},
        "beef": {"apt": "sudo apt install beef-xss -y"},
        "setoolkit": {"apt": "sudo apt install setoolkit -y"},
        "medusa": {"apt": "sudo apt install medusa -y"},
        "dnsenum": {"apt": "sudo apt install dnsenum -y"},
        "burpsuite": {"apt": "sudo apt install burpsuite -y"},
        "zap": {"apt": "sudo apt install zaproxy -y"},
        "wireshark": {"apt": "sudo apt install wireshark -y"},
    },
    
    # === ARCH / MANJARO ===
    'arch': {
        "nmap": {"pacman": "sudo pacman -S nmap --noconfirm"},
        "hydra": {"pacman": "sudo pacman -S hydra --noconfirm"},
        "sqlmap": {"pacman": "sudo pacman -S sqlmap --noconfirm", "pip": "pip install sqlmap"},
        "nikto": {"pacman": "sudo pacman -S nikto --noconfirm"},
        "gobuster": {"pacman": "sudo pacman -S gobuster --noconfirm", "go": "go install github.com/OJ/gobuster/v3@latest"},
        "wpscan": {"gem": "gem install wpscan"},
        "dirb": {"pacman": "sudo pacman -S dirb --noconfirm"},
        "john": {"pacman": "sudo pacman -S john --noconfirm"},
        "hashcat": {"pacman": "sudo pacman -S hashcat --noconfirm"},
        "aircrack-ng": {"pacman": "sudo pacman -S aircrack-ng --noconfirm"},
        "tcpdump": {"pacman": "sudo pacman -S tcpdump --noconfirm"},
        "exiftool": {"pacman": "sudo pacman -S exiftool --noconfirm"},
        "metasploit": {"pacman": "sudo pacman -S metasploit --noconfirm"},
        "netcat": {"pacman": "sudo pacman -S gnu-netcat --noconfirm"},
        "curl": {"pacman": "sudo pacman -S curl --noconfirm"},
        "git": {"pacman": "sudo pacman -S git --noconfirm"},
        "go": {"pacman": "sudo pacman -S go --noconfirm"},
        "ffuf": {"pacman": "sudo pacman -S ffuf --noconfirm", "go": "go install github.com/ffuf/ffuf/v2@latest"},
        "amass": {"pacman": "sudo pacman -S amass --noconfirm"},
        "bettercap": {"pacman": "sudo pacman -S bettercap --noconfirm"},
        "burpsuite": {"pacman": "sudo pacman -S burpsuite --noconfirm"},
        "wireshark": {"pacman": "sudo pacman -S wireshark-qt --noconfirm"},
    },
    
    # === FEDORA ===
    'fedora': {
        "nmap": {"dnf": "sudo dnf install nmap -y"},
        "hydra": {"dnf": "sudo dnf install hydra -y"},
        "sqlmap": {"dnf": "sudo dnf install sqlmap -y", "pip": "pip install sqlmap"},
        "nikto": {"dnf": "sudo dnf install nikto -y"},
        "gobuster": {"dnf": "sudo dnf install gobuster -y", "go": "go install github.com/OJ/gobuster/v3@latest"},
        "john": {"dnf": "sudo dnf install john -y"},
        "hashcat": {"dnf": "sudo dnf install hashcat -y"},
        "aircrack-ng": {"dnf": "sudo dnf install aircrack-ng -y"},
        "tcpdump": {"dnf": "sudo dnf install tcpdump -y"},
        "metasploit": {"dnf": "sudo dnf install metasploit -y"},
        "curl": {"dnf": "sudo dnf install curl -y"},
        "git": {"dnf": "sudo dnf install git -y"},
        "go": {"dnf": "sudo dnf install golang -y"},
        "ffuf": {"dnf": "sudo dnf install ffuf -y", "go": "go install github.com/ffuf/ffuf/v2@latest"},
        "wireshark": {"dnf": "sudo dnf install wireshark -y"},
    },
}

def get_install_cmd(tool_name, method='auto'):
    """Get install command for tool based on current environment"""
    env_cmds = INSTALL_COMMANDS.get(ENV, INSTALL_COMMANDS['termux'])
    
    if tool_name in env_cmds:
        tool_cmds = env_cmds[tool_name]
        if method == 'auto':
            return list(tool_cmds.values())[0]
        return tool_cmds.get(method, list(tool_cmds.values())[0])
    
    # Default fallback based on environment
    defaults = {
        'termux': f"pkg install {tool_name} -y || pip install {tool_name}",
        'debian': f"sudo apt install {tool_name} -y || pip install {tool_name}",
        'arch': f"sudo pacman -S {tool_name} --noconfirm || pip install {tool_name}",
        'fedora': f"sudo dnf install {tool_name} -y || pip install {tool_name}",
    }
    return defaults.get(ENV, defaults['termux'])

def get_available_methods(tool_name):
    """Get available install methods for a tool in current environment"""
    env_cmds = INSTALL_COMMANDS.get(ENV, INSTALL_COMMANDS['termux'])
    if tool_name in env_cmds:
        return list(env_cmds[tool_name].keys())
    return ['auto']

def get_env_name():
    """Get human-readable environment name"""
    names = {
        'termux': 'Termux (Android)',
        'debian': 'Debian/Ubuntu/Kali',
        'arch': 'Arch/Manjaro',
        'fedora': 'Fedora/RHEL',
        'suse': 'openSUSE',
        'macos': 'macOS',
        'linux': 'Linux'
    }
    return names.get(ENV, 'Linux')
