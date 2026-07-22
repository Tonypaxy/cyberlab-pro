import tkinter as tk
from gui.scrollable import make_scrollable
from tkinter import ttk
import subprocess
import os

class Terminal:
    def __init__(self, parent, config):
        self.parent = parent
        self.config = config
        self.frame = tk.Frame(parent, bg='#1a1a2e')
        self.process = None
    
    def build(self):
        self.frame.pack(fill="both", expand=True)
        
        # Terminal output
        self.output = tk.Text(self.frame, font=('Courier', 10),
                bg='#0a0a0a', fg='#00ff88', insertbackground='#00ff88',
                relief='flat', wrap='word')
        self.output.pack(fill='both', expand=True, padx=5, pady=(5,0))
        
        # Input bar
        input_frame = tk.Frame(self.frame, bg='#16213e', height=35)
        input_frame.pack(fill='x', padx=5, pady=5)
        input_frame.pack_propagate(False)
        
        tk.Label(input_frame, text="$", font=('Courier', 12, 'bold'),
                fg='#00ff88', bg='#16213e').pack(side='left', padx=5)
        
        self.cmd_entry = tk.Entry(input_frame, font=('Courier', 11),
                bg='#0a0a0a', fg='#fff', insertbackground='#fff',
                relief='flat')
        self.cmd_entry.pack(side='left', fill='x', expand=True, padx=(0,5))
        self.cmd_entry.bind('<Return>', self._execute)
        self.cmd_entry.focus()
        
        # Welcome message
        self.output.insert('end', "CyberLab Terminal\n")
        self.output.insert('end', "=" * 50 + "\n")
        self.output.insert('end', f"CWD: {os.getcwd()}\n")
        self.output.insert('end', "Type commands below. 'clear' to clear screen.\n\n")
        self.output.see('end')
    
    def _execute(self, event):
        cmd = self.cmd_entry.get().strip()
        self.cmd_entry.delete(0, 'end')
        
        if not cmd:
            return
        
        if cmd.lower() == 'clear':
            self.output.delete('1.0', 'end')
            return
        
        if cmd.lower() == 'exit':
            return
        
        self.output.insert('end', f"\n$ {cmd}\n", 'prompt')
        self.output.see('end')
        
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True,
                    text=True, timeout=30, cwd=os.getcwd())
            
            if result.stdout:
                self.output.insert('end', result.stdout)
            if result.stderr:
                self.output.insert('end', result.stderr, 'error')
            
            self.output.insert('end', f"\n[Exit: {result.returncode}]\n")
        except subprocess.TimeoutExpired:
            self.output.insert('end', "\n[Timeout: Command took too long]\n", 'error')
        except Exception as e:
            self.output.insert('end', f"\n[Error: {str(e)}]\n", 'error')
        
        self.output.see('end')
        self.output.tag_config('prompt', foreground='#00ff88')
        self.output.tag_config('error', foreground='#ff4444')
