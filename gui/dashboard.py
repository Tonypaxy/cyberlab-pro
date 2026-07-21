import tkinter as tk
from tkinter import ttk
import os

class Dashboard:
    def __init__(self, parent, system_monitor, tool_detector, db, config=None, navigate=None):
        self.parent = parent
        self.monitor = system_monitor
        self.detector = tool_detector
        self.db = db
        self.config = config
        self.navigate = navigate
        self.frame = tk.Frame(parent, bg='#1a1a2e')
        
    def build(self):
        self.frame.pack(fill='both', expand=True, padx=15, pady=15)
        
        header = tk.Frame(self.frame, bg='#1a1a2e')
        header.pack(fill='x', pady=(0,10))
        
        tk.Label(header, text="🛡️", font=('Courier', 28),
                fg='#00ff88', bg='#1a1a2e').pack(side='left', padx=(0,10))
        
        title_frame = tk.Frame(header, bg='#1a1a2e')
        title_frame.pack(side='left')
        tk.Label(title_frame, text="CYBERLAB PRO", font=('Courier', 16, 'bold'),
                fg='#00ff88', bg='#1a1a2e').pack(anchor='w')
        tk.Label(title_frame, text="Security Workspace Dashboard", font=('Courier', 9),
                fg='#666', bg='#1a1a2e').pack(anchor='w')
        
        tk.Button(header, text="🔄 Refresh", font=('Courier', 8),
                fg='#000', bg='#00ccff', relief='flat', padx=10,
                command=self._refresh).pack(side='right')
        
        last_proj = self.config.get('last_project') if self.config else None
        if last_proj:
            proj_frame = tk.Frame(self.frame, bg='#0f3460', padx=10, pady=5)
            proj_frame.pack(fill='x', pady=(0,10))
            tk.Label(proj_frame, text=f"📁 Active Project: {last_proj}", font=('Courier', 9, 'bold'),
                    fg='#00ff88', bg='#0f3460').pack(side='left')
        
        cards1 = tk.Frame(self.frame, bg='#1a1a2e')
        cards1.pack(fill='x', pady=3)
        
        info = self.monitor.get_summary()
        ram = info['ram']
        storage = info['storage']
        battery = self.monitor.get_battery_info()
        network = self.monitor.get_network_info()
        
        self._card(cards1, "🖥️ CPU", f"{info['cpu']}%", "#00ff88")
        self._card(cards1, "🧠 RAM", f"{ram['percent']}%", "#00ccff")
        self._card(cards1, "💾 Disk", f"{storage['free']}GB free", "#ffaa00")
        if battery:
            icon = "🔋" if battery.get('status') == 'Discharging' else "⚡"
            self._card(cards1, f"{icon} Batt", f"{battery.get('capacity', '?')}%", "#ccff00")
        else:
            self._card(cards1, "🔋 Batt", "N/A", "#666")
        
        cards2 = tk.Frame(self.frame, bg='#1a1a2e')
        cards2.pack(fill='x', pady=3)
        
        net_status = "Connected" if network.get('connected') else "Offline"
        net_color = "#00ff88" if network.get('connected') else "#cc0000"
        self._card(cards2, "🌐 Net", net_status, net_color)
        self._card(cards2, "🔧 Tools", str(self.detector.get_total_count()), "#cc00ff")
        projects = self.db.get_all_projects()
        self._card(cards2, "📁 Proj", str(len(projects)), "#00ccff")
        svcs = info.get("services", 0)
        self._card(cards2, "⚙️ Svcs", str(svcs), "#ff8800" if svcs > 0 else "#888")
        
        act_frame = tk.LabelFrame(self.frame, text=" Recent Activity ", font=('Courier', 10, 'bold'),
                fg='#00ccff', bg='#16213e', padx=10, pady=8)
        act_frame.pack(fill='x', pady=10)
        
        activities = self.db.get_recent_activity(5)
        if activities:
            for act in activities:
                row = tk.Frame(act_frame, bg='#16213e')
                row.pack(fill='x', pady=1)
                tk.Label(row, text=f"▸ {act['action']}", font=('Courier', 9),
                        fg='#aaa', bg='#16213e').pack(side='left')
                ts = act.get('timestamp', '')
                if ts:
                    tk.Label(row, text=str(ts)[:19], font=('Courier', 8),
                            fg='#555', bg='#16213e').pack(side='right')
        else:
            tk.Label(act_frame, text="No recent activity", font=('Courier', 9),
                    fg='#666', bg='#16213e').pack()
        
        tools_frame = tk.LabelFrame(self.frame, text=" Installed Tools ", font=('Courier', 10, 'bold'),
                fg='#00ccff', bg='#16213e', padx=10, pady=8)
        tools_frame.pack(fill='both', expand=True, pady=(0,10))
        
        for cat, tools in self.detector.detected.items():
            if tools:
                names = ', '.join([t['name'] for t in tools[:6]])
                icons = {"recon":"🎯","web":"🌍","network":"🌐","credentials":"🔑","programming":"💻","wireless":"📡","forensics":"🔍","exploitation":"💣"}
                icon = icons.get(cat, "📦")
                tk.Label(tools_frame, text=f"{icon} {cat}: {names}", font=('Courier', 8),
                        fg='#aaa', bg='#16213e', wraplength=550).pack(anchor='w', pady=1)
        
        quick_frame = tk.Frame(self.frame, bg='#1a1a2e')
        quick_frame.pack(fill='x')
        
        tk.Label(quick_frame, text="Quick Actions:", font=('Courier', 9, 'bold'),
                fg='#666', bg='#1a1a2e').pack(side='left', padx=(0,10))
        
        for text, cmd, color in [
            ("New Scan", "recon", "#00ff88"),
            ("Terminal", "terminal", "#00ccff"),
            ("Reports", "reports", "#ffaa00"),
            ("Projects", "projects", "#cc88ff"),
            ("Notes", "notes", "#ff88cc")
        ]:
            tk.Button(quick_frame, text=text, font=('Courier', 8),
                    fg='#000', bg=color, relief='flat', padx=8, pady=3,
                    command=lambda c=cmd: self._go(c)).pack(side='left', padx=2)
    
    def _card(self, parent, label, value, color):
        card = tk.Frame(parent, bg='#16213e', padx=12, pady=8)
        card.pack(side='left', fill='x', expand=True, padx=3)
        tk.Label(card, text=label, font=('Courier', 8), fg='#888', bg='#16213e').pack()
        tk.Label(card, text=value, font=('Courier', 14, 'bold'), fg=color, bg='#16213e').pack()
    
    def _go(self, command):
        if self.navigate:
            self.navigate(command)
    
    def _refresh(self):
        self.detector.detect_all()
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.build()
