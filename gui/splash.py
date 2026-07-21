import tkinter as tk
from tkinter import ttk

class SplashScreen:
    def __init__(self, duration=2.0):
        self.root = tk.Tk()
        self.duration = duration
        self.root.title("CyberLab Pro")
        self.root.overrideredirect(True)
        
        width, height = 420, 300
        x = (self.root.winfo_screenwidth() - width) // 2
        y = (self.root.winfo_screenheight() - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        self.root.configure(bg='#0a0e1a')
        
        # Border frame
        border = tk.Frame(self.root, bg='#00ff88', padx=2, pady=2)
        border.pack(fill='both', expand=True, padx=1, pady=1)
        
        frame = tk.Frame(border, bg='#0a0e1a')
        frame.pack(fill='both', expand=True)
        
        # Shield icon
        tk.Label(frame, text="🛡️", font=('Courier', 40),
                fg='#00ff88', bg='#0a0e1a').pack(pady=(20,5))
        
        # Title
        tk.Label(frame, text="CYBERLAB PRO", font=('Courier', 22, 'bold'),
                fg='#00ff88', bg='#0a0e1a').pack()
        
        # Subtitle
        tk.Label(frame, text="Professional Cybersecurity Workspace", font=('Courier', 9),
                fg='#00ccff', bg='#0a0e1a').pack()
        
        # Version
        tk.Label(frame, text="v1.0.0 | ARM 32-bit | Termux:X11", font=('Courier', 8),
                fg='#666', bg='#0a0e1a').pack(pady=(10,5))
        
        # Loading bar
        self.progress = ttk.Progressbar(frame, mode='indeterminate', length=250)
        self.progress.pack(pady=15)
        
        self.status = tk.Label(frame, text="Initializing...", font=('Courier', 9),
                fg='#888', bg='#0a0e1a')
        self.status.pack()
        
        # Tagline
        tk.Label(frame, text="Securing the mobile frontier", font=('Courier', 8, 'italic'),
                fg='#444', bg='#0a0e1a').pack(side='bottom', pady=10)
    
    def update(self, text):
        self.status.config(text=text)
        self.root.update()
    
    def show(self):
        self.progress.start(10)
        self.root.after(int(self.duration * 1000), self.close)
        self.root.mainloop()
    
    def close(self):
        self.progress.stop()
        self.root.destroy()
