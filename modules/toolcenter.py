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
                        command=lambda n=name: self._install_pkg(n)).pack(side='right', padx=1)
                tk.Button(row, text="🐍 pip", font=('Courier', 7),
                        fg='#000', bg='#ffaa00', relief='flat', padx=4,
                        command=lambda n=name: self._install_pip(n)).pack(side='right', padx=1)
    
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
            tool_args = self.args_db.get_args(tool['name'])
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
