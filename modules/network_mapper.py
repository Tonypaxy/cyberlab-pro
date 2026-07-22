import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import os, json, subprocess, threading, re
from gui.base_module import BaseModule

class NetworkMapper(BaseModule):
    def __init__(self, parent, db, logger):
        super().__init__(parent)
        self.db = db
        self.logger = logger
        self.current_project = None
        self.hosts = []
    
    def build_content(self):
        self.add_title("Network Mapper", "Visual network topology and host discovery")
        projects = self.db.get_all_projects()
        names = [p["name"] for p in projects]
        if names:
            pf = tk.Frame(self.inner, bg="#16213e", padx=10, pady=8)
            pf.pack(fill="x", padx=10, pady=5)
            tk.Label(pf, text="Project:", font=("Courier",10), fg="#fff", bg="#16213e").pack(side="left")
            self.project_var = tk.StringVar(value=names[0])
            ttk.Combobox(pf, textvariable=self.project_var, values=names, font=("Courier",10), state="readonly", width=25).pack(side="left", padx=10)
            self._set_project(names[0])
        sf = tk.Frame(self.inner, bg="#16213e", padx=10, pady=8)
        sf.pack(fill="x", padx=10, pady=5)
        tk.Label(sf, text="Target Network:", font=("Courier",10), fg="#fff", bg="#16213e").pack(anchor="w")
        self.target_entry = tk.Entry(sf, font=("Courier",11), bg="#0f3460", fg="#fff", relief="flat")
        self.target_entry.pack(fill="x", pady=3)
        self.target_entry.insert(0, "192.168.1.0/24")
        bf = tk.Frame(sf, bg="#16213e")
        bf.pack(fill="x", pady=5)
        tk.Button(bf, text="Ping Sweep", font=("Courier",9), fg="#000", bg="#00ccff", relief="flat", padx=10, command=self._ping_sweep).pack(side="left", padx=2)
        tk.Button(bf, text="Nmap Discovery", font=("Courier",9), fg="#000", bg="#00ff88", relief="flat", padx=10, command=self._nmap_discover).pack(side="left", padx=2)
        tk.Button(bf, text="ARP Scan", font=("Courier",9), fg="#000", bg="#ffaa00", relief="flat", padx=10, command=self._arp_scan).pack(side="left", padx=2)
        self.map_frame = tk.Frame(self.inner, bg="#1a1a2e")
        self.map_frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.status_label = self.add_status("Enter target network and scan")
    
    def _set_project(self, name):
        for p in self.db.get_all_projects():
            if p["name"] == name: self.current_project = p; break
    
    def _ping_sweep(self):
        target = self.target_entry.get().strip()
        if not target: return
        self.status_label.config(text="Ping sweeping " + target + "...")
        def do():
            hosts = []
            if "/" in target:
                base = ".".join(target.split("/")[0].split(".")[:3])
                for i in range(1, 255):
                    ip = base + "." + str(i)
                    try:
                        r = subprocess.run(["ping","-c","1","-W","1",ip], capture_output=True, timeout=2)
                        if r.returncode == 0:
                            hosts.append({"ip":ip,"status":"up","method":"ping"})
                    except: pass
            else:
                try:
                    r = subprocess.run(["ping","-c","1","-W","1",target], capture_output=True, timeout=2)
                    if r.returncode == 0: hosts.append({"ip":target,"status":"up","method":"ping"})
                except: pass
            self.hosts = hosts
            self.frame.after(0, self._render_map)
        threading.Thread(target=do, daemon=True).start()
    
    def _nmap_discover(self):
        target = self.target_entry.get().strip()
        if not target: return
        self.status_label.config(text="Nmap discovering " + target + "...")
        def do():
            try:
                r = subprocess.run(["nmap","-sn",target,"-oG","-"], capture_output=True, text=True, timeout=60)
                hosts = []
                for line in r.stdout.split("\n"):
                    if "Status: Up" in line:
                        ip = line.split()[1] if len(line.split()) > 1 else "unknown"
                        hosts.append({"ip":ip,"status":"up","method":"nmap"})
                self.hosts = hosts
                self.frame.after(0, self._render_map)
            except Exception as e:
                self.frame.after(0, lambda: self.status_label.config(text="Error: " + str(e)))
        threading.Thread(target=do, daemon=True).start()
    
    def _arp_scan(self):
        self.status_label.config(text="ARP scanning...")
        def do():
            try:
                r = subprocess.run(["arp-scan","-l"], capture_output=True, text=True, timeout=30)
                hosts = []
                for line in r.stdout.split("\n"):
                    parts = line.split()
                    if len(parts) >= 2 and re.match(r"\d+\.\d+\.\d+\.\d+", parts[0]):
                        hosts.append({"ip":parts[0],"mac":parts[1] if len(parts)>1 else "?","method":"arp"})
                self.hosts = hosts
                self.frame.after(0, self._render_map)
            except:
                self.frame.after(0, lambda: self.status_label.config(text="arp-scan not installed"))
        threading.Thread(target=do, daemon=True).start()
    
    def _render_map(self):
        for w in self.map_frame.winfo_children(): w.destroy()
        if not self.hosts:
            tk.Label(self.map_frame, text="No hosts discovered", font=("Courier",10), fg="#888", bg="#1a1a2e").pack(pady=20)
            return
        self.status_label.config(text="Found " + str(len(self.hosts)) + " hosts")
        tk.Label(self.map_frame, text="Network Map (" + str(len(self.hosts)) + " hosts)", font=("Courier",11,"bold"), fg="#00ff88", bg="#1a1a2e").pack(anchor="w")
        gw = tk.Frame(self.map_frame, bg="#16213e", padx=15, pady=10)
        gw.pack(fill="x", pady=5)
        tk.Label(gw, text="[ GATEWAY ]", font=("Courier",10,"bold"), fg="#ffaa00", bg="#16213e").pack()
        tk.Label(gw, text="Your Network", font=("Courier",8), fg="#888", bg="#16213e").pack()
        line = tk.Frame(self.map_frame, bg="#00ff88", height=2)
        line.pack(fill="x")
        hf = tk.Frame(self.map_frame, bg="#1a1a2e")
        hf.pack(fill="x", pady=5)
        row = tk.Frame(hf, bg="#1a1a2e")
        row.pack(fill="x")
        for i, host in enumerate(self.hosts):
            if i > 0 and i % 5 == 0:
                row = tk.Frame(hf, bg="#1a1a2e")
                row.pack(fill="x")
            card = tk.Frame(row, bg="#16213e", padx=8, pady=6)
            card.pack(side="left", padx=3, pady=3)
            sc = "#3fb950" if host.get("status") == "up" else "#f85149"
            tk.Label(card, text=host.get("ip","?"), font=("Courier",9,"bold"), fg=sc, bg="#16213e").pack()
            if host.get("mac"): tk.Label(card, text=host["mac"][:17], font=("Courier",7), fg="#888", bg="#16213e").pack()
            tk.Label(card, text=host.get("method",""), font=("Courier",6), fg="#666", bg="#16213e").pack()
            tk.Button(card, text="Scan", font=("Courier",7), fg="#000", bg="#00ccff", relief="flat", padx=4, command=lambda h=host: self._scan_host(h)).pack(pady=2)
    
    def _scan_host(self, host):
        ip = host.get("ip","")
        if not ip: return
        self.status_label.config(text="Scanning " + ip + "...")
        def do():
            try:
                r = subprocess.run(["nmap","-sV","-F",ip], capture_output=True, text=True, timeout=60)
                host["scan"] = r.stdout
                self.frame.after(0, lambda: self._show_scan(host))
            except Exception as e:
                self.frame.after(0, lambda: messagebox.showerror("Error",str(e)))
        threading.Thread(target=do, daemon=True).start()
    
    def _show_scan(self, host):
        d = tk.Toplevel(self.frame, bg="#1a1a2e")
        d.title(host.get("ip","Host")); d.geometry("600x400")
        tk.Label(d, text="Scan: " + host.get("ip",""), font=("Courier",12,"bold"), fg="#00ff88", bg="#1a1a2e").pack(pady=10)
        t = tk.Text(d, font=("Courier",9), bg="#0a0a0a", fg="#00ff88", relief="flat")
        t.pack(fill="both", expand=True, padx=10, pady=10)
        t.insert("1.0", host.get("scan","No data"))
        t.config(state="disabled")
        tk.Button(d, text="Close", font=("Courier",10), fg="#fff", bg="#666", relief="raised", padx=15, pady=5, command=d.destroy).pack(pady=5)
