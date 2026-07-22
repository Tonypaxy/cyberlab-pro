"""
CyberLab Pro - Native System Terminal
Launches the actual system terminal (Termux/bash) directly.
No emulation. Just the real thing in a window.
"""
import tkinter as tk
import subprocess
import os
import sys
import platform

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
        
        # Header bar
        bar = tk.Frame(self.frame, bg='#222222', height=26)
        bar.pack(fill='x')
        bar.pack_propagate(False)
        
        env = "TERMUX" if self.is_termux else platform.system().upper()
        tk.Label(bar, text=f"  {env} | {self.shell}", font=('Courier', 8),
                fg='#888', bg='#222222').pack(side='left', pady=4)
        
        # Launch real terminal button
        tk.Button(bar, text="Open Real Terminal", font=('Courier', 9),
                fg='#000', bg='#00ff88', relief='flat', padx=15,
                command=self._launch_native_terminal).pack(side='right', padx=5, pady=2)
        
        # Message area
        msg = tk.Frame(self.frame, bg='#000000')
        msg.pack(fill='both', expand=True)
        
        info = f"""
    CyberLab Terminal
    
    This uses your real system terminal.
    
    Shell: {self.shell}
    System: {'Termux/Android' if self.is_termux else platform.system()}
    Home: {os.path.expanduser('~')}
    
    Click 'Open Real Terminal' to launch.
    Or use the embedded command runner below.
    """
        
        tk.Label(msg, text=info, font=('Courier', 10),
                fg='#00ff88', bg='#000000', justify='left').pack(pady=20)
        
        # Quick command input
        input_frame = tk.Frame(self.frame, bg='#111111')
        input_frame.pack(fill='x', side='bottom')
        
        tk.Label(input_frame, text="$", font=('Courier', 11, 'bold'),
                fg='#00ff88', bg='#111111').pack(side='left', padx=8, pady=5)
        
        self.cmd_entry = tk.Entry(input_frame, font=('Courier', 11),
                bg='#000000', fg='#00ff88', insertbackground='#00ff88', relief='flat')
        self.cmd_entry.pack(side='left', fill='x', expand=True, padx=5, pady=5)
        self.cmd_entry.bind('<Return>', self._run_quick_cmd)
        
        tk.Button(input_frame, text="Run", font=('Courier', 10),
                fg='#000', bg='#00ff88', relief='flat', padx=10,
                command=lambda: self._run_quick_cmd(None)).pack(side='right', padx=5, pady=5)
        
        # Output area
        self.output = tk.Text(self.frame, font=('Courier', 9),
                bg='#000000', fg='#00ff88', relief='flat', wrap='word', height=8)
        self.output.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Pre-fill pending command
        if self.pending_cmd:
            self.cmd_entry.insert(0, self.pending_cmd)
        
        self.cmd_entry.focus()
    
    def _launch_native_terminal(self):
        """Open the actual system terminal"""
        if self.is_termux:
            # Open Termux app
            try:
                subprocess.Popen(['am', 'start', '-n', 'com.termux/.app.TermuxActivity'],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except:
                os.system('termux-open 2>/dev/null &')
        else:
            # Open Linux terminal
            terms = ['x-terminal-emulator', 'gnome-terminal', 'xfce4-terminal', 
                    'konsole', 'lxterminal', 'terminator', 'alacritty', 'kitty', 'xterm']
            for term in terms:
                try:
                    subprocess.Popen([term], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    break
                except:
                    continue
    
    def _run_quick_cmd(self, event=None):
        """Run a command and show output"""
        cmd = self.cmd_entry.get().strip()
        if not cmd: return
        
        self.cmd_entry.delete(0, 'end')
        self.output.insert('end', f"\n$ {cmd}\n{'='*40}\n", 'prompt')
        self.output.see('end')
        self.output.tag_config('prompt', foreground='#ffff00')
        
        def run():
            try:
                p = subprocess.Popen(cmd, shell=True, executable=self.shell,
                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                for line in p.stdout:
                    self.output.insert('end', line)
                    self.output.see('end')
                p.wait()
                self.output.insert('end', f"\n[Exit: {p.returncode}]\n\n")
                self.output.see('end')
            except Exception as e:
                self.output.insert('end', f"[X] {e}\n")
                self.output.see('end')
        
        import threading
        threading.Thread(target=run, daemon=True).start()
    
    def set_command(self, cmd):
        self.cmd_entry.delete(0, 'end')
        self.cmd_entry.insert(0, cmd)
        self.cmd_entry.focus()
