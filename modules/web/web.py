import subprocess as _sp

def _run_cmd(cmd, widget):
    """Run command and stream output to widget"""
    def _run():
        try:
            p = _sp.Popen(cmd, shell=True, stdout=_sp.PIPE, stderr=_sp.STDOUT, text=True, bufsize=1)
            for line in iter(p.stdout.readline, ''):
                widget.insert('end', line)
                widget.see('end')
                widget.update_idletasks()
            p.wait()
            widget.insert('end', f'\n✅ Exit: {p.returncode}\n')
            widget.see('end')
        except Exception as e:
            widget.insert('end', f'\n❌ {e}\n')
            widget.see('end')
    import threading
    threading.Thread(target=_run, daemon=True).start()

import tkinter as tk
from gui.scrollable import make_scrollable
from tkinter import ttk, messagebox
import subprocess
import threading
import shutil

class WebWorkspace:
    def __init__(self, parent, db, logger, detector):
        self.parent = parent
        self.db = db
        self.logger = logger
        self.detector = detector
        self.frame = tk.Frame(parent, bg='#1a1a2e')
    
    def build(self):
        self.frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        tk.Label(self.frame, text="Web Tools", font=('Courier', 18, 'bold'),
                fg='#00ff88', bg='#1a1a2e').pack(anchor='w', pady=(0,10))
        
        # URL input
        url_frame = tk.Frame(self.frame, bg='#16213e')
        url_frame.pack(fill='x', pady=10)
        
        tk.Label(url_frame, text="Target URL:", font=('Courier', 10),
                fg='#fff', bg='#16213e').pack(side='left', padx=10)
        self.url_entry = tk.Entry(url_frame, font=('Courier', 11), bg='#0f3460',
                fg='#fff', relief='flat')
        self.url_entry.pack(side='left', fill='x', expand=True, padx=10, pady=8)
        self.url_entry.insert(0, 'https://example.com')
        
        # Web tools - only show installed ones
        tools_frame = tk.LabelFrame(self.frame, text="Available Tools", 
                font=('Courier', 10, 'bold'), fg='#00ccff', bg='#16213e', padx=15, pady=15)
        tools_frame.pack(fill='x', pady=10)
        
        web_tools = [
            ("cURL GET", "curl -v"),
            ("cURL Headers", "curl -I"),
            ("cURL Full", "curl -v -L"),
            ("SQLMap", "sqlmap -u"),
            ("Dirb", "dirb"),
            ("Nikto", "nikto -h"),
            ("WPScan", "wpscan --url"),
            ("WhatWeb", "whatweb")
        ]
        
        for name, cmd in web_tools:
            tool_name = cmd.split()[0]
            installed = shutil.which(tool_name) is not None
            color = '#00ccff' if installed else '#444'
            state = 'normal' if installed else 'disabled'
            
            btn = tk.Button(tools_frame, text=name, font=('Courier', 9),
                    fg='#000' if installed else '#666', bg=color, relief='flat', 
                    padx=10, pady=5, state=state,
                    command=lambda n=name, c=cmd: self._run_web_tool(n, c))
            btn.pack(side='left', padx=3)
        
        # Output
        out_frame = tk.LabelFrame(self.frame, text="Output", font=('Courier', 10, 'bold'),
                fg='#00ccff', bg='#16213e', padx=5, pady=5)
        out_frame.pack(fill='both', expand=True, pady=(10,0))
        
        self.output = tk.Text(out_frame, font=('Courier', 9),
                bg='#0a0a0a', fg='#00ff88', relief='flat', wrap='word')
        self.output.pack(fill='both', expand=True)
    
    def _run_web_tool(self, name, cmd):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("Warning", "Enter a URL first")
            return
        
        full_cmd = f"{cmd} {url}"
        self.output.insert('end', f"\n{'='*50}\n[{name}] {full_cmd}\n{'='*50}\n\n")
        self.output.see('end')
        
        def run():
            try:
                process = subprocess.Popen(full_cmd, shell=True, stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT, text=True)
                for line in process.stdout:
                    self.output.insert('end', line)
                    self.output.see('end')
                process.wait()
                self.output.insert('end', f"\n[Done - Exit: {process.returncode}]\n\n")
                self.output.see('end')
            except Exception as e:
                self.output.insert('end', f"\nError: {str(e)}\n")
                self.output.see('end')
        
        threading.Thread(target=run, daemon=True).start()
