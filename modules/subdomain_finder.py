import tkinter as tk
from tkinter import messagebox
import subprocess, threading, os, socket, json
from gui.base_module import BaseModule

class SubdomainFinder(BaseModule):
    def __init__(self, parent, db, logger, detector):
        super().__init__(parent)
        self.db = db
        self.logger = logger
        self.detector = detector
        self.subdomains = set()

    def build_content(self):
        self.add_title("Subdomain Finder", "Multi-source subdomain enumeration")
        tk.Label(self.inner, text="Domain:", font=("Courier",10), fg="#fff", bg="#1a1a2e").pack(anchor="w", padx=10)
        self.domain_entry = tk.Entry(self.inner, font=("Courier",11), bg="#0f3460", fg="#fff", relief="flat")
        self.domain_entry.pack(fill="x", padx=10, pady=3)
        self.domain_entry.insert(0, "example.com")
        
        bf = tk.Frame(self.inner, bg="#1a1a2e"); bf.pack(fill="x", padx=10, pady=5)
        for t,c in [("All",self._all),("crt.sh",self._crtsh),("DNS Brute",self._dns),("Gobuster",self._gobuster),
                    ("Subfinder",self._subfinder),("Assetfinder",self._assetfinder)]:
            tk.Button(bf, text=t, font=("Courier",8), fg="#000", bg="#00ccff", relief="flat", padx=6, command=c).pack(side="left", padx=2)
        tk.Button(bf, text="Export", font=("Courier",8), fg="#000", bg="#00ff88", relief="flat", padx=6, command=self._export).pack(side="right", padx=2)
        tk.Button(bf, text="Resolve", font=("Courier",8), fg="#000", bg="#ffaa00", relief="flat", padx=6, command=self._resolve).pack(side="right", padx=2)
        tk.Button(bf, text="Clear", font=("Courier",8), fg="#fff", bg="#cc0000", relief="flat", padx=6, command=self._clear).pack(side="right", padx=2)
        
        self.results_frame = tk.Frame(self.inner, bg="#1a1a2e")
        self.results_frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.status = self.add_status("Ready")

    def _domain(self): return self.domain_entry.get().strip()

    def _add(self, subs):
        for s in subs:
            s = s.strip().lower().replace("*.","")
            if s and "." in s and len(s) < 100:
                self.subdomains.add(s)
        self._show()

    def _show(self):
        for w in self.results_frame.winfo_children(): w.destroy()
        if not self.subdomains:
            tk.Label(self.results_frame, text="No subdomains found yet", font=("Courier",10), fg="#888", bg="#1a1a2e").pack(pady=20)
            return
        self.status.config(text="Found " + str(len(self.subdomains)) + " subdomains")
        t = tk.Text(self.results_frame, font=("Courier",9), bg="#0a0a0a", fg="#00ff88", relief="flat", height=15)
        t.pack(fill="both", expand=True)
        for sub in sorted(self.subdomains):
            t.insert("end", sub + "\n")

    def _all(self):
        for f in [self._crtsh, self._dns, self._gobuster, self._subfinder, self._assetfinder]:
            self.frame.after(500, f)

    def _crtsh(self):
        dom = self._domain()
        if not dom: return
        self.status.config(text="Querying crt.sh...")
        def do():
            try:
                import urllib.request
                url = "https://crt.sh/?q=%25." + dom + "&output=json"
                req = urllib.request.Request(url, headers={"User-Agent":"CyberLab/1.0"})
                with urllib.request.urlopen(req, timeout=15) as r:
                    data = json.loads(r.read())
                    subs = set()
                    for entry in data[:500]:
                        name = entry.get("name_value","")
                        for n in name.split("\n"):
                            if dom in n: subs.add(n)
                    self.frame.after(0, lambda: self._add(subs))
            except: pass
        threading.Thread(target=do, daemon=True).start()

    def _dns(self):
        dom = self._domain()
        if not dom: return
        self.status.config(text="DNS brute force...")
        def do():
            wordlist = os.path.expanduser("~/wordlists/subdomains-top1million-5000.txt")
            if not os.path.exists(wordlist): wordlist = "/usr/share/wordlists/dirb/common.txt"
            subs = set()
            try:
                with open(wordlist, errors="ignore") as f:
                    for line in f:
                        word = line.strip().split(".")[0]
                        if word and len(word) > 2:
                            subs.add(word + "." + dom)
                        if len(subs) >= 200: break
                self.frame.after(0, lambda: self._add(subs))
            except: pass
        threading.Thread(target=do, daemon=True).start()

    def _gobuster(self):
        dom = self._domain()
        if not dom: return
        self.status.config(text="Gobuster running...")
        def do():
            try:
                wl = os.path.expanduser("~/wordlists/subdomains-top1million-5000.txt")
                if not os.path.exists(wl): wl = "/usr/share/wordlists/dirb/common.txt"
                r = subprocess.run(["gobuster","dns","-d",dom,"-w",wl,"-q"], capture_output=True, text=True, timeout=60)
                subs = set()
                for line in r.stdout.split("\n"):
                    if dom in line and line.split():
                        subs.add(line.split()[0].strip())
                self.frame.after(0, lambda: self._add(subs))
            except: pass
        threading.Thread(target=do, daemon=True).start()

    def _subfinder(self):
        dom = self._domain()
        if not dom: return
        self.status.config(text="Subfinder...")
        def do():
            try:
                r = subprocess.run(["subfinder","-d",dom,"-silent"], capture_output=True, text=True, timeout=60)
                self.frame.after(0, lambda: self._add(set(r.stdout.strip().split("\n"))))
            except: pass
        threading.Thread(target=do, daemon=True).start()

    def _assetfinder(self):
        dom = self._domain()
        if not dom: return
        self.status.config(text="Assetfinder...")
        def do():
            try:
                r = subprocess.run(["assetfinder",dom], capture_output=True, text=True, timeout=60)
                self.frame.after(0, lambda: self._add(set(r.stdout.strip().split("\n"))))
            except: pass
        threading.Thread(target=do, daemon=True).start()

    def _resolve(self):
        if not self.subdomains: return
        self.status.config(text="Resolving...")
        def do():
            resolved = []
            for sub in list(self.subdomains)[:100]:
                try:
                    ip = socket.gethostbyname(sub)
                    resolved.append(sub + " -> " + ip)
                except: pass
            self.frame.after(0, lambda: self._show_resolved(resolved))
        threading.Thread(target=do, daemon=True).start()

    def _show_resolved(self, resolved):
        for w in self.results_frame.winfo_children(): w.destroy()
        t = tk.Text(self.results_frame, font=("Courier",9), bg="#0a0a0a", fg="#00ff88", relief="flat", height=15)
        t.pack(fill="both", expand=True)
        for r in resolved: t.insert("end", r + "\n")
        self.status.config(text="Resolved " + str(len(resolved)) + " hosts")

    def _export(self):
        if not self.subdomains: return
        path = os.path.expanduser("~/subdomains_" + self._domain() + ".txt")
        with open(path, "w") as f:
            for sub in sorted(self.subdomains): f.write(sub + "\n")
        messagebox.showinfo("Exported", "Saved to " + path)

    def _clear(self):
        self.subdomains.clear()
        self._show()
        self.status.config(text="Cleared")
