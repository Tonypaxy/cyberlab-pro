import tkinter as tk
from tkinter import ttk, messagebox
import subprocess, threading, os, shutil, re, json
from datetime import datetime
from gui.base_module import BaseModule

class VulnScanner(BaseModule):
    def __init__(self, parent, db, logger):
        super().__init__(parent)
        self.db = db; self.logger = logger
        self.results = []; self.scanning = False

    def build_content(self):
        self.add_title("Vulnerability Scanner", "Multi-engine vuln scanning with auto-detection")
        
        tk.Label(self.inner, text="Target URL or IP:", font=("Courier",10), fg="#fff", bg="#1a1a2e").pack(anchor="w", padx=10)
        self.target_entry = tk.Entry(self.inner, font=("Courier",11), bg="#0f3460", fg="#fff", relief="flat")
        self.target_entry.pack(fill="x", padx=10, pady=3)
        self.target_entry.insert(0, "https://example.com")
        
        bf = tk.Frame(self.inner, bg="#1a1a2e"); bf.pack(fill="x", padx=10, pady=5)
        
        # Auto-detect all vuln scanners
        self.engines = self._detect_engines()
        for name, cmd, args, color in self.engines:
            tk.Button(bf, text=name, font=("Courier",8), fg="#000", bg=color, relief="flat", padx=6,
                    command=lambda c=cmd,a=args: self._run(c,a)).pack(side="left", padx=2)
        
        tk.Button(bf, text="Run All", font=("Courier",8,"bold"), fg="#fff", bg="#cc0000", relief="flat", padx=6,
                command=self._run_all).pack(side="right", padx=2)
        tk.Button(bf, text="STOP", font=("Courier",8), fg="#fff", bg="#cc0000", relief="flat", padx=6,
                command=self._stop).pack(side="right", padx=2)
        tk.Button(bf, text="Export", font=("Courier",8), fg="#000", bg="#00ff88", relief="flat", padx=6,
                command=self._export).pack(side="right", padx=2)
        
        self.progress = ttk.Progressbar(self.inner, mode="indeterminate", length=300)
        self.output = tk.Text(self.inner, font=("Courier",9), bg="#0a0a0a", fg="#00ff88", relief="flat", height=15)
        self.output.pack(fill="both", expand=True, padx=10, pady=5)
        self.status = self.add_status(f"Ready - {len(self.engines)} engines detected")

    def _detect_engines(self):
        """Auto-detect all installed vulnerability scanners"""
        engines = []
        
        # Nikto
        if shutil.which("nikto"):
            engines.append(("Nikto","nikto","-h {TARGET} -Tuning 4,9","#00ccff"))
        
        # Nuclei
        if shutil.which("nuclei"):
            engines.append(("Nuclei","nuclei","-u {TARGET} -severity critical,high,medium","#00ff88"))
            engines.append(("Nuclei All","nuclei","-u {TARGET}","#00ff88"))
        
        # WPScan
        if shutil.which("wpscan"):
            engines.append(("WPScan","wpscan","--url {TARGET} --enumerate vp,vt --api-token YOUR_TOKEN","#ffaa00"))
        
        # SQLMap
        if shutil.which("sqlmap"):
            engines.append(("SQLMap","sqlmap","-u {TARGET} --batch --level=2 --risk=2","#ff4444"))
        
        # ZAP
        if shutil.which("zap-cli") or shutil.which("zap"):
            engines.append(("ZAP Scan","zap-cli","quick-scan {TARGET}","#cc88ff"))
        
        # Arachni
        if shutil.which("arachni"):
            engines.append(("Arachni","arachni","{TARGET} --scope-include-subdomains","#ff00ff"))
        
        # Wapiti
        if shutil.which("wapiti"):
            engines.append(("Wapiti","wapiti","-u {TARGET}","#00ffff"))
        
        # Skipfish
        if shutil.which("skipfish"):
            engines.append(("Skipfish","skipfish","-o /tmp/skipfish {TARGET}","#ff8800"))
        
        # WhatWeb
        if shutil.which("whatweb"):
            engines.append(("WhatWeb","whatweb","-a 3 {TARGET}","#bc8cff"))
        
        # TestSSL
        if shutil.which("testssl.sh") or shutil.which("testssl"):
            engines.append(("TestSSL","testssl","{TARGET}","#58a6ff"))
        
        # SSLyze
        if shutil.which("sslyze"):
            engines.append(("SSLyze","sslyze","--regular {TARGET}","#39c5cf"))
        
        # Nmap vuln scripts
        if shutil.which("nmap"):
            engines.append(("Nmap Vuln","nmap","-sV --script vuln {TARGET}","#00ccff"))
            engines.append(("Nmap Auth","nmap","-sV --script auth {TARGET}","#00ccff"))
        
        # Legion
        if shutil.which("legion"):
            engines.append(("Legion","legion","{TARGET}","#d2991d"))
        
        # Sparta
        if shutil.which("sparta"):
            engines.append(("Sparta","sparta","{TARGET}","#ff4444"))
        
        # Joomscan
        if shutil.which("joomscan"):
            engines.append(("Joomscan","joomscan","-u {TARGET}","#ffaa00"))
        
        # Droopescan
        if shutil.which("droopescan"):
            engines.append(("Droopescan","droopescan","scan -u {TARGET}","#bc8cff"))
        
        # Wafw00f
        if shutil.which("wafw00f"):
            engines.append(("WAF Detect","wafw00f","{TARGET}","#00ff88"))
        
        # CMSeek
        if shutil.which("cmseek"):
            engines.append(("CMSeek","cmseek","-u {TARGET}","#ffaa00"))
        
        # Sn1per
        if shutil.which("sniper"):
            engines.append(("Sn1per","sniper","-t {TARGET}","#ff0000"))
        
        # Discover future scanners
        for path in os.environ.get("PATH","").split(":"):
            try:
                for f in os.listdir(path):
                    fpath = os.path.join(path,f)
                    if os.access(fpath, os.X_OK) and f not in [e[1] for e in engines]:
                        try:
                            r = subprocess.run([f,"--help"], capture_output=True, text=True, timeout=3)
                            h = (r.stdout + r.stderr).lower()
                            if any(kw in h for kw in ["vulnerability","vuln","exploit","xss","sqli","injection","security","audit","cms","web scan"]):
                                if f not in ["nmap","nikto","nuclei","wpscan","sqlmap","zap-cli","zap","arachni","wapiti","skipfish","whatweb","testssl","sslyze","legion","sparta","joomscan","droopescan","wafw00f","cmseek","sniper"]:
                                    engines.append((f" {f.title()}","{f}","{TARGET}","#666666"))
                        except: pass
            except: pass
        
        return engines

    def _run(self, tool, args):
        target = self.target_entry.get().strip()
        if not target: return
        
        cmd = args.replace("{TARGET}", target)
        full_cmd = f"{tool} {cmd}"
        
        self.scanning = True
        self.output.insert("end", f"\n{'='*60}\n[{tool}] {full_cmd[:80]}\n{'='*60}\n\n")
        self.output.see("end")
        self.status.config(text=f"Running {tool}...")
        self.progress.pack(fill="x", padx=10, pady=3)
        self.progress.start(10)
        
        def do():
            try:
                p = subprocess.Popen(full_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                for line in p.stdout:
                    if not self.scanning: p.kill(); break
                    self.output.insert("end", line); self.output.see("end")
                p.wait()
                self.frame.after(0, self.progress.stop)
                self.frame.after(0, self.progress.pack_forget)
                self.frame.after(0, lambda: self.status.config(text=f"Done - {tool}"))
            except Exception as e:
                self.frame.after(0, lambda: self.status.config(text=f"Error: {str(e)[:50]}"))
            self.scanning = False
        threading.Thread(target=do, daemon=True).start()

    def _run_all(self):
        for _, tool, args, _ in self.engines:
            if not self.scanning: break
            self._run(tool, args)
            self.frame.after(2000, lambda: None)  # Stagger scans

    def _stop(self):
        self.scanning = False
        self.progress.stop(); self.progress.pack_forget()
        self.output.insert("end", "\n[STOPPED]\n")
        self.status.config(text="Stopped")

    def _export(self):
        text = self.output.get("1.0","end-1c")
        if not text.strip(): return
        path = os.path.expanduser(f"~/vulnscan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
        with open(path,"w") as f: f.write(text)
        messagebox.showinfo("Exported", f"Saved to {path}")
