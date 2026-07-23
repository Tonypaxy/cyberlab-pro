import tkinter as tk
from tkinter import ttk, messagebox
import subprocess, threading, os, shutil, itertools, string
from datetime import datetime
from gui.base_module import BaseModule

class FuzzingToolkit(BaseModule):
    def __init__(self, parent, db, logger):
        super().__init__(parent)
        self.db = db; self.logger = logger
        self.running = False

    def build_content(self):
        self.add_title("Fuzzing Toolkit", "Parameter, Directory, API, File fuzzing")
        
        tk.Label(self.inner, text="Target URL:", font=("Courier",10), fg="#fff", bg="#1a1a2e").pack(anchor="w", padx=10)
        self.target_entry = tk.Entry(self.inner, font=("Courier",11), bg="#0f3460", fg="#fff", relief="flat")
        self.target_entry.pack(fill="x", padx=10, pady=3)
        self.target_entry.insert(0, "http://target.com/FUZZ")
        
        tk.Label(self.inner, text="Wordlist:", font=("Courier",10), fg="#fff", bg="#1a1a2e").pack(anchor="w", padx=10)
        wf = tk.Frame(self.inner, bg="#1a1a2e"); wf.pack(fill="x", padx=10, pady=3)
        self.wordlist_entry = tk.Entry(wf, font=("Courier",10), bg="#0f3460", fg="#fff", relief="flat")
        self.wordlist_entry.pack(side="left", fill="x", expand=True)
        self.wordlist_entry.insert(0, os.path.expanduser("~/wordlists/common.txt"))
        tk.Button(wf, text="Generate", font=("Courier",8), fg="#000", bg="#ffaa00", relief="flat", padx=8,
                command=self._generate_wordlist).pack(side="right", padx=2)
        tk.Button(wf, text="Browse", font=("Courier",8), fg="#000", bg="#888", relief="flat", padx=8,
                command=lambda: self.wordlist_entry.insert(0, "/path/to/wordlist.txt")).pack(side="right", padx=2)
        
        bf = tk.Frame(self.inner, bg="#1a1a2e"); bf.pack(fill="x", padx=10, pady=5)
        
        tools = self._detect_fuzzers()
        for name, cmd, color in tools:
            tk.Button(bf, text=name, font=("Courier",8), fg="#000", bg=color, relief="flat", padx=6,
                    command=lambda c=cmd: self._run(c)).pack(side="left", padx=2)
        
        tk.Button(bf, text="STOP", font=("Courier",8,"bold"), fg="#fff", bg="#cc0000", relief="flat", padx=6,
                command=self._stop).pack(side="right", padx=2)
        
        self.output = tk.Text(self.inner, font=("Courier",9), bg="#0a0a0a", fg="#00ff88", relief="flat", height=15)
        self.output.pack(fill="both", expand=True, padx=10, pady=5)
        self.status = self.add_status(f"Ready - {len(tools)} fuzzers detected")

    def _detect_fuzzers(self):
        tools = []
        
        # FFUF
        if shutil.which("ffuf"):
            tools.append(("FFUF Dir","ffuf -u URL -w WORDLIST -mc 200,301,302,403 -t 100 -of json -o /tmp/ffuf.json","#00ff88"))
            tools.append(("FFUF VHost","ffuf -u URL -w WORDLIST -H 'Host: FUZZ' -mc 200","#00ff88"))
            tools.append(("FFUF POST","ffuf -u URL -X POST -d 'user=FUZZ&pass=test' -w WORDLIST -mc 200","#00ff88"))
            tools.append(("FFUF Recursive","ffuf -u URL -w WORDLIST -recursion -recursion-depth 2","#00ff88"))
            tools.append(("FFUF Filter","ffuf -u URL -w WORDLIST -fc 404 -fw 10 -fl 5","#00ff88"))
        
        # Gobuster
        if shutil.which("gobuster"):
            tools.append(("Gobuster Dir","gobuster dir -u URL -w WORDLIST -x php,html,txt,js -t 50","#00ccff"))
            tools.append(("Gobuster DNS","gobuster dns -d TARGET -w WORDLIST -t 50","#00ccff"))
            tools.append(("Gobuster VHost","gobuster vhost -u URL -w WORDLIST","#00ccff"))
            tools.append(("Gobuster S3","gobuster s3 -w WORDLIST","#00ccff"))
        
        # Dirb
        if shutil.which("dirb"):
            tools.append(("Dirb","dirb URL WORDLIST -w -r","#ffaa00"))
            tools.append(("Dirb Big","dirb URL /usr/share/wordlists/dirb/big.txt -w","#ffaa00"))
        
        # Dirsearch
        if shutil.which("dirsearch"):
            tools.append(("Dirsearch","dirsearch -u URL -w WORDLIST -t 50 --json-report=/tmp/dirsearch.json","#ff4444"))
        
        # Wfuzz
        if shutil.which("wfuzz"):
            tools.append(("Wfuzz","wfuzz -c -z file,WORDLIST --hc 404 URL","#bc8cff"))
            tools.append(("Wfuzz POST","wfuzz -c -z file,WORDLIST -d 'user=FUZZ&pass=test' URL","#bc8cff"))
        
        # Feroxbuster
        if shutil.which("feroxbuster"):
            tools.append(("Feroxbuster","feroxbuster -u URL -w WORDLIST -t 50","#ff00ff"))
        
        # Param Miner / Arjun
        if shutil.which("arjun"):
            tools.append(("Arjun","arjun -u URL -t 20","#ff8800"))
        if shutil.which("paramspider"):
            tools.append(("ParamSpider","paramspider -d TARGET","#ff8800"))
        
        # API Fuzzing
        if shutil.which("ffuf"):
            tools.append(("API Fuzz","ffuf -u URL/api/FUZZ -w WORDLIST -H 'Content-Type: application/json'","#39c5cf"))
            tools.append(("JWT Fuzz","ffuf -u URL -w WORDLIST -H 'Authorization: Bearer FUZZ'","#39c5cf"))
        if shutil.which("kiterunner"):
            tools.append(("Kiterunner","kiterunner scan URL -w routes.kite","#39c5cf"))
        
        # SQLi Fuzzing
        if shutil.which("sqlmap"):
            tools.append(("SQLMap Fuzz","sqlmap -u URL --batch --level=3 --risk=2","#ff0000"))
        if shutil.which("ghauri"):
            tools.append(("Ghauri","ghauri -u URL --dbs","#ff0000"))
        
        # XSS Fuzzing
        if shutil.which("dalfox"):
            tools.append(("Dalfox","dalfox url URL","#ff4444"))
        if shutil.which("kxss"):
            tools.append(("KXSS","echo URL | kxss","#ff4444"))
        if shutil.which("xsstrike"):
            tools.append(("XSStrike","xsstrike -u URL","#ff4444"))
        
        # SSRF Fuzzing
        if shutil.which("ffuf"):
            tools.append(("SSRF Fuzz","ffuf -u URL -w ssrf_payloads.txt -H 'X-Forwarded-For: FUZZ'","#d2991d"))
        
        # Custom fuzzer
        tools.append(("Custom ASCII","python3 -c \"import itertools,string;[print(''.join(c)) for c in itertools.product(string.ascii_lowercase,repeat=3)]\" | head -1000","#666666"))
        tools.append(("Custom Numeric","python3 -c \"[print(i) for i in range(1,10000)]\"","#666666"))
        
        return tools

    def _run(self, cmd):
        target = self.target_entry.get().strip()
        wordlist = self.wordlist_entry.get().strip()
        
        if not target: return
        cmd = cmd.replace("URL", target)
        cmd = cmd.replace("TARGET", target.split("//")[-1].split("/")[0] if "//" in target else target)
        cmd = cmd.replace("WORDLIST", wordlist)
        
        self.output.insert("end", f"\n{'='*60}\n$ {cmd[:100]}\n{'='*60}\n\n")
        self.output.see("end")
        self.status.config(text="Fuzzing...")
        self.running = True
        
        def do():
            try:
                p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                for line in p.stdout:
                    if not self.running: p.kill(); break
                    self.output.insert("end", line); self.output.see("end")
                p.wait()
                self.status.config(text=f"Done - Exit: {p.returncode}")
            except Exception as e:
                self.output.insert("end", f"\n[X] {e}\n")
            self.running = False
        threading.Thread(target=do, daemon=True).start()

    def _generate_wordlist(self):
        d = tk.Toplevel(self.frame, bg="#1a1a2e"); d.title("Generate Wordlist"); d.geometry("400x350")
        tk.Label(d, text="Generate Quick Wordlist", font=("Courier",14,"bold"), fg="#00ff88", bg="#1a1a2e").pack(pady=10)
        
        options = [
            ("Numbers 1-1000", lambda: "\n".join(str(i) for i in range(1,1001))),
            ("3-char Lowercase", lambda: "\n".join("".join(c) for c in itertools.product(string.ascii_lowercase, repeat=3))),
            ("3-char Alphanumeric", lambda: "\n".join("".join(c) for c in itertools.product(string.ascii_lowercase+string.digits, repeat=3))),
            ("Common Extensions", lambda: "\n".join(["php","html","txt","js","css","jpg","png","gif","pdf","xml","json","bak","old","zip","tar","gz","sql","db"])),
            ("Common Files", lambda: "\n".join(["index","admin","login","wp-admin","config","backup","test","dev","api","upload","download","shell","cron"])),
            ("Common Params", lambda: "\n".join(["id","page","user","file","url","redirect","path","cmd","exec","query","search","sort","order","limit","offset"])),
            ("IDOR Range", lambda: "\n".join(str(i) for i in range(1,500))),
        ]
        
        for name, gen_func in options:
            tk.Button(d, text=name, font=("Courier",9), fg="#00ccff", bg="#16213e", relief="flat", padx=10, pady=4,
                    command=lambda g=gen_func,n=name: self._save_gen(g(),n,d)).pack(fill="x", padx=20, pady=2)

    def _save_gen(self, content, name, dialog):
        path = os.path.expanduser(f"~/wordlists/gen_{name.replace(' ','_')}.txt")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f: f.write(content)
        self.wordlist_entry.delete(0, "end")
        self.wordlist_entry.insert(0, path)
        dialog.destroy()
        messagebox.showinfo("Generated", f"Saved: {path}")

    def _stop(self):
        self.running = False
        self.output.insert("end", "\n[STOPPED]\n")
        self.status.config(text="Stopped")
