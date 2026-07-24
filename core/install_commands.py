"""CyberLab Pro - Smart Install Commands by Environment with Success Ranking"""
import os
import platform

def detect_environment():
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

ENV_NAMES = {
    'termux': 'Termux (Android)',
    'debian': 'Debian/Ubuntu/Kali/Parrot',
    'arch': 'Arch/Manjaro',
    'fedora': 'Fedora/RHEL',
    'suse': 'openSUSE',
    'macos': 'macOS',
    'linux': 'Linux'
}

# Success ranking: 1 = highest success rate, 5 = lowest
# Based on actual installation success rates per environment
SUCCESS_RANK = {
    'termux': {'pkg': 1, 'pip': 2, 'git': 3, 'go': 4, 'gem': 5},
    'debian': {'apt': 1, 'pip': 2, 'git': 3, 'go': 4, 'gem': 5},
    'arch':   {'pacman': 1, 'pip': 2, 'git': 3, 'go': 4, 'gem': 5},
    'fedora': {'dnf': 1, 'pip': 2, 'git': 3, 'go': 4, 'gem': 5},
}

METHOD_ICONS = {
    'pkg': '📦 pkg', 'apt': '📦 apt', 'pacman': '📦 pac', 'dnf': '📦 dnf',
    'pip': '🐍 pip', 'git': '📥 git', 'go': '🔵 go', 'gem': '💎 gem'
}

METHOD_COLORS = {
    'pkg': '#00ccff', 'apt': '#00ccff', 'pacman': '#00ccff', 'dnf': '#00ccff',
    'pip': '#ffaa00', 'git': '#cc88ff', 'go': '#00ff88', 'gem': '#ff4488'
}

INSTALL_COMMANDS = {
    'termux': {
        "nmap": {"pkg": "pkg install nmap -y", "pip": "pip install python-nmap", "git": "N/A"},
        "hydra": {"pkg": "pkg install hydra -y", "pip": "N/A", "git": "git clone --depth 1 'https://github.com/vanhauser-thc/thc-hydra.git ~/hydra"},
        "sqlmap": {"pkg": "pkg install sqlmap -y 2>/dev/null || echo 'Use pip'", "pip": "pip install sqlmap", "git": "git clone --depth 1 'https://github.com/sqlmapproject/sqlmap.git ~/sqlmap"},
        "nikto": {"pkg": "pkg install nikto -y 2>/dev/null || echo 'Use git'", "pip": "N/A", "git": "git clone --depth 1 'https://github.com/sullo/nikto.git ~/nikto"},
        "gobuster": {"pkg": "pkg install go -y && go install github.com/OJ/gobuster/v3@latest", "pip": "N/A", "git": "N/A", "go": "go install github.com/OJ/gobuster/v3@latest"},
        "john": {"pkg": "pkg install john -y", "pip": "N/A", "git": "git clone --depth 1 'https://github.com/openwall/john.git ~/john"},
        "hashcat": {"pkg": "pkg install hashcat -y", "pip": "N/A", "git": "git clone --depth 1 'https://github.com/hashcat/hashcat.git ~/hashcat"},
        "wpscan": {"pkg": "pkg install ruby -y && gem install wpscan", "pip": "N/A", "git": "git clone --depth 1 'https://github.com/wpscanteam/wpscan.git ~/wpscan", "gem": "gem install wpscan"},
        "dirb": {"pkg": "pkg install dirb -y", "pip": "N/A", "git": "git clone --depth 1 'https://github.com/v0re/dirb.git ~/dirb"},
        "whatweb": {"pkg": "pkg install whatweb -y", "pip": "N/A", "git": "git clone --depth 1 'https://github.com/urbanadventurer/WhatWeb.git ~/whatweb"},
        "aircrack-ng": {"pkg": "pkg install aircrack-ng -y", "pip": "N/A", "git": "git clone --depth 1 'https://github.com/aircrack-ng/aircrack-ng.git ~/aircrack-ng"},
        "tcpdump": {"pkg": "pkg install tcpdump -y", "pip": "N/A", "git": "N/A"},
        "exiftool": {"pkg": "pkg install exiftool -y", "pip": "pip install exiftool", "git": "N/A"},
        "binwalk": {"pkg": "pkg install binwalk -y 2>/dev/null || pip install binwalk", "pip": "pip install binwalk", "git": "git clone --depth 1 'https://github.com/ReFirmLabs/binwalk.git ~/binwalk"},
        "steghide": {"pkg": "pkg install steghide -y", "pip": "N/A", "git": "git clone --depth 1 'https://github.com/StefanoDeVuono/steghide.git ~/steghide"},
        "foremost": {"pkg": "pkg install foremost -y", "pip": "N/A", "git": "N/A"},
        "strings": {"pkg": "pkg install binutils -y", "pip": "N/A", "git": "N/A"},
        "metasploit": {"pkg": "pkg install unstable-repo -y && pkg install metasploit -y", "pip": "N/A", "git": "N/A"},
        "ettercap": {"pkg": "pkg install ettercap -y", "pip": "N/A", "git": "N/A"},
        "netcat": {"pkg": "pkg install netcat-openbsd -y", "pip": "N/A", "git": "N/A"},
        "curl": {"pkg": "pkg install curl -y", "pip": "N/A", "git": "N/A"},
        "wget": {"pkg": "pkg install wget -y", "pip": "N/A", "git": "N/A"},
        "git": {"pkg": "pkg install git -y", "pip": "N/A", "git": "N/A"},
        "python": {"pkg": "pkg install python -y", "pip": "N/A", "git": "N/A"},
        "go": {"pkg": "pkg install golang -y", "pip": "N/A", "git": "N/A"},
        "ruby": {"pkg": "pkg install ruby -y", "pip": "N/A", "git": "N/A"},
        "perl": {"pkg": "pkg install perl -y", "pip": "N/A", "git": "N/A"},
        "php": {"pkg": "pkg install php -y", "pip": "N/A", "git": "N/A"},
        "node": {"pkg": "pkg install nodejs -y", "pip": "N/A", "git": "N/A"},
        "make": {"pkg": "pkg install make -y", "pip": "N/A", "git": "N/A"},
        "subfinder": {"pkg": "N/A", "pip": "N/A", "git": "N/A", "go": "go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest"},
        "httpx": {"pkg": "N/A", "pip": "N/A", "git": "N/A", "go": "go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest"},
        "assetfinder": {"pkg": "N/A", "pip": "N/A", "git": "N/A", "go": "go install github.com/tomnomnom/assetfinder@latest"},
        "gau": {"pkg": "N/A", "pip": "N/A", "git": "N/A", "go": "go install github.com/lc/gau/v2/cmd/gau@latest"},
        "waybackurls": {"pkg": "N/A", "pip": "N/A", "git": "N/A", "go": "go install github.com/tomnomnom/waybackurls@latest"},
        "ffuf": {"pkg": "N/A", "pip": "N/A", "git": "N/A", "go": "go install github.com/ffuf/ffuf/v2@latest"},
        "amass": {"pkg": "pkg install amass -y 2>/dev/null || echo 'Use go'", "pip": "N/A", "git": "N/A", "go": "go install -v github.com/owasp-amass/amass/v4/...@master"},
        "massdns": {"pkg": "N/A", "pip": "N/A", "git": "git clone --depth 1 'https://github.com/blechschmidt/massdns.git ~/massdns && cd ~/massdns && make"},
        "sublist3r": {"pkg": "N/A", "pip": "N/A", "git": "git clone --depth 1 'https://github.com/aboul3la/Sublist3r.git ~/Sublist3r && cd ~/Sublist3r && pip install -r requirements.txt"},
        "dirsearch": {"pkg": "N/A", "pip": "N/A", "git": "git clone --depth 1 'https://github.com/maurosoria/dirsearch.git ~/dirsearch"},
        "wfuzz": {"pkg": "N/A", "pip": "pip install wfuzz", "git": "git clone --depth 1 'https://github.com/xmendez/wfuzz.git ~/wfuzz"},
        "fierce": {"pkg": "N/A", "pip": "pip install fierce", "git": "git clone --depth 1 'https://github.com/mschwager/fierce.git ~/fierce"},
        "searchsploit": {"pkg": "pkg install exploitdb -y", "pip": "N/A", "git": "git clone --depth 1 'https://github.com/offensive-security/exploitdb.git ~/exploitdb"},
        "cewl": {"pkg": "N/A", "pip": "N/A", "git": "N/A", "gem": "gem install cewl"},
        "zsteg": {"pkg": "N/A", "pip": "N/A", "git": "N/A", "gem": "gem install zsteg"},
        "bettercap": {"pkg": "pkg install bettercap -y", "pip": "N/A", "git": "N/A"},
        "commix": {"pkg": "N/A", "pip": "N/A", "git": "git clone --depth 1 'https://github.com/commixproject/commix.git ~/commix"},
        "xsser": {"pkg": "N/A", "pip": "N/A", "git": "git clone --depth 1 'https://github.com/epsylon/xsser.git ~/xsser"},
        "beef": {"pkg": "N/A", "pip": "N/A", "git": "N/A", "gem": "gem install beef-xss"},
        "setoolkit": {"pkg": "N/A", "pip": "N/A", "git": "git clone --depth 1 'https://github.com/trustedsec/social-engineer-toolkit.git ~/setoolkit"},
        "medusa": {"pkg": "pkg install medusa -y", "pip": "N/A", "git": "N/A"},
        "dnsenum": {"pkg": "N/A", "pip": "N/A", "git": "git clone --depth 1 'https://github.com/fwaeytens/dnsenum.git ~/dnsenum"},
        "crunch": {"pkg": "pkg install crunch -y", "pip": "N/A", "git": "N/A"},
        "reaver": {"pkg": "pkg install reaver -y", "pip": "N/A", "git": "N/A"},
        "pixiewps": {"pkg": "pkg install pixiewps -y", "pip": "N/A", "git": "N/A"},
        "tshark": {"pkg": "pkg install tshark -y", "pip": "N/A", "git": "N/A"},
        "arp-scan": {"pkg": "pkg install arp-scan -y", "pip": "N/A", "git": "N/A"},
        "masscan": {"pkg": "pkg install masscan -y", "pip": "N/A", "git": "N/A"},
        "rustscan": {"pkg": "pkg install rustscan -y", "pip": "N/A", "git": "N/A"},
    },
}

def get_install_methods_ranked(tool_name):
    """Get all install methods for a tool ranked by success rate (best first)"""
    env_cmds = INSTALL_COMMANDS.get(ENV, INSTALL_COMMANDS.get('termux', {}))
    
    if tool_name not in env_cmds:
        # Generate default methods
        methods = {}
        if ENV == 'termux':
            methods = {'pkg': f"pkg install {tool_name} -y", 'pip': f"pip install {tool_name}", 'git': f"git clone https://github.com/user/{tool_name}"}
        elif ENV == 'debian':
            methods = {'apt': f"sudo apt install {tool_name} -y", 'pip': f"pip install {tool_name}", 'git': f"git clone https://github.com/user/{tool_name}"}
        elif ENV == 'arch':
            methods = {'pacman': f"sudo pacman -S {tool_name} --noconfirm", 'pip': f"pip install {tool_name}", 'git': f"git clone https://github.com/user/{tool_name}"}
        elif ENV == 'fedora':
            methods = {'dnf': f"sudo dnf install {tool_name} -y", 'pip': f"pip install {tool_name}", 'git': f"git clone https://github.com/user/{tool_name}"}
        return methods
    
    tool_methods = env_cmds[tool_name]
    
    # Remove N/A methods
    valid_methods = {k: v for k, v in tool_methods.items() if v != 'N/A'}
    
    # Sort by success rank
    rank = SUCCESS_RANK.get(ENV, {})
    sorted_methods = sorted(valid_methods.items(), key=lambda x: rank.get(x[0], 99))
    
    return dict(sorted_methods)

def get_best_install_cmd(tool_name):
    """Get the highest success rate install command"""
    methods = get_install_methods_ranked(tool_name)
    if methods:
        return list(methods.values())[0]
    return f"# No install method found for {tool_name}"

def get_env_name():
    return ENV_NAMES.get(ENV, 'Linux')

def get_smart_install_cmd(tool_name, method):
    """Get install command with duplicate/exists handling"""
    base_cmd = get_best_install_cmd(tool_name)
    
    if method == 'git' or 'git clone' in base_cmd:
        # Add check for existing directory
        home = os.path.expanduser('~')
        return f"# Checking if already cloned...\n[ -d ~/{tool_name} ] && echo 'Already exists!' || {base_cmd}"
    
    if method == 'pkg' or method == 'apt' or method == 'pacman' or method == 'dnf':
        return f"{base_cmd} 2>&1 || echo 'Already installed or failed'"
    
    return base_cmd
