
import tkinter as tk
from tkinter import ttk, messagebox
import hashlib, os, subprocess, threading, re
from gui.base_module import BaseModule

class HashCracker(BaseModule):
    def __init__(self, parent, db, logger):
        super().__init__(parent)
        self.db = db
        self.logger = logger
        self.running = False

    def build_content(self):
        self.add_title("Hash Cracker", "Identify and crack hashes with john, hashcat, or built-in")
        
        tk.Label(self.inner, text="Paste hash:", font=("Courier",10), fg="#fff", bg="#1a1a2e").pack(anchor="w", padx=10)
        self.hash_entry = tk.Entry(self.inner, font=("Courier",10), bg="#0f3460", fg="#fff", relief="flat")
        self.hash_entry.pack(fill="x", padx=10, pady=3)
        
        # Identify button
        bf1 = tk.Frame(self.inner, bg="#1a1a2e")
        bf1.pack(fill="x", padx=10, pady=5)
        tk.Button(bf1, text="Identify Hash Type", font=("Courier",9), fg="#000", bg="#00ccff", relief="flat", padx=10,
                command=self._identify).pack(side="left", padx=2)
        self.id_label = tk.Label(bf1, text="", font=("Courier",9), fg="#ffaa00", bg="#1a1a2e")
        self.id_label.pack(side="left", padx=10)
        
        # Wordlist
        tk.Label(self.inner, text="Wordlist (optional):", font=("Courier",10), fg="#fff", bg="#1a1a2e").pack(anchor="w", padx=10, pady=(10,0))
        wf = tk.Frame(self.inner, bg="#1a1a2e")
        wf.pack(fill="x", padx=10, pady=3)
        self.wordlist_entry = tk.Entry(wf, font=("Courier",9), bg="#0f3460", fg="#fff", relief="flat")
        self.wordlist_entry.pack(side="left", fill="x", expand=True, padx=(0,5))
        self.wordlist_entry.insert(0, os.path.expanduser("~/wordlists/rockyou.txt"))
        tk.Button(wf, text="Browse", font=("Courier",8), fg="#000", bg="#888", relief="flat", padx=8,
                command=lambda: self.wordlist_entry.insert(0, "/path/to/wordlist.txt")).pack(side="right")
        
        # Crack methods
        bf2 = tk.Frame(self.inner, bg="#1a1a2e")
        bf2.pack(fill="x", padx=10, pady=5)
        for text, cmd in [
            ("Built-in Dict", self._builtin_dict),
            ("Built-in Brute", self._builtin_brute),
            ("John", self._john_crack),
            ("Hashcat Dict", self._hashcat_dict),
            ("Hashcat Brute", self._hashcat_brute),
        ]:
            tk.Button(bf2, text=text, font=("Courier",8), fg="#000", bg="#ffaa00", relief="flat", padx=6, command=cmd).pack(side="left", padx=2)
        
        tk.Button(self.inner, text="STOP", font=("Courier",9,"bold"), fg="#fff", bg="#cc0000",
                relief="flat", padx=10, command=self._stop).pack(pady=5)
        
        self.output = tk.Text(self.inner, font=("Courier",9), bg="#0a0a0a", fg="#00ff88", relief="flat", height=10)
        self.output.pack(fill="both", expand=True, padx=10, pady=5)
        self.status = self.add_status("Paste a hash to identify and crack")

    def _identify(self):
        h = self.hash_entry.get().strip()
        if not h: return
        hlen = len(h)
        types = []
        if hlen == 32 and re.match(r'^[a-f0-9]{32}$', h, re.I): types.append("MD5")
        if hlen == 40 and re.match(r'^[a-f0-9]{40}$', h, re.I): types.append("SHA1")
        if hlen == 64 and re.match(r'^[a-f0-9]{64}$', h, re.I): types.append("SHA256")
        if hlen == 128 and re.match(r'^[a-f0-9]{128}$', h, re.I): types.append("SHA512")
        if hlen == 56 and h.startswith("$2"): types.append("Bcrypt")
        if hlen == 34 and h.startswith("$1$"): types.append("MD5Crypt")
        if hlen == 98 and h.startswith("$5$"): types.append("SHA256Crypt")
        if hlen == 98 and h.startswith("$6$"): types.append("SHA512Crypt")
        if hlen == 32 and ":" in h: types.append("NTLM")
        if not types: types.append("Unknown")
        self.id_label.config(text=" | ".join(types))

    def _builtin_dict(self):
        h = self.hash_entry.get().strip()
        wf = self.wordlist_entry.get().strip()
        if not h or not os.path.isfile(wf):
            messagebox.showwarning("Warning", "Enter hash and valid wordlist path"); return
        self._identify()
        self.running = True
        self.status.config(text="Cracking with dictionary...")
        self.output.insert("end", "\n[*] Dictionary attack on " + h[:20] + "...\n")
        def do():
            try:
                with open(wf, errors="ignore") as f:
                    for line in f:
                        if not self.running: break
                        word = line.strip()
                        if hashlib.md5(word.encode()).hexdigest() == h.lower():
                            self.output.insert("end", "[+] CRACKED: " + word + " (MD5)\n")
                            self.status.config(text="Cracked: " + word)
                            self.running = False; return
                        if hashlib.sha1(word.encode()).hexdigest() == h.lower():
                            self.output.insert("end", "[+] CRACKED: " + word + " (SHA1)\n")
                            self.status.config(text="Cracked: " + word)
                            self.running = False; return
                        if hashlib.sha256(word.encode()).hexdigest() == h.lower():
                            self.output.insert("end", "[+] CRACKED: " + word + " (SHA256)\n")
                            self.status.config(text="Cracked: " + word)
                            self.running = False; return
                if self.running:
                    self.output.insert("end", "[-] Not found in wordlist\n")
                    self.status.config(text="Not found")
            except Exception as e:
                self.output.insert("end", "[X] " + str(e) + "\n")
            self.running = False
        threading.Thread(target=do, daemon=True).start()

    def _builtin_brute(self):
        h = self.hash_entry.get().strip()
        if not h: return
        self.running = True
        self.status.config(text="Brute forcing (4 chars max)...")
        self.output.insert("end", "\n[*] Brute force on " + h[:20] + "...\n")
        import itertools, string
        def do():
            chars = string.ascii_lowercase + string.digits
            for length in range(1, 5):
                if not self.running: break
                for combo in itertools.product(chars, repeat=length):
                    if not self.running: break
                    word = "".join(combo)
                    if hashlib.md5(word.encode()).hexdigest() == h.lower():
                        self.output.insert("end", "[+] CRACKED: " + word + " (MD5)\n")
                        self.status.config(text="Cracked: " + word)
                        self.running = False; return
            if self.running:
                self.output.insert("end", "[-] Not found (tried up to 4 chars)\n")
                self.status.config(text="Not found")
            self.running = False
        threading.Thread(target=do, daemon=True).start()

    def _john_crack(self):
        h = self.hash_entry.get().strip()
        wf = self.wordlist_entry.get().strip()
        if not h: return
        self.status.config(text="Running john...")
        self.output.insert("end", "\n[*] John the Ripper...\n")
        def do():
            try:
                with open("/tmp/cyberlab_hash.txt", "w") as f: f.write(h)
                cmd = ["john","--wordlist="+wf,"/tmp/cyberlab_hash.txt"] if os.path.isfile(wf) else ["john","/tmp/cyberlab_hash.txt"]
                p = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
                self.output.insert("end", p.stdout[-500:])
                r2 = subprocess.run(["john","--show","/tmp/cyberlab_hash.txt"], capture_output=True, text=True)
                self.output.insert("end", r2.stdout)
                self.status.config(text="Done")
            except Exception as e:
                self.output.insert("end", "[X] " + str(e) + "\n")
        threading.Thread(target=do, daemon=True).start()

    def _hashcat_dict(self):
        h = self.hash_entry.get().strip()
        wf = self.wordlist_entry.get().strip()
        if not h or not os.path.isfile(wf): return
        self.status.config(text="Running hashcat...")
        self.output.insert("end", "\n[*] Hashcat dictionary...\n")
        def do():
            try:
                with open("/tmp/cyberlab_hash.txt", "w") as f: f.write(h)
                p = subprocess.run(["hashcat","-m","0","-a","0","/tmp/cyberlab_hash.txt",wf,"--force"], capture_output=True, text=True, timeout=60)
                self.output.insert("end", p.stdout[-500:])
            except Exception as e:
                self.output.insert("end", "[X] " + str(e) + "\n")
        threading.Thread(target=do, daemon=True).start()

    def _hashcat_brute(self):
        h = self.hash_entry.get().strip()
        if not h: return
        self.status.config(text="Running hashcat brute...")
        self.output.insert("end", "\n[*] Hashcat brute force...\n")
        def do():
            try:
                with open("/tmp/cyberlab_hash.txt", "w") as f: f.write(h)
                p = subprocess.run(["hashcat","-m","0","-a","3","/tmp/cyberlab_hash.txt","?l?l?l?l","--force"], capture_output=True, text=True, timeout=60)
                self.output.insert("end", p.stdout[-500:])
            except Exception as e:
                self.output.insert("end", "[X] " + str(e) + "\n")
        threading.Thread(target=do, daemon=True).start()

    def _stop(self):
        self.running = False
        self.status.config(text="Stopped")
        self.output.insert("end", "\n[STOPPED]\n")
