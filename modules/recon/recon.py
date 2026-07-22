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
from tkinter import ttk, messagebox
import subprocess
import threading
import os
from datetime import datetime

class ReconWorkspace:
    def __init__(self, parent, db, logger, detector, notifier=None):
        self.parent = parent
        self.db = db
        self.logger = logger
        self.detector = detector
        self.notifier = notifier
        self.frame = tk.Frame(parent, bg='#1a1a2e')
        self.current_project = None
        self.running_processes = []
    
    def build(self):
        self.frame.pack(fill='both', expand=True)
        
        control_frame = tk.Frame(self.frame, bg='#16213e', width=300)
        control_frame.pack(side='left', fill='y')
        control_frame.pack_propagate(False)
        
        output_frame = tk.Frame(self.frame, bg='#1a1a2e')
        output_frame.pack(side='left', fill='both', expand=True)
        
        self._build_controls(control_frame)
        self._build_output(output_frame)
    
    def _build_controls(self, parent):
        tk.Label(parent, text="🎯 Recon Workspace", font=('Courier', 14, 'bold'),
                fg='#00ff88', bg='#16213e').pack(pady=10)
        
        proj_frame = tk.Frame(parent, bg='#16213e')
        proj_frame.pack(fill='x', padx=10, pady=5)
        tk.Label(proj_frame, text="Project:", font=('Courier', 9),
                fg='#aaa', bg='#16213e').pack(anchor='w')
        
        self.project_var = tk.StringVar()
        projects = self.db.get_all_projects()
        names = [p['name'] for p in projects]
        if names:
            self.project_menu = ttk.Combobox(proj_frame, textvariable=self.project_var,
                    values=names, font=('Courier', 9), state='readonly')
            self.project_menu.pack(fill='x', pady=2)
            self.project_menu.set(names[0])
            self._set_project(names[0])
        
        target_frame = tk.Frame(parent, bg='#16213e')
        target_frame.pack(fill='x', padx=10, pady=10)
        tk.Label(target_frame, text="Target:", font=('Courier', 9),
                fg='#aaa', bg='#16213e').pack(anchor='w')
        self.target_entry = tk.Entry(target_frame, font=('Courier', 10),
                bg='#0f3460', fg='#fff', relief='flat')
        self.target_entry.pack(fill='x', pady=2)
        self.target_entry.insert(0, 'example.com')
        
        quick_frame = tk.LabelFrame(parent, text="Quick Scans", font=('Courier', 10),
                fg='#00ccff', bg='#16213e', padx=5, pady=5)
        quick_frame.pack(fill='x', padx=10, pady=10)
        
        scans = [
            ("Nmap Fast", "nmap -F {target}"),
            ("Nmap Service", "nmap -sV {target}"),
            ("Nmap All Ports", "nmap -p- {target}"),
            ("Nmap Scripts", "nmap -sC {target}"),
            ("DNS Lookup", "dig {target} ANY"),
            ("Whois", "whois {target}"),
            ("Ping", "ping -c 4 {target}"),
            ("Traceroute", "traceroute {target}")
        ]
        
        for name, cmd in scans:
            tk.Button(quick_frame, text=name, font=('Courier', 8),
                    fg='#000', bg='#00ccff', relief='flat', pady=3,
                    command=lambda c=cmd, n=name: self._run_scan(c, n)).pack(fill='x', pady=1)
        
        tk.Button(parent, text="STOP ALL", font=('Courier', 10, 'bold'),
                fg='#fff', bg='#cc0000', relief='flat', pady=8,
                command=self._stop_all).pack(fill='x', padx=10, pady=10)
    
    def _build_output(self, parent):
        self.output_text = tk.Text(parent, font=('Courier', 9),
                bg='#0a0a0a', fg='#00ff88', relief='flat', wrap='word')
        self.output_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.status_label = tk.Label(parent, text="Ready", font=('Courier', 9),
                fg='#666', bg='#1a1a2e')
        self.status_label.pack(anchor='w', padx=10, pady=5)
    
    def _set_project(self, name):
        projects = self.db.get_all_projects()
        for p in projects:
            if p['name'] == name:
                self.current_project = p
                break
    
    def _run_scan(self, cmd_template, name):
        target = self.target_entry.get().strip()
        if not target:
            messagebox.showwarning("Warning", "Enter a target first")
            return
        cmd = cmd_template.replace('{target}', target)
        self._execute(cmd, name)
    
    def _execute(self, cmd, name):
        self.output_text.insert('end', f"\n{'='*60}\n")
        self.output_text.insert('end', f"[{datetime.now().strftime('%H:%M:%S')}] {name}\n$ {cmd}\n{'='*60}\n\n")
        self.output_text.see('end')
        self.status_label.config(text=f"Running: {name}...")
        
        if self.notifier:
            self.notifier(f"🔧 Started: {name}", "tool")
        
        def run():
            try:
                self.running_processes.append(cmd)
                _run_cmd(cmd, self.output_text)
                if cmd in self.running_processes:
                    self.running_processes.remove(cmd)
                exit_code = 0
                status = "Complete" if exit_code == 0 else f"Exit: {exit_code}"
                
                self.output_text.insert('end', f"\n[{datetime.now().strftime('%H:%M:%S')}] {status}\n\n")
                self.output_text.see('end')
                self.status_label.config(text=f"Done: {name}")
                
                # Notification
                if self.notifier:
                    if exit_code == 0:
                        self.notifier(f"✅ Complete: {name}", "success")
                    else:
                        self.notifier(f"⚠️ {name} finished with exit {exit_code}", "warning")
                
                if self.current_project:
                    log_dir = os.path.join(self.current_project['path'], 'logs')
                    os.makedirs(log_dir, exist_ok=True)
                    fname = f"recon_{name.replace(' ','_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                    with open(os.path.join(log_dir, fname), 'w') as f:
                        f.write(f"Command: {cmd}\nTime: {datetime.now()}\n{'='*60}\n")
                    
            except Exception as e:
                self.output_text.insert('end', f"\nError: {str(e)}\n")
                self.status_label.config(text=f"Error: {name}")
                if self.notifier:
                    self.notifier(f"❌ Error: {name}", "error")
        
        threading.Thread(target=run, daemon=True).start()
    
    def _stop_all(self):
        for proc in self.running_processes:
            try:
                proc.kill()
            except:
                pass
        self.running_processes.clear()
        self.status_label.config(text="Stopped")
        self.output_text.insert('end', "\n[STOPPED]\n\n")
        if self.notifier:
            self.notifier("🛑 All scans stopped", "warning")
