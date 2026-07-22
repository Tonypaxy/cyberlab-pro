import tkinter as tk

class Sidebar:
    def __init__(self, parent, command_callback=None):
        self.parent = parent
        self.command_callback = command_callback
        self.visible = True
        self.width = 185
        self.frame = tk.Frame(parent, bg='#16213e', width=self.width)
        self.buttons = {}
        self.active_button = None
        
        self.menu_items = [
            ("📊 Dashboard", "dashboard"),
            ("📁 Projects", "projects"),
            ("🔧 Tool Center", "tools"),
            ("🎯 Recon", "recon"),
            ("🌐 Network", "network"),
            ("🌍 Web", "web"),
            ("📡 SOC Monitor", "soc"),
            ("📋 Reports", "reports"),
            ("🔒 Evidence", "evidence"),
            ("📝 Notes", "notes"),
            ("💻 Terminal", "terminal"),
            ("🔌 Plugins", "plugins"),
            ("📝 Wordlist Gen", "wordlist"),
            ("⚠️ CVE Lookup", "cve"),
            ("🔐 Permissions", "permissions"),
            ("⚙️ Settings", "settings")
        ]
    
    def build(self):
        # Grid handled by launcher
        self.frame.grid_propagate(False)
        self.frame.grid_propagate(False)
        
        title_frame = tk.Frame(self.inner_frame, bg='#0f3460', height=50)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        tk.Label(title_frame, text="🛡️ CyberLab Pro", font=('Courier', 11, 'bold'),
                fg='#00ff88', bg='#0f3460').pack(pady=12)
        
        tk.Frame(self.inner_frame, bg='#00ff88', height=1).pack(fill='x', padx=10, pady=5)
        
        for text, cmd in self.menu_items:
            btn = tk.Button(self.frame, text=text, font=('Courier', 9),
                    fg='#00ccff', bg='#16213e', relief='flat', pady=8, padx=10,
                    anchor='w', justify='left',
                    command=lambda c=cmd: self._on_click(c))
            btn.pack(fill='x', padx=5, pady=1)
            self.buttons[cmd] = btn
        
        tk.Frame(self.inner_frame, bg='#00ff88', height=1).pack(fill='x', padx=10, pady=5)
        tk.Label(self.frame, text="v1.0.0 | ARM/Linux", font=('Courier', 7),
                fg='#555', bg='#16213e').pack(side='bottom', pady=5)
        
        self.set_active("dashboard")
    
    def set_active(self, command):
        for cmd, btn in self.buttons.items():
            btn.configure(fg='#00ccff', bg='#16213e')
        if command in self.buttons:
            self.buttons[command].configure(fg='#000', bg='#00ff88')
            self.active_button = command
    
    def toggle(self):
        if self.visible:
            self.frame.grid_remove()
            self.visible = False
        else:
            self.frame.grid()
            self.visible = True
    
    def _on_click(self, command):
        self.set_active(command)
        if self.command_callback:
            self.command_callback(command)
