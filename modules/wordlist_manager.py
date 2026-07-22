import tkinter as tk
from tkinter import ttk, messagebox
import os, threading, subprocess
from datetime import datetime
from gui.base_module import BaseModule

class WordlistManager(BaseModule):
    def __init__(self, parent, db, logger):
        super().__init__(parent)
        self.db = db
        self.logger = logger
        self.wordlist_dir = os.path.expanduser("~/wordlists")
        os.makedirs(self.wordlist_dir, exist_ok=True)
    
    def build_content(self):
        self.add_title("Wordlist Manager", "Download, merge, deduplicate, and manage wordlists")
        
        # Stats
        files = os.listdir(self.wordlist_dir) if os.path.exists(self.wordlist_dir) else []
        total_size = sum(os.path.getsize(os.path.join(self.wordlist_dir, f)) for f in files if os.path.isfile(os.path.join(self.wordlist_dir, f)))
        
        stats = tk.Frame(self.inner, bg="#16213e", padx=10, pady=8)
        stats.pack(fill="x", padx=10, pady=5)
        tk.Label(stats, text=f"Wordlists: {len(files)} | Total: {total_size//1024//1024}MB | Dir: {self.wordlist_dir}",
                font=("Courier",9), fg="#00ccff", bg="#16213e").pack(side="left")
        tk.Button(stats, text="Open Folder", font=("Courier",9), fg="#000", bg="#00ccff",
                relief="flat", padx=10, command=self._open_folder).pack(side="right", padx=3)
        tk.Button(stats, text="Refresh", font=("Courier",9), fg="#000", bg="#ffaa00",
                relief="flat", padx=10, command=self._refresh).pack(side="right", padx=3)
        
        # Download section
        def download_content(parent):
            presets = [
                ("rockyou.txt (14MB)", "https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt"),
                ("SecLists Discovery (DNS)", "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/DNS/subdomains-top1million-5000.txt"),
                ("SecLists Discovery (Web)", "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/common.txt"),
                ("SecLists Passwords (Common)", "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10k-most-common.txt"),
                ("Dirbuster Medium", "https://raw.githubusercontent.com/daviddias/node-dirbuster/master/lists/directory-list-2.3-medium.txt"),
                ("FuzzDB Attack", "https://raw.githubusercontent.com/fuzzdb-project/fuzzdb/master/attack/xss/xss-uri.txt"),
            ]
            for name, url in presets:
                row = tk.Frame(parent, bg="#16213e")
                row.pack(fill="x", pady=1)
                tk.Label(row, text=name, font=("Courier",9), fg="#00ccff", bg="#16213e", width=35, anchor="w").pack(side="left", padx=5)
                tk.Button(row, text="Download", font=("Courier",8), fg="#000", bg="#00ff88",
                        relief="flat", padx=8, command=lambda u=url, n=name: self._download(u, n)).pack(side="right", padx=2)
            
            tk.Label(parent, text="Custom URL:", font=("Courier",9), fg="#fff", bg="#1a1a2e").pack(anchor="w", pady=(10,0))
            cf = tk.Frame(parent, bg="#1a1a2e")
            cf.pack(fill="x", pady=5)
            self.custom_url = tk.Entry(cf, font=("Courier",9), bg="#0f3460", fg="#fff", relief="flat")
            self.custom_url.pack(side="left", fill="x", expand=True, padx=(0,5))
            tk.Button(cf, text="Download", font=("Courier",9), fg="#000", bg="#00ff88",
                    relief="flat", padx=10, command=self._download_custom).pack(side="right")
        
        self.add_section("Download Wordlists", download_content, "down", default_open=True)
        
        # Merge section
        def merge_content(parent):
            self.merge_list = tk.Listbox(parent, font=("Courier",9), bg="#0f3460", fg="#fff",
                    selectmode="multiple", relief="flat", height=8)
            self.merge_list.pack(fill="x", pady=5)
            for f in sorted(files):
                if os.path.isfile(os.path.join(self.wordlist_dir, f)):
                    self.merge_list.insert("end", f)
            
            mf = tk.Frame(parent, bg="#1a1a2e")
            mf.pack(fill="x", pady=5)
            tk.Label(mf, text="Output:", font=("Courier",9), fg="#fff", bg="#1a1a2e").pack(side="left")
            self.merge_output = tk.Entry(mf, font=("Courier",9), bg="#0f3460", fg="#fff", relief="flat")
            self.merge_output.pack(side="left", fill="x", expand=True, padx=5)
            self.merge_output.insert(0, "merged.txt")
            tk.Button(mf, text="Merge & Dedup", font=("Courier",9,"bold"), fg="#000", bg="#ffaa00",
                    relief="flat", padx=10, command=self._merge).pack(side="right")
        
        self.add_section("Merge & Deduplicate", merge_content, "up")
        
        # File list
        self.file_frame = tk.Frame(self.inner, bg="#1a1a2e")
        self.file_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.status_label = self.add_status("Ready")
        self._refresh_files()
    
    def _refresh(self):
        for w in self.inner.winfo_children(): w.destroy()
        self.build_content()
    
    def _refresh_files(self):
        for w in self.file_frame.winfo_children(): w.destroy()
        files = os.listdir(self.wordlist_dir) if os.path.exists(self.wordlist_dir) else []
        for f in sorted(files):
            fpath = os.path.join(self.wordlist_dir, f)
            if not os.path.isfile(fpath): continue
            size = os.path.getsize(fpath)
            lines = 0
            try:
                with open(fpath, errors="ignore") as fh:
                    for _ in fh: lines += 1
            except: pass
            
            card = tk.Frame(self.file_frame, bg="#16213e", padx=10, pady=6)
            card.pack(fill="x", pady=1)
            h = tk.Frame(card, bg="#16213e")
            h.pack(fill="x")
            tk.Label(h, text=f, font=("Courier",9,"bold"), fg="#00ff88", bg="#16213e").pack(side="left")
            tk.Label(h, text=f"{size//1024}KB | {lines} lines", font=("Courier",8), fg="#888", bg="#16213e").pack(side="right")
            bf = tk.Frame(card, bg="#16213e")
            bf.pack(fill="x")
            tk.Button(bf, text="Preview", font=("Courier",7), fg="#000", bg="#00ccff", relief="flat", padx=6,
                    command=lambda p=fpath: self._preview(p)).pack(side="left", padx=1)
            tk.Button(bf, text="Count", font=("Courier",7), fg="#000", bg="#ffaa00", relief="flat", padx=6,
                    command=lambda p=fpath: self._count(p)).pack(side="left", padx=1)
            tk.Button(bf, text="Delete", font=("Courier",7), fg="#fff", bg="#cc0000", relief="flat", padx=6,
                    command=lambda p=fpath: self._delete_file(p)).pack(side="left", padx=1)
    
    def _download(self, url, name):
        fname = url.split("/")[-1]
        fpath = os.path.join(self.wordlist_dir, fname)
        self.status_label.config(text=f"Downloading {fname}...")
        def do():
            try:
                subprocess.run(["wget", "-O", fpath, url], capture_output=True, timeout=120)
                self.frame.after(0, lambda: messagebox.showinfo("Done", f"Downloaded: {fname}"))
                self.frame.after(100, self._refresh)
            except Exception as e:
                self.frame.after(0, lambda: messagebox.showerror("Error", str(e)))
        threading.Thread(target=do, daemon=True).start()
    
    def _download_custom(self):
        url = self.custom_url.get().strip()
        if url: self._download(url, url.split("/")[-1])
    
    def _merge(self):
        selected = [self.merge_list.get(i) for i in self.merge_list.curselection()]
        if not selected: messagebox.showwarning("Warning", "Select wordlists to merge"); return
        output = self.merge_output.get().strip() or "merged.txt"
        output_path = os.path.join(self.wordlist_dir, output)
        self.status_label.config(text="Merging...")
        def do():
            seen = set()
            count = 0
            with open(output_path, "w") as out:
                for fname in selected:
                    fpath = os.path.join(self.wordlist_dir, fname)
                    try:
                        with open(fpath, errors="ignore") as fh:
                            for line in fh:
                                line = line.strip()
                                if line and line not in seen:
                                    out.write(line + "\n")
                                    seen.add(line)
                                    count += 1
                    except: pass
            self.frame.after(0, lambda: self.status_label.config(text=f"Merged {count} unique lines into {output}"))
            self.frame.after(0, lambda: messagebox.showinfo("Done", f"Merged: {count} unique lines"))
            self.frame.after(100, self._refresh)
        threading.Thread(target=do, daemon=True).start()
    
    def _preview(self, fpath):
        d = tk.Toplevel(self.frame, bg="#1a1a2e")
        d.title(os.path.basename(fpath)); d.geometry("500x400")
        t = tk.Text(d, font=("Courier",9), bg="#0a0a0a", fg="#00ff88", relief="flat")
        t.pack(fill="both", expand=True, padx=10, pady=10)
        try:
            with open(fpath, errors="ignore") as fh:
                t.insert("1.0", fh.read(10000))
        except: t.insert("1.0", "Error reading file")
        t.config(state="disabled")
        tk.Button(d, text="Close", font=("Courier",10), fg="#fff", bg="#666", relief="raised", padx=15, pady=5, command=d.destroy).pack(pady=5)
    
    def _count(self, fpath):
        try:
            with open(fpath, errors="ignore") as fh:
                count = sum(1 for _ in fh)
            messagebox.showinfo("Count", f"{os.path.basename(fpath)}: {count:,} lines")
        except: pass
    
    def _delete_file(self, fpath):
        if messagebox.askyesno("Delete", f"Delete {os.path.basename(fpath)}?"):
            os.remove(fpath)
            self._refresh()
    
    def _open_folder(self):
        try: subprocess.Popen(["termux-open", self.wordlist_dir])
        except: messagebox.showinfo("Folder", self.wordlist_dir)
