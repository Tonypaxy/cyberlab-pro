import tkinter as tk
from tkinter import ttk
import os, time, threading
from gui.base_module import BaseModule

class ResourceMonitor(BaseModule):
    def __init__(self, parent, db, logger, resource_manager=None):
        super().__init__(parent)
        self.db = db; self.logger = logger
        self.rm = resource_manager
        self.monitoring = True

    def build_content(self):
        self.add_title("Resource Monitor", "Task queue, memory, CPU, active scans")
        
        # Limits control
        lf = tk.Frame(self.inner, bg="#16213e", padx=10, pady=8)
        lf.pack(fill="x", padx=10, pady=5)
        tk.Label(lf, text="Max Concurrent Tasks:", font=("Courier",9), fg="#fff", bg="#16213e").pack(side="left")
        self.concurrent_var = tk.IntVar(value=3)
        tk.Spinbox(lf, from_=1, to=20, textvariable=self.concurrent_var, width=5, font=("Courier",9),
                bg="#0f3460", fg="#fff").pack(side="left", padx=5)
        tk.Button(lf, text="Apply", font=("Courier",8), fg="#000", bg="#00ff88", relief="flat", padx=8,
                command=self._apply_limits).pack(side="left", padx=5)
        
        tk.Label(lf, text="Memory Limit (MB):", font=("Courier",9), fg="#fff", bg="#16213e").pack(side="left", padx=10)
        self.memory_var = tk.IntVar(value=500)
        tk.Spinbox(lf, from_=100, to=4000, textvariable=self.memory_var, width=5, font=("Courier",9),
                bg="#0f3460", fg="#fff").pack(side="left", padx=5)
        
        # Stats cards
        self.stats_frame = tk.Frame(self.inner, bg="#1a1a2e")
        self.stats_frame.pack(fill="x", padx=10, pady=5)
        self._create_cards()
        
        # Active tasks
        self.tasks_frame = tk.Frame(self.inner, bg="#1a1a2e")
        self.tasks_frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.status = self.add_status("Monitoring system resources")
        
        self._update_loop()

    def _create_cards(self):
        for w in self.stats_frame.winfo_children(): w.destroy()
        cards = [
            ("CPU", self._get_cpu(), "#00ff88"),
            ("Memory", f"{self._get_mem()}MB", "#00ccff"),
            ("Active Tasks", str(self.rm.get_active_count() if self.rm else 0), "#ffaa00"),
            ("Queue", str(self.rm.get_queue_size() if self.rm else 0), "#cc88ff"),
        ]
        for name, value, color in cards:
            card = tk.Frame(self.stats_frame, bg="#16213e", padx=12, pady=8)
            card.pack(side="left", fill="x", expand=True, padx=3)
            tk.Label(card, text=name, font=("Courier",8), fg="#888", bg="#16213e").pack()
            tk.Label(card, text=str(value), font=("Courier",14,"bold"), fg=color, bg="#16213e").pack()

    def _get_cpu(self):
        try:
            with open("/proc/stat") as f:
                return str(int(f.readline().split()[1]) % 100) + "%"
        except: return "?"

    def _get_mem(self):
        try:
            with open("/proc/self/status") as f:
                for line in f:
                    if "VmRSS" in line: return int(line.split()[1]) // 1024
        except: pass
        return 0

    def _apply_limits(self):
        if self.rm:
            self.rm.set_limits(self.concurrent_var.get(), self.memory_var.get())
            self.status.config(text="Limits applied")

    def _update_loop(self):
        if self.monitoring:
            self._create_cards()
            # Show active tasks
            if self.rm:
                for w in self.tasks_frame.winfo_children(): w.destroy()
                for tid, info in list(self.rm.active_tasks.items())[-10:]:
                    status_color = {"running":"#ffaa00","completed":"#00ff88","failed":"#ff4444","cancelled":"#888"}
                    color = status_color.get(info.get("status",""), "#888")
                    tk.Label(self.tasks_frame, text=f"{tid[:10]}... {info['status']}",
                            font=("Courier",8), fg=color, bg="#1a1a2e").pack(anchor="w")
            self.frame.after(3000, self._update_loop)
