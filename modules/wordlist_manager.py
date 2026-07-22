import tkinter as tk
from tkinter import ttk, messagebox
import os, threading, subprocess
from gui.base_module import BaseModule

class WordlistManager(BaseModule):
    def __init__(self, parent, db, logger):
        super().__init__(parent)
        self.db = db
        self.logger = logger
        self.wordlist_dir = os.path.expanduser("~/wordlists")
        os.makedirs(self.wordlist_dir, exist_ok=True)

    def build_content(self):
        self.add_title("Wordlist Manager", "Download, merge, deduplicate wordlists")
        files = [f for f in os.listdir(self.wordlist_dir) if os.path.isfile(os.path.join(self.wordlist_dir, f))]
        total = sum(os.path.getsize(os.path.join(self.wordlist_dir, f)) for f in files)
        stats = tk.Frame(self.inner, bg="#16213e", padx=10, pady=8)
        stats.pack(fill="x", padx=10, pady=5)
        tk.Label(stats, text="Files: " + str(len(files)) + " | Size: " + str(total//1024//1024) + "MB",
                font=("Courier",8), fg="#00ccff", bg="#16213e").pack(side="left")
        tk.Button(stats, text="Refresh", font=("Courier",8), fg="#000", bg="#ffaa00", relief="flat", padx=8, command=self._refresh).pack(side="right", padx=2)
        tk.Button(stats, text="Open Folder", font=("Courier",8), fg="#000", bg="#00ccff", relief="flat", padx=8, command=self._open).pack(side="right", padx=2)

        def dl_content(parent):
            urls = [
                "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/DNS/subdomains-top1million-5000.txt",
                "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/common.txt",
                "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10k-most-common.txt",
            ]
            for url in urls:
                name = url.split("/")[-1]
                row = tk.Frame(parent, bg="#16213e")
                row.pack(fill="x", pady=1)
                tk.Label(row, text=name, font=("Courier",8), fg="#00ccff", bg="#16213e", width=35, anchor="w").pack(side="left", padx=5)
                tk.Button(row, text="Download", font=("Courier",8), fg="#000", bg="#00ff88", relief="flat", padx=8, command=lambda u=url: self._download(u)).pack(side="right", padx=2)
            tk.Label(parent, text="Custom URL:", font=("Courier",9), fg="#fff", bg="#1a1a2e").pack(anchor="w", pady=(10,0))
            cf = tk.Frame(parent, bg="#1a1a2e")
            cf.pack(fill="x", pady=5)
            self.custom_url = tk.Entry(cf, font=("Courier",9), bg="#0f3460", fg="#fff", relief="flat")
            self.custom_url.pack(side="left", fill="x", expand=True, padx=(0,5))
            tk.Button(cf, text="Download", font=("Courier",9), fg="#000", bg="#00ff88", relief="flat", padx=10, command=lambda: self._download(self.custom_url.get().strip())).pack(side="right")
        self.add_section("Download Wordlists", dl_content, "down", default_open=True)

        self.progress_frame = tk.Frame(self.inner, bg="#1a1a2e")
        self.progress_frame.pack(fill="x", padx=10, pady=5)
        self.progress_label = tk.Label(self.progress_frame, text="", font=("Courier",9), fg="#ffaa00", bg="#1a1a2e")
        self.progress_bar = ttk.Progressbar(self.progress_frame, mode="indeterminate", length=300)

        def merge_content(parent):
            self.merge_list = tk.Listbox(parent, font=("Courier",9), bg="#0f3460", fg="#fff", selectmode="multiple", relief="flat", height=6)
            self.merge_list.pack(fill="x", pady=5)
            for f in sorted(files): self.merge_list.insert("end", f)
            mf = tk.Frame(parent, bg="#1a1a2e")
            mf.pack(fill="x", pady=5)
            tk.Label(mf, text="Output:", font=("Courier",9), fg="#fff", bg="#1a1a2e").pack(side="left")
            self.merge_output = tk.Entry(mf, font=("Courier",9), bg="#0f3460", fg="#fff", relief="flat")
            self.merge_output.pack(side="left", fill="x", expand=True, padx=5)
            self.merge_output.insert(0, "merged.txt")
            tk.Button(mf, text="Merge & Dedup", font=("Courier",9,"bold"), fg="#000", bg="#ffaa00", relief="flat", padx=10, command=self._merge).pack(side="right")
        self.add_section("Merge & Deduplicate", merge_content, "up")

        self.file_frame = tk.Frame(self.inner, bg="#1a1a2e")
        self.file_frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.status_label = self.add_status("Ready")
        self._refresh_files()

    def _refresh(self):
        for w in self.inner.winfo_children(): w.destroy()
        self.build_content()

    def _refresh_files(self):
        for w in self.file_frame.winfo_children(): w.destroy()
        files = [f for f in os.listdir(self.wordlist_dir) if os.path.isfile(os.path.join(self.wordlist_dir, f))]
        for f in sorted(files):
            fpath = os.path.join(self.wordlist_dir, f)
            size = os.path.getsize(fpath)
            card = tk.Frame(self.file_frame, bg="#16213e", padx=10, pady=6)
            card.pack(fill="x", pady=1)
            h = tk.Frame(card, bg="#16213e")
            h.pack(fill="x")
            tk.Label(h, text=f, font=("Courier",9,"bold"), fg="#00ff88", bg="#16213e").pack(side="left")
            tk.Label(h, text=str(size//1024) + "KB", font=("Courier",8), fg="#888", bg="#16213e").pack(side="right")
            bf = tk.Frame(card, bg="#16213e")
            bf.pack(fill="x")
            tk.Button(bf, text="Preview", font=("Courier",7), fg="#000", bg="#00ccff", relief="flat", padx=6, command=lambda p=fpath: self._preview(p)).pack(side="left", padx=1)
            tk.Button(bf, text="Delete", font=("Courier",7), fg="#fff", bg="#cc0000", relief="flat", padx=6, command=lambda p=fpath: self._delete(p)).pack(side="left", padx=1)

    def _download(self, url):
        if not url: return
        fname = url.split("/")[-1].split("?")[0]
        fpath = os.path.join(self.wordlist_dir, fname)
        self.progress_label.config(text="Downloading " + fname + "...")
        self.progress_label.pack(pady=3)
        self.progress_bar.pack(fill="x", pady=3)
        self.progress_bar.start(10)
        def do():
            try:
                r = subprocess.run(["wget","-q","-O",fpath,url], capture_output=True, text=True, timeout=120)
                self.frame.after(0, self.progress_bar.stop)
                self.frame.after(0, self.progress_bar.pack_forget)
                self.frame.after(0, self.progress_label.pack_forget)
                if r.returncode == 0 and os.path.exists(fpath) and os.path.getsize(fpath) > 0:
                    self.frame.after(0, lambda: messagebox.showinfo("Done", "Downloaded: " + fname))
                    self.frame.after(100, self._refresh)
                else:
                    self.frame.after(0, lambda: messagebox.showerror("Error", "Download failed"))
            except Exception as e:
                self.frame.after(0, self.progress_bar.stop)
                self.frame.after(0, self.progress_bar.pack_forget)
                self.frame.after(0, self.progress_label.pack_forget)
                self.frame.after(0, lambda err=e: messagebox.showerror("Error", str(err)))
        threading.Thread(target=do, daemon=True).start()

    def _merge(self):
        selected = [self.merge_list.get(i) for i in self.merge_list.curselection()]
        if not selected: messagebox.showwarning("Warning", "Select wordlists"); return
        output = self.merge_output.get().strip() or "merged.txt"
        output_path = os.path.join(self.wordlist_dir, output)
        self.status_label.config(text="Merging...")
        def do():
            seen, count = set(), 0
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
            self.frame.after(0, lambda: self.status_label.config(text="Merged " + str(count) + " lines"))
            self.frame.after(0, lambda: messagebox.showinfo("Done", "Merged: " + str(count) + " lines"))
            self.frame.after(100, self._refresh)
        threading.Thread(target=do, daemon=True).start()

    def _preview(self, fpath):
        d = tk.Toplevel(self.frame, bg="#1a1a2e")
        d.title(os.path.basename(fpath)); d.geometry("500x400")
        t = tk.Text(d, font=("Courier",9), bg="#0a0a0a", fg="#00ff88", relief="flat")
        t.pack(fill="both", expand=True, padx=10, pady=10)
        try:
            with open(fpath, errors="ignore") as fh: t.insert("1.0", fh.read(10000))
        except: t.insert("1.0", "Error")
        t.config(state="disabled")
        tk.Button(d, text="Close", font=("Courier",10), fg="#fff", bg="#666", relief="flat", padx=15, pady=5, command=d.destroy).pack(pady=5)

    def _delete(self, fpath):
        if messagebox.askyesno("Delete", "Delete " + os.path.basename(fpath) + "?"):
            os.remove(fpath)
            self._refresh()

    def _open(self):
        try: subprocess.Popen(["termux-open", self.wordlist_dir])
        except: messagebox.showinfo("Folder", self.wordlist_dir)
