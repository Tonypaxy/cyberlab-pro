import tkinter as tk
from tkinter import ttk, messagebox
import subprocess, threading, os, shutil

class ToolCenter:
    def __init__(self, parent, detector, logger, navigate_callback=None):
        self.parent = parent
        self.detector = detector
        self.logger = logger
        self.navigate = navigate_callback
        self.frame = tk.Frame(parent, bg='#1a1a2e')
        self.pending_install = None
        self.expanded = {}
        self.content_frames = {}
        try:
            from core.tool_args import ToolArgsDatabase
            self.args_db = ToolArgsDatabase()
        except:
            self.args_db = None

    def build(self):
        for w in self.frame.winfo_children(): w.destroy()
        self.frame.pack(fill='both', expand=True)

        # Header with marquee
        h = tk.Frame(self.frame, bg='#1a1a2e'); h.pack(fill='x', padx=10, pady=(10,5))
        tk.Label(h, text="Tool Center", font=('Courier',18,'bold'), fg='#00ff88', bg='#1a1a2e').pack(side='left')

        installed = self.detector.get_total_count()
        missing = len(self.detector.get_missing_tools())
        tk.Label(h, text=f"{installed} installed | {missing} available", font=('Courier',9), fg='#888', bg='#1a1a2e').pack(side='right')
        tk.Button(h, text="Refresh", font=('Courier',8), fg='#000', bg='#ffaa00', relief='flat', padx=10,
                command=self._refresh_tools).pack(side='right', padx=5)

        # Marquee banner showing available examples count
        if self.args_db:
            total_examples = sum(len(v) for v in self.args_db.cache.values())
            marquee = tk.Frame(self.frame, bg='#0f3460', height=22)
            marquee.pack(fill='x', padx=10, pady=2)
            marquee.pack_propagate(False)
            self.marquee_text = tk.StringVar(value=f"  {total_examples}+ pre-built examples available | {len(self.args_db.cache)} tools covered | Click any tool to see examples  ")
            marquee_label = tk.Label(marquee, textvariable=self.marquee_text, font=('Courier',8),
                    fg='#ffaa00', bg='#0f3460', anchor='w')
            marquee_label.pack(fill='x', padx=5, pady=2)
            self._animate_marquee(marquee_label)

        from gui.scrollable import make_scrollable
        canvas, inner, v_bar, h_bar = make_scrollable(self.frame, '#1a1a2e')

        cat_icons = {'recon':'Recon','web':'Web','network':'Network','credentials':'Creds',
                'wireless':'Wireless','forensics':'Forensics','programming':'Dev',
                'exploitation':'Exploit','phishing_social':'Phish','osint':'OSINT',
                'social_engineering':'SocEng','reverse_engineering':'RevEng',
                'advanced_c2':'C2','evasion_bypass':'Evasion','red_team_infra':'RedTeam',
                'initial_access':'Access','privilege_escalation':'PrivEsc',
                'lateral_movement':'Lateral','exfiltration':'Exfil','persistence':'Persist',
                'defense_evasion':'DefEvade','credential_access':'Creds','cloud_attacks':'Cloud',
                'social_brute':'SocBrute','phishing_toolkits':'PhishKit'}

        for category, tools in self.detector.detected.items():
            if not tools: continue
            self._category_section(inner, category, tools, cat_icons.get(category, category[:10]), True)

        missing_tools = self.detector.get_missing_tools()
        if missing_tools:
            self._category_section(inner, 'available', missing_tools, 'Available', False)

    def _animate_marquee(self, label):
        text = self.marquee_text.get()
        self.marquee_text.set(text[1:] + text[0])
        self.frame.after(300, lambda: self._animate_marquee(label))

    def _category_section(self, parent, category, tools, icon, installed):
        count = len(tools)
        is_expanded = self.expanded.get(category, False)
        header = tk.Frame(parent, bg='#16213e', cursor='hand2')
        header.pack(fill='x', padx=5, pady=2)
        arrow = 'v' if is_expanded else '>'
        color = '#00ff88' if installed else '#ffaa00'
        tk.Button(header, text=f"{arrow} {icon} ({count})", font=('Courier',10,'bold'),
                fg=color, bg='#16213e', relief='flat', anchor='w', padx=10, pady=6,
                command=lambda: self._toggle_category(category, parent, tools, icon, installed)).pack(fill='x')
        content_frame = tk.Frame(parent, bg='#1a1a2e')
        if is_expanded:
            content_frame.pack(fill='x', padx=15, pady=(0,5))
            if installed: self._build_tool_list(content_frame, tools)
            else: self._build_missing_list(content_frame, tools)
        self.content_frames[category] = content_frame

    def _toggle_category(self, category, parent, tools, icon, installed):
        self.expanded[category] = not self.expanded.get(category, False)
        for w in self.frame.winfo_children(): w.destroy()
        self.build()

    def _build_tool_list(self, parent, tools):
        for tool in sorted(tools, key=lambda t: t['name']):
            row = tk.Frame(parent, bg='#1a1a2e'); row.pack(fill='x', pady=1)
            
            # Tool name with example count badge
            example_count = len(self.args_db.get_args(tool['name'])) if self.args_db else 0
            name_text = f"  {tool['name']}"
            if example_count > 1:
                name_text += f"  [{example_count} examples]"
            
            tk.Button(row, text=name_text, font=('Courier',9), fg='#00ff88', bg='#16213e',
                    relief='flat', anchor='w', padx=10, pady=4,
                    command=lambda t=tool: self._show_tool_detail(t)).pack(side='left', fill='x', expand=True)
            tk.Button(row, text="Run", font=('Courier',8), fg='#000', bg='#00ff88', relief='flat', padx=8,
                    command=lambda t=tool: self._run_tool_dialog(t)).pack(side='right', padx=1)
            tk.Button(row, text="Term", font=('Courier',8), fg='#000', bg='#00ccff', relief='flat', padx=8,
                    command=lambda t=tool: self._open_in_terminal(t)).pack(side='right', padx=1)

    def _build_missing_list(self, parent, tools):
        from collections import defaultdict
        try:
            from core.install_commands import get_install_methods_ranked, METHOD_ICONS, METHOD_COLORS, get_env_name
            env = get_env_name()
        except:
            env = "Termux"
        tk.Label(parent, text=f"Environment: {env} | Click to install", font=('Courier',8), fg='#ffaa00', bg='#1a1a2e').pack(anchor='w')
        for name in sorted([t['name'] for t in tools]):
            row = tk.Frame(parent, bg='#1a1a2e'); row.pack(fill='x', pady=1)
            tk.Label(row, text=f"  {name}", font=('Courier',9), fg='#888', bg='#1a1a2e', width=20, anchor='w').pack(side='left', padx=5)
            try:
                methods = get_install_methods_ranked(name)
                for method, cmd in list(methods.items())[:3]:
                    icon = METHOD_ICONS.get(method, method) if 'METHOD_ICONS' in dir() else method
                    color = METHOD_COLORS.get(method, '#888') if 'METHOD_COLORS' in dir() else '#888'
                    tk.Button(row, text=icon, font=('Courier',7), fg='#000', bg=color, relief='flat', padx=4,
                            command=lambda n=name, m=method, c=cmd: self._direct_install(n, m, c)).pack(side='right', padx=1)
            except:
                tk.Button(row, text='pkg', font=('Courier',7), fg='#000', bg='#00ccff', relief='flat', padx=4,
                        command=lambda n=name: self._direct_install(n, 'pkg', f'pkg install {n} -y')).pack(side='right', padx=1)
                tk.Button(row, text='pip', font=('Courier',7), fg='#000', bg='#ffaa00', relief='flat', padx=4,
                        command=lambda n=name: self._direct_install(n, 'pip', f'pip install {n}')).pack(side='right', padx=1)

    def _refresh_tools(self):
        self.detector.detect_all()
        for w in self.frame.winfo_children(): w.destroy()
        self.build()

    def _direct_install(self, tool_name, method, cmd):
        self.pending_install = cmd
        if self.navigate: self.navigate("terminal")

    def _open_in_terminal(self, tool):
        self.pending_install = tool['command']
        if self.navigate: self.navigate("terminal")

    def get_pending_install(self):
        cmd = self.pending_install; self.pending_install = None; return cmd

    def _show_tool_detail(self, tool):
        d = tk.Toplevel(self.parent, bg='#1a1a2e'); d.title(tool['name']); d.geometry("550x450")
        
        # Marquee header
        mf = tk.Frame(d, bg='#0f3460', height=20); mf.pack(fill='x'); mf.pack_propagate(False)
        examples = self.args_db.get_args(tool['name']) if self.args_db else []
        ex_text = f"  {tool['name']} - {len(examples)} pre-built examples available  "
        ex_var = tk.StringVar(value=ex_text)
        ex_label = tk.Label(mf, textvariable=ex_var, font=('Courier',8), fg='#ffaa00', bg='#0f3460', anchor='w')
        ex_label.pack(fill='x', padx=5, pady=1)
        def animate():
            t = ex_var.get(); ex_var.set(t[1:] + t[0])
            d.after(300, animate)
        animate()
        
        tk.Label(d, text=f"  {tool['name']}", font=('Courier',14,'bold'), fg='#00ff88', bg='#1a1a2e').pack(pady=8)
        tk.Label(d, text=f"Command: {tool['command']}  |  Path: {tool['path']}", font=('Courier',8), fg='#888', bg='#1a1a2e').pack()

        if examples:
            tk.Label(d, text=f"Pre-Built Examples ({len(examples)}):", font=('Courier',10,'bold'), fg='#ffaa00', bg='#1a1a2e').pack(anchor='w', padx=10, pady=(10,5))
            
            # Scrollable examples area
            ec = tk.Canvas(d, bg='#1a1a2e', highlightthickness=0, height=200)
            evs = tk.Scrollbar(d, orient='vertical', command=ec.yview)
            einf = tk.Frame(ec, bg='#1a1a2e')
            einf.bind('<Configure>', lambda e: ec.configure(scrollregion=ec.bbox('all')))
            ec.create_window((0,0), window=einf, anchor='nw', width=500)
            ec.configure(yscrollcommand=evs.set)
            ec.pack(side='left', fill='both', expand=True, padx=10, pady=5)
            evs.pack(side='right', fill='y')
            
            for arg, desc in examples[:30]:
                card = tk.Frame(einf, bg='#16213e', padx=8, pady=4); card.pack(fill='x', pady=1)
                h = tk.Frame(card, bg='#16213e'); h.pack(fill='x')
                tk.Button(h, text="Use", font=('Courier',8,'bold'), fg='#000', bg='#00ff88', relief='raised', padx=8, pady=2,
                        command=lambda a=arg: [d.destroy(), self._run_with_arg(tool, a)]).pack(side='left', padx=5)
                tk.Label(h, text=arg[:60], font=('Courier',9), fg='#00ccff', bg='#16213e').pack(side='left', padx=5)
                tk.Label(card, text=desc[:70], font=('Courier',8), fg='#888', bg='#16213e', wraplength=400).pack(anchor='w', padx=15)
        else:
            tk.Label(d, text="No pre-built examples", font=('Courier',9), fg='#888', bg='#1a1a2e').pack(pady=10)

        bf = tk.Frame(d, bg='#1a1a2e'); bf.pack(pady=8)
        tk.Button(bf, text="Run Tool", font=('Courier',10,'bold'), fg='#000', bg='#00ff88', relief='raised', padx=15, pady=6,
                command=lambda: [d.destroy(), self._run_tool_dialog(tool)]).pack(side='left', padx=3)
        tk.Button(bf, text="Terminal", font=('Courier',10), fg='#000', bg='#00ccff', relief='raised', padx=15, pady=6,
                command=lambda: [d.destroy(), self._open_in_terminal(tool)]).pack(side='left', padx=3)
        tk.Button(bf, text="Close", font=('Courier',10), fg='#fff', bg='#666', relief='raised', padx=15, pady=6, command=d.destroy).pack(side='left', padx=3)

    def _run_with_arg(self, tool, arg):
        d = tk.Toplevel(self.parent, bg='#1a1a2e'); d.title(f"Run: {tool['name']}"); d.geometry("700x450")
        tk.Label(d, text=f"  {tool['name']}", font=('Courier',14,'bold'), fg='#00ff88', bg='#1a1a2e').pack(pady=8)
        f = tk.Frame(d, bg='#16213e', padx=10, pady=8); f.pack(fill='x', padx=10, pady=5)
        tk.Label(f, text="Command:", font=('Courier',10), fg='#fff', bg='#16213e').pack(anchor='w')
        args_entry = tk.Entry(f, font=('Courier',11), bg='#0a0a0a', fg='#00ff88', relief='flat')
        args_entry.pack(fill='x', pady=3); args_entry.insert(0, arg)
        
        output = tk.Text(d, font=('Courier',9), bg='#0a0a0a', fg='#00ff88', relief='flat')
        output.pack(fill='both', expand=True, padx=10, pady=5)
        
        def execute():
            a = args_entry.get().strip(); cmd = f"{tool['command']} {a}"
            output.insert('end', f"\n$ {cmd}\n{'='*40}\n\n"); output.see('end')
            def run():
                try:
                    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
                    for line in iter(p.stdout.readline,''): output.insert('end', line); output.see('end')
                    p.wait(); output.insert('end', f"\n[Exit: {p.returncode}]\n")
                except Exception as e: output.insert('end', f"\n[X] {e}\n")
            threading.Thread(target=run, daemon=True).start()
        
        bf2 = tk.Frame(d, bg='#1a1a2e'); bf2.pack(fill='x', padx=10, pady=8)
        tk.Button(bf2, text="Execute", font=('Courier',10,'bold'), fg='#000', bg='#00ff88', relief='raised', padx=15, pady=6, command=execute).pack(side='left', padx=3)
        tk.Button(bf2, text="Close", font=('Courier',10), fg='#fff', bg='#666', relief='raised', padx=15, pady=6, command=d.destroy).pack(side='right', padx=3)
        args_entry.bind('<Return>', lambda e: execute()); args_entry.focus()

    def _run_tool_dialog(self, tool):
        self._run_with_arg(tool, "")
