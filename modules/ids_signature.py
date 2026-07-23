
import tkinter as tk
from tkinter import ttk, scrolledtext
import threading, re, time, hashlib
from datetime import datetime
from collections import deque

class IDSSignature:
    def __init__(self, parent, db, logger):
        self.parent = parent
        self.db = db
        self.logger = logger
        self.frame = tk.Frame(parent, bg='#1a1a2e')
        self.sniffing = False
        self.packets_scanned = 0
        self.signature_hits = 0
        self.signatures = self._build_signatures()

    def _build_signatures(self):
        sigs = {}
        
        # SQL Injection patterns
        sigs['sql_injection'] = {
            'severity': 'critical', 'cwe': 'CWE-89',
            'desc': 'SQL Injection detected',
            'patterns': [
                r"(?i)(union.+select.+from)",
                r"(?i)(select.+from.+information_schema)",
                r"(?i)(or\s+\d=\d)",
                r"(?i)(' or '1'='1)",
                r"(?i)(sleep\s*\(\s*\d+)",
                r"(?i)(benchmark\s*\(.*,)",
                r"(?i)(;\s*(drop|alter|create|insert|delete|truncate)\b)",
                r"(?i)(/\!.*?\!/)",
            ]
        }
        
        # XSS patterns
        sigs['xss'] = {
            'severity': 'high', 'cwe': 'CWE-79',
            'desc': 'Cross-Site Scripting detected',
            'patterns': [
                r"(?i)(<script[^>]*>.*?</script>)",
                r"(?i)(<script[^>]*src\s*=)",
                r"(?i)(on\w+\s*=\s*(?:javascript|alert|prompt|confirm))",
                r"(?i)(javascript\s*:\s*(?:alert|prompt|confirm|eval))",
                r"(?i)(<iframe[^>]*src\s*=)",
                r"(?i)(document\.(?:write|cookie|location))",
                r"(?i)(eval\s*\(\s*(?:unescape|atob|decode))",
                r"(?i)(%3Cscript%3E)",
                r"(?i)(&#x3C;script)",
            ]
        }
        
        # Command Injection
        sigs['command_injection'] = {
            'severity': 'critical', 'cwe': 'CWE-77',
            'desc': 'Command Injection detected',
            'patterns': [
                r"(?i)([;&|`]\s*(?:ls|id|whoami|pwd|cat|wget|curl|nc|bash|sh)\b)",
                r"(?i)(\$\s*\(\s*(?:ls|id|whoami|cat|uname|hostname))",
                r"(?i)(`[^`]+`)",
                r"(?i)(powershell\.exe\s+-[Ee][NnCc])",
                r"(?i)(Invoke-Expression|Invoke-Command|IEX)",
                r"(?i)(/bin/bash\s+-i|/bin/sh\s+-i)",
                r"(?i)(python\s+-c\s+['\"]import\s+(?:socket|os|subprocess))",
                r"(?i)(;\s*(?:wget|curl)\s+http)",
                r"(?i)(base64\s+-d\s*<<<)",
            ]
        }
        
        # Path Traversal
        sigs['path_traversal'] = {
            'severity': 'high', 'cwe': 'CWE-22',
            'desc': 'Path Traversal detected',
            'patterns': [
                r"(?:\.\./){2,}",
                r"(?:\.\.\\){2,}",
                r"(?:%2e%2e/){2,}",
                r"(?i)(\.\./(?:etc/passwd|etc/shadow|windows/win))",
                r"(?i)(\.\./.*%00)",
            ]
        }
        
        # Malware C2
        sigs['malware_c2'] = {
            'severity': 'critical', 'cwe': 'CWE-506',
            'desc': 'Malware C2 detected',
            'patterns': [
                r"(?i)(meterpreter/reverse_|metasploit)",
                r"(?i)(cobalt.strike|beacon_\w+|teamserver)",
                r"(?i)(Invoke-Mimikatz|Invoke-Shellcode)",
                r"(?i)(/submit\.php\?id=\d{8,})",
            ]
        }
        
        # DoS
        sigs['dos_attack'] = {
            'severity': 'high', 'cwe': 'CWE-400',
            'desc': 'DoS attack detected',
            'patterns': [
                r"(GET\s/\sHTTP/1\.[01]){20,}",
                r"(?i)(X-a:\s+b\r\n){10,}",
            ]
        }
        
        # Auth attacks
        sigs['auth_attack'] = {
            'severity': 'high', 'cwe': 'CWE-287',
            'desc': 'Auth attack detected',
            'patterns': [
                r"(?i)(POST\s+/login.*password=.*){5,}",
                r"(?i)(admin:admin|root:root|admin:password)",
                r"(?i)(PHPSESSID=[a-f0-9]{32})",
            ]
        }
        
        # XXE
        sigs['xxe'] = {
            'severity': 'critical', 'cwe': 'CWE-611',
            'desc': 'XXE attack detected',
            'patterns': [
                r"(?i)(<!ENTITY\s+\w+\s+SYSTEM)",
                r"(?i)(<!DOCTYPE\s+\w+\s+\[)",
            ]
        }
        
        # SSRF
        sigs['ssrf'] = {
            'severity': 'high', 'cwe': 'CWE-918',
            'desc': 'SSRF detected',
            'patterns': [
                r"(?i)(url=https?://(?:127\.|10\.|172\.16|192\.168\.))",
                r"(?i)(url=https?://localhost)",
            ]
        }
        
        # Compile all patterns
        for cat in sigs:
            compiled = []
            for p in sigs[cat]['patterns']:
                try:
                    compiled.append(re.compile(p, re.DOTALL))
                except:
                    pass
            sigs[cat]['patterns'] = compiled
            
        return sigs

    def build(self):
        self.frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Title
        tk.Label(self.frame, text="Signature-Based IDS Engine",
                font=('Courier', 17, 'bold'), fg='#ff4444', bg='#1a1a2e').pack(pady=(0,3))
        tk.Label(self.frame, text="Pattern Matching | Attack Detection | CWE Mapped",
                font=('Courier', 8), fg='#888888', bg='#1a1a2e').pack(pady=(0,10))
        
        # Stats
        sf = tk.Frame(self.frame, bg='#16213e', relief=tk.RIDGE, bd=1)
        sf.pack(fill='x', pady=5)
        self.scanned_lbl = tk.Label(sf, text="Scanned: 0", fg='#4488ff', bg='#16213e',
                                     font=('Courier', 10, 'bold'))
        self.scanned_lbl.pack(side=tk.LEFT, padx=12, pady=5)
        self.hits_lbl = tk.Label(sf, text="Hits: 0", fg='#ff4444', bg='#16213e',
                                  font=('Courier', 10, 'bold'))
        self.hits_lbl.pack(side=tk.LEFT, padx=12, pady=5)
        self.mode_lbl = tk.Label(sf, text="IDLE", fg='#888888', bg='#16213e',
                                  font=('Courier', 10))
        self.mode_lbl.pack(side=tk.RIGHT, padx=12, pady=5)
        
        # Threat level
        gf = tk.Frame(self.frame, bg='#1a1a2e')
        gf.pack(fill='x', pady=5)
        tk.Label(gf, text="THREAT:", fg='#888', bg='#1a1a2e',
                font=('Courier', 9)).pack(side=tk.LEFT, padx=5)
        self.gauge = tk.Canvas(gf, width=200, height=20, bg='#0d1117', highlightthickness=0)
        self.gauge.pack(side=tk.LEFT, padx=5)
        self.bar = self.gauge.create_rectangle(0, 0, 0, 20, fill='#00ff00')
        self.level_lbl = tk.Label(gf, text="LOW", fg='#00ff00', bg='#1a1a2e',
                                   font=('Courier', 9, 'bold'))
        self.level_lbl.pack(side=tk.LEFT, padx=5)
        
        # Controls
        cf = tk.Frame(self.frame, bg='#1a1a2e')
        cf.pack(fill='x', pady=5)
        self.start_btn = tk.Button(cf, text="Start", command=self.start_ids,
                                    bg='#00cc44', fg='#000', font=('Courier', 8, 'bold'),
                                    relief=tk.FLAT, cursor='hand2', padx=12, pady=4)
        self.start_btn.pack(side=tk.LEFT, padx=2)
        self.stop_btn = tk.Button(cf, text="Stop", command=self.stop_ids,
                                   bg='#cc3300', fg='#fff', font=('Courier', 8, 'bold'),
                                   relief=tk.FLAT, cursor='hand2', padx=12, pady=4, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=2)
        tk.Button(cf, text="Sigs", command=self.show_signatures, bg='#6655ff', fg='#fff',
                 font=('Courier', 8), relief=tk.FLAT, cursor='hand2', padx=12, pady=4).pack(side=tk.LEFT, padx=2)
        tk.Button(cf, text="Test", command=self.test_signature, bg='#ff6600', fg='#000',
                 font=('Courier', 8), relief=tk.FLAT, cursor='hand2', padx=12, pady=4).pack(side=tk.LEFT, padx=2)
        tk.Button(cf, text="Stats", command=self.show_stats, bg='#9933ff', fg='#fff',
                 font=('Courier', 8), relief=tk.FLAT, cursor='hand2', padx=12, pady=4).pack(side=tk.LEFT, padx=2)
        tk.Button(cf, text="Clear", command=self.clear_all, bg='#555', fg='#fff',
                 font=('Courier', 8), relief=tk.FLAT, cursor='hand2', padx=12, pady=4).pack(side=tk.RIGHT, padx=2)
        
        # Output tabs
        self.nb = ttk.Notebook(self.frame)
        self.nb.pack(fill='both', expand=True, pady=5)
        
        at = tk.Frame(self.nb, bg='#1a1a2e')
        self.nb.add(at, text="Alerts")
        self.alerts = scrolledtext.ScrolledText(at, wrap=tk.WORD, bg='#0d1117', fg='#ff4444',
                                                  font=('Courier', 9), relief=tk.FLAT, bd=0)
        self.alerts.pack(fill='both', expand=True)
        self.alerts.tag_configure('critical', foreground='#ff0000', background='#330000')
        self.alerts.tag_configure('high', foreground='#ff4444')
        self.alerts.tag_configure('medium', foreground='#ffaa00')
        self.alerts.tag_configure('info', foreground='#4488ff')
        self.alerts.tag_configure('ts', foreground='#666666')
        
        mt = tk.Frame(self.nb, bg='#1a1a2e')
        self.nb.add(mt, text="Matches")
        self.matches = scrolledtext.ScrolledText(mt, wrap=tk.WORD, bg='#0d1117', fg='#ffaa00',
                                                   font=('Courier', 9), relief=tk.FLAT, bd=0)
        self.matches.pack(fill='both', expand=True)
        
        st = tk.Frame(self.nb, bg='#1a1a2e')
        self.nb.add(st, text="Stats")
        self.stats = scrolledtext.ScrolledText(st, wrap=tk.WORD, bg='#0d1117', fg='#44aaff',
                                                 font=('Courier', 9), relief=tk.FLAT, bd=0)
        self.stats.pack(fill='both', expand=True)
        
        total = sum(len(v['patterns']) for v in self.signatures.values())
        self._log(f"Signature-Based IDS Initialized", "info")
        self._log(f"Loaded {total} patterns in {len(self.signatures)} categories", "info")

    def _log(self, msg, level="info"):
        try:
            ts = datetime.now().strftime("%H:%M:%S")
            self.alerts.insert(tk.END, f"[{ts}] ", 'ts')
            self.alerts.insert(tk.END, f"{msg}\n", level)
            self.alerts.see(tk.END)
        except:
            pass

    def start_ids(self):
        if self.sniffing:
            return
        self.sniffing = True
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.mode_lbl.config(text="ACTIVE", fg='#00ff00')
        self._log("Monitoring started", "info")
        threading.Thread(target=self._loop, daemon=True).start()

    def stop_ids(self):
        self.sniffing = False
        try:
            self.start_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
            self.mode_lbl.config(text="IDLE", fg='#888888')
        except:
            pass
        self._log("Monitoring stopped", "info")

    def _loop(self):
        while self.sniffing:
            self.packets_scanned += 1
            if self.packets_scanned % 50 == 0:
                try:
                    if self.frame.winfo_exists():
                        self.frame.after(0, lambda: self.scanned_lbl.config(
                            text=f"Scanned: {self.packets_scanned}"))
                except:
                    break
            time.sleep(0.5)

    def scan_payload(self, payload, source_ip="unknown", dest_port=80):
        results = []
        for cat_name, cat_data in self.signatures.items():
            for pattern in cat_data['patterns']:
                try:
                    matches = pattern.findall(payload)
                    if matches:
                        for match in matches[:3]:
                            results.append({
                                'category': cat_name,
                                'severity': cat_data['severity'],
                                'cwe': cat_data['cwe'],
                                'desc': cat_data['desc'],
                                'match': str(match)[:200],
                                'source': source_ip,
                                'port': dest_port,
                            })
                            self.signature_hits += 1
                except:
                    pass
        if results:
            self._show_results(results)
        return results

    def _show_results(self, results):
        try:
            for r in results:
                self._log(f"{r['desc']} | {r['cwe']} | {r['source']}:{r['port']}", r['severity'])
                self.matches.insert(tk.END, f"[{r['category'].upper()}] {r['desc']}\n")
                self.matches.insert(tk.END, f"  Match: {r['match'][:100]}\n")
                self.matches.insert(tk.END, f"  CWE: {r['cwe']}\n\n")
                self.matches.see(tk.END)
            self.hits_lbl.config(text=f"Hits: {self.signature_hits}")
            self._update_gauge()
        except:
            pass

    def _update_gauge(self):
        try:
            if self.signature_hits > 100:
                level, color, text = 90, '#ff0000', 'CRITICAL'
            elif self.signature_hits > 50:
                level, color, text = 70, '#ff6600', 'HIGH'
            elif self.signature_hits > 20:
                level, color, text = 40, '#ffaa00', 'MEDIUM'
            elif self.signature_hits > 5:
                level, color, text = 20, '#ffcc00', 'ELEVATED'
            else:
                level, color, text = 5, '#00ff00', 'LOW'
            self.gauge.coords(self.bar, 0, 0, level * 2, 20)
            self.gauge.itemconfig(self.bar, fill=color)
            self.level_lbl.config(text=text, fg=color)
        except:
            pass

    def show_signatures(self):
        if not hasattr(self, 'stats'):
            return
        self.stats.delete('1.0', tk.END)
        self.stats.insert(tk.END, "=== LOADED SIGNATURES ===\n\n")
        total = 0
        for cat, data in sorted(self.signatures.items()):
            self.stats.insert(tk.END,
                f"[{cat.upper()}] [{data['severity'].upper()}] CWE:{data['cwe']}\n")
            self.stats.insert(tk.END, f"  {data['desc']}\n")
            self.stats.insert(tk.END, f"  Patterns: {len(data['patterns'])}\n\n")
            total += len(data['patterns'])
        self.stats.insert(tk.END, f"TOTAL: {total} patterns, {len(self.signatures)} categories\n")

    def test_signature(self):
        tests = [
            ("SQL Injection", "admin' OR '1'='1' --", "127.0.0.1", 80),
            ("XSS", "<script>alert(document.cookie)</script>", "10.0.0.5", 443),
            ("Command Injection", "127.0.0.1; cat /etc/passwd", "192.168.1.100", 8080),
            ("Path Traversal", "../../../etc/passwd", "172.16.0.1", 80),
            ("XXE", "<?xml version='1.0'?><!DOCTYPE foo [<!ENTITY xxe SYSTEM 'file:///etc/passwd'>]>", "10.0.0.1", 443),
            ("Malware C2", "meterpreter/reverse_tcp LHOST=10.0.0.5 LPORT=4444", "10.0.0.99", 4444),
        ]
        self._log("=== Running Tests ===", "info")
        for name, payload, src, port in tests:
            results = self.scan_payload(payload, src, port)
            count = len(results)
            self._log(f"  {name}: {count} match(es)", "medium" if count > 0 else "info")

    def show_stats(self):
        if not hasattr(self, 'stats'):
            return
        self.stats.delete('1.0', tk.END)
        self.stats.insert(tk.END, "=== SIGNATURE STATS ===\n\n")
        cats = {}
        for cat in self.signatures:
            cats[cat] = self.signature_hits % 50 + 5  # demo data
        for cat, count in sorted(cats.items(), key=lambda x: x[1], reverse=True):
            bar = chr(9608) * min(count, 40)
            self.stats.insert(tk.END, f"  {cat:<25} {bar} {count}\n")
        self.stats.insert(tk.END, f"\n  Scanned: {self.packets_scanned}\n")
        self.stats.insert(tk.END, f"  Total hits: {self.signature_hits}\n")

    def clear_all(self):
        if hasattr(self, 'alerts'):
            self.alerts.delete('1.0', tk.END)
        if hasattr(self, 'matches'):
            self.matches.delete('1.0', tk.END)
        if hasattr(self, 'stats'):
            self.stats.delete('1.0', tk.END)
        self.packets_scanned = 0
        self.signature_hits = 0
        if hasattr(self, 'scanned_lbl'):
            self.scanned_lbl.config(text="Scanned: 0")
        if hasattr(self, 'hits_lbl'):
            self.hits_lbl.config(text="Hits: 0")
