
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import os, json
from gui.base_module import BaseModule
from gui.dropdown import Dropdown

class SessionLogger(BaseModule):
    def __init__(self, parent, db, logger):
        super().__init__(parent)
        self.db = db
        self.app_logger = logger
    
    def build_content(self):
        self.add_title("Session Logger", "Complete activity history for deconfliction and reports")
        
        self.db.cursor.execute("SELECT COUNT(*) FROM activity")
        total = self.db.cursor.fetchone()[0]
        self.db.cursor.execute("SELECT COUNT(DISTINCT action) FROM activity")
        unique = self.db.cursor.fetchone()[0]
        
        stats = tk.Frame(self.inner, bg='#16213e', padx=10, pady=8)
        stats.pack(fill='x', padx=10, pady=5)
        tk.Label(stats, text=f"Total Actions: {total} | Unique: {unique}",
                font=('Courier', 10), fg='#00ccff', bg='#16213e').pack(side='left')
        tk.Button(stats, text="Export Full Log", font=('Courier', 9), fg='#000', bg='#00ff88',
                relief='flat', padx=10, command=self._export_log).pack(side='right', padx=3)
        
        sf = tk.Frame(self.inner, bg='#1a1a2e')
        sf.pack(fill='x', padx=10, pady=5)
        self.search_entry = tk.Entry(sf, font=('Courier', 10), bg='#16213e', fg='#fff', relief='flat')
        self.search_entry.pack(side='left', fill='x', expand=True)
        self.search_entry.insert(0, 'Search actions...')
        self.search_entry.bind('<Return>', lambda e: self._load_logs())
        tk.Button(sf, text="Search", font=('Courier', 9), fg='#000', bg='#00ccff',
                relief='flat', padx=10, command=self._load_logs).pack(side='right', padx=3)
        
        self.log_frame = tk.Frame(self.inner, bg='#1a1a2e')
        self.log_frame.pack(fill='both', expand=True, padx=10, pady=5)
        self.status = self.add_status("")
        self._load_logs()
    
    def _load_logs(self, filter_action=None):
        for w in self.log_frame.winfo_children(): w.destroy()
        search = self.search_entry.get().strip()
        if search == 'Search actions...': search = ''
        
        query = "SELECT * FROM activity"
        params = []
        conditions = []
        if filter_action:
            conditions.append("action = ?")
            params.append(filter_action)
        if search:
            conditions.append("(action LIKE ? OR details LIKE ?)")
            params.extend([f'%{search}%', f'%{search}%'])
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        query += " ORDER BY timestamp DESC LIMIT 200"
        
        self.db.cursor.execute(query, params)
        logs = [dict(row) for row in self.db.cursor.fetchall()]
        
        if not logs:
            tk.Label(self.log_frame, text="No activity recorded yet.",
                    font=('Courier', 10), fg='#888', bg='#1a1a2e').pack(expand=True)
            return
        
        self.status.config(text=f"Showing {len(logs)} actions")
        
        action_colors = {'startup':'#3fb950','shutdown':'#f85149','module_opened':'#00ccff'}
        
        for log in logs:
            card = tk.Frame(self.log_frame, bg='#16213e', padx=10, pady=6)
            card.pack(fill='x', pady=1)
            h = tk.Frame(card, bg='#16213e')
            h.pack(fill='x')
            color = action_colors.get(log.get('action',''), '#888')
            tk.Label(h, text=log.get('action','?'), font=('Courier', 9, 'bold'),
                    fg=color, bg='#16213e').pack(side='left')
            ts = log.get('timestamp','')
            if ts: tk.Label(h, text=str(ts)[:19], font=('Courier', 8), fg='#666', bg='#16213e').pack(side='right')
            details = log.get('details','')
            if details: tk.Label(card, text=details[:100], font=('Courier', 8), fg='#aaa', bg='#16213e',
                    wraplength=self.canvas.winfo_width()-60).pack(anchor='w')
    
    def _export_log(self):
        self.db.cursor.execute("SELECT * FROM activity ORDER BY timestamp DESC")
        logs = [dict(row) for row in self.db.cursor.fetchall()]
        if not logs: messagebox.showinfo("Export", "No activity"); return
        
        export_dir = os.path.join(os.path.dirname(__file__), '..', 'reports')
        os.makedirs(export_dir, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        json_path = os.path.join(export_dir, f'session_{ts}.json')
        with open(json_path, 'w') as f: json.dump(logs, f, indent=2, default=str)
        
        html_path = os.path.join(export_dir, f'session_{ts}.html')
        with open(html_path, 'w') as f:
            f.write('<html><head><style>body{background:#0a0a0a;color:#00ff88;font:12px monospace}table{border-collapse:collapse}td,th{border:1px solid #333;padding:6px}</style></head><body>')
            f.write(f'<h1>Session Log</h1><table><tr><th>Time</th><th>Action</th><th>Details</th></tr>')
            for log in logs: f.write(f'<tr><td>{str(log.get("timestamp",""))[:19]}</td><td>{log.get("action","")}</td><td>{log.get("details","")[:100]}</td></tr>')
            f.write('</table></body></html>')
        messagebox.showinfo("Exported", f"Log exported to:\n{json_path}\n{html_path}")
