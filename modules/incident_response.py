import tkinter as tk
from tkinter import ttk, messagebox
import subprocess, threading, os, shutil, hashlib, json, re
from datetime import datetime
from gui.base_module import BaseModule

class IncidentResponse(BaseModule):
    def __init__(self, parent, db, logger):
        super().__init__(parent)
        self.db = db; self.logger = logger
        self.case_dir = os.path.expanduser("~/ir_case")
        os.makedirs(self.case_dir, exist_ok=True)
        self.findings = []

    def build_content(self):
        self.add_title("Incident Response", "Log analysis, timeline, IOC scanner, memory forensics")
        
        tk.Label(self.inner, text="Target (file/dir/host):", font=("Courier",10), fg="#fff", bg="#1a1a2e").pack(anchor="w", padx=10)
        self.target_entry = tk.Entry(self.inner, font=("Courier",10), bg="#0f3460", fg="#fff", relief="flat")
        self.target_entry.pack(fill="x", padx=10, pady=3)
        self.target_entry.insert(0, "/var/log")
        
        bf = tk.Frame(self.inner, bg="#1a1a2e"); bf.pack(fill="x", padx=10, pady=5)
        
        tools = self._detect_tools()
        for name, func, color in tools:
            tk.Button(bf, text=name, font=("Courier",8), fg="#000", bg=color, relief="flat", padx=6,
                    command=func).pack(side="left", padx=2)
        
        tk.Button(bf, text="FULL IR", font=("Courier",8,"bold"), fg="#fff", bg="#cc0000",
                relief="flat", padx=8, command=self._full_ir).pack(side="right", padx=2)
        tk.Button(bf, text="Report", font=("Courier",8), fg="#000", bg="#00ff88",
                relief="flat", padx=8, command=self._report).pack(side="right", padx=2)
        
        self.output = tk.Text(self.inner, font=("Courier",9), bg="#0a0a0a", fg="#00ff88", relief="flat", height=15)
        self.output.pack(fill="both", expand=True, padx=10, pady=5)
        self.status = self.add_status(f"Ready - {len(tools)} IR tools detected")

    def _get_target(self): return self.target_entry.get().strip()

    def _detect_tools(self):
        tools = []
        
        # === LOG ANALYSIS ===
        tools.append(("Auth Log", self._auth_log, "#58a6ff"))
        tools.append(("Syslog Errors", self._syslog_errors, "#58a6ff"))
        tools.append(("Apache Access", self._apache_access, "#58a6ff"))
        tools.append(("Nginx Access", self._nginx_access, "#58a6ff"))
        tools.append(("SSH Attempts", self._ssh_attempts, "#ff4444"))
        tools.append(("Failed Logins", self._failed_logins, "#ff4444"))
        tools.append(("Sudo Usage", self._sudo_usage, "#ffaa00"))
        
        # === IOC SCANNER ===
        if shutil.which("grep"):
            tools.append(("IOC IPs", self._ioc_ips, "#ff0000"))
            tools.append(("IOC URLs", self._ioc_urls, "#ff0000"))
            tools.append(("IOC Hashes", self._ioc_hashes, "#ff0000"))
            tools.append(("IOC Emails", self._ioc_emails, "#ff0000"))
        tools.append(("Suspicious Files", self._suspicious_files, "#ff0000"))
        tools.append(("Modified Files", self._modified_files, "#ffaa00"))
        
        # === TIMELINE ===
        tools.append(("File Timeline", self._file_timeline, "#d2991d"))
        tools.append(("Recent Files", self._recent_files, "#d2991d"))
        
        # === MEMORY ===
        if shutil.which("volatility3") or shutil.which("vol"):
            tools.append(("Volatility", self._run_volatility, "#ff00ff"))
        if shutil.which("lime"):
            tools.append(("LiME Capture", lambda: self._cmd("insmod lime.ko path=/tmp/mem.lime format=lime"), "#ff00ff"))
        
        # === PROCESS ===
        tools.append(("Process List", self._process_list, "#00ccff"))
        tools.append(("Network Conns", self._network_conns, "#00ccff"))
        tools.append(("Listening Ports", self._listening_ports, "#00ccff"))
        tools.append(("Cron Jobs", self._cron_jobs, "#00ccff"))
        tools.append(("Startup Items", self._startup_items, "#00ccff"))
        
        # === USERS ===
        tools.append(("User Accounts", self._user_accounts, "#bc8cff"))
        tools.append(("Logged In Users", self._logged_in_users, "#bc8cff"))
        tools.append(("SSH Keys", self._ssh_keys, "#bc8cff"))
        
        # === PERSISTENCE ===
        tools.append(("Persistence Check", self._persistence_check, "#ff0000"))
        
        # === CONTAINMENT ===
        tools.append(("Block IP", self._block_ip, "#cc0000"))
        tools.append(("Kill Process", self._kill_process, "#cc0000"))
        tools.append(("Quarantine File", self._quarantine_file, "#cc0000"))
        
        return tools

    def _cmd(self, cmd):
        target = self._get_target()
        cmd = cmd.replace("TARGET", target)
        self.output.insert("end", f"\n{'='*60}\n$ {cmd[:100]}\n{'='*60}\n\n")
        self.output.see("end")
        def do():
            try:
                p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                out = p.stdout.read()[:10000]
                self.frame.after(0, lambda: self.output.insert("end", out))
                self.frame.after(0, self.output.see("end"))
                self.status.config(text="Done")
            except Exception as e:
                self.output.insert("end", f"\n[X] {e}\n")
        threading.Thread(target=do, daemon=True).start()

    def _auth_log(self): self._cmd("grep -E 'Failed|Accepted|error|invalid' /var/log/auth.log 2>/dev/null | tail -50")
    def _syslog_errors(self): self._cmd("grep -iE 'error|fail|critical|emerg|alert' /var/log/syslog 2>/dev/null | tail -50")
    def _apache_access(self): self._cmd("tail -100 /var/log/apache2/access.log 2>/dev/null")
    def _nginx_access(self): self._cmd("tail -100 /var/log/nginx/access.log 2>/dev/null")
    def _ssh_attempts(self): self._cmd("grep -E 'Failed|Accepted|invalid' /var/log/auth.log 2>/dev/null | tail -30")
    def _failed_logins(self): self._cmd("lastb 2>/dev/null | head -20")
    def _sudo_usage(self): self._cmd("grep sudo /var/log/auth.log 2>/dev/null | tail -20")
    
    def _ioc_ips(self):
        ips = self._get_target()
        self.output.insert("end", "\n[*] Scanning for suspicious IPs...\n")
        self._cmd(f"grep -rE '[0-9]+\\.[0-9]+\\.[0-9]+\\.[0-9]+' TARGET 2>/dev/null | head -50")
    
    def _ioc_urls(self):
        self._cmd("grep -rE 'https?://[^\\s]+' TARGET 2>/dev/null | head -50")
    
    def _ioc_hashes(self):
        self._cmd("grep -rE '[a-fA-F0-9]{32}|[a-fA-F0-9]{40}|[a-fA-F0-9]{64}' TARGET 2>/dev/null | head -30")
    
    def _ioc_emails(self):
        self._cmd("grep -rE '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}' TARGET 2>/dev/null | head -30")
    
    def _suspicious_files(self):
        self._cmd("find TARGET -type f \\( -name '*.exe' -o -name '*.bat' -o -name '*.ps1' -o -name '*.vbs' -o -name '*.scr' -o -name '*.pif' \\) 2>/dev/null | head -30")
    
    def _modified_files(self):
        self._cmd("find TARGET -type f -mtime -7 2>/dev/null | head -30")
    
    def _file_timeline(self):
        self._cmd("find TARGET -type f -printf '%T+ %p\\n' 2>/dev/null | sort -r | head -50")
    
    def _recent_files(self):
        self._cmd("find TARGET -type f -mtime -1 2>/dev/null | head -30")
    
    def _process_list(self): self._cmd("ps aux --sort=-%mem | head -30")
    def _network_conns(self): self._cmd("netstat -tunap 2>/dev/null | head -30 || ss -tunap | head -30")
    def _listening_ports(self): self._cmd("netstat -tlnp 2>/dev/null | head -20 || ss -tlnp | head -20")
    def _cron_jobs(self): self._cmd("cat /etc/crontab 2>/dev/null; ls -la /etc/cron.* 2>/dev/null")
    def _startup_items(self): self._cmd("ls -la /etc/init.d/ 2>/dev/null; ls -la /etc/systemd/system/ 2>/dev/null")
    def _user_accounts(self): self._cmd("cat /etc/passwd 2>/dev/null | grep -E '/bin/bash|/bin/sh'")
    def _logged_in_users(self): self._cmd("w 2>/dev/null || who")
    def _ssh_keys(self): self._cmd("find /home -name 'authorized_keys' -exec ls -la {} \\; 2>/dev/null")
    def _persistence_check(self):
        self._cmd("echo '[Checking cron]' && crontab -l 2>/dev/null; echo '[Checking rc.local]' && cat /etc/rc.local 2>/dev/null; echo '[Checking bashrc]' && grep -E 'curl|wget|nc|bash -i' ~/.bashrc 2>/dev/null")
    
    def _run_volatility(self):
        vol = "vol" if shutil.which("vol") else "volatility3"
        self._cmd(f"{vol} -f TARGET windows.info 2>/dev/null || {vol} -f TARGET imageinfo 2>/dev/null")
    
    def _block_ip(self):
        ip = self._get_target()
        if not ip: return
        self._cmd(f"iptables -A INPUT -s {ip} -j DROP 2>/dev/null && echo 'Blocked {ip}' || echo 'Need root'")
    
    def _kill_process(self):
        pid = self._get_target()
        self._cmd(f"kill -9 {pid} 2>/dev/null && echo 'Killed PID {pid}' || echo 'Need PID'")
    
    def _quarantine_file(self):
        f = self._get_target()
        if not os.path.exists(f): return
        dest = os.path.join(self.case_dir, "quarantine", os.path.basename(f))
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        shutil.move(f, dest)
        self.output.insert("end", f"\n[+] Quarantined: {f} -> {dest}\n")
        self.output.see("end")

    def _full_ir(self):
        for name, func, _ in self._detect_tools()[:15]:
            self.frame.after(500, func)

    def _report(self):
        text = self.output.get("1.0","end-1c")
        path = os.path.join(self.case_dir, f"ir_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
        with open(path, "w") as f:
            f.write(f"Incident Response Report\n{'='*50}\n")
            f.write(f"Date: {datetime.now()}\n")
            f.write(f"Target: {self._get_target()}\n\n")
            f.write(text)
        messagebox.showinfo("Report", f"Saved to {path}")

    def _stop(self):
        self.output.insert("end", "\n[STOPPED]\n")
        self.status.config(text="Stopped")
