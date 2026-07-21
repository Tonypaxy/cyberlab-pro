import tkinter as tk
from tkinter import ttk, messagebox

class SettingsPanel:
    def __init__(self, parent, config, logger, theme_callback=None):
        self.parent = parent
        self.config = config
        self.logger = logger
        self.theme_callback = theme_callback
        self.frame = tk.Frame(parent, bg='#1a1a2e')
        
    def build(self):
        for w in self.frame.winfo_children(): w.destroy()
        self.frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        tk.Label(self.frame, text="⚙️ Settings", font=('Courier', 18, 'bold'),
                fg='#00ff88', bg='#1a1a2e').pack(anchor='w', pady=(0,20))
        
        # Theme
        tf = tk.LabelFrame(self.frame, text=" Theme ", font=('Courier', 10, 'bold'),
                fg='#00ccff', bg='#16213e', padx=15, pady=15)
        tf.pack(fill='x', pady=10)
        
        self.theme_var = tk.StringVar(value=self.config.get('theme', 'dark'))
        themes = ["dark", "amoled", "matrix", "light", "cyberpunk", "ocean"]
        
        for name in themes:
            def make_cmd(n):
                return lambda: self._switch_theme(n)
            
            rb = tk.Radiobutton(tf, text=name.title(), variable=self.theme_var,
                    value=name, font=('Courier', 10), fg='#fff', bg='#16213e',
                    selectcolor='#00ff88', activebackground='#16213e',
                    activeforeground='#00ff88',
                    command=make_cmd(name))
            rb.pack(anchor='w', pady=3)
        
        # Apply now button
        tk.Button(tf, text="✅ Apply Theme Now", font=('Courier', 10, 'bold'),
                fg='#000', bg='#00ff88', relief='raised', padx=15, pady=8,
                command=lambda: self._switch_theme(self.theme_var.get())).pack(pady=(10,0))
        
        # Window
        sf = tk.LabelFrame(self.frame, text=" Window ", font=('Courier', 10, 'bold'),
                fg='#00ccff', bg='#16213e', padx=15, pady=15)
        sf.pack(fill='x', pady=10)
        
        tk.Label(sf, text="Size (WxH):", font=('Courier', 10), fg='#fff', bg='#16213e').pack(side='left')
        self.geo_entry = tk.Entry(sf, font=('Courier', 10), bg='#0f3460', fg='#fff', relief='flat', width=15)
        self.geo_entry.pack(side='left', padx=10)
        self.geo_entry.insert(0, self.config.get('window_geometry', '800x600'))
        
        # Options
        of = tk.LabelFrame(self.frame, text=" Options ", font=('Courier', 10, 'bold'),
                fg='#00ccff', bg='#16213e', padx=15, pady=15)
        of.pack(fill='x', pady=10)
        
        self.auto_save = tk.BooleanVar(value=self.config.get('auto_save', True))
        tk.Checkbutton(of, text="Auto-save", variable=self.auto_save,
                font=('Courier', 10), fg='#fff', bg='#16213e',
                selectcolor='#00ff88').pack(anchor='w')
        
        self.notify_var = tk.BooleanVar(value=self.config.get('notifications', True))
        tk.Checkbutton(of, text="Notifications", variable=self.notify_var,
                font=('Courier', 10), fg='#fff', bg='#16213e',
                selectcolor='#00ff88').pack(anchor='w')
        
        # About
        af = tk.LabelFrame(self.frame, text=" About ", font=('Courier', 10, 'bold'),
                fg='#00ccff', bg='#16213e', padx=15, pady=15)
        af.pack(fill='x', pady=10)
        
        tk.Label(af, text=f"CyberLab Pro v{self.config.get('version')}",
                font=('Courier', 10, 'bold'), fg='#00ff88', bg='#16213e').pack(anchor='w')
        tk.Label(af, text="Termux & Linux Cybersecurity Workspace",
                font=('Courier', 9), fg='#aaa', bg='#16213e').pack(anchor='w')
        
        # Save button
        tk.Button(self.frame, text="💾 Save Settings", font=('Courier', 12, 'bold'),
                fg='#000', bg='#00ff88', relief='raised', padx=25, pady=10,
                command=self._save).pack(pady=15)
    
    def _switch_theme(self, name):
        """Switch theme immediately"""
        self.config.set('theme', name)
        self.logger.app_logger.info(f"Theme changed to: {name}")
        if self.theme_callback:
            self.theme_callback(name)
        messagebox.showinfo("Theme", f"Theme changed to {name.title()}!")
    
    def _save(self):
        self.config.set('theme', self.theme_var.get())
        self.config.set('window_geometry', self.geo_entry.get())
        self.config.set('auto_save', self.auto_save.get())
        self.config.set('notifications', self.notify_var.get())
        self.config.save()
        self.logger.app_logger.info("Settings saved")
        messagebox.showinfo("Saved", "Settings saved!")
