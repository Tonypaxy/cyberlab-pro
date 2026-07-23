import tkinter as tk

class ToolBar:
    def __init__(self, parent, callbacks=None, toggle_sidebar=None):
        self.parent = parent; self.callbacks = callbacks or {}; self.toggle_sidebar = toggle_sidebar
        self.frame = tk.Frame(parent, bg='#0f3460', height=35)
        self.buttons = {}
    
    def build(self):
        self.frame.pack_propagate(False)
        
        # Hamburger menu
        tk.Button(self.frame, text="☰", font=('Courier', 12, 'bold'),
                fg='#00ff88', bg='#0f3460', relief='flat', padx=10,
                command=lambda: self.toggle_sidebar and self.toggle_sidebar()).pack(side='left', pady=3)
        
        # Quick buttons - minimal horizontal
        for icon, cmd in [("Home", "dashboard"), ("Scan", "recon"), ("Term", "terminal")]:
            btn = tk.Button(self.frame, text=icon, font=('Courier', 9),
                    fg='#aaa', bg='#0f3460', relief='flat', padx=8, pady=3,
                    command=lambda c=cmd: self._click(c))
            btn.pack(side='left', pady=3)
            self.buttons[cmd] = btn
        
        self.set_active("dashboard")
    
    def set_active(self, command):
        for cmd, btn in self.buttons.items():
            btn.configure(fg='#aaa', bg='#0f3460')
        if command in self.buttons:
            self.buttons[command].configure(fg='#000', bg='#00ff88')
    
    def _click(self, command):
        self.set_active(command)
        if command in self.callbacks: self.callbacks[command]()
