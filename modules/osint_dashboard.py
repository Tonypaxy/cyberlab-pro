import tkinter as tk
from tkinter import ttk, messagebox
import subprocess, threading, os, shutil, json, re
from datetime import datetime
from gui.base_module import BaseModule

class OSINTDashboard(BaseModule):
    def __init__(self, parent, db, logger):
        super().__init__(parent)
        self.db = db; self.logger = logger
        self.results = {}

    def build_content(self):
        self.add_title("OSINT Dashboard", "Username search, email lookup, domain intel, social media")
        
        # Search type tabs
        search_frame = tk.Frame(self.inner, bg="#16213e", padx=10, pady=8)
        search_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Label(search_frame, text="Search:", font=("Courier",10), fg="#fff", bg="#16213e").pack(anchor="w")
        self.search_entry = tk.Entry(search_frame, font=("Courier",11), bg="#0f3460", fg="#fff", relief="flat")
        self.search_entry.pack(fill="x", pady=3)
        self.search_entry.insert(0, "username or email@domain.com")
        self.search_entry.bind("<Return>", lambda e: self._search_all())
        
        bf = tk.Frame(search_frame, bg="#16213e"); bf.pack(fill="x", pady=5)
        
        searches = self._detect_osint_tools()
        for name, func, color in searches:
            tk.Button(bf, text=name, font=("Courier",8), fg="#000", bg=color, relief="flat", padx=8,
                    command=func).pack(side="left", padx=2)
        
        tk.Button(bf, text="SEARCH ALL", font=("Courier",9,"bold"), fg="#fff", bg="#cc0000",
                relief="raised", padx=12, command=self._search_all).pack(side="right", padx=5)
        
        self.results_frame = tk.Frame(self.inner, bg="#1a1a2e")
        self.results_frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.status = self.add_status("Ready - Enter username/email and search")

    def _detect_osint_tools(self):
        searches = []
        
        if shutil.which("sherlock"):
            searches.append(("Sherlock", self._run_sherlock, "#00ff88"))
        if shutil.which("holehe"):
            searches.append(("Holehe", self._run_holehe, "#ffaa00"))
        if shutil.which("theHarvester"):
            searches.append(("theHarvester", self._run_harvester, "#00ccff"))
        if shutil.which("twint") or shutil.which("tweepy"):
            searches.append(("Twitter", self._run_twitter, "#1da1f2"))
        if shutil.which("instaloader"):
            searches.append(("Instagram", self._run_instagram, "#e4405f"))
        if shutil.which("facebook-scraper"):
            searches.append(("Facebook", self._run_facebook, "#1877f2"))
        if shutil.which("tiktok-scraper"):
            searches.append(("TikTok", self._run_tiktok, "#000000"))
        
        # Always available searches
        searches.append(("Domain Info", self._run_domain, "#58a6ff"))
        searches.append(("Email Check", self._run_email_check, "#bc8cff"))
        searches.append(("Username Check", self._run_username_check, "#ff4444"))
        searches.append(("Google Dork", self._run_google_dork, "#ff4444"))
        searches.append(("HaveIBeenPwned", self._run_hibp, "#ff4444"))
        
        return searches

    def _search_all(self):
        query = self.search_entry.get().strip()
        if not query: return
        for w in self.results_frame.winfo_children(): w.destroy()
        self.output = tk.Text(self.results_frame, font=("Courier",9), bg="#0a0a0a", fg="#00ff88", relief="flat", height=20)
        self.output.pack(fill="both", expand=True)
        self.output.insert("end", f"╔{'═'*50}╗\n")
        self.output.insert("end", f"║  OSINT SEARCH: {query[:40]}\n")
        self.output.insert("end", f"╚{'═'*50}╝\n\n")
        self.status.config(text="Searching all sources...")
        
        for name, func, _ in self._detect_osint_tools():
            self.frame.after(500, func)

    def _run_sherlock(self):
        query = self.search_entry.get().strip()
        self.status.config(text="Sherlock searching...")
        def do():
            try:
                r = subprocess.run(["sherlock", query, "--output", "/tmp/sherlock", "--timeout", "10"],
                        capture_output=True, text=True, timeout=60)
                found = [l for l in r.stdout.split("\n") if "[+]" in l]
                self.frame.after(0, lambda: self._add_result("Sherlock (Username Search)", found))
            except: self.frame.after(0, lambda: self._add_result("Sherlock", ["Not installed"]))
        threading.Thread(target=do, daemon=True).start()

    def _run_holehe(self):
        query = self.search_entry.get().strip()
        if "@" not in query: return
        def do():
            try:
                r = subprocess.run(["holehe", query], capture_output=True, text=True, timeout=30)
                found = [l for l in r.stdout.split("\n") if "[+]" in l]
                self.frame.after(0, lambda: self._add_result("Holehe (Email Check)", found))
            except: pass
        threading.Thread(target=do, daemon=True).start()

    def _run_harvester(self):
        query = self.search_entry.get().strip()
        def do():
            try:
                r = subprocess.run(["theHarvester", "-d", query, "-b", "google,linkedin,github"],
                        capture_output=True, text=True, timeout=30)
                self.frame.after(0, lambda: self._add_result("theHarvester", r.stdout[:2000].split("\n")))
            except: pass
        threading.Thread(target=do, daemon=True).start()

    def _run_twitter(self):
        query = self.search_entry.get().strip()
        def do():
            try:
                r = subprocess.run(["twint", "-u", query, "--limit", "20"],
                        capture_output=True, text=True, timeout=30)
                self.frame.after(0, lambda: self._add_result("Twitter", r.stdout[:500].split("\n")))
            except: pass
        threading.Thread(target=do, daemon=True).start()

    def _run_instagram(self):
        query = self.search_entry.get().strip()
        def do():
            try:
                r = subprocess.run(["instaloader", query, "--no-pictures", "--no-videos"],
                        capture_output=True, text=True, timeout=30)
                self.frame.after(0, lambda: self._add_result("Instagram", r.stdout[:500].split("\n")))
            except: pass
        threading.Thread(target=do, daemon=True).start()

    def _run_facebook(self):
        query = self.search_entry.get().strip()
        def do():
            try:
                r = subprocess.run(["facebook-scraper", "-u", query, "--posts", "5"],
                        capture_output=True, text=True, timeout=30)
                self.frame.after(0, lambda: self._add_result("Facebook", r.stdout[:500].split("\n")))
            except: pass
        threading.Thread(target=do, daemon=True).start()

    def _run_tiktok(self):
        query = self.search_entry.get().strip()
        def do():
            try:
                r = subprocess.run(["tiktok-scraper", "-u", query, "-n", "10"],
                        capture_output=True, text=True, timeout=30)
                self.frame.after(0, lambda: self._add_result("TikTok", r.stdout[:500].split("\n")))
            except: pass
        threading.Thread(target=do, daemon=True).start()

    def _run_domain(self):
        query = self.search_entry.get().strip()
        if not "." in query: query = query + ".com"
        def do():
            try:
                r = subprocess.run(["whois", query], capture_output=True, text=True, timeout=15)
                self.frame.after(0, lambda: self._add_result("Domain WHOIS", r.stdout[:1000].split("\n")))
            except: pass
        threading.Thread(target=do, daemon=True).start()

    def _run_email_check(self):
        query = self.search_entry.get().strip()
        if "@" not in query: return
        def do():
            try:
                r = subprocess.run(["holehe", query], capture_output=True, text=True, timeout=20)
                self.frame.after(0, lambda: self._add_result("Email Registered Sites", r.stdout[:500].split("\n")))
            except: pass
        threading.Thread(target=do, daemon=True).start()

    def _run_username_check(self):
        query = self.search_entry.get().strip()
        sites = ["twitter.com","instagram.com","github.com","reddit.com","youtube.com","tiktok.com",
                 "facebook.com","linkedin.com","pinterest.com","medium.com","twitch.tv","telegram.org"]
        def do():
            results = []
            for site in sites:
                try:
                    import urllib.request
                    url = f"https://{site}/{query}"
                    req = urllib.request.Request(url, headers={"User-Agent":"CyberLab/1.0"})
                    with urllib.request.urlopen(req, timeout=5) as r:
                        if r.status == 200:
                            results.append(f"[+] Found: {url}")
                except: pass
            self.frame.after(0, lambda: self._add_result("Username Check", results))
        threading.Thread(target=do, daemon=True).start()

    def _run_google_dork(self):
        query = self.search_entry.get().strip()
        dorks = [
            f'site:{query} filetype:pdf',
            f'site:{query} intitle:"index of"',
            f'site:{query} inurl:admin',
            f'site:{query} ext:sql | ext:db | ext:backup',
            f'site:pastebin.com {query}',
            f'site:github.com {query}',
        ]
        self._add_result("Google Dorks (Copy to browser)", dorks)

    def _run_hibp(self):
        query = self.search_entry.get().strip()
        if "@" not in query: return
        def do():
            try:
                import urllib.request
                url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{query}"
                req = urllib.request.Request(url, headers={"User-Agent":"CyberLab","hibp-api-key":""})
                with urllib.request.urlopen(req, timeout=10) as r:
                    if r.status == 200:
                        data = json.loads(r.read())
                        results = [f"[!] PWNED! Found in {len(data)} breaches:"]
                        for breach in data:
                            results.append(f"  - {breach.get('Name','?')} ({breach.get('BreachDate','?')})")
                        self.frame.after(0, lambda: self._add_result("HaveIBeenPwned", results))
            except: pass
        threading.Thread(target=do, daemon=True).start()

    def _add_result(self, title, lines):
        if not hasattr(self, 'output'): return
        self.output.insert("end", f"\n{'─'*50}\n")
        self.output.insert("end", f"  {title}\n")
        self.output.insert("end", f"{'─'*50}\n")
        for line in lines[:30]:
            if line.strip():
                self.output.insert("end", f"  {line.strip()[:100]}\n")
        self.output.see("end")
        self.status.config(text=f"Found: {title}")
