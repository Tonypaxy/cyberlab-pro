import tkinter as tk
from tkinter import ttk, messagebox
import subprocess, threading, os, shutil, json, time
from datetime import datetime
from gui.base_module import BaseModule

class AutoRecon(BaseModule):
    def __init__(self, parent, db, logger, detector):
        super().__init__(parent)
        self.db = db; self.logger = logger; self.detector = detector
        self.current_project = None
        self.running = False
        self.results = {"subdomains":[], "ports":[], "services":[], "vulns":[], "urls":[], "emails":[]}
        self.steps = []
        self.current_step = 0

    def build_content(self):
        self.add_title("Auto-Recon Pipeline", "One-click automated reconnaissance chain")
        
        projects = self.db.get_all_projects()
        names = [p["name"] for p in projects]
        if names:
            pf = tk.Frame(self.inner, bg="#16213e", padx=10, pady=8)
            pf.pack(fill="x", padx=10, pady=5)
            tk.Label(pf, text="Project:", font=("Courier",10), fg="#fff", bg="#16213e").pack(side="left")
            self.project_var = tk.StringVar(value=names[0])
            ttk.Combobox(pf, textvariable=self.project_var, values=names, font=("Courier",10), state="readonly", width=25).pack(side="left", padx=10)
            self._set_project(names[0])
        
        tk.Label(self.inner, text="Target Domain:", font=("Courier",10), fg="#fff", bg="#1a1a2e").pack(anchor="w", padx=10)
        self.target_entry = tk.Entry(self.inner, font=("Courier",11), bg="#0f3460", fg="#fff", relief="flat")
        self.target_entry.pack(fill="x", padx=10, pady=3)
        self.target_entry.insert(0, "example.com")
        
        # Pipeline steps selection
        tk.Label(self.inner, text="Pipeline Steps:", font=("Courier",10,"bold"), fg="#ffaa00", bg="#1a1a2e").pack(anchor="w", padx=10, pady=(10,0))
        
        self.step_vars = {}
        steps = [
            ("1. Subdomain Enumeration", "subdomains", True),
            ("2. DNS Resolution", "dns", True),
            ("3. Port Scanning (Top 1000)", "ports", True),
            ("4. Service Detection", "services", True),
            ("5. Web Tech Fingerprinting", "web", True),
            ("6. Vulnerability Scanning", "vulns", False),
            ("7. URL/Endpoint Discovery", "urls", True),
            ("8. Email/Contact Harvesting", "emails", False),
            ("9. Screenshot Web Services", "screenshots", False),
            ("10. Generate Report", "report", True),
        ]
        
        for text, key, default in steps:
            var = tk.BooleanVar(value=default)
            self.step_vars[key] = var
            tk.Checkbutton(self.inner, text=text, variable=var, font=("Courier",9),
                    fg="#888", bg="#1a1a2e", selectcolor="#00ff88", activebackground="#1a1a2e").pack(anchor="w", padx=20)
        
        # Control buttons
        bf = tk.Frame(self.inner, bg="#1a1a2e"); bf.pack(fill="x", padx=10, pady=10)
        tk.Button(bf, text="START PIPELINE", font=("Courier",12,"bold"), fg="#000", bg="#00ff88",
                relief="raised", padx=20, pady=10, command=self._start).pack(side="left", padx=5)
        tk.Button(bf, text="STOP", font=("Courier",10,"bold"), fg="#fff", bg="#cc0000",
                relief="raised", padx=15, pady=10, command=self._stop).pack(side="left", padx=5)
        tk.Button(bf, text="Export Report", font=("Courier",10), fg="#000", bg="#ffaa00",
                relief="raised", padx=15, pady=10, command=self._export).pack(side="right", padx=5)
        
        # Progress bar
        self.progress = ttk.Progressbar(self.inner, mode="determinate", length=300)
        self.progress.pack(fill="x", padx=10, pady=3)
        self.progress_label = tk.Label(self.inner, text="Ready", font=("Courier",9), fg="#888", bg="#1a1a2e")
        self.progress_label.pack()
        
        # Output
        self.output = tk.Text(self.inner, font=("Courier",9), bg="#0a0a0a", fg="#00ff88", relief="flat", height=12)
        self.output.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.status = self.add_status("Ready - Configure steps and click START")

    def _set_project(self, name):
        for p in self.db.get_all_projects():
            if p["name"] == name: self.current_project = p; break

    def _start(self):
        target = self.target_entry.get().strip()
        if not target: messagebox.showwarning("Warning","Enter target domain"); return
        
        self.running = True
        self.results = {"subdomains":[], "ports":[], "services":[], "vulns":[], "urls":[], "emails":[]}
        
        # Build pipeline steps
        self.steps = []
        if self.step_vars["subdomains"].get(): self.steps.append(("Subdomain Enumeration", self._run_subdomains))
        if self.step_vars["dns"].get(): self.steps.append(("DNS Resolution", self._run_dns))
        if self.step_vars["ports"].get(): self.steps.append(("Port Scanning", self._run_ports))
        if self.step_vars["services"].get(): self.steps.append(("Service Detection", self._run_services))
        if self.step_vars["web"].get(): self.steps.append(("Web Fingerprinting", self._run_web))
        if self.step_vars["vulns"].get(): self.steps.append(("Vulnerability Scan", self._run_vulns))
        if self.step_vars["urls"].get(): self.steps.append(("URL Discovery", self._run_urls))
        if self.step_vars["emails"].get(): self.steps.append(("Email Harvesting", self._run_emails))
        if self.step_vars["report"].get(): self.steps.append(("Generate Report", self._run_report))
        
        if not self.steps:
            messagebox.showwarning("Warning","Select at least one step"); return
        
        self.current_step = 0
        self.output.delete("1.0","end")
        self.output.insert("end", f"{'='*60}\n")
        self.output.insert("end", f"  AUTO-RECON PIPELINE - {target}\n")
        self.output.insert("end", f"  Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        self.output.insert("end", f"  Steps: {len(self.steps)}\n")
        self.output.insert("end", f"{'='*60}\n\n")
        self.output.see("end")
        
        self.progress["maximum"] = len(self.steps)
        self.progress["value"] = 0
        self._run_next()

    def _run_next(self):
        if not self.running or self.current_step >= len(self.steps):
            if self.running:
                self.output.insert("end", f"\n{'='*60}\n")
                self.output.insert("end", f"  PIPELINE COMPLETE!\n")
                self.output.insert("end", f"  Finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                self.output.insert("end", f"{'='*60}\n")
                self.status.config(text="Pipeline complete!")
            self.running = False
            return
        
        name, func = self.steps[self.current_step]
        self.progress_label.config(text=f"[{self.current_step+1}/{len(self.steps)}] {name}")
        self.output.insert("end", f"\n{'─'*40}\n[{self.current_step+1}] {name}\n{'─'*40}\n")
        self.output.see("end")
        self.status.config(text=f"Running: {name}...")
        self.progress["value"] = self.current_step
        
        def run_step():
            try:
                func()
            except Exception as e:
                self.output.insert("end", f"\n[X] Error: {e}\n")
            self.current_step += 1
            self.frame.after(500, self._run_next)
        
        threading.Thread(target=run_step, daemon=True).start()

    def _run_subdomains(self):
        target = self.target_entry.get().strip()
        tools_used = []
        
        # crt.sh
        try:
            import urllib.request
            url = f"https://crt.sh/?q=%25.{target}&output=json"
            req = urllib.request.Request(url, headers={"User-Agent":"CyberLab/1.0"})
            with urllib.request.urlopen(req, timeout=15) as r:
                data = json.loads(r.read())
                for entry in data[:200]:
                    name = entry.get("name_value","")
                    for n in name.split("\n"):
                        if target in n and n not in self.results["subdomains"]:
                            self.results["subdomains"].append(n.strip().lower().replace("*.",""))
            tools_used.append("crt.sh")
        except: pass
        
        # Subfinder
        if shutil.which("subfinder"):
            try:
                r = subprocess.run(["subfinder","-d",target,"-silent"], capture_output=True, text=True, timeout=60)
                for sub in r.stdout.strip().split("\n"):
                    if sub and sub not in self.results["subdomains"]:
                        self.results["subdomains"].append(sub.strip())
                tools_used.append("subfinder")
            except: pass
        
        self.output.insert("end", f"  Found {len(self.results['subdomains'])} subdomains via {', '.join(tools_used)}\n")
        self.output.see("end")

    def _run_dns(self):
        target = self.target_entry.get().strip()
        targets = self.results.get("subdomains", [])[:50] or [target]
        resolved = []
        import socket
        for sub in targets:
            try:
                ip = socket.gethostbyname(sub)
                resolved.append(f"{sub} -> {ip}")
            except: pass
        self.output.insert("end", f"  Resolved {len(resolved)}/{len(targets)} hosts\n")
        self.output.see("end")

    def _run_ports(self):
        target = self.target_entry.get().strip()
        if shutil.which("nmap"):
            try:
                r = subprocess.run(["nmap","-F","-T4","--open",target,"-oG","-"], capture_output=True, text=True, timeout=120)
                for line in r.stdout.split("\n"):
                    if "/open/" in line:
                        parts = line.split()
                        if len(parts) >= 5:
                            self.results["ports"].append({"host":parts[1],"ports":parts[3],"services":parts[4]})
                self.output.insert("end", f"  Found open ports on target\n")
            except: pass
        else:
            self.output.insert("end", "  [Skipped] nmap not installed\n")

    def _run_services(self):
        target = self.target_entry.get().strip()
        if shutil.which("nmap"):
            try:
                r = subprocess.run(["nmap","-sV","-F","-T4",target], capture_output=True, text=True, timeout=120)
                self.results["services"] = r.stdout
                self.output.insert("end", "  Service detection complete\n")
            except: pass

    def _run_web(self):
        target = self.target_entry.get().strip()
        if shutil.which("whatweb"):
            try:
                r = subprocess.run(["whatweb",f"https://{target}"], capture_output=True, text=True, timeout=30)
                self.output.insert("end", f"  {r.stdout.strip()[:200]}\n")
            except: pass

    def _run_vulns(self):
        target = self.target_entry.get().strip()
        if shutil.which("nmap"):
            try:
                r = subprocess.run(["nmap","-sV","--script","vuln","-F",target], capture_output=True, text=True, timeout=180)
                self.results["vulns"] = r.stdout
                self.output.insert("end", "  Vulnerability scan complete\n")
            except: pass

    def _run_urls(self):
        target = self.target_entry.get().strip()
        # Gau
        if shutil.which("gau"):
            try:
                r = subprocess.run(["gau",target], capture_output=True, text=True, timeout=60)
                urls = r.stdout.strip().split("\n")
                self.results["urls"] = urls[:200]
                self.output.insert("end", f"  Found {len(urls)} URLs via gau\n")
            except: pass

    def _run_emails(self):
        target = self.target_entry.get().strip()
        # theHarvester
        if shutil.which("theHarvester"):
            try:
                r = subprocess.run(["theHarvester","-d",target,"-b","google"], capture_output=True, text=True, timeout=30)
                import re
                emails = set(re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', r.stdout))
                self.results["emails"] = list(emails)
                self.output.insert("end", f"  Found {len(emails)} emails\n")
            except: pass

    def _run_report(self):
        target = self.target_entry.get().strip()
        if not self.current_project: return
        
        export_dir = os.path.join(self.current_project["path"], "exports")
        os.makedirs(export_dir, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = os.path.join(export_dir, f"recon_{target}_{ts}.html")
        
        with open(path, "w") as f:
            f.write(f"<html><head><style>body{{background:#0a0a0a;color:#00ff88;font:12px monospace;padding:20px}}h1{{color:#ffaa00}}h2{{color:#00ccff;border-bottom:1px solid #333}}table{{border-collapse:collapse;width:100%}}td,th{{border:1px solid #333;padding:6px}}</style></head><body>")
            f.write(f"<h1>Auto-Recon Report: {target}</h1>")
            f.write(f"<p>Generated: {datetime.now()}</p>")
            
            if self.results["subdomains"]:
                f.write(f"<h2>Subdomains ({len(self.results['subdomains'])})</h2><ul>")
                for s in sorted(self.results["subdomains"])[:50]:
                    f.write(f"<li>{s}</li>")
                f.write("</ul>")
            
            if self.results["ports"]:
                f.write(f"<h2>Open Ports</h2><table><tr><th>Host</th><th>Ports</th><th>Services</th></tr>")
                for p in self.results["ports"]:
                    f.write(f"<tr><td>{p.get('host','')}</td><td>{p.get('ports','')}</td><td>{p.get('services','')}</td></tr>")
                f.write("</table>")
            
            if self.results["emails"]:
                f.write(f"<h2>Emails ({len(self.results['emails'])})</h2><ul>")
                for e in sorted(self.results["emails"])[:20]:
                    f.write(f"<li>{e}</li>")
                f.write("</ul>")
            
            f.write("</body></html>")
        
        self.output.insert("end", f"  Report saved: {path}\n")
        self.logger.log_project_action(self.current_project["name"], f"auto_recon_report")

    def _stop(self):
        self.running = False
        self.status.config(text="Stopped")
        self.output.insert("end", "\n[STOPPED]\n")

    def _export(self):
        if not self.current_project: return
        target = self.target_entry.get().strip()
        export_dir = os.path.join(self.current_project["path"], "exports")
        os.makedirs(export_dir, exist_ok=True)
        path = os.path.join(export_dir, f"recon_{target}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        with open(path, "w") as f:
            json.dump(self.results, f, indent=2)
        messagebox.showinfo("Exported", f"Saved to {path}")
