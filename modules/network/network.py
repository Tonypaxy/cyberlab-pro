import tkinter as tk
from tkinter import messagebox
import subprocess, threading, socket
from gui.base_module import BaseModule
from gui.dropdown import Dropdown

class NetworkWorkspace(BaseModule):
    def __init__(self, parent, db, logger):
        super().__init__(parent)
        self.db = db; self.logger = logger
    
    def build_content(self):
        self.add_title("Network Tools", "Network testing and connectivity tools")
        
        # Host info
        try:
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
            self.create_card(f"Host: {hostname}", f"IP: {ip}", '#58a6ff')
        except: pass
        
        # Network tools - VERTICAL dropdown
        def tools_content(parent):
            tools = [
                ("Ping", "ping -c 4"),
                ("Traceroute", "traceroute"),
                ("Netcat Listen", "nc -lvp"),
                ("Netcat Connect", "nc -v"),
                ("ARP Table", "arp -a"),
                ("Netstat", "netstat -tuln"),
                ("DNS Lookup", "nslookup"),
                ("Curl", "curl -I"),
            ]
            self.target_entries = {}
            for name, cmd in tools:
                row = tk.Frame(parent, bg='#16213e')
                row.pack(fill='x', pady=1)
                tk.Label(row, text=name, font=('Courier', 9), fg='#00ccff', bg='#16213e', width=15, anchor='w').pack(side='left', padx=5)
                e = tk.Entry(row, font=('Courier', 9), bg='#0f3460', fg='#fff', relief='flat')
                e.pack(side='left', fill='x', expand=True, padx=5)
                e.insert(0, 'target' if name not in ('ARP Table','Netstat') else '')
                self.target_entries[name] = e
                tk.Button(row, text="Run", font=('Courier', 8), fg='#000', bg='#00ff88', relief='flat', padx=8,
                        command=lambda n=name, c=cmd: self._run(n, c)).pack(side='right', padx=2)
        
        self.add_section("Tools", tools_content, "🌐", default_open=True)
        
        # Output
        self.output = self.add_text(height=12)
    
    def _run(self, name, cmd):
        target = ""
        if name in self.target_entries:
            target = self.target_entries[name].get().strip()
        full_cmd = f"{cmd} {target}" if target else cmd
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
