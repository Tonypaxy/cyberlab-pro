import tkinter as tk

class ToolBar:
    def __init__(self, parent, callbacks=None, toggle_sidebar=None):
        self.parent = parent
        self.callbacks = callbacks or {}
        self.toggle_sidebar = toggle_sidebar
        self.frame = tk.Frame(parent, bg='#0f3460', height=40)
        self.buttons = {}
        self.active_button = None
        
    def build(self):
        self.frame.pack(side='top', fill='x')
        self.frame.pack_propagate(False)
        
        # Hamburger
        self.hamburger_btn = tk.Button(self.frame, text="☰", font=('Courier', 14, 'bold'),
                fg='#00ff88', bg='#0f3460', relief='flat', padx=10,
                activebackground='#16213e', activeforeground='#00ff88',
                command=self._toggle)
        self.hamburger_btn.pack(side='left', pady=3)
        
        tk.Frame(self.frame, bg='#1a3a5e', width=1).pack(side='left', fill='y', padx=5)
        
        # Navigation buttons
        buttons = [
            ("🏠", "dashboard"),
            ("📁", "projects"),
            ("🎯", "recon"),
            ("💻", "terminal"),
            ("⚙️", "settings")
        ]
        
        for icon, cmd in buttons:
            btn = tk.Button(self.frame, text=icon, font=('Courier', 12),
                    fg='#aaa', bg='#0f3460', relief='flat', padx=8, pady=2,
                    activebackground='#00ff88', activeforeground='#000',
                    command=lambda c=cmd: self._click(c))
            btn.pack(side='left', pady=3, padx=1)
            self.buttons[cmd] = btn
        
        self.status_label = tk.Label(self.frame, text="", font=('Courier', 8),
                fg='#888', bg='#0f3460')
        self.status_label.pack(side='right', padx=10)
        
        self.set_active("dashboard")
    
    def set_active(self, command):
        for cmd, btn in self.buttons.items():
            btn.configure(fg='#aaa', bg='#0f3460')
        if command in self.buttons:
            self.buttons[command].configure(fg='#000', bg='#00ff88')
            self.active_button = command
    
    def _toggle(self):
        if self.toggle_sidebar:
            self.toggle_sidebar()
    
    def _click(self, command):
        self.set_active(command)
        if command in self.callbacks:
            self.callbacks[command]()  # Call immediately
    
    def set_status(self, text):
        self.status_label.config(text=text)
