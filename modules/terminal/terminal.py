import tkinter as tk
import subprocess
import threading
import os
import sys
import re

class Terminal:
    def __init__(self, parent, config, pending_cmd=None):
        self.parent = parent
        self.config = config
        self.pending_cmd = pending_cmd
        self.frame = tk.Frame(parent, bg='#000000')
        self.is_termux = os.path.exists('/data/data/com.termux/files/usr/bin/bash')
        self.shell = os.environ.get('SHELL', '/bin/bash')
        
    def build(self):
        for w in self.frame.winfo_children(): w.destroy()
        self.frame.pack(fill='both', expand=True)
        
        bar = tk.Frame(self.frame, bg='#1a1a1a', height=24)
        bar.pack(fill='x'); bar.pack_propagate(False)
        
        env = "TERMUX" if self.is_termux else "LINUX"
        tk.Label(bar, text=f"  {env} | {self.shell}", font=('Courier', 8),
                fg='#888', bg='#1a1a1a').pack(side='left', pady=3)
        
        self.output = tk.Text(self.frame, font=('Courier', 10),
                bg='#000000', fg='#00ff00', insertbackground='#00ff00',
                relief='flat', wrap='word')
        self.output.pack(fill='both', expand=True, padx=5, pady=(5,0))
        
        input_frame = tk.Frame(self.frame, bg='#111111')
        input_frame.pack(fill='x', side='bottom')
        
        tk.Label(input_frame, text="$", font=('Courier', 11, 'bold'),
                fg='#00ff00', bg='#111111').pack(side='left', padx=8, pady=5)
        
        self.cmd_entry = tk.Entry(input_frame, font=('Courier', 11),
                bg='#000000', fg='#00ff00', insertbackground='#00ff00', relief='flat')
        self.cmd_entry.pack(side='left', fill='x', expand=True, padx=5, pady=5)
        self.cmd_entry.bind('<Return>', self._run)
        
        tk.Button(input_frame, text="Run", font=('Courier', 10),
                fg='#000', bg='#00ff00', relief='flat', padx=10,
                command=lambda: self._run(None)).pack(side='right', padx=5, pady=5)
        
        if self.pending_cmd:
            self.cmd_entry.insert(0, self.pending_cmd)
        
        self.cmd_entry.focus()
    
    def _run(self, event=None):
        cmd = self.cmd_entry.get().strip()
        if not cmd: return
        self.cmd_entry.delete(0, 'end')
        
        self.output.insert('end', f"\n$ {cmd}\n")
        self.output.see('end')
        
        def execute():
            try:
                p = subprocess.Popen(cmd, shell=True, executable=self.shell,
                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                output_text = ""
                for line in p.stdout:
                    self.output.insert('end', line)
                    self.output.see('end')
                    output_text += line
                p.wait()
                self.output.insert('end', f"\n[Exit: {p.returncode}]\n")
                self.output.see('end')
                
            except Exception as e:
                self.output.insert('end', f"[X] {e}\n")
                self.output.see('end')
        
        threading.Thread(target=execute, daemon=True).start()
    
    
    def set_command(self, cmd):
        self.cmd_entry.delete(0, 'end')
        self.cmd_entry.insert(0, cmd)
        self.cmd_entry.focus()
