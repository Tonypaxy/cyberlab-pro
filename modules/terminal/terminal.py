import tkinter as tk
import subprocess, threading, os, sys, signal, time

class Terminal:
    def __init__(self, parent, config, pending_cmd=None):
        self.parent = parent
        self.config = config
        self.pending_cmd = pending_cmd
        self.frame = tk.Frame(parent, bg='#0d1117')
        self.is_termux = os.path.exists('/data/data/com.termux/files/usr/bin/bash')
        self.shell = os.environ.get('SHELL', '/bin/bash')
        self.current_process = None
        self.command_history = []
        self.history_index = 0
        self.output_lines = 0
        self.full_output = ""
        self._file_backed = False

    def build(self):
        for w in self.frame.winfo_children(): w.destroy()
        self.frame.pack(fill='both', expand=True)
        
        toolbar = tk.Frame(self.frame, bg='#161b22', height=28)
        toolbar.pack(fill='x'); toolbar.pack_propagate(False)
        
        env = "TERMUX" if self.is_termux else "LINUX"
        tk.Label(toolbar, text=f"  {env} | {self.shell}", font=('Courier',9,'bold'),
                fg='#58a6ff', bg='#161b22').pack(side='left', pady=4)
        
        self.status_dot = tk.Label(toolbar, text="●", font=('Courier',9), fg='#3fb950', bg='#161b22')
        self.status_dot.pack(side='left', padx=5)
        
        self.line_count = tk.Label(toolbar, text="0 lines", font=('Courier',8), fg='#8b949e', bg='#161b22')
        self.line_count.pack(side='left', padx=5)
        
        tk.Button(toolbar, text="Kill", font=('Courier',9), fg='#f85149', bg='#161b22',
                relief='flat', padx=10, command=self._kill).pack(side='right')
        tk.Button(toolbar, text="Clear", font=('Courier',9), fg='#8b949e', bg='#161b22',
                relief='flat', padx=10, command=self._clear).pack(side='right')
        tk.Button(toolbar, text="Save", font=('Courier',9), fg='#58a6ff', bg='#161b22',
                relief='flat', padx=10, command=self._save_output).pack(side='right')
        
        # Main output - NO cap on what's stored
        self.output = tk.Text(self.frame, font=('Courier',10),
                bg='#0d1117', fg='#c9d1d9', insertbackground='#58a6ff',
                relief='flat', wrap='word', padx=5, pady=5,
                maxundo=0,  # Disable undo to save memory on huge outputs
                autoseparators=False)
        self.output.pack(fill='both', expand=True)
        
        scroll = tk.Scrollbar(self.output)
        scroll.pack(side='right', fill='y')
        self.output.configure(yscrollcommand=scroll.set)
        scroll.config(command=self.output.yview)
        
        # Input
        input_frame = tk.Frame(self.frame, bg='#161b22', height=36)
        input_frame.pack(fill='x'); input_frame.pack_propagate(False)
        
        self.prompt_label = tk.Label(input_frame, text="$", font=('Courier',11,'bold'),
                fg='#58a6ff', bg='#161b22')
        self.prompt_label.pack(side='left', padx=8)
        
        self.cmd_entry = tk.Entry(input_frame, font=('Courier',11),
                bg='#161b22', fg='#c9d1d9', insertbackground='#58a6ff',
                relief='flat', bd=0)
        self.cmd_entry.pack(side='left', fill='x', expand=True, padx=5)
        self.cmd_entry.bind('<Return>', self._execute)
        self.cmd_entry.bind('<Up>', self._history_up)
        self.cmd_entry.bind('<Down>', self._history_down)
        self.cmd_entry.bind('<Control-c>', lambda e: self._kill())
        self.cmd_entry.bind('<Control-l>', lambda e: self._clear())
        
        tk.Button(input_frame, text="Run", font=('Courier',10,'bold'),
                fg='#000', bg='#3fb950', relief='flat', padx=12,
                command=lambda: self._execute(None)).pack(side='right', padx=2)
        
        if self.pending_cmd:
            self.cmd_entry.insert(0, self.pending_cmd)
            self._write(f"[*] Command ready - press Enter\n", '#d2991d')
        
        self.cmd_entry.focus()

    def _write(self, text, color='#c9d1d9'):
        """Write with automatic display trimming but full storage"""
        self.full_output += text
        
        tag = f'c_{color.replace("#","")}'
        self.output.tag_config(tag, foreground=color)
        self.output.insert('end', text, tag)
        self.output.see('end')
        
        self.output_lines += text.count('\n')
        
        # For extremely large outputs (>100K lines), switch to file-backed storage
        if self.output_lines > 100000 and not hasattr(self, '_file_backed'):
            self._write("[*] Large output detected - enabling file backup\n", '#d2991d')
            self._file_backed = True
        
        # For extremely large outputs (>100K lines), switch to file-backed storage
        if self.output_lines > 100000 and not hasattr(self, '_file_backed'):
            self._write("[*] Large output detected - enabling file backup\n", '#d2991d')
            self._file_backed = True
        

        
        # Update line count in toolbar
        self.line_count.config(text=f"{self.output_lines:,} lines")
        
        # Update UI without blocking
        self.output.update_idletasks()

    def _execute(self, event=None):
        cmd = self.cmd_entry.get().strip()
        self.cmd_entry.delete(0, 'end')
        if not cmd: return
        
        if not self.command_history or self.command_history[-1] != cmd:
            self.command_history.append(cmd)
        self.history_index = len(self.command_history)
        
        if cmd.lower() in ('clear', 'cls'): self._clear(); return
        if cmd.lower() == 'exit': return
        
        if cmd.startswith('cd '):
            try:
                os.chdir(os.path.expanduser(cmd[3:].strip()))
                self._write(f"📂 {os.getcwd()}\n", '#58a6ff')
            except Exception as e:
                self._write(f"cd: {e}\n", '#f85149')
            return
        
        if self.current_process and self.current_process.poll() is None:
            self._write("[!] Process running. Click Kill first.\n", '#d2991d')
            self.cmd_entry.insert(0, cmd)
            return
        
        self._write(f"\n$ {cmd}\n", '#c9d1d9')
        self.status_dot.config(fg='#d2991d')
        
        def run():
            try:
                self.current_process = subprocess.Popen(
                    cmd, shell=True, executable=self.shell,
                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                    text=True, bufsize=1, universal_newlines=True,
                    preexec_fn=os.setsid if hasattr(os, 'setsid') else None
                )
                
                # Read line by line - no buffer limit
                for line in iter(self.current_process.stdout.readline, ''):
                    self.frame.after(0, lambda l=line: self._write(l))
                
                self.current_process.wait()
                code = self.current_process.returncode
                
                self.frame.after(0, lambda: self._write(f"\n[Exit: {code}]\n", '#8b949e'))
                self.frame.after(0, lambda: self.status_dot.config(fg='#3fb950' if code == 0 else '#f85149'))
                self.current_process = None
                
            except Exception as e:
                self.frame.after(0, lambda: self._write(f"\n[X] {e}\n", '#f85149'))
                self.frame.after(0, lambda: self.status_dot.config(fg='#f85149'))
                self.current_process = None
        
        threading.Thread(target=run, daemon=True).start()

    def _kill(self):
        if self.current_process and self.current_process.poll() is None:
            try:
                if hasattr(os, 'killpg'):
                    os.killpg(os.getpgid(self.current_process.pid), signal.SIGKILL)
                else:
                    self.current_process.kill()
                self._write("\n[KILLED]\n", '#f85149')
                self.status_dot.config(fg='#f85149')
                self.current_process = None
            except Exception as e:
                self._write(f"\n[X] {e}\n", '#f85149')

    def _clear(self):
        self.output.delete('1.0', 'end')
        self.full_output = ""
        self.output_lines = 0
        self.line_count.config(text="0 lines")

    def _save_output(self):
        if not self.full_output.strip(): return
        path = os.path.expanduser(f"~/terminal_output_{int(time.time())}.txt")
        with open(path, 'w') as f:
            f.write(self.full_output)
        self._write(f"\n[Saved to {path}]\n", '#58a6ff')

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
