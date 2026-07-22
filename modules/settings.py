import tkinter as tk
from gui.scrollable import make_scrollable
from tkinter import ttk, messagebox

class Settings:
    def __init__(self, parent, config, logger):
        self.parent = parent
        self.config = config
        self.logger = logger
        self.frame = tk.Frame(parent, bg='#1a1a2e')
        self.themes = {
            "dark": {"bg": "#1a1a2e", "fg": "#00ff88", "accent": "#16213e"},
            "amoled": {"bg": "#000000", "fg": "#00ff88", "accent": "#111111"},
            "matrix": {"bg": "#0a0a0a", "fg": "#00ff41", "accent": "#0d0d0d"},
            "light": {"bg": "#f0f0f0", "fg": "#000000", "accent": "#ffffff"}
        }
    
    def build(self):
        self.frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        tk.Label(self.frame, text="Settings", font=('Courier', 18, 'bold'),
                fg='#00ff88', bg='#1a1a2e').pack(anchor='w', pady=(0,20))
        
        # Theme selector
        theme_frame = tk.LabelFrame(self.frame, text="Theme", font=('Courier', 10, 'bold'),
                fg='#00ccff', bg='#16213e', padx=15, pady=15)
        theme_frame.pack(fill='x', pady=10)
        
        self.theme_var = tk.StringVar(value=self.config.get('theme', 'dark'))
        
        for name, colors in self.themes.items():
            rb = tk.Radiobutton(theme_frame, text=name.title(), variable=self.theme_var,
                    value=name, font=('Courier', 10), fg='#fff', bg='#16213e',
                    selectcolor='#00ff88', activebackground='#16213e',
                    activeforeground='#00ff88', command=self._preview_theme)
            rb.pack(anchor='w', pady=2)
        
        # Window size
        size_frame = tk.LabelFrame(self.frame, text="Window", font=('Courier', 10, 'bold'),
                fg='#00ccff', bg='#16213e', padx=15, pady=15)
        size_frame.pack(fill='x', pady=10)
        
        tk.Label(size_frame, text="Geometry (WxH):", font=('Courier', 10),
                fg='#fff', bg='#16213e').pack(side='left')
        self.geo_entry = tk.Entry(size_frame, font=('Courier', 10), bg='#0f3460',
                fg='#fff', relief='flat', width=15)
        self.geo_entry.pack(side='left', padx=10)
        self.geo_entry.insert(0, self.config.get('window_geometry', '800x600'))
        
        # Auto-save toggle
        opts_frame = tk.LabelFrame(self.frame, text="Options", font=('Courier', 10, 'bold'),
                fg='#00ccff', bg='#16213e', padx=15, pady=15)
        opts_frame.pack(fill='x', pady=10)
        
        self.auto_save_var = tk.BooleanVar(value=self.config.get('auto_save', True))
        tk.Checkbutton(opts_frame, text="Auto-save settings", variable=self.auto_save_var,
                font=('Courier', 10), fg='#fff', bg='#16213e',
                selectcolor='#00ff88', activebackground='#16213e',
                activeforeground='#00ff88').pack(anchor='w')
        
        # System info
        sys_frame = tk.LabelFrame(self.frame, text="About", font=('Courier', 10, 'bold'),
                fg='#00ccff', bg='#16213e', padx=15, pady=15)
        sys_frame.pack(fill='x', pady=10)
        
        tk.Label(sys_frame, text=f"CyberLab Pro v{self.config.get('version')}",
                font=('Courier', 10, 'bold'), fg='#00ff88', bg='#16213e').pack(anchor='w')
        tk.Label(sys_frame, text="Termux Cybersecurity Workspace",
                font=('Courier', 9), fg='#aaa', bg='#16213e').pack(anchor='w')
        tk.Label(sys_frame, text="Optimized for ARM 32-bit",
                font=('Courier', 9), fg='#aaa', bg='#16213e').pack(anchor='w')
        
        # Save button
        tk.Button(self.frame, text="Save Settings", font=('Courier', 12, 'bold'),
                fg='#000', bg='#00ff88', relief='flat', padx=25, pady=10,
                command=self._save_settings).pack(pady=20)
    
    def _preview_theme(self):
        theme = self.themes[self.theme_var.get()]
        # Preview on settings frame
        self.frame.configure(bg=theme['bg'])
    
    def _save_settings(self):
        self.config.set('theme', self.theme_var.get())
        self.config.set('window_geometry', self.geo_entry.get())
        self.config.set('auto_save', self.auto_save_var.get())
        self.logger.app_logger.info(f"Settings updated: theme={self.theme_var.get()}")
        messagebox.showinfo("Settings", "Settings saved!\nRestart to apply theme changes.")
