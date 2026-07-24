import tkinter as tk
from tkinter import messagebox
from datetime import datetime

class RecoveryManager:
    def __init__(self, parent, db, logger, session_manager, navigate_callback=None):
        self.parent = parent; self.db = db; self.logger = logger
        self.session = session_manager; self.navigate = navigate_callback
        self.frame = tk.Frame(parent, bg='#1a1a2e')

    def build(self):
        self.frame.pack(fill='both', expand=True, padx=10, pady=10)
        tk.Label(self.frame, text="Session Recovery", font=('Courier',16,'bold'), fg='#ffaa00', bg='#1a1a2e').pack(anchor='w')
        tk.Label(self.frame, text="Restore previous sessions and recovery points", font=('Courier',9), fg='#888', bg='#1a1a2e').pack(anchor='w', pady=5)
        
        # Current session info
        cf = tk.LabelFrame(self.frame, text=" Current Session ", font=('Courier',10,'bold'), fg='#00ff88', bg='#16213e', padx=10, pady=8)
        cf.pack(fill='x', pady=5)
        last_mod = self.session.get_last_module() or "dashboard"
        last_proj = self.session.get_last_project()
        tk.Label(cf, text=f"Last Module: {last_mod}", font=('Courier',9), fg='#00ccff', bg='#16213e').pack(anchor='w')
        tk.Label(cf, text=f"Last Project: {last_proj.get('name','None') if last_proj else 'None'}", font=('Courier',9), fg='#00ccff', bg='#16213e').pack(anchor='w')
        tk.Label(cf, text=f"Theme: {self.session.get_theme()}", font=('Courier',9), fg='#00ccff', bg='#16213e').pack(anchor='w')
        
        tk.Button(cf, text="Save Recovery Point", font=('Courier',9,'bold'), fg='#000', bg='#00ff88',
                relief='raised', padx=15, pady=6, command=self._save_point).pack(pady=5)
        
        # Recovery points
        rf = tk.LabelFrame(self.frame, text=" Recovery Points ", font=('Courier',10,'bold'), fg='#ffaa00', bg='#16213e', padx=10, pady=8)
        rf.pack(fill='both', expand=True, pady=5)
        
        points = self.session.get_recovery_points()
        if not points:
            tk.Label(rf, text="No recovery points saved yet", font=('Courier',9), fg='#888', bg='#16213e').pack(pady=10)
        else:
            for i, point in enumerate(reversed(points)):
                card = tk.Frame(rf, bg='#16213e', padx=10, pady=6); card.pack(fill='x', pady=2)
                h = tk.Frame(card, bg='#16213e'); h.pack(fill='x')
                pt_name = point.get('name','auto')
                pt_time = datetime.fromtimestamp(point.get('time',0)).strftime('%Y-%m-%d %H:%M:%S')
                tk.Label(h, text=f"{pt_name} - {pt_time}", font=('Courier',9,'bold'), fg='#ffaa00', bg='#16213e').pack(side='left')
                tk.Label(h, text=f"Module: {point.get('module','?')}", font=('Courier',8), fg='#888', bg='#16213e').pack(side='right')
                
                proj = point.get('project',{})
                if proj:
                    tk.Label(card, text=f"Project: {proj.get('name','?')}", font=('Courier',8), fg='#888', bg='#16213e').pack(anchor='w')
                
                bf = tk.Frame(card, bg='#16213e'); bf.pack(fill='x')
                actual_idx = len(points) - 1 - i
                tk.Button(bf, text="Restore", font=('Courier',8), fg='#000', bg='#ffaa00', relief='flat', padx=8,
                        command=lambda idx=actual_idx: self._restore(idx)).pack(side='left', padx=1)
                tk.Button(bf, text="Delete", font=('Courier',8), fg='#fff', bg='#cc0000', relief='flat', padx=8,
                        command=lambda idx=actual_idx: self._delete(idx)).pack(side='left', padx=1)

        tk.Label(self.frame, text="Auto-saves on shutdown. Max 10 points.", font=('Courier',7), fg='#555', bg='#1a1a2e').pack(pady=5)

    def _save_point(self):
        self.session.create_recovery_point("manual")
        messagebox.showinfo("Saved", "Recovery point saved!")
        for w in self.frame.winfo_children(): w.destroy()
        self.build()

    def _restore(self, index):
        if self.session.restore_recovery_point(index):
            messagebox.showinfo("Restored", "Session restored! Navigating...")
            if self.navigate:
                mod = self.session.get_last_module()
                self.navigate(mod or "dashboard")

    def _delete(self, index):
        points = self.session.get_recovery_points()
        if 0 <= index < len(points):
            points.pop(index)
            self.session.data["recovery_points"] = points
            self.session._save()
            for w in self.frame.winfo_children(): w.destroy()
            self.build()
