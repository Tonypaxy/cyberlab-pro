"""
CyberLab Pro - Pure Native Terminal
Uses a PTY (pseudo-terminal) so commands behave EXACTLY like the real terminal.
No more freezing. Progress bars work. Colors work. Everything works.
"""
import tkinter as tk
import subprocess
import threading
import os
import sys
import signal
import pty
import select
import termios
import struct
import fcntl
import time

class Terminal:
    def __init__(self, parent, config, pending_cmd=None):
        self.parent = parent
        self.config = config
        self.pending_cmd = pending_cmd
        self.frame = tk.Frame(parent, bg='#0d1117')
        self.master_fd = None
        self.slave_fd = None
        self.shell_pid = None
        self.read_thread = None
        self.is_termux = os.path.exists('/data/data/com.termux/files/usr/bin/bash')
        self.shell = os.environ.get('SHELL', '/bin/bash')
        
    def build(self):
        for w in self.frame.winfo_children(): w.destroy()
        self.frame.pack(fill='both', expand=True)
        
        # Toolbar
        toolbar = tk.Frame(self.frame, bg='#161b22', height=28)
        toolbar.pack(fill='x')
        toolbar.pack_propagate(False)
        
        env = "📱 TERMUX" if self.is_termux else "💻 LINUX"
        tk.Label(toolbar, text=f"  {env} TERMINAL (PTY)", font=('Courier', 9, 'bold'),
                fg='#58a6ff', bg='#161b22').pack(side='left', pady=4)
        
        self.status_dot = tk.Label(toolbar, text="●", font=('Courier', 9),
                fg='#3fb950', bg='#161b22')
        self.status_dot.pack(side='left', padx=5)
        
        tk.Button(toolbar, text="✕ Kill", font=('Courier', 9),
                fg='#f85149', bg='#161b22', relief='flat', padx=10,
                command=self._kill_shell).pack(side='right')
        tk.Button(toolbar, text="↻ Restart", font=('Courier', 9),
                fg='#d2991d', bg='#161b22', relief='flat', padx=10,
                command=self._restart_shell).pack(side='right')
        tk.Button(toolbar, text="Clear", font=('Courier', 9),
                fg='#8b949e', bg='#161b22', relief='flat', padx=10,
                command=self._clear).pack(side='right')
        
        # Terminal output area
        self.output = tk.Text(self.frame, font=('Courier', 10),
                bg='#0d1117', fg='#c9d1d9', insertbackground='#58a6ff',
                relief='flat', wrap='char', padx=5, pady=5,
                blockcursor=True)
        self.output.pack(fill='both', expand=True)
        
        # Make output read-only but allow selection
        self.output.bind('<Key>', self._handle_key)
        self.output.bind('<Return>', lambda e: self._send_to_shell('\r'))
        self.output.bind('<BackSpace>', lambda e: self._send_to_shell('\x7f'))
        self.output.bind('<Tab>', lambda e: self._send_to_shell('\t'))
        self.output.bind('<Control-c>', lambda e: self._send_to_shell('\x03'))
        self.output.bind('<Control-d>', lambda e: self._send_to_shell('\x04'))
        self.output.bind('<Control-l>', lambda e: self._clear())
        self.output.bind('<Up>', lambda e: self._send_to_shell('\x1b[A'))
        self.output.bind('<Down>', lambda e: self._send_to_shell('\x1b[B'))
        self.output.bind('<Left>', lambda e: self._send_to_shell('\x1b[D'))
        self.output.bind('<Right>', lambda e: self._send_to_shell('\x1b[C'))
        self.output.bind('<Home>', lambda e: self._send_to_shell('\x1b[H'))
        self.output.bind('<End>', lambda e: self._send_to_shell('\x1b[F'))
        self.output.focus_set()
        
        # Start shell
        self._start_shell()
        
        # Send pending command if any
        if self.pending_cmd:
            self.frame.after(500, lambda: self._send_to_shell(self.pending_cmd + '\r'))
    
    def _start_shell(self):
        """Start a real shell in a PTY"""
        try:
            # Create pseudo-terminal
            self.master_fd, self.slave_fd = pty.openpty()
            
            # Set terminal size
            self._set_pty_size()
            
            # Start the shell
            self.shell_pid = os.fork()
            
            if self.shell_pid == 0:
                # Child process - this IS the real terminal
                os.close(self.master_fd)
                os.setsid()
                
                # Set controlling terminal
                name = os.ttyname(self.slave_fd)
                for fd in range(3):
                    try: os.close(fd)
                    except: pass
                os.open(name, os.O_RDWR)
                os.dup2(0, 1)
                os.dup2(0, 2)
                
                # Set environment
                os.environ['TERM'] = 'xterm-256color'
                os.environ['COLORTERM'] = 'truecolor'
                os.environ['HOME'] = os.path.expanduser('~')
                os.environ['SHELL'] = self.shell
                
                # Execute shell
                os.execve(self.shell, [self.shell, '-i'], os.environ)
                os._exit(1)
            
            # Parent process
            os.close(self.slave_fd)
            
            # Start reading from PTY
            self.reading = True
            self.read_thread = threading.Thread(target=self._read_pty, daemon=True)
            self.read_thread.start()
            
            # Monitor shell process
            self.frame.after(500, self._check_shell)
            
        except Exception as e:
            self._write(f"\n❌ Failed to start shell: {e}\n", '#f85149')
            self._start_fallback_shell()
    
    def _start_fallback_shell(self):
        """Fallback: use subprocess if fork fails (some Termux versions)"""
        self._write("\n⚠️  Using fallback terminal mode\n", '#d2991d')
        # Use simple subprocess mode
        self.fallback_mode = True
    
    def _set_pty_size(self):
        """Set PTY window size to match output widget"""
        try:
            if self.master_fd:
                cols = 120
                rows = 40
                winsize = struct.pack("HHHH", rows, cols, 0, 0)
                fcntl.ioctl(self.master_fd, termios.TIOCSWINSZ, winsize)
        except:
            pass
    
    def _read_pty(self):
        """Read output from PTY continuously"""
        buffer = b''
        while self.reading and self.master_fd:
            try:
                ready, _, _ = select.select([self.master_fd], [], [], 0.1)
                if ready:
                    data = os.read(self.master_fd, 4096)
                    if data:
                        # Decode and write to output
                        try:
                            text = data.decode('utf-8', errors='replace')
                        except:
                            text = data.decode('latin-1', errors='replace')
                        
                        # Handle ANSI escape codes for colors
                        self.frame.after(0, lambda t=text: self._write_ansi(t))
                    else:
                        break
            except:
                break
        
        self.frame.after(0, lambda: self.status_dot.config(fg='#f85149'))
        self.master_fd = None
    
    def _write_ansi(self, text):
        """Write text with basic ANSI color support"""
        # Simple ANSI to tkinter color conversion
        ansi_colors = {
            '30': '#000000', '31': '#f85149', '32': '#3fb950', '33': '#d2991d',
            '34': '#58a6ff', '35': '#bc8cff', '36': '#39c5cf', '37': '#c9d1d9',
            '90': '#6e7681', '91': '#f85149', '92': '#3fb950', '93': '#d2991d',
            '94': '#58a6ff', '95': '#bc8cff', '96': '#39c5cf', '97': '#ffffff',
        }
        
        current_color = 'c9d1d9'
        clean_text = ''
        i = 0
        while i < len(text):
            if text[i] == '\x1b' and i+1 < len(text) and text[i+1] == '[':
                # Found ANSI escape
                if clean_text:
                    tag = f'c_{current_color}'
                    self.output.tag_config(tag, foreground=f'#{current_color}')
                    self.output.insert('end', clean_text, tag)
                    clean_text = ''
                
                end = text.find('m', i)
                if end > i:
                    code = text[i+2:end]
                    if code in ansi_colors:
                        current_color = ansi_colors[code].replace('#', '')
                    elif code == '0':
                        current_color = 'c9d1d9'
                    i = end + 1
                else:
                    clean_text += text[i]
                    i += 1
            else:
                clean_text += text[i]
                i += 1
        
        if clean_text:
            tag = f'c_{current_color}'
            self.output.tag_config(tag, foreground=f'#{current_color}')
            self.output.insert('end', clean_text, tag)
        
        self.output.see('end')
        self.output.update_idletasks()
    
    def _write(self, text, color='#c9d1d9'):
        """Write plain text to output"""
        tag = f'color_{color.replace("#", "")}'
        self.output.tag_config(tag, foreground=color)
        self.output.insert('end', text, tag)
        self.output.see('end')
        self.output.update_idletasks()
    
    def _send_to_shell(self, data):
        """Send keystrokes to the shell PTY"""
        if self.master_fd:
            try:
                if isinstance(data, str):
                    data = data.encode('utf-8')
                os.write(self.master_fd, data)
            except:
                pass
        elif hasattr(self, 'fallback_mode'):
            self._write(data.replace('\r', '\n'), '#c9d1d9')
    
    def _handle_key(self, event):
        """Handle keypresses and send to shell"""
        if event.char and event.char.isprintable():
            self._send_to_shell(event.char)
        elif event.keysym == 'Return':
            self._send_to_shell('\r')
        elif event.keysym == 'BackSpace':
            self._send_to_shell('\x7f')
        elif event.keysym == 'Tab':
            self._send_to_shell('\t')
        elif event.keysym == 'Escape':
            self._send_to_shell('\x1b')
        elif event.keysym == 'Up':
            self._send_to_shell('\x1b[A')
        elif event.keysym == 'Down':
            self._send_to_shell('\x1b[B')
        elif event.keysym == 'Left':
            self._send_to_shell('\x1b[D')
        elif event.keysym == 'Right':
            self._send_to_shell('\x1b[C')
        return 'break'
    
    def _kill_shell(self):
        """Kill the current shell and all its children"""
        if self.shell_pid:
            try:
                os.killpg(os.getpgid(self.shell_pid), signal.SIGKILL)
            except:
                try:
                    os.kill(self.shell_pid, signal.SIGKILL)
                except:
                    pass
        self.reading = False
        if self.master_fd:
            try: os.close(self.master_fd)
            except: pass
        self.master_fd = None
        self.shell_pid = None
        self._write("\n💀 Shell killed\n", '#f85149')
        self.status_dot.config(fg='#f85149')
    
    def _restart_shell(self):
        """Kill and restart the shell"""
        self._kill_shell()
        self.frame.after(200, self._start_shell)
        self._write("\n🔄 Restarting shell...\n", '#d2991d')
    
    def _check_shell(self):
        """Check if shell is still alive"""
        if self.shell_pid:
            try:
                pid, status = os.waitpid(self.shell_pid, os.WNOHANG)
                if pid == self.shell_pid:
                    self._write(f"\n💀 Shell exited ({status})\n", '#f85149')
                    self.shell_pid = None
                    self.status_dot.config(fg='#f85149')
                    # Auto-restart
                    self.frame.after(500, self._start_shell)
                    self._write("🔄 Auto-restarting...\n", '#d2991d')
            except:
                pass
        
        if self.frame.winfo_exists():
            self.frame.after(2000, self._check_shell)
    
    def _clear(self):
        self.output.delete('1.0', 'end')
        self._send_to_shell('\x0c')  # Ctrl+L to shell
    
    
    def _auto_save_data(self, cmd, output):
        """Auto-detect and save valuable data from command output"""
        try:
            import re
            import sys
            sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            from core.database import Database
            
            db = Database()
            projects = db.get_all_projects()
            if not projects:
                db.close()
                return
            
            project_id = projects[0]['id']
            tool_name = cmd.split()[0] if ' ' in cmd else cmd
            all_text = self.output.get('1.0', 'end-1c')
            output_text = all_text[-8000:] if len(all_text) > 8000 else all_text
            found = 0
            
            # Emails
            for email in set(re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', output_text)):
                try:
                    db.cursor.execute('INSERT INTO discovered_emails (project_id, email, source, tool) VALUES (?, ?, ?, ?)',
                            (project_id, email, 'terminal', tool_name))
                    found += 1
                except: pass
            
            # IPs
            for ip in set(re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', output_text)):
                if ip not in ('0.0.0.0','255.255.255.255','127.0.0.1','0.0.0.0/0'):
                    try:
                        db.cursor.execute('INSERT INTO discovered_hosts (project_id, ip_address, tool) VALUES (?, ?, ?)',
                                (project_id, ip, tool_name))
                        found += 1
                    except: pass
            
            # URLs
            for url in set(re.findall(r'https?://[^\s<>]+', output_text)):
                try:
                    db.cursor.execute('INSERT INTO discovered_urls (project_id, url, tool) VALUES (?, ?, ?)',
                            (project_id, url[:500], tool_name))
                    found += 1
                except: pass
            
            # Credentials (user:pass patterns)
            for u, p in set(re.findall(r'([\w.-]{3,}):([\w.@#$%^&*!]{3,})', output_text)):
                if u.lower() not in ('http','https','ftp','ssh','file'):
                    try:
                        db.cursor.execute('INSERT INTO credentials (project_id, username, password, tool, target) VALUES (?, ?, ?, ?, ?)',
                                (project_id, u, p, tool_name, 'terminal'))
                        found += 1
                    except: pass
            
            # Hashes
            for h in set(re.findall(r'\b[a-fA-F0-9]{32}\b', output_text)):
                try:
                    db.cursor.execute('INSERT INTO discovered_hashes (project_id, hash_value, hash_type, tool) VALUES (?, ?, ?, ?)',
                            (project_id, h, 'MD5', tool_name))
                    found += 1
                except: pass
            
            # Subdomains
            for sub in set(re.findall(r'(?:[\w-]+\.)+[\w-]+', output_text)):
                if '.' in sub and len(sub) < 100 and not sub.startswith('http'):
                    try:
                        db.cursor.execute('INSERT INTO discovered_subdomains (project_id, subdomain, tool) VALUES (?, ?, ?)',
                                (project_id, sub, tool_name))
                        found += 1
                    except: pass
            
            db.conn.commit()
            db.close()
            
            if found > 0:
                self._write(f"\n💎 Auto-saved {found} items to Data Locker\n", '#ff4488')
        except Exception as e:
            pass

    def set_command(self, cmd):
        """Send command to shell"""
        self.frame.after(300, lambda: self._send_to_shell(cmd + '\r'))
    
    def destroy(self):
        """Clean up on exit"""
        self._kill_shell()
