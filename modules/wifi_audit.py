import tkinter as tk
from tkinter import ttk, messagebox
import os, subprocess, threading
from gui.base_module import BaseModule

class WiFiAudit(BaseModule):
    def __init__(self, parent, db, logger):
        super().__init__(parent)
        self.db = db
        self.logger = logger
        self.monitor_process = None

    def build_content(self):
        self.add_title("WiFi Audit", "Monitor mode, handshake capture, WPA cracking")
        tk.Label(self.inner, text="WARNING: Only audit networks you own or have permission to test!",
                font=("Courier",9,"bold"), fg="#ff0000", bg="#1a1a2e").pack(pady=5)
        tk.Label(self.inner, text="Interface:", font=("Courier",10), fg="#fff", bg="#1a1a2e").pack(anchor="w", padx=10)
        self.iface_entry = tk.Entry(self.inner, font=("Courier",10), bg="#0f3460", fg="#fff", relief="flat")
        self.iface_entry.pack(fill="x", padx=10, pady=3)
        self.iface_entry.insert(0, "wlan0")
        bf = tk.Frame(self.inner, bg="#1a1a2e"); bf.pack(fill="x", padx=10, pady=5)
        for t,c in [("Scan",self._scan),("Monitor On",self._mon_on),("Monitor Off",self._mon_off),
                    ("Capture",self._capture),("Deauth",self._deauth),("Crack WPA",self._crack),("Stop",self._stop)]:
            tk.Button(bf, text=t, font=("Courier",8), fg="#000", bg="#00ccff", relief="flat", padx=6, command=c).pack(side="left", padx=2)
        self.output = tk.Text(self.inner, font=("Courier",9), bg="#0a0a0a", fg="#00ff88", relief="flat", height=12)
        self.output.pack(fill="both", expand=True, padx=10, pady=5)
        self.status = self.add_status("Ready")

    def _iface(self): return self.iface_entry.get().strip()

    def _run(self, cmd):
        self.status.config(text="Running...")
        def do():
            try:
                p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                self.monitor_process = p
                for line in p.stdout:
                    self.output.insert("end", line); self.output.see("end")
                p.wait()
                self.status.config(text="Done")
            except Exception as e:
                self.output.insert("end", "[X] " + str(e) + "\n")
        threading.Thread(target=do, daemon=True).start()

    def _scan(self):
        iface = self._iface()
        self.output.insert("end", "\n[*] Scanning...\n")
        self._run("termux-wifi-scaninfo 2>/dev/null || iwlist " + iface + " scan 2>/dev/null | grep -E 'ESSID|Signal|Channel' || nmcli dev wifi list 2>/dev/null")

    def _mon_on(self):
        iface = self._iface()
        self.output.insert("end", "\n[*] Monitor mode on " + iface + "...\n")
        self._run("airmon-ng start " + iface + " 2>/dev/null || iwconfig " + iface + " mode monitor 2>/dev/null")

    def _mon_off(self):
        iface = self._iface()
        self.output.insert("end", "\n[*] Managed mode...\n")
        self._run("airmon-ng stop " + iface + "mon 2>/dev/null || iwconfig " + iface + " mode managed 2>/dev/null")

    def _capture(self):
        iface = self._iface()
        self.output.insert("end", "\n[*] Capturing handshakes...\n")
        self._run("airodump-ng " + iface + "mon -w /tmp/capture 2>/dev/null")

    def _deauth(self):
        iface = self._iface()
        self.output.insert("end", "\n[*] Deauth attack...\n")
        self._run("aireplay-ng --deauth 10 -a 00:11:22:33:44:55 " + iface + "mon 2>/dev/null")

    def _crack(self):
        self.output.insert("end", "\n[*] Cracking WPA...\n")
        self._run("aircrack-ng -w ~/wordlists/rockyou.txt /tmp/capture-01.cap 2>/dev/null")

    def _stop(self):
        if self.monitor_process:
            try: self.monitor_process.kill()
            except: pass
        self.output.insert("end", "\n[STOPPED]\n")
        self.status.config(text="Stopped")
