"""
CyberLab Pro - Tool Center with Vertical Dropdown Layout
All tools organized in collapsible categories. Click to expand.
"""
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
        self.expanded = {}  # Track which categories are expanded
        self.stop_flags = {}
        
        try:
            from core.tool_args import ToolArgsDatabase
            self.args_db = ToolArgsDatabase()
        except:
            self.args_db = None
    
    def build(self):
        for w in self.frame.winfo_children(): w.destroy()
        self.frame.pack(fill='both', expand=True)
        
        # Header
        h = tk.Frame(self.frame, bg='#1a1a2e')
        h.pack(fill='x', padx=10, pady=(10,5))
        tk.Label(h, text="Tool Center", font=('Courier', 18, 'bold'),
                fg='#00ff88', bg='#1a1a2e').pack(side='left')
        
        installed = self.detector.get_total_count()
        missing = len(self.detector.get_missing_tools())
        tk.Label(h, text=f"{installed} installed | {missing} available",
                font=('Courier', 9), fg='#888', bg='#1a1a2e').pack(side='right')
        
        # Scrollable area for categories
        from gui.scrollable import make_scrollable
        canvas, inner, v_bar, h_bar = make_scrollable(self.frame, '#1a1a2e')
        
        # Category icons
        cat_icons = {
            'recon': '🎯', 'web': '🌍', 'network': '🌐', 'credentials': '🔑',
            'wireless': '📡', 'forensics': '🔍', 'programming': '💻', 'exploitation': '💣',
            'hash_crypto': '#️⃣', 'stegano': '🖼️', 'dos': '💥', 'secure_delete': '🗑️',
            'malware_analysis': '🦠', 'phishing_social': '🎣', 'osint': '🔎',
            'wifi_bluetooth': '📶', 'web_exploit': '🕸️', 'android_hacking': '📱', 'voip': '📞'
        }
        
        # Build installed tools by category
        for category, tools in self.detector.detected.items():
            if not tools: continue
            self._category_section(inner, category, tools, cat_icons.get(category, '📦'), True)
        
        # Missing tools section
        missing_tools = self.detector.get_missing_tools()
        if missing_tools:
            self._category_section(inner, 'available', missing_tools, '⬜', False)
    
    def _category_section(self, parent, category, tools, icon, installed):
        """Create a collapsible category section"""
        count = len(tools)
        is_expanded = self.expanded.get(category, False)
        
        # Category header (clickable)
        header = tk.Frame(parent, bg='#16213e', cursor='hand2')
        header.pack(fill='x', padx=5, pady=2)
        
        arrow = '▼' if is_expanded else '▶'
        color = '#00ff88' if installed else '#ffaa00'
        
        toggle_btn = tk.Button(header, text=f"{arrow} {icon} {category.upper()} ({count})",
                font=('Courier', 10, 'bold'), fg=color, bg='#16213e',
                relief='flat', anchor='w', padx=10, pady=6,
                command=lambda: self._toggle_category(category, parent, tools, icon, installed))
        toggle_btn.pack(fill='x')
        
        # Content frame (hidden by default)
        content_frame = tk.Frame(parent, bg='#1a1a2e')
        
        if is_expanded:
            content_frame.pack(fill='x', padx=15, pady=(0,5))
            if installed:
                self._build_tool_list(content_frame, tools)
            else:
                self._build_missing_list(content_frame, tools)
        
        # Store reference
        if not hasattr(self, '_content_frames'):
            self._content_frames = {}
        self._content_frames[category] = content_frame
    
    def _toggle_category(self, category, parent, tools, icon, installed):
        """Toggle category expand/collapse"""
        self.expanded[category] = not self.expanded.get(category, False)
        # Rebuild
        for w in self.frame.winfo_children():
            w.destroy()
        self.build()
    
    def _build_tool_list(self, parent, tools):
        """Build vertical tool list with expandable details"""
        for tool in sorted(tools, key=lambda t: t['name']):
            self._tool_row(parent, tool)
    
    def _tool_row(self, parent, tool):
        """Single tool row - click to show details"""
        row = tk.Frame(parent, bg='#1a1a2e')
        row.pack(fill='x', pady=1)
        
        # Tool name (clickable)
        name_btn = tk.Button(row, text=f"✅ {tool['name']}", font=('Courier', 9),
                fg='#00ff88', bg='#16213e', relief='flat', anchor='w', padx=10, pady=4,
                command=lambda: self._show_tool_detail(tool))
        name_btn.pack(side='left', fill='x', expand=True)
        
        # Quick action buttons
        tk.Button(row, text="Run", font=('Courier', 8), fg='#000', bg='#00ff88',
                relief='flat', padx=8, command=lambda: self._run_tool_dialog(tool)).pack(side='right', padx=1)
        tk.Button(row, text="Term", font=('Courier', 8), fg='#000', bg='#00ccff',
                relief='flat', padx=8, command=lambda: self._open_in_terminal(tool)).pack(side='right', padx=1)
    
    def _show_tool_detail(self, tool):
        """Show tool details in a popup"""
        d = tk.Toplevel(self.parent, bg='#1a1a2e')
        d.title(tool['name']); d.geometry("500x400")
        
        tk.Label(d, text=f"✅ {tool['name']}", font=('Courier', 14, 'bold'),
                fg='#00ff88', bg='#1a1a2e').pack(pady=10)
        tk.Label(d, text=f"Command: {tool['command']}\nPath: {tool['path']}\nVersion: {tool.get('version','?')}",
                font=('Courier', 9), fg='#aaa', bg='#1a1a2e').pack(pady=5)
        
        # Arguments
        if self.args_db:
            args = self.args_db.get_args(tool['name'])
            if args:
                tk.Label(d, text="Quick Arguments:", font=('Courier', 10, 'bold'),
                        fg='#ffaa00', bg='#1a1a2e').pack(pady=(10,5))
                arg_frame = tk.Frame(d, bg='#1a1a2e')
                arg_frame.pack(fill='x', padx=10)
                for arg, desc in args[:12]:
                    f = tk.Frame(arg_frame, bg='#16213e')
                    f.pack(fill='x', pady=1)
                    tk.Label(f, text=f"{arg[:20]}", font=('Courier', 9),
                            fg='#00ccff', bg='#16213e', width=22, anchor='w').pack(side='left', padx=5)
                    tk.Label(f, text=desc[:40], font=('Courier', 8),
                            fg='#888', bg='#16213e', anchor='w').pack(side='left', padx=5)
        
        btn_f = tk.Frame(d, bg='#1a1a2e')
        btn_f.pack(pady=10)
        tk.Button(btn_f, text="Run Tool", font=('Courier', 10, 'bold'),
                fg='#000', bg='#00ff88', relief='raised', padx=15, pady=6,
                command=lambda: [d.destroy(), self._run_tool_dialog(tool)]).pack(side='left', padx=3)
        tk.Button(btn_f, text="Open in Terminal", font=('Courier', 10),
                fg='#000', bg='#00ccff', relief='raised', padx=15, pady=6,
                command=lambda: [d.destroy(), self._open_in_terminal(tool)]).pack(side='left', padx=3)
        tk.Button(btn_f, text="Close", font=('Courier', 10),
                fg='#fff', bg='#666', relief='raised', padx=15, pady=6,
                command=d.destroy).pack(side='left', padx=3)
    
    def _build_missing_list(self, parent, tools):
        """Build missing tools list with install buttons"""
        from collections import defaultdict
        by_cat = defaultdict(list)
        for t in tools:
            by_cat[t['category']].append(t['name'])
        
        try:
            from core.install_commands import get_install_methods_ranked, METHOD_ICONS, METHOD_COLORS
        except:
            METHOD_ICONS = {'pkg':'pkg','pip':'pip','git':'git'}
            METHOD_COLORS = {'pkg':'#00ccff','pip':'#ffaa00','git':'#cc88ff'}
        
        for name in sorted([t['name'] for t in tools]):
            row = tk.Frame(parent, bg='#1a1a2e')
            row.pack(fill='x', pady=1)
            tk.Label(row, text=f"⬜ {name}", font=('Courier', 9),
                    fg='#888', bg='#1a1a2e').pack(side='left', padx=5)
            
            # Install buttons
            try:
                methods = get_install_methods_ranked(name)
                for method, cmd in list(methods.items())[:3]:
                    icon = METHOD_ICONS.get(method, method)
                    color = METHOD_COLORS.get(method, '#888')
                    tk.Button(row, text=icon, font=('Courier', 7),
                            fg='#000', bg=color, relief='flat', padx=4,
                            command=lambda n=name, m=method, c=cmd: self._direct_install(n, m, c)
                            ).pack(side='right', padx=1)
            except:
                tk.Button(row, text="pkg", font=('Courier', 7),
                        fg='#000', bg='#00ccff', relief='flat', padx=4,
                        command=lambda n=name: self._direct_install(n, 'pkg', f'pkg install {n} -y')
                        ).pack(side='right', padx=1)
    
    def _direct_install(self, tool_name, method, cmd):
        """Direct install - goes to terminal"""
        self.pending_install = cmd
        self.logger.log_tool_execution(tool_name, cmd, f"install_{method}")
        if self.navigate:
            self.navigate("terminal")
    
    def _open_in_terminal(self, tool):
        self.pending_install = tool['command']
        if self.navigate:
            self.navigate("terminal")
    
    def get_pending_install(self):
        cmd = self.pending_install; self.pending_install = None; return cmd
    
    def _run_tool_dialog(self, tool):
        """Run tool with args"""
        d = tk.Toplevel(self.parent, bg='#1a1a2e')
        d.title(f"Run: {tool['name']}"); d.geometry("700x450")
        
        tk.Label(d, text=f"▶ {tool['name']}", font=('Courier', 14, 'bold'),
                fg='#00ff88', bg='#1a1a2e').pack(pady=8)
        
        # Args input
        f = tk.Frame(d, bg='#16213e', padx=10, pady=8)
        f.pack(fill='x', padx=10, pady=5)
        tk.Label(f, text="Command:", font=('Courier', 10), fg='#fff', bg='#16213e').pack(anchor='w')
        args_entry = tk.Entry(f, font=('Courier', 11), bg='#0a0a0a', fg='#00ff88', relief='flat')
        args_entry.pack(fill='x', pady=3)
        
        # Quick args
        if self.args_db:
            args = self.args_db.get_args(tool['name'])
            if args:
                af = tk.Frame(d, bg='#1a1a2e')
                af.pack(fill='x', padx=10)
                for arg, desc in args[:15]:
                    tk.Button(af, text=arg[:14], font=('Courier', 7),
                            fg='#000', bg='#0f3460', relief='flat',
                            command=lambda a=arg: args_entry.insert('end', ' '+a)
                            ).pack(side='left', padx=1, pady=1)
        
        # Output
        output = tk.Text(d, font=('Courier', 9), bg='#0a0a0a', fg='#00ff88', relief='flat')
        output.pack(fill='both', expand=True, padx=10, pady=5)
        
        stop_flag = [False]
        
        def execute():
            args = args_entry.get().strip()
            cmd = f"{tool['command']} {args}" if args else tool['command']
            output.insert('end', f"\n$ {cmd}\n{'='*40}\n\n")
            output.see('end')
            stop_flag[0] = False
            
            def run():
                try:
                    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, text=True, bufsize=1)
                    for line in iter(p.stdout.readline, ''):
                        if stop_flag[0]: p.kill(); break
                        output.insert('end', line); output.see('end')
                    p.wait()
                    output.insert('end', f"\n[Exit: {p.returncode}]\n")
                    output.see('end')
                except Exception as e:
                    output.insert('end', f"\n[X] {e}\n")
            threading.Thread(target=run, daemon=True).start()
        
        bf = tk.Frame(d, bg='#1a1a2e')
        bf.pack(fill='x', padx=10, pady=8)
        tk.Button(bf, text="Execute", font=('Courier', 10, 'bold'),
                fg='#000', bg='#00ff88', relief='raised', padx=15, pady=6,
                command=execute).pack(side='left', padx=3)
        tk.Button(bf, text="Stop", font=('Courier', 10),
                fg='#fff', bg='#cc0000', relief='raised', padx=15, pady=6,
                command=lambda: stop_flag.__setitem__(0, True)).pack(side='left', padx=3)
        tk.Button(bf, text="Close", font=('Courier', 10),
                fg='#fff', bg='#666', relief='raised', padx=15, pady=6,
                command=d.destroy).pack(side='right', padx=3)
        
        args_entry.bind('<Return>', lambda e: execute())
        args_entry.focus()
