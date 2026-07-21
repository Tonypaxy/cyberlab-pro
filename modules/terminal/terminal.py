import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import threading
import os
import signal
import shutil

class Terminal:
    def __init__(self, parent, config, pending_cmd=None):
        self.parent = parent
        self.config = config
        self.pending_cmd = pending_cmd
        self.frame = tk.Frame(parent, bg='#1a1a2e')
        self.current_process = None
        self.command_history = []
        self.history_index = 0
        
    def build(self):
        self.frame.pack(fill='both', expand=True)
        
        # Toolbar
        toolbar = tk.Frame(self.frame, bg='#0f3460', height=32)
        toolbar.pack(fill='x')
        toolbar.pack_propagate(False)
        
        tk.Label(toolbar, text="💻 Terminal", font=('Courier', 10, 'bold'),
                fg='#00ff88', bg='#0f3460').pack(side='left', padx=10)
        
        self.proc_label = tk.Label(toolbar, text="Ready", font=('Courier', 9),
                fg='#888', bg='#0f3460')
        self.proc_label.pack(side='left', padx=10)
        
        tk.Button(toolbar, text="🛑 Kill", font=('Courier', 8),
                fg='#fff', bg='#cc0000', relief='flat', padx=8,
                command=self._kill).pack(side='right', padx=3)
        tk.Button(toolbar, text="🗑 Clear", font=('Courier', 8),
                fg='#000', bg='#ffaa00', relief='flat', padx=8,
                command=self._clear).pack(side='right', padx=3)
        tk.Button(toolbar, text="📋 CWD", font=('Courier', 8),
                fg='#000', bg='#00ccff', relief='flat', padx=8,
                command=self._show_cwd).pack(side='right', padx=3)
        
        # Main area
        main = tk.Frame(self.frame, bg='#1a1a2e')
        main.pack(fill='both', expand=True)
        
        # Output
        out_frame = tk.Frame(main, bg='#1a1a2e')
        out_frame.pack(fill='both', expand=True, padx=5, pady=(5,0))
        
        self.output = tk.Text(out_frame, font=('Courier', 10),
                bg='#0a0a0a', fg='#00ff88', insertbackground='#00ff88',
                relief='flat', wrap='word')
        self.output.pack(side='left', fill='both', expand=True)
        
        scroll = tk.Scrollbar(out_frame, orient='vertical', command=self.output.yview)
        scroll.pack(side='right', fill='y')
        self.output.configure(yscrollcommand=scroll.set)
        
        # Input
        input_frame = tk.Frame(main, bg='#16213e', height=40)
        input_frame.pack(fill='x', padx=5, pady=5)
        input_frame.pack_propagate(False)
        
        tk.Label(input_frame, text="$", font=('Courier', 12, 'bold'),
                fg='#00ff88', bg='#16213e').pack(side='left', padx=8)
        
        self.cmd_entry = tk.Entry(input_frame, font=('Courier', 11),
                bg='#0a0a0a', fg='#fff', insertbackground='#fff', relief='flat')
        self.cmd_entry.pack(side='left', fill='x', expand=True, padx=(0,5))
        self.cmd_entry.bind('<Return>', self._execute)
        self.cmd_entry.bind('<Up>', self._history_up)
        self.cmd_entry.bind('<Down>', self._history_down)
        
        tk.Button(input_frame, text="▶", font=('Courier', 14, 'bold'),
                fg='#000', bg='#00ff88', relief='flat', padx=12,
                command=lambda: self._execute(None)).pack(side='right', padx=2)
        
        # Welcome
        self._write("🛡️  CyberLab Terminal — Full Bash Power\n", 'header')
        self._write("═" * 55 + "\n", 'header')
        self._write(f"📂 {os.getcwd()}\n", 'info')
        self._write("Runs ANY command: nmap, gobuster, pkg install, git clone...\n", 'info')
        self._write("NO timeout. Arrow keys for history. 🛑 Kill to stop.\n\n", 'info')
        
        if self.pending_cmd:
            self.cmd_entry.insert(0, self.pending_cmd)
            self._write(f"📦 Command ready! Press Enter:\n  {self.pending_cmd}\n\n", 'warning')
        
        self.cmd_entry.focus()
    
    def _write(self, text, tag=None):
        self.output.insert('end', text, tag)
        self.output.see('end')
        self.output.update_idletasks()
    
    def _execute(self, event=None):
        cmd = self.cmd_entry.get().strip()
        self.cmd_entry.delete(0, 'end')
        
        if not cmd:
            return
        
        # History
        if not self.command_history or self.command_history[-1] != cmd:
            self.command_history.append(cmd)
        self.history_index = len(self.command_history)
        
        # Built-ins
        if cmd.lower() == 'clear' or cmd.lower() == 'cls':
            self._clear()
            return
        if cmd.lower() == 'exit':
            return
        if cmd.lower() == 'help':
            self._show_help()
            return
        if cmd.lower() == 'pwd' or cmd.lower() == 'cwd':
            self._write(f"{os.getcwd()}\n", 'info')
            return
        
        # Cd command
        if cmd.startswith('cd '):
            try:
                path = cmd[3:].strip()
                os.chdir(os.path.expanduser(path))
                self._write(f"📂 {os.getcwd()}\n", 'info')
            except Exception as e:
                self._write(f"❌ {e}\n", 'error')
            return
        
        # Kill existing process
        if self.current_process and self.current_process.poll() is None:
            self._write("⚠️  Process running. Click 🛑 Kill first or wait.\n", 'warning')
            self.cmd_entry.insert(0, cmd)
            return
        
        # Execute
        self._write(f"\n$ {cmd}\n", 'prompt')
        self.proc_label.config(text="Running...", fg='#ffaa00')
        
        def run():
            try:
                self.current_process = subprocess.Popen(
                    cmd, shell=True,
                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                    text=True, bufsize=1, universal_newlines=True,
                    preexec_fn=os.setsid if hasattr(os, 'setsid') else None
                )
                
                for line in iter(self.current_process.stdout.readline, ''):
                    self.frame.after(0, lambda l=line: self._write(l))
                
                self.current_process.wait()
                code = self.current_process.returncode
                
                self.frame.after(0, lambda: self._write("─" * 55 + "\n"))
                if code == 0:
                    self.frame.after(0, lambda: self._write("✅ Done\n\n", 'success'))
                else:
                    self.frame.after(0, lambda: self._write(f"⚠️  Exit: {code}\n\n", 'warning'))
                
                self.frame.after(0, lambda: self.proc_label.config(text="Ready", fg='#888'))
                self.current_process = None
                
            except Exception as e:
                self.frame.after(0, lambda: self._write(f"❌ {e}\n\n", 'error'))
                self.frame.after(0, lambda: self.proc_label.config(text="Error", fg='#cc0000'))
                self.current_process = None
        
        threading.Thread(target=run, daemon=True).start()
    
    def _kill(self):
        if self.current_process and self.current_process.poll() is None:
            try:
                if hasattr(os, 'killpg'):
                    os.killpg(os.getpgid(self.current_process.pid), signal.SIGTERM)
                else:
                    self.current_process.kill()
                self._write("\n🛑 Killed\n\n", 'warning')
                self.proc_label.config(text="Killed", fg='#cc0000')
                self.current_process = None
            except Exception as e:
                self._write(f"❌ {e}\n", 'error')
        else:
            self._write("No process running\n", 'info')
    
    def _clear(self):
        self.output.delete('1.0', 'end')
    
    def _show_cwd(self):
        self._write(f"📂 {os.getcwd()}\n", 'info')
        files = os.listdir('.')[:20]
        self._write("  " + '  '.join(files) + "\n", 'info')
    
    def _show_help(self):
        self._write("""
🛡️  CyberLab Terminal Commands:
  clear/cls  - Clear screen
  exit       - Close session  
  help       - This help
  pwd/cwd    - Show current directory
  cd <dir>   - Change directory
  🛑 Kill    - Stop running process
  ↑/↓        - Command history

Full bash power: pipes, redirection, &&, ||, ; all work.
Examples:
  nmap -sV 192.168.1.1
  pkg install python -y
  go build && ./binary
  cat /proc/cpuinfo | grep model
  find . -name "*.py" -exec grep -l "TODO" {} \\;
""", 'info')
    
    def _history_up(self, event):
        if self.command_history and self.history_index > 0:
            self.history_index -= 1
            self.cmd_entry.delete(0, 'end')
            self.cmd_entry.insert(0, self.command_history[self.history_index])
    
    def _history_down(self, event):
        if self.history_index < len(self.command_history) - 1:
            self.history_index += 1
            self.cmd_entry.delete(0, 'end')
            self.cmd_entry.insert(0, self.command_history[self.history_index])
        else:
            self.history_index = len(self.command_history)
            self.cmd_entry.delete(0, 'end')
    
    def set_command(self, cmd):
        self.cmd_entry.delete(0, 'end')
        self.cmd_entry.insert(0, cmd)
        self.cmd_entry.focus()
