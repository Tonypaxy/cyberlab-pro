
import tkinter as tk
from tkinter import ttk, messagebox
import os, subprocess, threading
from gui.base_module import BaseModule
from gui.dropdown import Dropdown

class DoSModule(BaseModule):
    def __init__(self, parent, db, logger, detector):
        super().__init__(parent)
        self.db = db
        self.logger = logger
        self.detector = detector
        self.running = []

    def build_content(self):
        self.add_title("DoS Testing", "Stress testing and denial of service tools - USE ONLY WITH PERMISSION")
        tk.Label(self.inner, text="WARNING: Use only on systems you own or have written permission to test!",
                font=("Courier",9,"bold"), fg="#ff0000", bg="#1a1a2e").pack(pady=5)
        
        tk.Label(self.inner, text="Target:", font=("Courier",10), fg="#fff", bg="#1a1a2e").pack(anchor="w", padx=10)
        self.target_entry = tk.Entry(self.inner, font=("Courier",11), bg="#0f3460", fg="#fff", relief="flat")
        self.target_entry.pack(fill="x", padx=10, pady=3)
        self.target_entry.insert(0, "127.0.0.1")
        
        tk.Label(self.inner, text="Port:", font=("Courier",10), fg="#fff", bg="#1a1a2e").pack(anchor="w", padx=10)
        self.port_entry = tk.Entry(self.inner, font=("Courier",10), bg="#0f3460", fg="#fff", relief="flat", width=10)
        self.port_entry.pack(fill="x", padx=10, pady=3)
        self.port_entry.insert(0, "80")
        
        tools = self.detector.detected.get("dos", [])
        if not tools:
            tools = [{"name":"hping3","command":"hping3"},{"name":"slowloris","command":"slowloris"},{"name":"ab","command":"ab"}]
        
        for tool in tools:
            def make_content(parent, t=tool):
                args = self._get_args(t["name"])
                for arg, desc in args:
                    card = tk.Frame(parent, bg="#16213e", padx=10, pady=6)
                    card.pack(fill="x", pady=1)
                    h = tk.Frame(card, bg="#16213e")
                    h.pack(fill="x")
                    tk.Label(h, text=arg[:30], font=("Courier",9,"bold"), fg="#ff4444", bg="#16213e").pack(side="left")
                    tk.Label(h, text=desc[:30], font=("Courier",8), fg="#888", bg="#16213e").pack(side="left", padx=5)
                    tk.Button(h, text="Run", font=("Courier",7), fg="#000", bg="#ff0000", relief="flat", padx=6,
                            command=lambda a=arg: self._run(t["command"] + " " + a)).pack(side="right", padx=1)
                    tk.Button(h, text="Stop All", font=("Courier",7), fg="#fff", bg="#cc0000", relief="flat", padx=6,
                            command=self._stop_all).pack(side="right", padx=1)
            self.add_section(tool["name"], make_content, "boom")
        
        tk.Button(self.inner, text="STOP ALL ATTACKS", font=("Courier",10,"bold"), fg="#fff", bg="#cc0000",
                relief="raised", padx=15, pady=8, command=self._stop_all).pack(pady=10)
        
        self.output = tk.Text(self.inner, font=("Courier",9), bg="#0a0a0a", fg="#ff4444", relief="flat", height=10)
        self.output.pack(fill="both", expand=True, padx=10, pady=5)
        self.status = self.add_status("Ready - Enter target and port")

    def _get_args(self, name):
        db = {
            "hping3": [("-S target -p 80 --flood","SYN flood"),("-S target -p 443 --flood","HTTPS flood"),("--udp target -p 53 --flood","UDP flood"),("-1 target --flood","ICMP flood"),("-S target -p 80 --rand-source","Random source")],
            "slowloris": [("-p 80 target","HTTP slow"),("-p 443 target --https","HTTPS slow"),("-s 500","500 sockets"),("--sleeptime 10","Sleep 10s")],
            "goldeneye": [("target -w 100 -s 200","100 workers"),("target -w 500","500 workers"),("-m random","Random method")],
            "ab": [("-n 1000 -c 10 http://target/","1000 requests"),("-n 10000 -c 100 http://target/","10K requests"),("-t 30 -c 10 http://target/","30s test")],
            "siege": [("-c 100 -t 30s http://target","100 users"),("-c 200 -r 50 http://target","200 users"),("-f urls.txt","URL file")],
        }
        return db.get(name, [("--help","Show help")])

    def _run(self, cmd):
        target = self.target_entry.get().strip()
        port = self.port_entry.get().strip()
        cmd = cmd.replace("target", target).replace("{target}", target).replace("{PORT}", port)
        self.output.insert("end", "\n$ " + cmd + "\n" + "="*40 + "\n")
        self.output.see("end")
        self.status.config(text="Running...")
        def do():
            try:
                p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                self.running.append(p)
                for line in p.stdout:
                    self.output.insert("end", line); self.output.see("end")
                p.wait()
                if p in self.running: self.running.remove(p)
                self.output.insert("end", "\n[Exit: " + str(p.returncode) + "]\n")
            except Exception as e:
                self.output.insert("end", "\n[X] " + str(e) + "\n")
        threading.Thread(target=do, daemon=True).start()

    def _stop_all(self):
        for p in self.running:
            try: p.kill()
            except: pass
        self.running.clear()
        self.output.insert("end", "\n[ALL STOPPED]\n")
        self.status.config(text="Stopped")
