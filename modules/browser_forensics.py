import tkinter as tk
from tkinter import ttk, messagebox
import subprocess, threading, os, shutil, sqlite3, json, re, base64
from datetime import datetime
from gui.base_module import BaseModule

class BrowserForensics(BaseModule):
    def __init__(self, parent, db, logger):
        super().__init__(parent)
        self.db = db; self.logger = logger
        self.output_dir = os.path.expanduser("~/browser_forensics")
        os.makedirs(self.output_dir, exist_ok=True)

    def build_content(self):
        self.add_title("Browser Forensics", "Cookies, history, passwords, cache, downloads")
        
        bf = tk.Frame(self.inner, bg="#1a1a2e"); bf.pack(fill="x", padx=10, pady=5)
        
        tools = self._detect_tools()
        for name, func, color in tools:
            tk.Button(bf, text=name, font=("Courier",8), fg="#000", bg=color, relief="flat", padx=6,
                    command=func).pack(side="left", padx=2)
        
        tk.Button(bf, text="FULL SCAN", font=("Courier",8,"bold"), fg="#fff", bg="#cc0000",
                relief="flat", padx=8, command=self._full_scan).pack(side="right", padx=2)
        
        self.output = tk.Text(self.inner, font=("Courier",9), bg="#0a0a0a", fg="#00ff88", relief="flat", height=15)
        self.output.pack(fill="both", expand=True, padx=10, pady=5)
        self.status = self.add_status(f"Ready - {len(tools)} forensics tools available")

    def _detect_tools(self):
        tools = []
        
        # === CHROME ===
        chrome_path = os.path.expanduser("~/.config/google-chrome/Default")
        if os.path.exists(chrome_path):
            tools.append(("Chrome History", self._chrome_history, "#4285f4"))
            tools.append(("Chrome Cookies", self._chrome_cookies, "#4285f4"))
            tools.append(("Chrome Passwords", self._chrome_passwords, "#4285f4"))
            tools.append(("Chrome Bookmarks", self._chrome_bookmarks, "#4285f4"))
            tools.append(("Chrome Cache", self._chrome_cache, "#4285f4"))
            tools.append(("Chrome Downloads", self._chrome_downloads, "#4285f4"))
            tools.append(("Chrome Autofill", self._chrome_autofill, "#4285f4"))
            tools.append(("Chrome Extensions", self._chrome_extensions, "#4285f4"))
        
        # === FIREFOX ===
        firefox_path = os.path.expanduser("~/.mozilla/firefox")
        if os.path.exists(firefox_path):
            for profile in os.listdir(firefox_path):
                if profile.endswith(".default-release") or profile.endswith(".default"):
                    tools.append(("Firefox History", lambda: self._firefox_db(profile, "places.sqlite", "moz_places", "url,title,visit_count,last_visit_date"), "#ff9500"))
                    tools.append(("Firefox Cookies", lambda: self._firefox_db(profile, "cookies.sqlite", "moz_cookies", "host,name,value,expiry"), "#ff9500"))
                    tools.append(("Firefox Passwords", lambda: self._firefox_db(profile, "logins.json", None, None), "#ff9500"))
                    tools.append(("Firefox Bookmarks", lambda: self._firefox_db(profile, "places.sqlite", "moz_bookmarks", "title,dateAdded"), "#ff9500"))
                    tools.append(("Firefox Downloads", lambda: self._firefox_db(profile, "places.sqlite", "moz_annos", "content"), "#ff9500"))
                    break
        
        # === OPERA ===
        opera_path = os.path.expanduser("~/.config/opera")
        if os.path.exists(opera_path):
            tools.append(("Opera History", lambda: self._opera_data("History"), "#ff1b2d"))
            tools.append(("Opera Cookies", lambda: self._opera_data("Cookies"), "#ff1b2d"))
        
        # === BRAVE ===
        brave_path = os.path.expanduser("~/.config/BraveSoftware/Brave-Browser/Default")
        if os.path.exists(brave_path):
            tools.append(("Brave History", lambda: self._brave_data("History"), "#fb542b"))
            tools.append(("Brave Cookies", lambda: self._brave_data("Cookies"), "#fb542b"))
        
        # === EDGE ===
        edge_path = os.path.expanduser("~/.config/microsoft-edge/Default")
        if os.path.exists(edge_path):
            tools.append(("Edge History", lambda: self._edge_data("History"), "#0078d7"))
            tools.append(("Edge Cookies", lambda: self._edge_data("Cookies"), "#0078d7"))
        
        # === ALL BROWSERS ===
        tools.append(("All Browsers Report", self._all_browsers_report, "#00ff88"))
        tools.append(("Extract All URLs", self._extract_urls, "#58a6ff"))
        tools.append(("Extract All Emails", self._extract_emails, "#bc8cff"))
        tools.append(("Extract All Creds", self._extract_creds, "#ff4444"))
        tools.append(("Search History", self._search_history, "#ffaa00"))
        tools.append(("Timeline View", self._timeline_view, "#d2991d"))
        
        # === TOOLS ===
        if shutil.which("sqlite3"):
            tools.append(("SQLite Browser", lambda: self._cmd("sqlite3 DB '.tables'"), "#888888"))
        if shutil.which("hindsight"):
            tools.append(("Hindsight", lambda: self._cmd("hindsight -i CHROME_PATH -o " + self.output_dir), "#888888"))
        if shutil.which("browser-history"):
            tools.append(("Browser History CLI", lambda: self._cmd("browser-history"), "#888888"))
        
        return tools

    def _read_sqlite(self, db_path, table, columns="*", limit=100):
        try:
            if not os.path.exists(db_path): return f"[X] Not found: {db_path}"
            conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
            cursor = conn.cursor()
            cursor.execute(f"SELECT {columns} FROM {table} ORDER BY rowid DESC LIMIT {limit}")
            rows = cursor.fetchall()
            conn.close()
            return rows
        except Exception as e:
            return f"[X] {e}"

    def _chrome_history(self):
        path = os.path.expanduser("~/.config/google-chrome/Default/History")
        rows = self._read_sqlite(path, "urls", "url,title,visit_count,datetime(last_visit_time/1000000-11644473600,'unixepoch') as visit_time")
        self._display_table(rows, ["URL","Title","Visits","Last Visit"])

    def _chrome_cookies(self):
        path = os.path.expanduser("~/.config/google-chrome/Default/Cookies")
        rows = self._read_sqlite(path, "cookies", "host_key,name,value,datetime(expires_utc/1000000-11644473600,'unixepoch') as expiry")
        self._display_table(rows, ["Host","Name","Value","Expiry"])

    def _chrome_passwords(self):
        path = os.path.expanduser("~/.config/google-chrome/Default/Login Data")
        rows = self._read_sqlite(path, "logins", "origin_url,username_value,password_value")
        self._display_table(rows, ["URL","Username","Password (encrypted)"])

    def _chrome_bookmarks(self):
        path = os.path.expanduser("~/.config/google-chrome/Default/Bookmarks")
        try:
            with open(path) as f:
                data = json.load(f)
                urls = []
                def extract(nodes):
                    for node in nodes:
                        if node.get("type") == "url":
                            urls.append((node.get("name",""), node.get("url","")))
                        if "children" in node:
                            extract(node["children"])
                extract(data.get("roots",{}).get("bookmark_bar",{}).get("children",[]))
                self._display_table(urls[:50], ["Name","URL"])
        except Exception as e:
            self.output.insert("end", f"\n[X] {e}\n")

    def _chrome_cache(self):
        path = os.path.expanduser("~/.cache/google-chrome/Default/Cache")
        if os.path.exists(path):
            files = os.listdir(path)[:30]
            self.output.insert("end", f"\n[*] Cache files ({len(os.listdir(path))} total):\n")
            for f in files[:30]:
                fpath = os.path.join(path, f)
                size = os.path.getsize(fpath) if os.path.isfile(fpath) else 0
                self.output.insert("end", f"  {f} ({size} bytes)\n")
        else:
            self.output.insert("end", "\n[X] Chrome cache not found\n")

    def _chrome_downloads(self):
        path = os.path.expanduser("~/.config/google-chrome/Default/History")
        rows = self._read_sqlite(path, "downloads", "target_path,datetime(start_time/1000000-11644473600,'unixepoch') as dl_time,total_bytes")
        self._display_table(rows, ["File","Download Time","Size"])

    def _chrome_autofill(self):
        path = os.path.expanduser("~/.config/google-chrome/Default/Web Data")
        rows = self._read_sqlite(path, "autofill", "name,value")
        self._display_table(rows, ["Field","Value"])

    def _chrome_extensions(self):
        path = os.path.expanduser("~/.config/google-chrome/Default/Extensions")
        if os.path.exists(path):
            self.output.insert("end", "\n[*] Chrome Extensions:\n")
            for ext in os.listdir(path)[:20]:
                self.output.insert("end", f"  {ext}\n")
        else:
            self.output.insert("end", "\n[X] Extensions not found\n")

    def _firefox_db(self, profile, db_file, table, columns):
        profile_path = os.path.expanduser(f"~/.mozilla/firefox/{profile}")
        path = os.path.join(profile_path, db_file)
        if db_file.endswith(".json"):
            if os.path.exists(path):
                with open(path) as f:
                    data = json.load(f)
                    self.output.insert("end", f"\n[*] Firefox {db_file}:\n")
                    self.output.insert("end", json.dumps(data, indent=2)[:3000] + "\n")
        else:
            rows = self._read_sqlite(path, table, columns)
            self._display_table(rows, columns.split(",") if columns else ["Data"])

    def _opera_data(self, db_file):
        path = os.path.expanduser(f"~/.config/opera/{db_file}")
        rows = self._read_sqlite(path, "urls" if "History" in db_file else "cookies", "*")
        self._display_table(rows, ["Data"])

    def _brave_data(self, db_file):
        path = os.path.expanduser(f"~/.config/BraveSoftware/Brave-Browser/Default/{db_file}")
        rows = self._read_sqlite(path, "urls" if "History" in db_file else "cookies", "*")
        self._display_table(rows, ["Data"])

    def _edge_data(self, db_file):
        path = os.path.expanduser(f"~/.config/microsoft-edge/Default/{db_file}")
        rows = self._read_sqlite(path, "urls" if "History" in db_file else "cookies", "*")
        self._display_table(rows, ["Data"])

    def _extract_urls(self):
        self.output.insert("end", "\n[*] Extracting URLs from all browsers...\n")
        # Chrome
        chrome_hist = os.path.expanduser("~/.config/google-chrome/Default/History")
        if os.path.exists(chrome_hist):
            rows = self._read_sqlite(chrome_hist, "urls", "url")
            if isinstance(rows, list):
                self.output.insert("end", f"\n[Chrome] {len(rows)} URLs\n")
                for r in rows[:20]: self.output.insert("end", f"  {r[0]}\n")
        # Firefox
        for profile in os.listdir(os.path.expanduser("~/.mozilla/firefox")):
            if profile.endswith(".default-release"):
                ff = os.path.expanduser(f"~/.mozilla/firefox/{profile}/places.sqlite")
                rows = self._read_sqlite(ff, "moz_places", "url")
                if isinstance(rows, list):
                    self.output.insert("end", f"\n[Firefox] {len(rows)} URLs\n")
                    for r in rows[:20]: self.output.insert("end", f"  {r[0]}\n")
                break

    def _extract_emails(self):
        self.output.insert("end", "\n[*] Scanning for emails in browser data...\n")
        all_text = ""
        paths = [
            os.path.expanduser("~/.config/google-chrome/Default/History"),
            os.path.expanduser("~/.config/google-chrome/Default/Web Data"),
        ]
        for path in paths:
            if os.path.exists(path):
                try:
                    conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
                    for table in ["urls","autofill","logins"]:
                        try:
                            cursor = conn.execute(f"SELECT * FROM {table} LIMIT 100")
                            for row in cursor:
                                all_text += str(row) + " "
                        except: pass
                    conn.close()
                except: pass
        emails = set(re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', all_text))
        self.output.insert("end", f"\nFound {len(emails)} emails:\n")
        for e in list(emails)[:20]:
            self.output.insert("end", f"  {e}\n")

    def _extract_creds(self):
        self.output.insert("end", "\n[*] Extracting saved credentials...\n")
        chrome_login = os.path.expanduser("~/.config/google-chrome/Default/Login Data")
        if os.path.exists(chrome_login):
            rows = self._read_sqlite(chrome_login, "logins", "origin_url,username_value,password_value")
            if isinstance(rows, list):
                self.output.insert("end", f"\n[Chrome] {len(rows)} saved logins\n")
                for r in rows[:20]:
                    self.output.insert("end", f"  URL: {r[0]}\n  User: {r[1]}\n  Pass: [encrypted]\n\n")

    def _search_history(self):
        d = tk.Toplevel(self.frame, bg="#1a1a2e"); d.title("Search History"); d.geometry("500x300")
        tk.Label(d, text="Search term:", font=("Courier",10), fg="#fff", bg="#1a1a2e").pack(pady=10)
        search_e = tk.Entry(d, font=("Courier",10), bg="#16213e", fg="#fff", relief="flat")
        search_e.pack(fill="x", padx=20, pady=5)
        def search():
            term = search_e.get().strip()
            if not term: return
            self.output.insert("end", f"\n[*] Searching for: {term}\n")
            chrome_hist = os.path.expanduser("~/.config/google-chrome/Default/History")
            if os.path.exists(chrome_hist):
                conn = sqlite3.connect(f"file:{chrome_hist}?mode=ro", uri=True)
                cursor = conn.execute(f"SELECT url,title FROM urls WHERE url LIKE '%{term}%' OR title LIKE '%{term}%' LIMIT 30")
                for row in cursor:
                    self.output.insert("end", f"  {row[0]} - {row[1]}\n")
                conn.close()
            d.destroy()
        tk.Button(d, text="Search", font=("Courier",10,"bold"), fg="#000", bg="#ffaa00", relief="raised", padx=20, pady=8, command=search).pack(pady=10)

    def _timeline_view(self):
        self.output.insert("end", "\n[*] Building browser timeline...\n")
        chrome_hist = os.path.expanduser("~/.config/google-chrome/Default/History")
        if os.path.exists(chrome_hist):
            conn = sqlite3.connect(f"file:{chrome_hist}?mode=ro", uri=True)
            cursor = conn.execute("SELECT url,title,datetime(last_visit_time/1000000-11644473600,'unixepoch') as t FROM urls ORDER BY last_visit_time DESC LIMIT 50")
            for row in cursor:
                self.output.insert("end", f"  [{row[2]}] {row[0]}\n")
            conn.close()

    def _all_browsers_report(self):
        self._extract_urls()
        self._extract_emails()
        self._extract_creds()
        self._timeline_view()

    def _display_table(self, rows, headers):
        if isinstance(rows, str):
            self.output.insert("end", f"\n{rows}\n"); return
        if not rows:
            self.output.insert("end", "\n[No data found]\n"); return
        
        self.output.insert("end", f"\n{' | '.join(headers)}\n")
        self.output.insert("end", "-" * 60 + "\n")
        for row in rows[:50]:
            self.output.insert("end", " | ".join(str(c)[:50] for c in row) + "\n")
        self.output.insert("end", f"\n({len(rows)} total entries)\n")
        self.output.see("end")

    def _full_scan(self):
        for name, func, _ in self._detect_tools()[:12]:
            self.frame.after(500, func)

    def _cmd(self, cmd):
        self.output.insert("end", f"\n{'='*40}\n$ {cmd[:80]}\n{'='*40}\n\n")
        self.output.see("end")
        def do():
            try:
                p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                out = p.stdout.read()[:5000]
                self.frame.after(0, lambda: self.output.insert("end", out))
                self.frame.after(0, self.output.see("end"))
            except: pass
        threading.Thread(target=do, daemon=True).start()
