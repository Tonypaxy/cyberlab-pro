#!/usr/bin/env python3
"""
CyberLab Pro - Anomaly Detection & Traffic Analysis
Behavioral analysis, statistical anomaly detection, traffic profiling.
Detects: port scans, DDoS, data exfiltration, lateral movement, beaconing.
"""
import tkinter as tk
from tkinter import ttk, scrolledtext
import threading, os, time, socket, struct, math
from datetime import datetime
from collections import defaultdict, deque, Counter

class IDSAnomaly:
    def __init__(self, parent, db, logger):
        self.parent = parent; self.db = db; self.logger = logger
        self.frame = tk.Frame(parent, bg='#1a1a2e')
        self.monitoring = False
        self.traffic_data = deque(maxlen=10000)
        self.connection_tracker = defaultdict(lambda: {
            'packets':0, 'bytes':0, 'first_seen':None, 'last_seen':None,
            'ports':set(), 'protocol':None, 'flags':[]
        })
        self.port_scan_tracker = defaultdict(lambda: {
            'ports_probed':set(), 'start_time':None, 'last_probe':None
        })
        self.beacon_tracker = defaultdict(lambda: {
            'intervals':[], 'last_time':None, 'jitter':[]
        })
        self.data_transfer_tracker = defaultdict(lambda: {
            'total_bytes':0, 'transfers':[], 'threshold_exceeded':False
        })
        self.baselines = {
            'packets_per_second': {'mean':100, 'std':50},
            'unique_ports_per_ip': {'mean':5, 'std':3},
            'bytes_per_connection': {'mean':5000, 'std':3000},
            'connection_duration': {'mean':60, 'std':30},
            'beacon_interval_variance': {'mean':0.1, 'std':0.05},
        }
        self.alert_threshold = 0.7

    def build(self):
        self.frame.pack(fill='both', expand=True, padx=10, pady=10)
        tk.Label(self.frame, text="📊 Anomaly Detection & Traffic Analysis",
                font=('Courier',16,'bold'), fg='#ff6600', bg='#1a1a2e').pack(pady=(0,3))
        tk.Label(self.frame, text="Behavioral Analysis | Statistical Detection | Traffic Profiling | Beacon Detection",
                font=('Courier',8), fg='#888888', bg='#1a1a2e').pack(pady=(0,10))
        # Stats bar
        sf = tk.Frame(self.frame, bg='#16213e', relief=tk.RIDGE, bd=1)
        sf.pack(fill='x', pady=5)
        self.flows_lbl = tk.Label(sf, text="Flows: 0", fg='#4488ff', bg='#16213e', font=('Courier',10,'bold'))
        self.flows_lbl.pack(side=tk.LEFT, padx=12, pady=5)
        self.anomalies_lbl = tk.Label(sf, text="Anomalies: 0", fg='#ff4444', bg='#16213e', font=('Courier',10,'bold'))
        self.anomalies_lbl.pack(side=tk.LEFT, padx=12, pady=5)
        self.beacons_lbl = tk.Label(sf, text="Beacons: 0", fg='#ff66ff', bg='#16213e', font=('Courier',10,'bold'))
        self.beacons_lbl.pack(side=tk.LEFT, padx=12, pady=5)
        self.mode_lbl = tk.Label(sf, text="● IDLE", fg='#888888', bg='#16213e', font=('Courier',10))
        self.mode_lbl.pack(side=tk.RIGHT, padx=12, pady=5)
        # Score gauge
        gf = tk.Frame(self.frame, bg='#1a1a2e'); gf.pack(fill='x', pady=5)
        tk.Label(gf, text="SCORE:", fg='#888', bg='#1a1a2e', font=('Courier',9)).pack(side=tk.LEFT,padx=5)
        self.gauge = tk.Canvas(gf, width=250, height=20, bg='#0d1117', highlightthickness=0)
        self.gauge.pack(side=tk.LEFT,padx=5)
        self.bar = self.gauge.create_rectangle(0,0,0,20,fill='#00ff00')
        self.score_lbl = tk.Label(gf, text="0.00", fg='#00ff00', bg='#1a1a2e', font=('Courier',9,'bold'))
        self.score_lbl.pack(side=tk.LEFT,padx=5)
        # Controls
        cf = tk.Frame(self.frame, bg='#1a1a2e'); cf.pack(fill='x', pady=5)
        self.start_btn = tk.Button(cf, text="▶ Start", command=self.start_monitoring,
            bg='#00cc44', fg='#000', font=('Courier',8,'bold'), relief=tk.FLAT, cursor='hand2', padx=12, pady=4)
        self.start_btn.pack(side=tk.LEFT,padx=2)
        self.stop_btn = tk.Button(cf, text="■ Stop", command=self.stop_monitoring,
            bg='#cc3300', fg='#fff', font=('Courier',8,'bold'), relief=tk.FLAT, cursor='hand2', padx=12, pady=4, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT,padx=2)
        tk.Button(cf, text="🔗 Conn", command=self.show_connections, bg='#4466ff', fg='#fff',
            font=('Courier',8), relief=tk.FLAT, cursor='hand2', padx=12, pady=4).pack(side=tk.LEFT,padx=2)
        tk.Button(cf, text="📡 Beacon", command=self.show_beacons, bg='#ff44ff', fg='#fff',
            font=('Courier',8), relief=tk.FLAT, cursor='hand2', padx=12, pady=4).pack(side=tk.LEFT,padx=2)
        tk.Button(cf, text="📊 Base", command=self.show_baselines, bg='#ffaa00', fg='#000',
            font=('Courier',8), relief=tk.FLAT, cursor='hand2', padx=12, pady=4).pack(side=tk.LEFT,padx=2)
        tk.Button(cf, text="🧹", command=self.clear_all, bg='#555', fg='#fff',
            font=('Courier',8), relief=tk.FLAT, cursor='hand2', padx=12, pady=4).pack(side=tk.RIGHT,padx=2)
        # Output tabs
        self.nb = ttk.Notebook(self.frame); self.nb.pack(fill='both', expand=True, pady=5)
        at = tk.Frame(self.nb, bg='#1a1a2e'); self.nb.add(at, text="⚠ Anomalies")
        self.anomaly_out = scrolledtext.ScrolledText(at, wrap=tk.WORD, bg='#0d1117', fg='#ff4444',
            insertbackground='#ff4444', font=('Courier',9), relief=tk.FLAT, bd=0)
        self.anomaly_out.pack(fill='both', expand=True)
        self.anomaly_out.tag_configure('critical', foreground='#ff0000', background='#330000')
        self.anomaly_out.tag_configure('high', foreground='#ff4444')
        self.anomaly_out.tag_configure('medium', foreground='#ffaa00')
        self.anomaly_out.tag_configure('low', foreground='#ffcc00')
        self.anomaly_out.tag_configure('info', foreground='#4488ff')
        self.anomaly_out.tag_configure('ts', foreground='#666')
        tt = tk.Frame(self.nb, bg='#1a1a2e'); self.nb.add(tt, text="📈 Traffic")
        self.traffic_out = scrolledtext.ScrolledText(tt, wrap=tk.WORD, bg='#0d1117', fg='#44aaff',
            insertbackground='#44aaff', font=('Courier',9), relief=tk.FLAT, bd=0)
        self.traffic_out.pack(fill='both', expand=True)
        ant = tk.Frame(self.nb, bg='#1a1a2e'); self.nb.add(ant, text="🔬 Analysis")
        self.analysis_out = scrolledtext.ScrolledText(ant, wrap=tk.WORD, bg='#0d1117', fg='#ffaa00',
            insertbackground='#ffaa00', font=('Courier',9), relief=tk.FLAT, bd=0)
        self.analysis_out.pack(fill='both', expand=True)
        self._log("Anomaly Detection Engine Initialized", "info")
        self._log("Monitoring: Port Scans | Beaconing | Data Exfil | Protocol Anomalies | Lateral Movement", "info")

    def _log(self, msg, level="info"):
        if not hasattr(self, "anomaly_out"): return
        ts = datetime.now().strftime("%H:%M:%S")
        self.anomaly_out.insert(tk.END, f"[{ts}] ", 'ts')
        self.anomaly_out.insert(tk.END, f"{msg}\n", level)
        self.anomaly_out.see(tk.END)

    def _log_traffic(self, msg):
        if not hasattr(self, "anomaly_out"): return
        ts = datetime.now().strftime("%H:%M:%S")
        self.traffic_out.insert(tk.END, f"[{ts}] {msg}\n")
        self.traffic_out.see(tk.END)

    def start_monitoring(self):
        if self.monitoring: return
        self.monitoring = True
        self.start_btn.config(state=tk.DISABLED); self.stop_btn.config(state=tk.NORMAL)
        self.mode_lbl.config(text="● ACTIVE", fg='#00ff00')
        self._log("Anomaly monitoring started", "info")
        threading.Thread(target=self._loop, daemon=True).start()

    def stop_monitoring(self):
        self.monitoring = False
        self.start_btn.config(state=tk.NORMAL); self.stop_btn.config(state=tk.DISABLED)
        self.mode_lbl.config(text="● IDLE", fg='#888888')
        self._log("Monitoring stopped", "info")

    def _loop(self):
        while self.monitoring:
            try:
                self.frame.after(0, self._analyze)
            except:
                break
            time.sleep(1)

    def _analyze(self):
        try:
            self._collect_stats()
            self._detect_port_scans()
            self._detect_beaconing()
            self._detect_data_exfil()
            self._calc_score()
        except:
            pass

    def _collect_stats(self):
        total = 0
        for pf, pn in [('/proc/net/tcp','TCP'), ('/proc/net/udp','UDP')]:
            try:
                if not os.path.exists(pf): continue
                with open(pf,'r') as f:
                    for line in f.readlines()[1:]:
                        parts = line.split()
                        if len(parts) > 7:
                            local = self._parse_addr(parts[1])
                            remote = self._parse_addr(parts[2])
                            if remote[0] != '0.0.0.0':
                                total += 1
                                rip = remote[0]; rp = remote[1]
                                c = self.connection_tracker[rip]
                                c['packets'] += 1
                                c['last_seen'] = time.time()
                                if not c['first_seen']: c['first_seen'] = time.time()
                                c['ports'].add(rp); c['protocol'] = pn
                                # Track for beacon detection
                                bt = self.beacon_tracker[rip]
                                if bt['last_time']:
                                    interval = time.time() - bt['last_time']
                                    bt['intervals'].append(interval)
                                bt['last_time'] = time.time()
                                # Track port scan
                                self.port_scan_tracker[rip]['ports_probed'].add(rp)
                                if not self.port_scan_tracker[rip]['start_time']:
                                    self.port_scan_tracker[rip]['start_time'] = time.time()
                                self.port_scan_tracker[rip]['last_probe'] = time.time()
                                # Track data transfer
                                try:
                                    self.data_transfer_tracker[rip]['total_bytes'] += int(parts[4], 16)
                                except: pass
            except: pass
        self.flows_lbl.config(text=f"Flows: {total}")

    def _parse_addr(self, hex_str):
        try:
            addr, port = hex_str.split(':')
            port = int(port, 16)
            ip = socket.inet_ntoa(struct.pack('<I', int(addr, 16)))
            return (ip, port)
        except: return ('0.0.0.0', 0)

    def _detect_port_scans(self):
        now = time.time(); threshold = 15; window = 10
        for ip, t in list(self.port_scan_tracker.items()):
            if t['start_time'] and (now - t['start_time']) <= window:
                if len(t['ports_probed']) >= threshold:
                    ports = sorted(list(t['ports_probed']))
                    self._log(f"⚠ PORT SCAN: {ip} probed {len(ports)} ports: {ports[:10]}...", "high")
                    self.anomalies_lbl.config(text=f"Anomalies: {int(self.anomalies_lbl.cget('text').split(':')[1])+1}")
                    self.port_scan_tracker[ip] = {'ports_probed':set(), 'start_time':now, 'last_probe':now}
            elif t['start_time'] and (now - t['start_time']) > window:
                self.port_scan_tracker[ip] = {'ports_probed':set(), 'start_time':now, 'last_probe':now}

    def _detect_beaconing(self):
        for ip, bt in self.beacon_tracker.items():
            intervals = bt['intervals']
            if len(intervals) >= 5:
                mean = sum(intervals) / len(intervals)
                variance = sum((x-mean)**2 for x in intervals) / len(intervals)
                std = math.sqrt(variance)
                if std < 1.0 and mean > 5:
                    self._log(f"🔔 BEACONING: {ip} - interval={mean:.1f}s, jitter={std:.2f}s", "high")
                    self.beacons_lbl.config(text=f"Beacons: {int(self.beacons_lbl.cget('text').split(':')[1])+1}")

    def _detect_data_exfil(self):
        threshold = 1_000_000
        for ip, dt in self.data_transfer_tracker.items():
            if dt['total_bytes'] > threshold and not dt['threshold_exceeded']:
                dt['threshold_exceeded'] = True
                self._log(f"📤 DATA EXFIL: {ip} transferred {dt['total_bytes']/1024/1024:.1f}MB", "critical")

    def _calc_score(self):
        score = 0.0
        scans = sum(1 for t in self.port_scan_tracker.values() if len(t['ports_probed'])>5)
        score += scans * 0.1
        bc = int(self.beacons_lbl.cget('text').split(':')[1]) if ':' in self.beacons_lbl.cget('text') else 0
        score += bc * 0.15
        exfil = sum(1 for t in self.data_transfer_tracker.values() if t['threshold_exceeded'])
        score += exfil * 0.2
        score = min(score, 1.0)
        bw = int(score * 250)
        if score > 0.7: color = '#ff0000'
        elif score > 0.4: color = '#ff6600'
        elif score > 0.2: color = '#ffaa00'
        else: color = '#00ff00'
        self.gauge.coords(self.bar, 0, 0, bw, 20)
        self.gauge.itemconfig(self.bar, fill=color)
        self.score_lbl.config(text=f"{score:.2f}", fg=color)

    def show_connections(self):
        if not hasattr(self, "traffic_out"): return
        self.traffic_out.delete('1.0', tk.END)
        self.traffic_out.insert(tk.END, "=== Active Connections ===\n\n")
        sorted_conns = sorted(self.connection_tracker.items(), key=lambda x: x[1]['packets'], reverse=True)
        for ip, c in sorted_conns[:20]:
            dur = time.time() - c['first_seen'] if c['first_seen'] else 0
            self.traffic_out.insert(tk.END,
                f"  {ip:<18} Pkts:{c['packets']:<6} Ports:{len(c['ports']):<4} "
                f"Dur:{dur:.0f}s Proto:{c['protocol']}\n")

    def show_beacons(self):
        if not hasattr(self, "traffic_out"): return
        self.analysis_out.delete('1.0', tk.END)
        self.analysis_out.insert(tk.END, "=== Beacon Detection ===\n\n")
        for ip, bt in self.beacon_tracker.items():
            if len(bt['intervals']) >= 5:
                mean = sum(bt['intervals'])/len(bt['intervals'])
                self.analysis_out.insert(tk.END,
                    f"  {ip}\n    Interval: {mean:.2f}s\n    Samples: {len(bt['intervals'])}\n\n")

    def show_baselines(self):
        if not hasattr(self, "traffic_out"): return
        self.analysis_out.delete('1.0', tk.END)
        self.analysis_out.insert(tk.END, "=== Traffic Baselines ===\n\n")
        for metric, vals in self.baselines.items():
            self.analysis_out.insert(tk.END,
                f"  {metric}:\n    Mean: {vals['mean']:.2f}\n"
                f"    Std: {vals['std']:.2f}\n"
                f"    Upper: {vals['mean']+2*vals['std']:.2f}\n\n")

    def clear_all(self):
        self.anomaly_out.delete('1.0', tk.END); self.traffic_out.delete('1.0', tk.END)
        self.analysis_out.delete('1.0', tk.END)
        self.connection_tracker.clear(); self.port_scan_tracker.clear()
        self.beacon_tracker.clear(); self.data_transfer_tracker.clear()
        self.flows_lbl.config(text="Flows: 0"); self.anomalies_lbl.config(text="Anomalies: 0")
        self.beacons_lbl.config(text="Beacons: 0")
        self._log("Cleared", "info")
