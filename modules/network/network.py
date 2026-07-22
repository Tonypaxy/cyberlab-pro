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
import socket
from datetime import datetime

class NetworkWorkspace:
    def __init__(self, parent, db, logger):
        self.parent = parent
        self.db = db
        self.logger = logger
        self.frame = tk.Frame(parent, bg='#1a1a2e')
    
    def build(self):
        self.frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        tk.Label(self.frame, text="Network Tools", font=('Courier', 18, 'bold'),
                fg='#00ff88', bg='#1a1a2e').pack(anchor='w', pady=(0,10))
        
        # Network info
        info_frame = tk.LabelFrame(self.frame, text="Local Network Info", 
                font=('Courier', 10, 'bold'), fg='#00ccff', bg='#16213e', padx=15, pady=15)
        info_frame.pack(fill='x', pady=5)
        
        try:
            hostname = socket.gethostname()
            tk.Label(info_frame, text=f"Hostname: {hostname}", font=('Courier', 10),
                    fg='#fff', bg='#16213e').pack(anchor='w')
        except:
            pass
        
        try:
            ip = socket.gethostbyname(socket.gethostname())
            tk.Label(info_frame, text=f"Local IP: {ip}", font=('Courier', 10),
                    fg='#fff', bg='#16213e').pack(anchor='w')
        except:
            pass
        
        # Tools grid
        tools = [
            ("Ping", "ping -c 4", "Target IP/host"),
            ("Traceroute", "traceroute", "Target IP/host"),
            ("Netcat Listen", "nc -lvp", "Port number"),
            ("Netcat Connect", "nc -v", "IP port"),
            ("ARP Table", "arp -a", ""),
            ("Netstat", "netstat -tuln", ""),
            ("DNS Lookup", "nslookup", "Domain"),
            ("Curl", "curl -I", "URL")
        ]
        
        self.target_entries = {}
        
        for name, cmd, placeholder in tools:
            tool_frame = tk.LabelFrame(self.frame, text=name, font=('Courier', 9),
                    fg='#00ccff', bg='#16213e', padx=10, pady=8)
            tool_frame.pack(fill='x', pady=3)
            
            entry_frame = tk.Frame(tool_frame, bg='#16213e')
            entry_frame.pack(fill='x')
            
            if placeholder:
                entry = tk.Entry(entry_frame, font=('Courier', 10), bg='#0f3460',
                        fg='#fff', relief='flat')
                entry.pack(side='left', fill='x', expand=True, padx=(0,5))
                entry.insert(0, placeholder)
                self.target_entries[name] = entry
            
            tk.Button(entry_frame, text="Run", font=('Courier', 9),
                    fg='#000', bg='#00ff88', relief='flat', padx=10,
                    command=lambda n=name, c=cmd: self._run_tool(n, c)).pack(side='right')
        
        # Output
        output_frame = tk.LabelFrame(self.frame, text="Output", font=('Courier', 10, 'bold'),
                fg='#00ccff', bg='#16213e', padx=5, pady=5)
        output_frame.pack(fill='both', expand=True, pady=(10,0))
        
        self.output = tk.Text(output_frame, font=('Courier', 9),
                bg='#0a0a0a', fg='#00ff88', relief='flat', wrap='word')
        self.output.pack(fill='both', expand=True)
    
    def _run_tool(self, name, cmd):
        target = ""
        if name in self.target_entries:
            target = self.target_entries[name].get().strip()
            if not target:
                messagebox.showwarning("Warning", f"Enter target for {name}")
                return
            full_cmd = f"{cmd} {target}"
        else:
            full_cmd = cmd
        
        self.output.insert('end', f"\n{'='*50}\n")
        self.output.insert('end', f"[{name}] {full_cmd}\n{'='*50}\n\n")
        self.output.see('end')
        
        def run():
            try:
                process = subprocess.Popen(full_cmd, shell=True, stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT, text=True)
                for line in process.stdout:
                    self.output.insert('end', line)
                    self.output.see('end')
                self.output.insert('end', f"\n[Exit: {process.returncode}]\n\n")
                self.output.see('end')
                self.logger.log_tool_execution(name, full_cmd, "completed")
            except Exception as e:
                self.output.insert('end', f"Error: {str(e)}\n")
        
        threading.Thread(target=run, daemon=True).start()
