import tkinter as tk
from tkinter import messagebox
import hashlib, os, threading
from gui.base_module import BaseModule

class ChecksumVerifier(BaseModule):
    def __init__(self, parent, db, logger):
        super().__init__(parent)
        self.db = db
        self.logger = logger

    def build_content(self):
        self.add_title("Checksum Verifier", "MD5 SHA1 SHA256 file integrity checking")
        sf = tk.Frame(self.inner, bg="#16213e", padx=10, pady=8)
        sf.pack(fill="x", padx=10, pady=5)
        tk.Label(sf, text="File or Directory:", font=("Courier",10), fg="#fff", bg="#16213e").pack(anchor="w")
        self.path_entry = tk.Entry(sf, font=("Courier",10), bg="#0f3460", fg="#fff", relief="flat")
        self.path_entry.pack(fill="x", pady=3)
        self.path_entry.insert(0, os.path.expanduser("~"))
        bf = tk.Frame(sf, bg="#16213e")
        bf.pack(fill="x", pady=5)
        for t, a in [("MD5","md5"),("SHA1","sha1"),("SHA256","sha256"),("All","all")]:
            tk.Button(bf, text=t, font=("Courier",9), fg="#000", bg="#00ccff", relief="flat", padx=10, command=lambda alg=a: self._verify(alg)).pack(side="left", padx=2)
        tk.Label(self.inner, text="Expected hash (optional):", font=("Courier",10), fg="#fff", bg="#1a1a2e").pack(anchor="w", padx=10, pady=(10,0))
        self.hash_entry = tk.Entry(self.inner, font=("Courier",10), bg="#0f3460", fg="#fff", relief="flat")
        self.hash_entry.pack(fill="x", padx=10, pady=3)
        tk.Button(self.inner, text="Compare", font=("Courier",9), fg="#000", bg="#ffaa00", relief="flat", padx=10, command=self._compare).pack(pady=5)
        self.results_frame = tk.Frame(self.inner, bg="#1a1a2e")
        self.results_frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.status_label = self.add_status("Ready")

    def _hash_file(self, fpath, algo):
        h = hashlib.new(algo)
        with open(fpath, "rb") as f:
            while True:
                chunk = f.read(8192)
                if not chunk: break
                h.update(chunk)
        return h.hexdigest()

    def _verify(self, algo):
        path = self.path_entry.get().strip()
        if not os.path.exists(path):
            messagebox.showerror("Error","Path not found")
            return
        for w in self.results_frame.winfo_children(): w.destroy()
        t = tk.Text(self.results_frame, font=("Courier",8), bg="#0a0a0a", fg="#00ff88", relief="flat", wrap="word", height=15)
        t.pack(fill="both", expand=True)
        self.status_label.config(text="Hashing...")
        def do():
            algos = ["md5","sha1","sha256"] if algo == "all" else [algo]
            if os.path.isfile(path):
                files = [path]
            else:
                files = []
                for root, dirs, fnames in os.walk(path):
                    for f in fnames:
                        files.append(os.path.join(root,f))
                        if len(files) >= 50: break
                    if len(files) >= 50: break
            for fpath in files[:50]:
                try:
                    size = os.path.getsize(fpath)
                    fname = os.path.basename(fpath)
                    for a in algos:
                        h = self._hash_file(fpath, a)
                        line = a.upper() + " " + h + " " + fname + " (" + str(size) + " bytes)\\n"
                        t.insert("end", line)
                except Exception as e:
                    t.insert("end", "ERROR " + fpath + ": " + str(e) + "\\n")
            self.status_label.config(text="Done")
            t.see("end")
        threading.Thread(target=do, daemon=True).start()

    def _compare(self):
        expected = self.hash_entry.get().strip()
        path = self.path_entry.get().strip()
        if not expected or not os.path.isfile(path):
            messagebox.showwarning("Warning","Enter hash and valid file path")
            return
        md5 = self._hash_file(path, "md5")
        sha1 = self._hash_file(path, "sha1")
        sha256 = self._hash_file(path, "sha256")
        match = expected.lower() in [md5.lower(), sha1.lower(), sha256.lower()]
        for w in self.results_frame.winfo_children(): w.destroy()
        result = "MATCH" if match else "NO MATCH"
        color = "#00ff88" if match else "#ff4444"
        tk.Label(self.results_frame, text=result, font=("Courier",14,"bold"), fg=color, bg="#1a1a2e").pack(pady=10)
        tk.Label(self.results_frame, text="MD5: " + md5 + "\nSHA1: " + sha1 + "\nSHA256: " + sha256, font=("Courier",9), fg="#888", bg="#1a1a2e").pack()
