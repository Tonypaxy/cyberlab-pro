import tkinter as tk
from tkinter import ttk, messagebox

class SettingsPanel:
    def __init__(self, parent, config, logger, theme_callback=None):
        self.parent = parent
        self.config = config
        self.logger = logger
        self.theme_callback = theme_callback
        self.frame = tk.Frame(parent, bg='#1a1a2e')
        self.themes = {
            "dark": {"bg": "#1a1a2e", "fg": "#00ff88", "accent": "#16213e"},
            "amoled": {"bg": "#000000", "fg": "#00ff88", "accent": "#111111"},
            "matrix": {"bg": "#0a0a0a", "fg": "#00ff41", "accent": "#0d0d0d"},
            "light": {"bg": "#f5f5f5", "fg": "#333333", "accent": "#ffffff"}, "cyberpunk": {"bg": "#0d0221", "fg": "#ff2a6d", "accent": "#1a0533"}, "ocean": {"bg": "#0a192f", "fg": "#64ffda", "accent": "#112240"}
        }
    
    def build(self):
        self.frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        tk.Label(self.frame, text="⚙️ Settings", font=('Courier', 18, 'bold'),
                fg='#00ff88', bg='#1a1a2e').pack(anchor='w', pady=(0,20))
        
        # Theme selector with live preview
        theme_frame = tk.LabelFrame(self.frame, text="Theme (Live Preview)", font=('Courier', 10, 'bold'),
                fg='#00ccff', bg='#16213e', padx=15, pady=15)
        theme_frame.pack(fill='x', pady=10)
        
        self.theme_var = tk.StringVar(value=self.config.get('theme', 'dark'))
        
        for name, colors in self.themes.items():
            preview = tk.Frame(theme_frame, bg=colors['bg'], height=30)
            preview.pack(fill='x', pady=3)
            
            rb = tk.Radiobutton(preview, text=f"  {name.title()}", variable=self.theme_var,
                    value=name, font=('Courier', 10), fg=colors['fg'], bg=colors['bg'],
                    selectcolor=colors['fg'], activebackground=colors['bg'],
                    activeforeground=colors['fg'],
                    command=lambda n=name: self._apply_theme_preview(n))
            rb.pack(side='left', padx=5, pady=3)
            
            # Color swatches
            swatch = tk.Frame(preview, bg=colors['fg'], width=20, height=20)
            swatch.pack(side='right', padx=2, pady=5)
            swatch2 = tk.Frame(preview, bg=colors['accent'], width=20, height=20)
            swatch2.pack(side='right', padx=2, pady=5)
        
        tk.Button(theme_frame, text="✅ Apply Theme Now", font=('Courier', 10, 'bold'),
                fg='#000', bg='#00ff88', relief='flat', padx=15, pady=8,
                command=self._apply_theme).pack(pady=10)
        
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
        
        # Options
        opts_frame = tk.LabelFrame(self.frame, text="Options", font=('Courier', 10, 'bold'),
                fg='#00ccff', bg='#16213e', padx=15, pady=15)
        opts_frame.pack(fill='x', pady=10)
        
        self.auto_save_var = tk.BooleanVar(value=self.config.get('auto_save', True))
        tk.Checkbutton(opts_frame, text="Auto-save settings", variable=self.auto_save_var,
                font=('Courier', 10), fg='#fff', bg='#16213e',
                selectcolor='#00ff88', activebackground='#16213e').pack(anchor='w')
        
        self.notify_var = tk.BooleanVar(value=self.config.get('notifications', True))
        tk.Checkbutton(opts_frame, text="Enable toast notifications", variable=self.notify_var,
                font=('Courier', 10), fg='#fff', bg='#16213e',
                selectcolor='#00ff88', activebackground='#16213e').pack(anchor='w')
        
        # About
        sys_frame = tk.LabelFrame(self.frame, text="About", font=('Courier', 10, 'bold'),
                fg='#00ccff', bg='#16213e', padx=15, pady=15)
        sys_frame.pack(fill='x', pady=10)
        
        tk.Label(sys_frame, text=f"CyberLab Pro v{self.config.get('version')}",
                font=('Courier', 10, 'bold'), fg='#00ff88', bg='#16213e').pack(anchor='w')
        tk.Label(sys_frame, text="Termux & Linux Cybersecurity Workspace",
                font=('Courier', 9), fg='#aaa', bg='#16213e').pack(anchor='w')
        tk.Label(sys_frame, text="ARM 32-bit | Offline-first | Cross-platform",
                font=('Courier', 9), fg='#aaa', bg='#16213e').pack(anchor='w')
        
        tk.Button(self.frame, text="💾 Save Settings", font=('Courier', 12, 'bold'),
                fg='#000', bg='#00ff88', relief='flat', padx=25, pady=10,
                command=self._save).pack(pady=20)
    
    def _apply_theme_preview(self, name):
        """Preview theme on settings panel only"""
        colors = self.themes.get(name, self.themes['dark'])
        self.frame.configure(bg=colors['bg'])
    
    def _apply_theme(self):
        """Apply theme to entire application"""
        name = self.theme_var.get()
        self.config.set('theme', name)
        if self.theme_callback:
            self.theme_callback(name)
        self.logger.app_logger.info(f"Theme changed to {name}")
    
    def _save(self):
        self.config.set('theme', self.theme_var.get())
        self.config.set('window_geometry', self.geo_entry.get())
        self.config.set('auto_save', self.auto_save_var.get())
        self.config.set('notifications', self.notify_var.get())
        self.logger.app_logger.info("Settings saved")
        messagebox.showinfo("Settings", "Settings saved!")
