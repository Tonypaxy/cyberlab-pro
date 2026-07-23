import tkinter as tk

class Sidebar:
    def __init__(self, parent, command_callback=None):
        self.parent = parent
        self.command_callback = command_callback
        self.frame = tk.Frame(parent, bg='#16213e', width=185)
        
        self.menu_items = [
            "Dashboard", "Projects", "Tool Center", "Recon", "Network", "Web",
            "SOC Monitor", "Reports", "Evidence", "Notes", "Terminal", "Plugins",
            "CVE Lookup", "Wordlist Gen", "Permissions", "Payload Gen",
            "Session Log", "API Lookup", "Templates", "Vault", "Net Map",
            "Wordlists", "Log Analyzer", "Sanitizer", "Checksum",
            "Exploits", "Subdomains", "Port Scan", "Forensics",
            "Wireless", "Cloud", "Stego", "Resources",
            "Auto Recon", "OSINT", "Passwords", "Fuzzing", "Malware",
            "Reverse Eng", "Social Eng", "Settings"
        ]
        
        self.cmd_map = {
            "Dashboard":"dashboard","Projects":"projects","Tool Center":"tools",
            "Recon":"recon","Network":"network","Web":"web","SOC Monitor":"soc",
            "Reports":"reports","Evidence":"evidence","Notes":"notes",
            "Terminal":"terminal","Plugins":"plugins","CVE Lookup":"cve",
            "Wordlist Gen":"wordlist","Permissions":"permissions","Payload Gen":"payloads",
            "Session Log":"sessions","API Lookup":"api","Templates":"templates",
            "Vault":"vault","Net Map":"mapper","Wordlists":"wordlists",
            "Log Analyzer":"loganalyzer","Sanitizer":"sanitizer","Checksum":"checksum",
            "Exploits":"exploits","Subdomains":"subdomains","Port Scan":"portscan",
            "Forensics":"forensics","Wireless":"wireless2","Cloud":"cloud",
            "Stego":"stego","Resources":"resources","Auto Recon":"autorecon",
            "OSINT":"osint","Passwords":"passwords","Fuzzing":"fuzzing","Malware":"malware",
            "Reverse Eng":"reverse","Social Eng":"social","Settings":"settings"
        }
    
    def build(self):
        self.frame.pack_propagate(False)
        
        tk.Label(self.frame, text="CyberLab Pro", font=('Courier', 11, 'bold'),
                fg='#00ff88', bg='#0f3460', height=2).pack(fill='x')
        
        scrollbar = tk.Scrollbar(self.frame, orient='vertical')
        scrollbar.pack(side='right', fill='y')
        
        h_scrollbar = tk.Scrollbar(self.frame, orient='horizontal')
        h_scrollbar.pack(side='bottom', fill='x')
        
        self.listbox = tk.Listbox(self.frame, font=('Courier', 9),
                bg='#16213e', fg='#00ccff', selectbackground='#00ff88',
                selectforeground='#000', relief='flat', borderwidth=0,
                yscrollcommand=scrollbar.set, xscrollcommand=h_scrollbar.set,
                activestyle='none', highlightthickness=0, height=35)
        self.listbox.pack(fill='both', expand=True)
        
        scrollbar.config(command=self.listbox.yview)
        h_scrollbar.config(command=self.listbox.xview)
        
        for item in self.menu_items:
            self.listbox.insert('end', f"  {item}")
        
        self.listbox.bind('<<ListboxSelect>>', self._on_select)
        self.listbox.selection_set(0)
        
        tk.Label(self.frame, text="v1.0.0", font=('Courier', 7),
                fg='#555', bg='#16213e').pack(side='bottom', pady=2)
    
    def set_active(self, command):
        for name, cmd in self.cmd_map.items():
            if cmd == command:
                idx = list(self.cmd_map.keys()).index(name)
                if idx < self.listbox.size():
                    self.listbox.selection_clear(0, 'end')
                    self.listbox.selection_set(idx)
                    self.listbox.see(idx)
                break
    
    def _on_select(self, event):
        selection = self.listbox.curselection()
        if selection:
            idx = selection[0]
            item_name = self.menu_items[idx]
            cmd = self.cmd_map.get(item_name)
            if cmd and self.command_callback:
                self.command_callback(cmd)
