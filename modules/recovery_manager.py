import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
import threading, time

class RecoveryManager:
    def __init__(self, parent, db, logger, session_manager, navigate_callback=None):
        self.parent = parent; self.db = db; self.logger = logger
        self.session = session_manager; self.navigate = navigate_callback
        self.frame = tk.Frame(parent, bg='#1a1a2e')
        self.auto_save_active = True
        self._start_auto_save()

    def _start_auto_save(self):
        """Auto-save every 5 minutes and clean old points"""
        def auto_saver():
            while self.auto_save_active:
                time.sleep(300)  # 5 minutes
                if self.auto_save_active:
                    self._auto_save_point()
                    self._clean_old_points()
        threading.Thread(target=auto_saver, daemon=True).start()

    def _auto_save_point(self):
        """Auto-save current state"""
        try:
            self.session.create_recovery_point("auto")
        except: pass

    def _clean_old_points(self):
        """Delete recovery points older than 48 hours"""
        try:
            points = self.session.data.get("recovery_points", [])
            cutoff = time.time() - 172800  # 48 hours
            self.session.data["recovery_points"] = [p for p in points if p.get("time", 0) > cutoff]
            self.session._save()
        except: pass

    def build(self):
        self.frame.pack(fill='both', expand=True, padx=10, pady=10)
        tk.Label(self.frame, text="Session Recovery", font=('Courier',16,'bold'), fg='#ffaa00', bg='#1a1a2e').pack(anchor='w')
        tk.Label(self.frame, text="Auto-saves every 5 min | Deletes after 48 hours", font=('Courier',9), fg='#888', bg='#1a1a2e').pack(anchor='w', pady=5)
        
        # Current session
        cf = tk.LabelFrame(self.frame, text=" Current Session ", font=('Courier',10,'bold'), fg='#00ff88', bg='#16213e', padx=10, pady=8)
        cf.pack(fill='x', pady=5)
        last_mod = self.session.get_last_module() or "dashboard"
        last_proj = self.session.get_last_project()
        theme = self.session.get_theme()
        
        info_frame = tk.Frame(cf, bg='#16213e'); info_frame.pack(fill='x')
        tk.Label(info_frame, text=f"Module: {last_mod}", font=('Courier',9), fg='#00ccff', bg='#16213e').pack(anchor='w')
        tk.Label(info_frame, text=f"Project: {last_proj.get('name','None') if last_proj else 'None'}", font=('Courier',9), fg='#00ccff', bg='#16213e').pack(anchor='w')
        tk.Label(info_frame, text=f"Theme: {theme}", font=('Courier',9), fg='#00ccff', bg='#16213e').pack(anchor='w')
        tk.Label(info_frame, text=f"Auto-Save: {'ON' if self.auto_save_active else 'OFF'}", font=('Courier',9), fg='#3fb950' if self.auto_save_active else '#cc0000', bg='#16213e').pack(anchor='w')
        
        bf = tk.Frame(cf, bg='#16213e'); bf.pack(fill='x', pady=5)
        tk.Button(bf, text="Save Now", font=('Courier',9,'bold'), fg='#000', bg='#00ff88', relief='raised', padx=15, pady=6,
                command=self._manual_save).pack(side='left', padx=3)
        tk.Button(bf, text="Toggle Auto-Save", font=('Courier',9), fg='#000', bg='#ffaa00', relief='raised', padx=10, pady=6,
                command=self._toggle_auto).pack(side='left', padx=3)
        tk.Button(bf, text="Clean Old (>48h)", font=('Courier',9), fg='#fff', bg='#cc0000', relief='raised', padx=10, pady=6,
                command=self._clean_now).pack(side='left', padx=3)
        
        # Statistics
        sf = tk.LabelFrame(self.frame, text=" Statistics ", font=('Courier',10,'bold'), fg='#00ccff', bg='#16213e', padx=10, pady=8)
        sf.pack(fill='x', pady=5)
        points = self.session.get_recovery_points()
        auto_count = sum(1 for p in points if p.get('name') == 'auto')
        manual_count = sum(1 for p in points if p.get('name') == 'manual')
        shutdown_count = sum(1 for p in points if p.get('name') == 'shutdown')
        major_count = sum(1 for p in points if p.get('name') == 'major')
        
        stat_row = tk.Frame(sf, bg='#16213e'); stat_row.pack(fill='x')
        tk.Label(stat_row, text=f"Auto: {auto_count}", font=('Courier',9), fg='#3fb950', bg='#16213e').pack(side='left', padx=10)
        tk.Label(stat_row, text=f"Manual: {manual_count}", font=('Courier',9), fg='#ffaa00', bg='#16213e').pack(side='left', padx=10)
        tk.Label(stat_row, text=f"Shutdown: {shutdown_count}", font=('Courier',9), fg='#ff4444', bg='#16213e').pack(side='left', padx=10)
        tk.Label(stat_row, text=f"Major: {major_count}", font=('Courier',9), fg='#bc8cff', bg='#16213e').pack(side='left', padx=10)
        
        # Recovery points list
        rf = tk.LabelFrame(self.frame, text=" Recovery Points ", font=('Courier',10,'bold'), fg='#ffaa00', bg='#16213e', padx=10, pady=8)
        rf.pack(fill='both', expand=True, pady=5)
        
        if not points:
            tk.Label(rf, text="No recovery points yet\nAuto-saves every 5 minutes", font=('Courier',9), fg='#888', bg='#16213e').pack(pady=20)
        else:
            for i, point in enumerate(reversed(points)):
                card = tk.Frame(rf, bg='#16213e', padx=10, pady=6); card.pack(fill='x', pady=2)
                h = tk.Frame(card, bg='#16213e'); h.pack(fill='x')
                
                pt_name = point.get('name','auto')
                pt_time = datetime.fromtimestamp(point.get('time',0))
                time_ago = datetime.now() - pt_time
                hours_ago = int(time_ago.total_seconds() / 3600)
                
                name_colors = {'auto':'#3fb950','manual':'#ffaa00','shutdown':'#ff4444','major':'#bc8cff'}
                color = name_colors.get(pt_name, '#888')
                
                tk.Label(h, text=f"{pt_name.upper()} - {pt_time.strftime('%m/%d %H:%M')} ({hours_ago}h ago)", 
                        font=('Courier',9,'bold'), fg=color, bg='#16213e').pack(side='left')
                tk.Label(h, text=f"Module: {point.get('module','?')}", font=('Courier',8), fg='#888', bg='#16213e').pack(side='right')
                
                proj = point.get('project',{})
                if proj:
                    tk.Label(card, text=f"Project: {proj.get('name','?')}", font=('Courier',8), fg='#888', bg='#16213e').pack(anchor='w')
                
                bf2 = tk.Frame(card, bg='#16213e'); bf2.pack(fill='x')
                actual_idx = len(points) - 1 - i
                tk.Button(bf2, text="Restore", font=('Courier',8), fg='#000', bg='#ffaa00', relief='flat', padx=8,
                        command=lambda idx=actual_idx: self._restore(idx)).pack(side='left', padx=1)
                tk.Button(bf2, text="Delete", font=('Courier',8), fg='#fff', bg='#cc0000', relief='flat', padx=8,
                        command=lambda idx=actual_idx: self._delete(idx)).pack(side='left', padx=1)

    def _manual_save(self):
        self.session.create_recovery_point("manual")
        self.session.create_recovery_point("major")  # Also save as major
        self._refresh()

    def _toggle_auto(self):
        self.auto_save_active = not self.auto_save_active
        self._refresh()

    def _clean_now(self):
        self._clean_old_points()
        self._refresh()

    def _restore(self, index):
        if self.session.restore_recovery_point(index):
            messagebox.showinfo("Restored", "Session restored! Navigating...")
            if self.navigate:
                self.navigate(self.session.get_last_module() or "dashboard")

    def _delete(self, index):
        points = self.session.get_recovery_points()
        if 0 <= index < len(points):
            points.pop(index)
            self.session.data["recovery_points"] = points
            self.session._save()
            self._refresh()

    def _refresh(self):
        for w in self.frame.winfo_children(): w.destroy()
        self.build()
