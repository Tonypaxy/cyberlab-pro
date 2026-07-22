import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import os, json, subprocess
from gui.base_module import BaseModule

class ReportTemplates(BaseModule):
    def __init__(self, parent, db, logger):
        super().__init__(parent)
        self.db = db
        self.logger = logger
        self.current_project = None
        self.section_entries = {}
        self.templates = {
            "Executive Summary": ["Engagement Overview","Scope","Key Findings","Risk Rating","Critical Issues","Recommendations"],
            "Technical Findings": ["Vulnerability Title","CVE Reference","CVSS Score","Affected Systems","Description","PoC","Impact","Remediation"],
            "Web App Test": ["App Overview","Authentication","Authorization","XSS/SQLi","Session Mgmt","File Upload","API Security"],
            "Network Pentest": ["External Recon","Port Scanning","Service Enum","Vulnerability Assessment","Exploitation","Post-Exploitation"],
            "Bug Bounty": ["Vulnerability Title","Severity","Endpoint","Description","Steps to Reproduce","PoC","Impact","Suggested Fix"],
        }

    def build_content(self):
        self.add_title("Report Templates", "Pre-built pentest report formats")
        projects = self.db.get_all_projects()
        names = [p["name"] for p in projects]
        if names:
            pf = tk.Frame(self.inner, bg="#16213e", padx=10, pady=8)
            pf.pack(fill="x", padx=10, pady=5)
            tk.Label(pf, text="Project:", font=("Courier",10), fg="#fff", bg="#16213e").pack(side="left")
            self.project_var = tk.StringVar(value=names[0])
            ttk.Combobox(pf, textvariable=self.project_var, values=names, font=("Courier",10), state="readonly", width=25).pack(side="left", padx=10)
            self._set_project(names[0])
        for name, sections in self.templates.items():
            tk.Button(self.inner, text=name + " (" + str(len(sections)) + " sections)", font=("Courier",9),
                    fg="#00ccff", bg="#16213e", relief="flat", anchor="w", padx=10, pady=4,
                    command=lambda n=name: self._load(n)).pack(fill="x", padx=10, pady=1)
        self.editor_frame = tk.Frame(self.inner, bg="#1a1a2e")
        self.editor_frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.status_label = self.add_status("Select a template")

    def _set_project(self, name):
        for p in self.db.get_all_projects():
            if p["name"] == name: self.current_project = p; break

    def _load(self, name):
        for w in self.editor_frame.winfo_children(): w.destroy()
        template = self.templates.get(name)
        if not template: return
        self.status_label.config(text="Template: " + name)
        self.section_entries = {}
        for section in template:
            card = tk.Frame(self.editor_frame, bg="#16213e", padx=10, pady=6)
            card.pack(fill="x", pady=2)
            tk.Label(card, text=section, font=("Courier",9,"bold"), fg="#ffaa00", bg="#16213e").pack(anchor="w")
            t = tk.Text(card, font=("Courier",9), bg="#0f3460", fg="#fff", relief="flat", height=3, wrap="word")
            t.pack(fill="x", pady=3)
            self.section_entries[section] = t
        bf = tk.Frame(self.editor_frame, bg="#1a1a2e")
        bf.pack(fill="x", pady=10)
        tk.Button(bf, text="Export HTML", font=("Courier",10,"bold"), fg="#000", bg="#00ff88", relief="raised", padx=15, pady=6, command=lambda: self._export("html")).pack(side="left", padx=3)
        tk.Button(bf, text="Export TXT", font=("Courier",10), fg="#000", bg="#00ccff", relief="raised", padx=15, pady=6, command=lambda: self._export("txt")).pack(side="left", padx=3)

    def _export(self, fmt):
        if not self.current_project: messagebox.showwarning("Warning","Select a project"); return
        export_dir = os.path.join(self.current_project["path"], "exports")
        os.makedirs(export_dir, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        sections = {}
        for name, w in self.section_entries.items():
            sections[name] = w.get("1.0","end-1c").strip()
        if fmt == "html":
            path = os.path.join(export_dir, "report_" + ts + ".html")
            with open(path, "w") as f:
                f.write("<html><head><style>body{background:#fff;color:#333;font:14px Arial;max-width:800px;margin:40px auto}h1{color:#1a1a2e;border-bottom:3px solid #00ff88}h2{color:#333;margin-top:30px}.section{margin:20px 0;padding:15px;background:#f9f9f9;border-left:4px solid #00ff88}</style></head><body>")
                f.write("<h1>" + self.status_label.cget("text").replace("Template: ","") + "</h1>")
                for n, c in sections.items():
                    f.write("<h2>" + n + "</h2><div class=\"section\">" + (c or "N/A") + "</div>")
                f.write("</body></html>")
        elif fmt == "txt":
            path = os.path.join(export_dir, "report_" + ts + ".txt")
            with open(path, "w") as f:
                f.write(self.status_label.cget("text").replace("Template: ","") + "\n" + "="*50 + "\n\n")
                for n, c in sections.items():
                    f.write("--- " + n + " ---\n" + (c or "N/A") + "\n\n")
        messagebox.showinfo("Exported", "Report saved to:\n" + path)
        self.logger.log_project_action(self.current_project["name"], "report_exported")