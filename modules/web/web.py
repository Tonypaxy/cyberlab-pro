import tkinter as tk
from tkinter import messagebox
import subprocess, threading, shutil
from gui.base_module import BaseModule
from gui.dropdown import Dropdown

class WebWorkspace(BaseModule):
    def __init__(self, parent, db, logger, detector):
        super().__init__(parent)
        self.db = db; self.logger = logger; self.detector = detector
    
    def build_content(self):
        self.add_title("Web Tools", "Web application testing and scanning")
        
        # URL input
        tf = tk.Frame(self.inner, bg='#16213e', padx=10, pady=8)
        tf.pack(fill='x', padx=10, pady=5)
        tk.Label(tf, text="Target URL:", font=('Courier', 10), fg='#fff', bg='#16213e').pack(anchor='w')
        self.url_entry = tk.Entry(tf, font=('Courier', 11), bg='#0f3460', fg='#fff', relief='flat')
        self.url_entry.pack(fill='x', pady=3)
        self.url_entry.insert(0, 'https://example.com')
        
        # Web tools - VERTICAL dropdown
        def tools_content(parent):
            tools = [
                ("cURL GET", "curl -v"),
                ("cURL Headers", "curl -I"),
                ("cURL Full", "curl -v -L"),
                ("SQLMap", "sqlmap -u"),
                ("Dirb", "dirb"),
                ("Nikto", "nikto -h"),
                ("WPScan", "wpscan --url"),
                ("WhatWeb", "whatweb"),
            ]
            for name, cmd in tools:
                tool_name = cmd.split()[0]
                installed = shutil.which(tool_name) is not None
                color = '#00ff88' if installed else '#444'
                state = 'normal' if installed else 'disabled'
                tk.Button(parent, text=name, font=('Courier', 9), fg='#000' if installed else '#666',
                        bg=color, relief='flat', anchor='w', padx=10, pady=3, state=state,
                        command=lambda n=name, c=cmd: self._run(n, c)).pack(fill='x', pady=1)
        
        self.add_section("Scanning Tools", tools_content, "🌍", default_open=True)
        
        # Output
        self.output = self.add_text(height=15)
    
    def _run(self, name, cmd):
        url = self.url_entry.get().strip()
        if not url: messagebox.showwarning("Warning", "Enter a URL"); return
        full_cmd = f"{cmd} {url}"
        self.output.insert('end', f"\n{'='*50}\n[{name}] {full_cmd}\n{'='*50}\n\n")
        self.output.see('end')
        
        def do():
            try:
                p = subprocess.Popen(full_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                for line in p.stdout:
                    self.output.insert('end', line); self.output.see('end')
                p.wait()
                self.output.insert('end', f"\n[Exit: {p.returncode}]\n\n"); self.output.see('end')
            except Exception as e:
                self.output.insert('end', f"\n[X] {e}\n")
        threading.Thread(target=do, daemon=True).start()
