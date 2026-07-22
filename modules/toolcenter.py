from core.install_commands import get_install_methods_ranked, get_best_install_cmd, get_env_name, METHOD_ICONS, METHOD_COLORS
import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import threading
import os
import tempfile

class ToolCenter:
    def __init__(self, parent, detector, logger, navigate_callback=None):
        self.parent = parent
        self.detector = detector
        self.logger = logger
        self.navigate = navigate_callback
        self.frame = tk.Frame(parent, bg='#1a1a2e')
        self.pending_install = None
        
        try:
            from core.tool_args import ToolArgsDatabase
            self.args_db = ToolArgsDatabase()
        except:
            self.args_db = None
    
    def build(self):
        self.frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        header = tk.Frame(self.frame, bg='#1a1a2e')
        header.pack(fill='x', pady=(0,10))
        
        tk.Label(header, text="🔧 Tool Center", font=('Courier', 18, 'bold'),
                fg='#00ff88', bg='#1a1a2e').pack(side='left')
        
        installed = self.detector.get_total_count()
        missing = len(self.detector.get_missing_tools())
        tk.Label(header, text=f"✅ {installed} | ⬜ {missing}",
                font=('Courier', 9), fg='#aaa', bg='#1a1a2e').pack(side='right')
        
        self.notebook = ttk.Notebook(self.frame)
        self.notebook.pack(fill='both', expand=True)
        
        style = ttk.Style()
        style.theme_use('default')
        style.configure('TNotebook', background='#1a1a2e', borderwidth=0)
        style.configure('TNotebook.Tab', background='#16213e', foreground='#00ccff',
                padding=[12, 4], font=('Courier', 8))
        style.map('TNotebook.Tab', background=[('selected', '#0f3460')],
                foreground=[('selected', '#00ff88')])
        
        for category, tools in self.detector.detected.items():
            if tools:
                tab = tk.Frame(self.notebook, bg='#1a1a2e')
                self.notebook.add(tab, text=f"  {category.upper()} ({len(tools)})  ")
                self._build_tool_list(tab, tools)
        
        missing_tools = self.detector.get_missing_tools()
        if missing_tools:
            tab = tk.Frame(self.notebook, bg='#1a1a2e')
            self.notebook.add(tab, text=f"  ⬜ AVAILABLE ({len(missing_tools)})  ")
            self._build_missing_list(tab, missing_tools)
            
            # Install All button
            btn_frame = tk.Frame(tab, bg="#1a1a2e")
            btn_frame.pack(fill="x", pady=5)
            tk.Button(btn_frame, text="📥 Install All Missing Tools", font=("Courier", 9, "bold"),
                    fg="#000", bg="#ffaa00", relief="raised", padx=15, pady=5,
                    command=self._show_manual_install_all).pack()
    
    def _build_tool_list(self, parent, tools):
        canvas = tk.Canvas(parent, bg='#1a1a2e', highlightthickness=0)
        scrollbar = tk.Scrollbar(parent, orient='vertical', command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg='#1a1a2e')
        scroll_frame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.create_window((0,0), window=scroll_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        for tool in sorted(tools, key=lambda t: t['name']):
            card = tk.Frame(scroll_frame, bg='#16213e', relief='flat', bd=0)
            card.pack(fill='x', padx=5, pady=2)
            
            info = tk.Frame(card, bg='#16213e')
            info.pack(side='left', fill='x', expand=True, padx=10, pady=6)
            
            tk.Label(info, text=f"✅ {tool['name']}", font=('Courier', 10, 'bold'),
                    fg='#00ff88', bg='#16213e').pack(anchor='w')
            tk.Label(info, text=f"Cmd: {tool['command']}  |  {tool['path']}",
                    font=('Courier', 8), fg='#888', bg='#16213e').pack(anchor='w')
            
            actions = tk.Frame(card, bg='#16213e')
            actions.pack(side='right', padx=10, pady=6)
            
            tk.Button(actions, text="▶ Run", font=('Courier', 8),
                    fg='#000', bg='#00ff88', relief='flat', padx=8,
                    command=lambda t=tool: self._run_tool_dialog(t)).pack(pady=1)
            
            tk.Button(actions, text="💻 Terminal", font=('Courier', 8),
                    fg='#000', bg='#00ccff', relief='flat', padx=8,
                    command=lambda t=tool: self._open_in_terminal(t)).pack(pady=1)
    
    def _build_missing_list(self, parent, tools):
        canvas = tk.Canvas(parent, bg='#1a1a2e', highlightthickness=0)
        scrollbar = tk.Scrollbar(parent, orient='vertical', command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg='#1a1a2e')
        scroll_frame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.create_window((0,0), window=scroll_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        from collections import defaultdict
        by_cat = defaultdict(list)
        for t in tools:
            by_cat[t['category']].append(t['name'])
        
        for cat, names in sorted(by_cat.items()):
            frame = tk.LabelFrame(scroll_frame, text=f" {cat.upper()} ", font=('Courier', 9),
                    fg='#00ccff', bg='#16213e', padx=10, pady=5)
            frame.pack(fill='x', pady=3, padx=5)
            for name in sorted(names):
                row = tk.Frame(frame, bg='#16213e')
                row.pack(fill='x', pady=1)
                tk.Label(row, text=f"⬜ {name}", font=('Courier', 9),
                        fg='#888', bg='#16213e').pack(side='left')
                tk.Button(row, text="📦 pkg", font=('Courier', 7),
                        fg='#000', bg='#00ccff', relief='flat', padx=4,
                        command=lambda n=name: self._manual_install_dialog(n)).pack(side='right', padx=1)
                tk.Button(row, text="🐍 pip", font=('Courier', 7),
                        fg='#000', bg='#ffaa00', relief='flat', padx=4,
                        command=lambda n=name: self._manual_install_dialog(n)).pack(side='right', padx=1)
    
    def _install_pkg(self, name):
        self.pending_install = f"pkg install {name} -y"
        self._goto_terminal()
    
    def _install_pip(self, name):
        self.pending_install = f"pip install {name}"
        self._goto_terminal()
    
    def _goto_terminal(self):
        if self.navigate:
            self.navigate("terminal")
    
    def get_pending_install(self):
        cmd = self.pending_install
        self.pending_install = None
        return cmd
    
    def _open_in_terminal(self, tool):
        """Open tool in the embedded terminal with pre-filled command"""
        cmd = tool['command']
        self.pending_install = cmd
        if self.navigate:
            self.navigate("terminal")
    
    def _run_tool_dialog(self, tool):
        """Run tool with args in a dialog with real-time output"""
        dialog = tk.Toplevel(self.parent, bg='#1a1a2e')
        dialog.title(f"Run: {tool['name']}")
        dialog.geometry("750x500")
        
        # Title
        tk.Label(dialog, text=f"▶ {tool['name']}", font=('Courier', 14, 'bold'),
                fg='#00ff88', bg='#1a1a2e').pack(pady=8)
        tk.Label(dialog, text=f"Path: {tool['path']}", font=('Courier', 8),
                fg='#666', bg='#1a1a2e').pack()
        
        # Quick args
        if self.args_db:
            tool_args = self.args_db.get_args(tool["name"])
            grouped = self.args_db.get_args_grouped(tool["name"])
            if tool_args:
                qf = tk.LabelFrame(dialog, text=" Quick Args (click to add) ", font=('Courier', 9),
                        fg='#ffaa00', bg='#16213e', padx=8, pady=5)
                qf.pack(fill='x', padx=10, pady=5)
                
                row = tk.Frame(qf, bg='#16213e')
                row.pack(fill='x')
                col = 0
                for arg, desc in tool_args[:18]:
                    if col % 3 == 0 and col > 0:
                        row = tk.Frame(qf, bg='#16213e')
                        row.pack(fill='x')
                    
                    f = tk.Frame(row, bg='#16213e')
                    f.pack(side='left', fill='x', expand=True, padx=2, pady=1)
                    tk.Button(f, text=arg[:16], font=('Courier', 7),
                            fg='#000', bg='#00ccff', relief='flat', padx=2,
                            command=lambda a=arg: args_entry.insert('end', ' ' + a)
                            ).pack(fill='x')
                    tk.Label(f, text=desc[:15], font=('Courier', 6),
                            fg='#666', bg='#16213e').pack()
                    col += 1
        
        # Args input
        input_f = tk.Frame(dialog, bg='#16213e', padx=10, pady=8)
        input_f.pack(fill='x', padx=10, pady=5)
        tk.Label(input_f, text="Command:", font=('Courier', 10), fg='#fff', bg='#16213e').pack(anchor='w')
        
        entry_row = tk.Frame(input_f, bg='#16213e')
        entry_row.pack(fill='x')
        
        args_entry = tk.Entry(entry_row, font=('Courier', 12), bg='#0a0a0a',
                fg='#00ff88', insertbackground='#00ff88', relief='flat')
        args_entry.pack(side='left', fill='x', expand=True)
        args_entry.focus()
        
        stop_flag = [False]
        
        def execute():
            args = args_entry.get().strip()
            cmd = f"{tool['command']} {args}" if args else tool['command']
            output.insert('end', f"\n$ {cmd}\n{'─'*50}\n\n")
            output.see('end')
            stop_flag[0] = False
            
            def run():
                try:
                    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, text=True, bufsize=1)
                    for line in iter(p.stdout.readline, ''):
                        if stop_flag[0]:
                            p.kill()
                            break
                        output.insert('end', line)
                        output.see('end')
                    p.wait()
                    if stop_flag[0]:
                        output.insert('end', "\n🛑 Stopped\n")
                    else:
                        output.insert('end', f"\n✅ Exit: {p.returncode}\n")
                    output.see('end')
                except Exception as e:
                    output.insert('end', f"\n❌ {e}\n")
                    output.see('end')
            
            threading.Thread(target=run, daemon=True).start()
        
        tk.Button(entry_row, text="▶", font=('Courier', 14, 'bold'),
                fg='#000', bg='#00ff88', relief='flat', padx=12,
                command=execute).pack(side='right', padx=5)
        args_entry.bind('<Return>', lambda e: execute())
        
        # Output
        output = tk.Text(dialog, font=('Courier', 9), bg='#0a0a0a', fg='#00ff88',
                relief='flat', wrap='word')
        output.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Buttons
        bf = tk.Frame(dialog, bg='#1a1a2e')
        bf.pack(fill='x', padx=10, pady=8)
        tk.Button(bf, text="▶ Run", font=('Courier', 10, 'bold'),
                fg='#000', bg='#00ff88', relief='flat', padx=15, pady=6,
                command=execute).pack(side='left', padx=5)
        tk.Button(bf, text="🛑 Stop", font=('Courier', 10),
                fg='#fff', bg='#cc0000', relief='flat', padx=15, pady=6,
                command=lambda: stop_flag.__setitem__(0, True)).pack(side='left', padx=5)
        tk.Button(bf, text="💻 Open in Terminal", font=('Courier', 10),
                fg='#000', bg='#00ccff', relief='flat', padx=15, pady=6,
                command=lambda: [dialog.destroy(), self._open_in_terminal(tool)]).pack(side='left', padx=5)
        tk.Button(bf, text="Close", font=('Courier', 10),
                fg='#fff', bg='#666', relief='flat', padx=15, pady=6,
                command=dialog.destroy).pack(side='right', padx=5)

    def _manual_install_dialog(self, tool_name, method="auto"):
        """Manual installation dialog with step by step instructions"""
        dialog = tk.Toplevel(self.parent, bg='#1a1a2e')
        dialog.title(f"Manual Install: {tool_name}")
        dialog.geometry("600x500")
        
        tk.Label(dialog, text=f"📦 Manual Installation: {tool_name}", font=('Courier', 14, 'bold'),
                fg='#00ff88', bg='#1a1a2e').pack(pady=15)
        
        # Instructions based on tool type
        instructions = {
            "nmap": "pkg install nmap -y",
            "hydra": "pkg install hydra -y",
            "sqlmap": "pip install sqlmap",
            "nikto": "pkg install git -y\ngit clone https://github.com/sullo/nikto.git ~/nikto\necho 'alias nikto=~/nikto/program/nikto.pl' >> ~/.bashrc",
            "gobuster": "pkg install golang -y\ngo install github.com/OJ/gobuster/v3@latest\necho 'export PATH=\$PATH:~/go/bin' >> ~/.bashrc",
            "wpscan": "pkg install ruby -y\ngem install wpscan",
            "dirb": "pkg install dirb -y",
            "whatweb": "pkg install whatweb -y",
            "john": "pkg install john -y",
            "hashcat": "pkg install hashcat -y",
            "crunch": "pkg install crunch -y",
            "aircrack-ng": "pkg install aircrack-ng -y",
            "tcpdump": "pkg install tcpdump -y",
            "exiftool": "pkg install exiftool -y",
            "steghide": "pkg install steghide -y",
            "binwalk": "pkg install python -y && pip install binwalk",
            "foremost": "pkg install foremost -y",
            "strings": "pkg install binutils -y",
            "metasploit": "pkg install unstable-repo -y && pkg install metasploit -y",
            "ettercap": "pkg install ettercap -y",
            "netcat": "pkg install netcat-openbsd -y",
            "curl": "pkg install curl -y",
            "wget": "pkg install wget -y",
            "git": "pkg install git -y",
            "python": "pkg install python -y",
            "go": "pkg install golang -y",
            "ruby": "pkg install ruby -y",
            "perl": "pkg install perl -y",
            "php": "pkg install php -y",
            "node": "pkg install nodejs -y",
            "gcc": "pkg install clang -y",
            "make": "pkg install make -y",
            "subfinder": "pkg install golang -y && go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest",
            "httpx": "pkg install golang -y && go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest",
            "assetfinder": "pkg install golang -y && go install github.com/tomnomnom/assetfinder@latest",
            "gau": "pkg install golang -y && go install github.com/lc/gau/v2/cmd/gau@latest",
            "waybackurls": "pkg install golang -y && go install github.com/tomnomnom/waybackurls@latest",
            "ffuf": "pkg install golang -y && go install github.com/ffuf/ffuf/v2@latest",
            "amass": "pkg install amass -y",
            "massdns": "pkg install git make -y && git clone https://github.com/blechschmidt/massdns.git ~/massdns && cd ~/massdns && make",
            "sublist3r": "pkg install git python -y && git clone https://github.com/aboul3la/Sublist3r.git ~/Sublist3r && cd ~/Sublist3r && pip install -r requirements.txt",
            "dirsearch": "pkg install git python -y && git clone https://github.com/maurosoria/dirsearch.git ~/dirsearch",
            "commix": "pkg install git python -y && git clone https://github.com/commixproject/commix.git ~/commix",
            "xsser": "pkg install git python -y && git clone https://github.com/epsylon/xsser.git ~/xsser",
            "wfuzz": "pip install wfuzz",
            "fierce": "pip install fierce",
            "dnsenum": "pkg install git perl -y && git clone https://github.com/fwaeytens/dnsenum.git ~/dnsenum",
            "searchsploit": "pkg install exploitdb -y",
            "beef": "pkg install ruby -y && gem install beef-xss",
            "setoolkit": "pkg install git python -y && git clone https://github.com/trustedsec/social-engineer-toolkit.git ~/setoolkit",
            "cewl": "pkg install ruby -y && gem install cewl",
            "medusa": "pkg install medusa -y",
            "zsteg": "pkg install ruby -y && gem install zsteg",
            "bettercap": "pkg install bettercap -y",
            "rustscan": "pkg install rustscan -y",
            "masscan": "pkg install masscan -y",
            "arp-scan": "pkg install arp-scan -y",
            "tshark": "pkg install tshark -y",
            "reaver": "pkg install reaver -y",
            "pixiewps": "pkg install pixiewps -y",
        }
        
        # Get instructions or generate default
        cmd = get_install_cmd(tool_name, method) if "get_install_cmd" in dir() else instructions.get(tool_name, f"# No specific instructions for {tool_name}\n# Try these methods:\n\n# Method 1: pkg\npkg install {tool_name} -y\n\n# Method 2: pip\npip install {tool_name}\n\n# Method 3: search\npkg search {tool_name}")
        
        # Instruction text
        inst_frame = tk.LabelFrame(dialog, text=" Installation Commands ", font=('Courier', 10, 'bold'),
                fg='#00ccff', bg='#16213e', padx=10, pady=10)
        inst_frame.pack(fill='both', expand=True, padx=15, pady=10)
        
        inst_text = tk.Text(inst_frame, font=('Courier', 9), bg='#0a0a0a', fg='#00ff88',
                relief='flat', wrap='word', height=12)
        inst_text.pack(fill='both', expand=True)
        inst_text.insert('1.0', cmd)
        
        # Method selector
        method_frame = tk.LabelFrame(dialog, text=" Choose Install Method ", font=('Courier', 10, 'bold'),
                fg='#00ccff', bg='#16213e', padx=10, pady=10)
        method_frame.pack(fill='x', padx=15, pady=10)
        
        methods = [
            ("📦 Open in Terminal", lambda: self._open_terminal_with_cmd(cmd)),
            ("📋 Copy to Clipboard", lambda: self._copy_cmd(cmd)),
            ("💾 Save as Script", lambda: self._save_script(tool_name, cmd)),
            ("🔇 Background Install", lambda: self._background_install(tool_name, cmd)),
        ]
        
        for text, command in methods:
            tk.Button(method_frame, text=text, font=('Courier', 9),
                    fg='#000', bg='#00ccff', relief='raised', padx=10, pady=5,
                    command=command).pack(side='left', padx=3, pady=5)
        
        # Manual steps
        steps_frame = tk.LabelFrame(dialog, text=" Manual Steps ", font=('Courier', 10, 'bold'),
                fg='#ffaa00', bg='#16213e', padx=10, pady=10)
        steps_frame.pack(fill='x', padx=15, pady=10)
        
        steps = [
            "1. Copy the command above",
            "2. Open Termux app",
            "3. Paste and run the command",
            "4. Wait for installation to complete",
            "5. Return to CyberLab and click Refresh",
            "6. Tool will appear in Tool Center"
        ]
        
        for step in steps:
            tk.Label(steps_frame, text=step, font=('Courier', 9),
                    fg='#aaa', bg='#16213e').pack(anchor='w')
        
        tk.Button(dialog, text="Close", font=('Courier', 10),
                fg='#fff', bg='#666', relief='raised', padx=20, pady=5,
                command=dialog.destroy).pack(pady=10)
    
    def _open_terminal_with_cmd(self, cmd):
        """Open embedded terminal with command"""
        self.pending_install = cmd
        if self.navigate:
            self.navigate("terminal")
    
    def _copy_cmd(self, cmd):
        """Copy command to clipboard"""
        try:
            self.frame.clipboard_clear()
            self.frame.clipboard_append(cmd)
            messagebox.showinfo("Copied", "Command copied to clipboard!\nPaste in Termux.")
        except:
            messagebox.showinfo("Command", f"Copy this:\n\n{cmd}")
    
    def _save_script(self, cmd, tool_name):
        """Save install command as shell script"""
        script_dir = os.path.join(os.path.dirname(__file__), '..', 'scripts')
        os.makedirs(script_dir, exist_ok=True)
        script_path = os.path.join(script_dir, f'install_{tool_name}.sh')
        
        with open(script_path, 'w') as f:
            f.write(f'#!/bin/bash\n# Install {tool_name}\n{cmd}\n')
        os.chmod(script_path, 0o755)
        
        messagebox.showinfo("Script Saved", f"Install script saved to:\n{script_path}\n\nRun with:\nbash {script_path}")
    
    def _background_install(self, cmd, tool_name):
        """Run installation in background"""
        if messagebox.askyesno("Background Install", 
                f"Install {tool_name} in background?\n\nThis will run silently.\nCheck logs for progress."):
            self.logger.log_tool_execution(tool_name, cmd, "background_install_started")
            
            def run():
                import subprocess
                try:
                    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=300)
                    if result.returncode == 0:
                        self.logger.log_tool_execution(tool_name, cmd, "installed")
                    else:
                        self.logger.log_tool_execution(tool_name, cmd, f"failed: {result.returncode}")
                except Exception as e:
                    self.logger.log_error(f"install_{tool_name}", e)
            
            import threading
            threading.Thread(target=run, daemon=True).start()
            messagebox.showinfo("Installing", f"Installing {tool_name} in background...\nCheck logs at: logs/tools.log")
    
    def _show_manual_install_all(self):
        """Show dialog to install all missing tools at once"""
        missing = self.detector.get_missing_tools()
        if not missing:
            messagebox.showinfo("All Installed", "All tools are already installed!")
            return
        
        dialog = tk.Toplevel(self.parent, bg='#1a1a2e')
        dialog.title("Install All Missing Tools")
        dialog.geometry("500x400")
        
        tk.Label(dialog, text="📦 Install All Missing Tools", font=('Courier', 14, 'bold'),
                fg='#00ff88', bg='#1a1a2e').pack(pady=15)
        
        tk.Label(dialog, text=f"Found {len(missing)} tools not installed:", font=('Courier', 10),
                fg='#fff', bg='#1a1a2e').pack()
        
        # List missing tools
        list_frame = tk.Frame(dialog, bg='#16213e')
        list_frame.pack(fill='both', expand=True, padx=15, pady=10)
        
        canvas = tk.Canvas(list_frame, bg='#16213e', highlightthickness=0)
        scrollbar = tk.Scrollbar(list_frame, orient='vertical', command=canvas.yview)
        sf = tk.Frame(canvas, bg='#16213e')
        sf.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.create_window((0,0), window=sf, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        for tool in missing:
            tk.Label(sf, text=f"⬜ {tool['name']} ({tool['category']})", font=('Courier', 9),
                    fg='#888', bg='#16213e').pack(anchor='w', pady=1)
        
        # Generate combined install script
        def generate_all_script():
            script = "#!/bin/bash\necho 'Installing all missing tools...'\n"
            for tool in missing:
                name = tool['name']
                cmd = self.INSTALL_COMMANDS.get(name, f"pkg install {name} -y || pip install {name}")
                if isinstance(cmd, dict):
                    cmd = list(cmd.values())[0]
                script += f"\necho '=== Installing {name} ==='\n{cmd}\n"
            
            script_dir = os.path.join(os.path.dirname(__file__), '..', 'scripts')
            os.makedirs(script_dir, exist_ok=True)
            script_path = os.path.join(script_dir, 'install_all_tools.sh')
            with open(script_path, 'w') as f:
                f.write(script)
            os.chmod(script_path, 0o755)
            
            messagebox.showinfo("Script Saved", 
                    f"Install script saved!\n\n{script_path}\n\nRun: bash {script_path}")
            dialog.destroy()
        
        tk.Button(dialog, text="📥 Generate Install All Script", font=('Courier', 10, 'bold'),
                fg='#000', bg='#00ff88', relief='raised', padx=15, pady=8,
                command=generate_all_script).pack(pady=10)
        
        tk.Button(dialog, text="Close", font=('Courier', 10),
                fg='#fff', bg='#666', relief='raised', padx=15, pady=5,
                command=dialog.destroy).pack(pady=5)

    def _build_missing_list(self, parent, tools):
        canvas = tk.Canvas(parent, bg='#1a1a2e', highlightthickness=0)
        scrollbar = tk.Scrollbar(parent, orient='vertical', command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg='#1a1a2e')
        scroll_frame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.create_window((0,0), window=scroll_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Show environment
        env_name = get_env_name() if 'get_env_name' in dir() else "Termux"
        tk.Label(scroll_frame, text=f"🖥️  Environment: {env_name}",
                font=('Courier', 9, 'bold'), fg='#00ccff', bg='#1a1a2e').pack(anchor='w', pady=5)
        
        tk.Label(scroll_frame, text="Click any button to see install instructions",
                font=('Courier', 8), fg='#888', bg='#1a1a2e').pack(anchor='w', pady=3)
        
        from collections import defaultdict
        by_cat = defaultdict(list)
        for t in tools:
            by_cat[t['category']].append(t['name'])
        
        for cat, names in sorted(by_cat.items()):
            frame = tk.LabelFrame(scroll_frame, text=f" {cat.upper()} ", font=('Courier', 9),
                    fg='#00ccff', bg='#16213e', padx=10, pady=5)
            frame.pack(fill='x', pady=3, padx=5)
            
            for name in sorted(names):
                row = tk.Frame(frame, bg='#16213e')
                row.pack(fill='x', pady=1)
                tk.Label(row, text=f"⬜ {name}", font=('Courier', 9),
                        fg='#888', bg='#16213e').pack(side='left')
                
                # Get available methods for this tool in current environment
                try:
                    methods = get_available_methods(name)
                except:
                    methods = ['pkg', 'pip', 'git']
                
                # Method icons and colors
                method_styles = {
                    'pkg': ('📦 pkg', '#00ccff'),
                    'apt': ('📦 apt', '#00ccff'),
                    'pacman': ('📦 pac', '#00ccff'),
                    'dnf': ('📦 dnf', '#00ccff'),
                    'pip': ('🐍 pip', '#ffaa00'),
                    'git': ('📥 git', '#cc88ff'),
                    'go': ('🔵 go', '#00ff88'),
                    'gem': ('💎 gem', '#ff4488'),
                    'auto': ('🔧 auto', '#888888'),
                }
                
                for method in methods[:4]:  # Show max 4 buttons
                    style = method_styles.get(method, ('📥 ' + method, '#888'))
                    tk.Button(row, text=style[0], font=('Courier', 7),
                            fg='#000', bg=style[1], relief='flat', padx=4,
                            command=lambda n=name, m=method: self._manual_install_dialog(n, m)
                            ).pack(side='right', padx=1)
