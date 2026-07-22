import tkinter as tk
from tkinter import ttk, messagebox
import subprocess, threading, os, re
from datetime import datetime
from gui.base_module import BaseModule

class LogAnalyzer(BaseModule):
    def __init__(self, parent, db, logger):
        super().__init__(parent)
        self.db = db
        self.logger = logger
        self.current_project = None

    def build_content(self):
        self.add_title("Log Analyzer", "Import and analyze Apache, Nginx, SSH, system logs")
        projects = self.db.get_all_projects()
        names = [p["name"] for p in projects]
        if names:
            pf = tk.Frame(self.inner, bg="#16213e", padx=10, pady=8)
            pf.pack(fill="x", padx=10, pady=5)
            tk.Label(pf, text="Project:", font=("Courier",10), fg="#fff", bg="#16213e").pack(side="left")
            self.project_var = tk.StringVar(value=names[0])
            ttk.Combobox(pf, textvariable=self.project_var, values=names, font=("Courier",10), state="readonly", width=25).pack(side="left", padx=10)
            self._set_project(names[0])

        sf = tk.Frame(self.inner, bg="#16213e", padx=10, pady=8)
        sf.pack(fill="x", padx=10, pady=5)
        tk.Label(sf, text="Log File Path:", font=("Courier",10), fg="#fff", bg="#16213e").pack(anchor="w")
        self.path_entry = tk.Entry(sf, font=("Courier",10), bg="#0f3460", fg="#fff", relief="flat")
        self.path_entry.pack(fill="x", pady=3)
        self.path_entry.insert(0, "/var/log/apache2/access.log")

        bf = tk.Frame(sf, bg="#16213e")
        bf.pack(fill="x", pady=5)
        for text, cmd in [("Apache",self._parse_apache),("Nginx",self._parse_nginx),("SSH",self._parse_ssh),("Syslog",self._parse_syslog)]:
            tk.Button(bf, text=text, font=("Courier",9), fg="#000", bg="#00ccff", relief="flat", padx=10, command=cmd).pack(side="left", padx=2)

        self.results_frame = tk.Frame(self.inner, bg="#1a1a2e")
        self.results_frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.status_label = self.add_status("Enter log file path and select type")

    def _set_project(self, name):
        for p in self.db.get_all_projects():
            if p["name"] == name: self.current_project = p; break

    def _read_log(self):
        path = self.path_entry.get().strip()
        if not os.path.exists(path):
            messagebox.showerror("Error", "File not found: " + path)
            return None
        with open(path, errors="ignore") as f:
            return f.read()

    def _show_results(self, title, data):
        for w in self.results_frame.winfo_children(): w.destroy()
        if not data:
            tk.Label(self.results_frame, text="No data found", font=("Courier",10), fg="#888", bg="#1a1a2e").pack(pady=20)
            return
        tk.Label(self.results_frame, text=title + " (" + str(len(data)) + " entries)", font=("Courier",11,"bold"), fg="#00ff88", bg="#1a1a2e").pack(anchor="w")
        t = tk.Text(self.results_frame, font=("Courier",8), bg="#0a0a0a", fg="#00ff88", relief="flat", wrap="word", height=15)
        t.pack(fill="both", expand=True, pady=5)
        for item in data[:100]:
            t.insert("end", str(item)[:200] + "\n")
        self.status_label.config(text="Found " + str(len(data)) + " entries")

    def _parse_apache(self):
        log = self._read_log()
        if not log: return
        results = []
        ips = set(re.findall(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", log))
        for ip in ips:
            count = log.count(ip)
            results.append({"ip": ip, "requests": count})
        results.sort(key=lambda x: x["requests"], reverse=True)
        self._show_results("Apache Log Analysis", results)

    def _parse_nginx(self):
        self._parse_apache()

    def _parse_ssh(self):
        log = self._read_log()
        if not log: return
        results = []
        failed = log.count("Failed password")
        accepted = log.count("Accepted password")
        ips = set(re.findall(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", log))
        for ip in ips:
            if "Failed" in log[log.find(ip):log.find(ip)+100]:
                results.append({"ip": ip, "type": "Failed attempt"})
        results.insert(0, {"summary": f"Failed: {failed} | Accepted: {accepted}"})
        self._show_results("SSH Log Analysis", results)

    def _parse_syslog(self):
        log = self._read_log()
        if not log: return
        errors = [l.strip() for l in log.split("\n") if "error" in l.lower() or "fail" in l.lower() or "critical" in l.lower()]
        self._show_results("Syslog Errors", errors[:50])
