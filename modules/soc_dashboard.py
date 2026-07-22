from gui.scrollable_frame import create_scrollable
import tkinter as tk
from gui.scrollable import make_scrollable
from tkinter import ttk
import threading
import time
from datetime import datetime

class SOCDashboard:
    def __init__(self, parent, monitor, detector, db, logger, notifier=None):
        self.parent = parent
        self.monitor = monitor
        self.detector = detector
        self.db = db
        self.logger = logger
        self.notifier = notifier
        self.frame = tk.Frame(parent, bg='#0a0a0a')
        self.monitoring = False
        self.alerts = []
    
    def build(self):
        self.frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Header
        header = tk.Frame(self.frame, bg='#0a0a0a')
        header.pack(fill='x', pady=(0,10))
        
        tk.Label(header, text="🛡️ SOC Dashboard", font=('Courier', 18, 'bold'),
                fg='#ff0000', bg='#0a0a0a').pack(side='left')
        
        self.monitor_btn = tk.Button(header, text="▶ Start Monitoring", font=('Courier', 10),
                fg='#000', bg='#00ff88', relief='flat', padx=15,
                command=self._toggle_monitoring)
        self.monitor_btn.pack(side='right')
        
        # Stats row
        stats = tk.Frame(self.frame, bg='#0a0a0a')
        stats.pack(fill='x', pady=5)
        
        self.cpu_label = self._stat_card(stats, "CPU", "0%", "#00ff88")
        self.ram_label = self._stat_card(stats, "RAM", "0%", "#00ccff")
        self.disk_label = self._stat_card(stats, "DISK", "0GB", "#ffaa00")
        self.net_label = self._stat_card(stats, "NET", "--", "#cc00ff")
        self.proc_label = self._stat_card(stats, "PROCS", "0", "#ff8800")
        
        # Alert area
        alert_frame = tk.LabelFrame(self.frame, text=" Alerts ", font=('Courier', 10, 'bold'),
                fg='#ff0000', bg='#111', padx=10, pady=10)
        alert_frame.pack(fill='x', pady=10)
        
        self.alert_text = tk.Text(alert_frame, font=('Courier', 9), bg='#0a0a0a',
                fg='#ff4444', height=8, relief='flat', wrap='word')
        self.alert_text.pack(fill='x')
        
        # Log area
        log_frame = tk.LabelFrame(self.frame, text=" Live Log ", font=('Courier', 10, 'bold'),
                fg='#00ccff', bg='#111', padx=10, pady=10)
        log_frame.pack(fill='both', expand=True, pady=5)
        
        self.log_text = tk.Text(log_frame, font=('Courier', 9), bg='#0a0a0a',
                fg='#00ff88', relief='flat', wrap='word')
        self.log_text.pack(fill='both', expand=True)
    
    def _stat_card(self, parent, label, value, color):
        card = tk.Frame(parent, bg='#111', padx=12, pady=8, relief='flat', bd=0)
        card.pack(side='left', fill='x', expand=True, padx=3)
        tk.Label(card, text=label, font=('Courier', 8), fg='#666', bg='#111').pack()
        val = tk.Label(card, text=value, font=('Courier', 16, 'bold'), fg=color, bg='#111')
        val.pack()
        return val
    
    def _toggle_monitoring(self):
        if self.monitoring:
            self.monitoring = False
            self.monitor_btn.config(text="▶ Start Monitoring", bg='#00ff88')
            self._log("Monitoring stopped")
        else:
            self.monitoring = True
            self.monitor_btn.config(text="⏹ Stop Monitoring", bg='#cc0000')
            self._log("🔴 SOC Monitoring started")
            threading.Thread(target=self._monitor_loop, daemon=True).start()
    
    def _monitor_loop(self):
        while self.monitoring:
            try:
                info = self.monitor.get_summary()
                ram = info['ram']
                storage = info['storage']
                battery = self.monitor.get_battery_info()
                network = self.monitor.get_network_info()
                
                # Update UI
                self.frame.after(0, lambda: self.cpu_label.config(text=f"{info['cpu']}%"))
                self.frame.after(0, lambda: self.ram_label.config(text=f"{ram['percent']}%"))
                self.frame.after(0, lambda: self.disk_label.config(text=f"{storage['free']}GB"))
                
                net_status = "UP" if network.get('connected') else "DOWN"
                self.frame.after(0, lambda: self.net_label.config(text=net_status))
                
                # Check thresholds and alert
                if info['cpu'] > 80:
                    self._alert(f"⚠️ High CPU: {info['cpu']}%")
                if ram['percent'] > 90:
                    self._alert(f"⚠️ High RAM: {ram['percent']}%")
                if storage['free'] < 1:
                    self._alert(f"⚠️ Low disk: {storage['free']}GB free")
                
                tools = self.detector.get_total_count()
                self.frame.after(0, lambda: self.proc_label.config(text=str(tools)))
                
                self._log(f"[{datetime.now().strftime('%H:%M:%S')}] CPU:{info['cpu']}% RAM:{ram['percent']}% Disk:{storage['free']}GB Net:{net_status}")
                
            except Exception as e:
                self._log(f"Error: {e}")
            
            time.sleep(3)
    
    def _alert(self, message):
        timestamp = datetime.now().strftime('%H:%M:%S')
        self.alert_text.insert('end', f"[{timestamp}] {message}\n")
        self.alert_text.see('end')
        if self.notifier:
            self.notifier(message, "warning")
    
    def _log(self, message):
        self.log_text.insert('end', f"{message}\n")
        self.log_text.see('end')
        # Keep last 100 lines
        lines = int(self.log_text.index('end-1c').split('.')[0])
        if lines > 100:
            self.log_text.delete('1.0', f'{lines-100}.0')
