import tkinter as tk
from tkinter import ttk, messagebox
import subprocess, threading, re, socket, os, shutil
from datetime import datetime
from gui.base_module import BaseModule

class PortScanner(BaseModule):
    def __init__(self, parent, db, logger):
        super().__init__(parent)
        self.db = db
        self.logger = logger
        self.results = []
        self.scanning = False

    def build_content(self):
        self.add_title("Port Scanner", "Fast port scanning with nmap, masscan, rustscan")
        
        tk.Label(self.inner, text="Target IP or Range:", font=("Courier",10), fg="#fff", bg="#1a1a2e").pack(anchor="w", padx=10)
        self.target_entry = tk.Entry(self.inner, font=("Courier",11), bg="#0f3460", fg="#fff", relief="flat")
        self.target_entry.pack(fill="x", padx=10, pady=3)
        self.target_entry.insert(0, "192.168.1.1")
        
        pf = tk.Frame(self.inner, bg="#1a1a2e"); pf.pack(fill="x", padx=10, pady=5)
        tk.Label(pf, text="Ports:", font=("Courier",9), fg="#888", bg="#1a1a2e").pack(side="left")
        self.port_entry = tk.Entry(pf, font=("Courier",9), bg="#0f3460", fg="#fff", relief="flat", width=20)
        self.port_entry.pack(side="left", padx=5)
        self.port_entry.insert(0, "1-1000")
        
        presets = [("Top 100","1-100"),("Top 1000","1-1000"),("All","1-65535"),("Web","80,443,8080,8443"),("Database","1433,3306,5432,27017,6379"),("Windows","135,139,445,3389,5985")]
        for t,p in presets:
            tk.Button(pf, text=t, font=("Courier",7), fg="#000", bg="#16213e", relief="flat", padx=4,
                    command=lambda v=p: self.port_entry.delete(0,"end") or self.port_entry.insert(0,v)).pack(side="left", padx=1)
        
        bf = tk.Frame(self.inner, bg="#1a1a2e"); bf.pack(fill="x", padx=10, pady=5)
        # Auto-detect available scanners and their best args
        self.scanners = self._detect_scanners()
        for name, tool, args, color in self.scanners:
            tk.Button(bf, text=name, font=("Courier",8), fg="#000", bg=color, relief="flat", padx=6,
                    command=lambda t=tool,a=args: self._scan(t,a)).pack(side="left", padx=2)
        
        tk.Button(bf, text="STOP", font=("Courier",8,"bold"), fg="#fff", bg="#cc0000", relief="flat", padx=6,
                command=self._stop).pack(side="right", padx=2)
        tk.Button(bf, text="Export", font=("Courier",8), fg="#000", bg="#00ff88", relief="flat", padx=6,
                command=self._export).pack(side="right", padx=2)
        
        self.progress = ttk.Progressbar(self.inner, mode="indeterminate", length=300)
        
        self.results_frame = tk.Frame(self.inner, bg="#1a1a2e")
        self.results_frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.status = self.add_status("Ready - Enter target and choose scan type")

    def _detect_scanners(self):
        """Auto-detect all installed port scanners and return best configs"""
        import shutil
        scanners = []
        
        # Nmap variants
        if shutil.which("nmap"):
            scanners.append(("Nmap Fast","nmap","-F -T4","#00ccff"))
            scanners.append(("Nmap Full","nmap","-p- -T4 --open","#00ccff"))
            scanners.append(("Nmap Service","nmap","-sV -T4 --open","#00ccff"))
            scanners.append(("Nmap Scripts","nmap","-sC -sV -T4","#00ccff"))
        
        # Masscan
        if shutil.which("masscan"):
            scanners.append(("Masscan Fast","masscan","--rate=1000","#ffaa00"))
            scanners.append(("Masscan Full","masscan","--rate=5000 -p1-65535","#ffaa00"))
        
        # Rustscan
        if shutil.which("rustscan"):
            scanners.append(("Rustscan","rustscan","-t 2000","#cc88ff"))
        
        # Naabu (ProjectDiscovery)
        if shutil.which("naabu"):
            scanners.append(("Naabu Fast","naabu","-top-ports 100","#00ff88"))
            scanners.append(("Naabu Full","naabu","-p -","#00ff88"))
        
        # Zmap
        if shutil.which("zmap"):
            scanners.append(("Zmap TCP","zmap","-p 443","#ff4444"))
        
        # MassDNS
        if shutil.which("massdns"):
            scanners.append(("MassDNS","massdns","-r resolvers.txt","#bc8cff"))
        
        # Unicornscan
        if shutil.which("unicornscan"):
            scanners.append(("Unicornscan","unicornscan","-Iv","#ff00ff"))
        
        # Sx (Fast Port Scanner)
        if shutil.which("sx"):
            scanners.append(("SX Fast","sx","scan tcp --top-ports 100","#00ffff"))
        
        # ScanCannon
        if shutil.which("scancannon"):
            scanners.append(("ScanCannon","scancannon","","#ff8800"))
        
        # Ping (always available)
        scanners.append(("Ping Sweep","ping","-c 1 -W 1","#888888"))
        
        # Any future scanner in PATH with --help containing "scan" or "port"
        import subprocess
        for cmd in ["nmap","masscan","rustscan","naabu","zmap","sx","unicornscan","scancannon","massdns"]:
            pass  # Already handled above
        
        # Discover unknown scanners
        for path in os.environ.get("PATH","").split(":"):
            try:
                for f in os.listdir(path):
                    fpath = os.path.join(path,f)
                    if os.access(fpath, os.X_OK) and f not in [s[1] for s in scanners]:
                        try:
                            r = subprocess.run([f,"--help"], capture_output=True, text=True, timeout=3)
                            help_text = r.stdout + r.stderr
                            if any(kw in help_text.lower() for kw in ["port","scan","packet","tcp","udp","syn"]):
                                if f not in ["nmap","masscan","rustscan","naabu","zmap","sx","unicornscan","scancannon","massdns","ping"]:
                                    scanners.append((f" {f.title()}","{f}","","#666666"))
                        except: pass
            except: pass
        
        return scanners

    def _scan(self, tool, args):
        target = self.target_entry.get().strip()
        ports = self.port_entry.get().strip()
        if not target: return
        
        self.scanning = True
        self.results = []
        for w in self.results_frame.winfo_children(): w.destroy()
        
        if tool == "masscan":
            cmd = f"masscan {target} -p{ports} {args} -oJ /tmp/masscan.json 2>/dev/null"
        elif tool == "rustscan":
            cmd = f"rustscan -a {target} -p {ports} {args} 2>/dev/null"
        elif tool == "ping":
            cmd = f"ping -c 1 -W 1 {target} 2>/dev/null"
        else:
            cmd = f"{tool} {target} -p {ports} {args} 2>/dev/null"
        
        self.status.config(text=f"Scanning: {cmd[:60]}...")
        self.progress.pack(fill="x", padx=10, pady=3)
        self.progress.start(10)
        
        def do():
            try:
                p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                output = ""
                for line in p.stdout:
                    if not self.scanning: p.kill(); break
                    output += line
                p.wait()
                
                self.frame.after(0, lambda: self.progress.stop())
                self.frame.after(0, lambda: self.progress.pack_forget())
                
                if tool == "masscan":
                    import json
                    try:
                        with open("/tmp/masscan.json") as f:
                            data = json.load(f)
                            for item in data:
                                for port_info in item.get("ports",[]):
                                    self.results.append({
                                        "ip": item.get("ip","?"),
                                        "port": port_info.get("port","?"),
                                        "proto": port_info.get("proto","?"),
                                        "service": port_info.get("service",{}).get("name","?")
                                    })
                    except: pass
                else:
                    for line in output.split("\n"):
                        if "/tcp" in line or "/udp" in line and "open" in line.lower():
                            parts = line.split()
                            if len(parts) >= 3:
                                self.results.append({"port": parts[0], "state": parts[1], "service": parts[2] if len(parts)>2 else "?"})
                
                self.frame.after(0, self._show_results)
                self.frame.after(0, lambda: self.status.config(text=f"Found {len(self.results)} open ports"))
            except Exception as e:
                self.frame.after(0, lambda: self.status.config(text=f"Error: {str(e)[:50]}"))
            self.scanning = False
        threading.Thread(target=do, daemon=True).start()

    def _show_results(self):
        for w in self.results_frame.winfo_children(): w.destroy()
        if not self.results:
            tk.Label(self.results_frame, text="No open ports found", font=("Courier",10), fg="#888", bg="#1a1a2e").pack(pady=20)
            return
        
        tk.Label(self.results_frame, text=f"Open Ports ({len(self.results)})", font=("Courier",11,"bold"), fg="#00ff88", bg="#1a1a2e").pack(anchor="w")
        
        t = tk.Text(self.results_frame, font=("Courier",9), bg="#0a0a0a", fg="#00ff88", relief="flat", height=15)
        t.pack(fill="both", expand=True, pady=5)
        
        t.insert("end", f"{'PORT':<12} {'STATE':<10} {'SERVICE':<15} {'IP':<15}\n")
        t.insert("end", "="*55 + "\n")
        
        for r in self.results:
            port = str(r.get("port","?"))
            state = r.get("state","open")
            service = str(r.get("service","?"))[:15]
            ip = str(r.get("ip",""))[:15]
            t.insert("end", f"{port:<12} {state:<10} {service:<15} {ip:<15}\n")

    def _stop(self):
        self.scanning = False
        self.progress.stop()
        self.progress.pack_forget()
        self.status.config(text="Stopped")

    def _export(self):
        if not self.results: return
        path = os.path.expanduser(f"~/portscan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
        with open(path, "w") as f:
            f.write(f"Port Scan Results\n{'='*50}\n")
            f.write(f"Target: {self.target_entry.get()}\n")
            f.write(f"Time: {datetime.now()}\n\n")
            for r in self.results:
                f.write(f"{str(r.get('port','?')):<10} {r.get('state','open'):<10} {str(r.get('service','?')):<20}\n")
        messagebox.showinfo("Exported", f"Saved to {path}")

import os
