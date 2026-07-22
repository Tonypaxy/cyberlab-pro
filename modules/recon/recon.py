import tkinter as tk
from tkinter import ttk, messagebox
import subprocess, threading, os
from datetime import datetime
from gui.base_module import BaseModule
from gui.dropdown import Dropdown

class ReconWorkspace(BaseModule):
    def __init__(self, parent, db, logger, detector, notifier=None):
        super().__init__(parent)
        self.db = db; self.logger = logger; self.detector = detector; self.notifier = notifier
        self.current_project = None; self.running_processes = []
    
    def build_content(self):
        self.add_title("Recon Workspace", "Target-based scanning and reconnaissance")
        
        # Project selector
        projects = self.db.get_all_projects()
        names = [p['name'] for p in projects]
        if names:
            pf = tk.Frame(self.inner, bg='#16213e', padx=10, pady=8)
            pf.pack(fill='x', padx=10, pady=5)
            tk.Label(pf, text="Project:", font=('Courier', 10), fg='#fff', bg='#16213e').pack(side='left')
            self.project_var = tk.StringVar(value=names[0])
            ttk.Combobox(pf, textvariable=self.project_var, values=names, font=('Courier', 10),
                    state='readonly', width=25).pack(side='left', padx=10)
            self._set_project(names[0])
        
        # Target input
        tf = tk.Frame(self.inner, bg='#16213e', padx=10, pady=8)
        tf.pack(fill='x', padx=10, pady=5)
        tk.Label(tf, text="Target:", font=('Courier', 10), fg='#fff', bg='#16213e').pack(anchor='w')
        self.target_entry = tk.Entry(tf, font=('Courier', 11), bg='#0f3460', fg='#fff', relief='flat')
        self.target_entry.pack(fill='x', pady=3)
        self.target_entry.insert(0, 'example.com')
        
        # Quick Scans - VERTICAL dropdown
        def scan_content(parent):
            scans = [
                ("Nmap Fast (-F)", "nmap -F {target}"),
                ("Nmap Service (-sV)", "nmap -sV {target}"),
                ("Nmap All Ports (-p-)", "nmap -p- {target}"),
                ("Nmap Scripts (-sC)", "nmap -sC {target}"),
                ("DNS Lookup", "dig {target} ANY"),
                ("Whois", "whois {target}"),
                ("Ping", "ping -c 4 {target}"),
                ("Traceroute", "traceroute {target}"),
            ]
            for name, cmd in scans:
                tk.Button(parent, text=name, font=('Courier', 9), fg='#00ccff', bg='#16213e',
                        relief='flat', anchor='w', padx=10, pady=3,
                        command=lambda c=cmd, n=name: self._run_scan(c, n)).pack(fill='x', pady=1)
        
        self.add_section("Quick Scans", scan_content, "🎯", default_open=True)
        
        # Recon tools dropdown
        def tools_content(parent):
            recon_tools = self.detector.detected.get('recon', [])
            for tool in recon_tools[:10]:
                tk.Button(parent, text=f"{tool['name']} {tool.get('version','')}", font=('Courier', 9),
                        fg='#00ff88', bg='#16213e', relief='flat', anchor='w', padx=10, pady=3,
                        command=lambda t=tool: self._run_tool(t)).pack(fill='x', pady=1)
        
        self.add_section("Installed Tools", tools_content, "🔧")
        
        # Stop button
        tk.Button(self.inner, text="STOP ALL SCANS", font=('Courier', 10, 'bold'),
                fg='#fff', bg='#cc0000', relief='raised', padx=15, pady=8,
                command=self._stop_all).pack(pady=10)
        
        # Output area
        self.output_text = self.add_text(height=15)
        self.status_label = self.add_status("Ready")
    
    def _set_project(self, name):
        for p in self.db.get_all_projects():
            if p['name'] == name: self.current_project = p; break
    
    def _run_scan(self, cmd_template, name):
        target = self.target_entry.get().strip()
        if not target: messagebox.showwarning("Warning", "Enter a target"); return
        self._execute(cmd_template.replace('{target}', target), name)
    
    def _run_tool(self, tool):
        target = self.target_entry.get().strip()
        if not target: messagebox.showwarning("Warning", "Enter a target"); return
        self._execute(f"{tool['command']} {target}", tool['name'])
    
    def _execute(self, cmd, name):
        self.output_text.insert('end', f"\n{'='*50}\n[{datetime.now().strftime('%H:%M:%S')}] {name}\n$ {cmd}\n{'='*50}\n\n")
        self.output_text.see('end')
        self.status_label.config(text=f"Running: {name}...")
        
        def run():
            try:
                p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                self.running_processes.append(p)
                for line in p.stdout:
                    self.output_text.insert('end', line); self.output_text.see('end')
                p.wait()
                if p in self.running_processes: self.running_processes.remove(p)
                self.output_text.insert('end', f"\n[Exit: {p.returncode}]\n\n"); self.output_text.see('end')
                self.status_label.config(text=f"Done: {name}")
                if self.current_project:
                    log_dir = os.path.join(self.current_project['path'], 'logs')
                    os.makedirs(log_dir, exist_ok=True)
                    with open(os.path.join(log_dir, f"recon_{name.replace(' ','_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"), 'w') as f:
                        f.write(f"Command: {cmd}\nTime: {datetime.now()}\n{'='*50}\n")
            except Exception as e:
                self.output_text.insert('end', f"\n[X] {e}\n")
        threading.Thread(target=run, daemon=True).start()
    
    def _stop_all(self):
        for p in self.running_processes:
            try: p.kill()
            except: pass
        self.running_processes.clear()
        self.status_label.config(text="Stopped")
        self.output_text.insert('end', "\n[STOPPED]\n\n")
