import tkinter as tk

class Sidebar:
    def __init__(self, parent, command_callback=None):
        self.parent = parent
        self.command_callback = command_callback
        self.visible = True
        self.width = 185
        self.frame = tk.Frame(parent, bg='#16213e', width=self.width)
        
        self.menu_items = [
            ("Dashboard", "dashboard"),
            ("Projects", "projects"),
            ("Tool Center", "tools"),
            ("Recon", "recon"),
            ("Network", "network"),
            ("Web", "web"),
            ("SOC Monitor", "soc"),
            ("Reports", "reports"),
            ("Evidence", "evidence"),
            ("Notes", "notes"),
            ("Terminal", "terminal"),
            ("Plugins", "plugins"),
            ("CVE Lookup", "cve"),
            ("Wordlist Gen", "wordlist"),
            ("Permissions", "permissions"),
            ("Settings", "settings")
        ]
        
        self.buttons = {}
        self.active_button = None
    
    def build(self):
        self.frame.grid_propagate(False)
        
        # Scrollable canvas
        canvas = tk.Canvas(self.frame, bg='#16213e', width=self.width-5, highlightthickness=0)
        scrollbar = tk.Scrollbar(self.frame, orient='vertical', command=canvas.yview)
        inner = tk.Frame(canvas, bg='#16213e')
        
        inner.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.create_window((0,0), window=inner, anchor='nw', width=self.width-5)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Title
        title_frame = tk.Frame(inner, bg='#0f3460', height=50, width=self.width-5)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        tk.Label(title_frame, text="CyberLab Pro", font=('Courier', 11, 'bold'),
                fg='#00ff88', bg='#0f3460').pack(pady=12)
        
        tk.Frame(inner, bg='#00ff88', height=1).pack(fill='x', padx=10, pady=5)
        
        # Menu buttons
        for text, cmd in self.menu_items:
            btn = tk.Button(inner, text=text, font=('Courier', 9),
                    fg='#00ccff', bg='#16213e', relief='flat', pady=8, padx=10,
                    anchor='w', justify='left', width=18,
                    command=lambda c=cmd: self._on_click(c))
            btn.pack(fill='x', padx=5, pady=1)
            self.buttons[cmd] = btn
        
        # Bottom
        tk.Frame(inner, bg='#00ff88', height=1).pack(fill='x', padx=10, pady=5)
        tk.Label(inner, text="v1.0.0 | ARM/Linux", font=('Courier', 7),
                fg='#555', bg='#16213e').pack(pady=5)
        
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
