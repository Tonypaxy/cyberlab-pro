import tkinter as tk
from tkinter import ttk, messagebox
import subprocess, threading, os, shutil, json, tarfile, hashlib
from datetime import datetime
from gui.base_module import BaseModule

class BackupRestore(BaseModule):
    def __init__(self, parent, db, logger):
        super().__init__(parent)
        self.db = db; self.logger = logger

    def build_content(self):
        self.add_title("Backup & Restore", "Save and restore entire CyberLab configuration")
        
        # Backup section
        def backup_content(parent):
            tk.Label(parent, text="Backup Name:", font=("Courier",10), fg="#fff", bg="#1a1a2e").pack(anchor="w")
            self.backup_name = tk.Entry(parent, font=("Courier",10), bg="#0f3460", fg="#fff", relief="flat")
            self.backup_name.pack(fill="x", pady=3)
            self.backup_name.insert(0, f"cyberlab_backup_{datetime.now().strftime('%Y%m%d')}")
            
            bf = tk.Frame(parent, bg="#1a1a2e"); bf.pack(fill="x", pady=5)
            
            options = [
                ("Everything", self._backup_full, "#00ff88"),
                ("Config Only", self._backup_config, "#00ccff"),
                ("Projects Only", self._backup_projects, "#ffaa00"),
                ("Tools & Plugins", self._backup_tools, "#bc8cff"),
                ("Themes & Settings", self._backup_themes, "#d2991d"),
            ]
            for name, func, color in options:
                tk.Button(bf, text=name, font=("Courier",9), fg="#000", bg=color, relief="flat", padx=10, command=func).pack(side="left", padx=2)
        
        self.add_section("Create Backup", backup_content, "save", default_open=True)
        
        # Restore section
        def restore_content(parent):
            tk.Label(parent, text="Backup File:", font=("Courier",10), fg="#fff", bg="#1a1a2e").pack(anchor="w")
            self.restore_path = tk.Entry(parent, font=("Courier",10), bg="#0f3460", fg="#fff", relief="flat")
            self.restore_path.pack(fill="x", pady=3)
            
            # List existing backups
            backup_dir = os.path.expanduser("~/cyberlab_backups")
            if os.path.exists(backup_dir):
                backups = sorted([f for f in os.listdir(backup_dir) if f.endswith('.tar.gz')], reverse=True)
                if backups:
                    tk.Label(parent, text="Existing backups:", font=("Courier",9), fg="#888", bg="#1a1a2e").pack(anchor="w", pady=(10,0))
                    for b in backups[:10]:
                        path = os.path.join(backup_dir, b)
                        size = os.path.getsize(path) // 1024
                        date = datetime.fromtimestamp(os.path.getmtime(path)).strftime("%Y-%m-%d %H:%M")
                        row = tk.Frame(parent, bg="#16213e")
                        row.pack(fill="x", pady=1)
                        tk.Label(row, text=f"{b}", font=("Courier",8), fg="#00ff88", bg="#16213e").pack(side="left", padx=5)
                        tk.Label(row, text=f"{size}KB | {date}", font=("Courier",7), fg="#888", bg="#16213e").pack(side="right", padx=5)
                        tk.Button(row, text="Restore", font=("Courier",7), fg="#000", bg="#ffaa00", relief="flat", padx=6,
                                command=lambda p=path: self._restore_backup(p)).pack(side="right", padx=2)
                        tk.Button(row, text="Delete", font=("Courier",7), fg="#fff", bg="#cc0000", relief="flat", padx=6,
                                command=lambda p=path: self._delete_backup(p)).pack(side="right", padx=2)
            
            bf = tk.Frame(parent, bg="#1a1a2e"); bf.pack(fill="x", pady=10)
            tk.Button(bf, text="Restore Selected", font=("Courier",9), fg="#000", bg="#ffaa00",
                    relief="raised", padx=15, pady=6, command=self._restore_selected).pack(side="left", padx=3)
            tk.Button(bf, text="Verify Integrity", font=("Courier",9), fg="#000", bg="#00ccff",
                    relief="raised", padx=15, pady=6, command=self._verify_backup).pack(side="left", padx=3)
        
        self.add_section("Restore Backup", restore_content, "restore")
        
        # Export section
        def export_content(parent):
            options = [
                ("Export All as ZIP", self._export_zip, "#00ff88"),
                ("Export Projects", self._export_projects, "#00ccff"),
                ("Export Plugins", self._export_plugins, "#ffaa00"),
                ("Export Themes", self._export_themes, "#bc8cff"),
                ("Export Database", self._export_database, "#ff4444"),
                ("Export Wordlists", self._export_wordlists, "#d2991d"),
            ]
            for name, func, color in options:
                tk.Button(parent, text=name, font=("Courier",9), fg="#000", bg=color, relief="flat", padx=10,
                        command=func).pack(fill="x", pady=2, padx=20)
        
        self.add_section("Export Data", export_content, "export")
        
        # Auto-backup toggle
        af = tk.Frame(self.inner, bg="#16213e", padx=10, pady=8)
        af.pack(fill="x", padx=10, pady=10)
        self.auto_backup_var = tk.BooleanVar(value=False)
        tk.Checkbutton(af, text="Auto-backup on exit", variable=self.auto_backup_var,
                font=("Courier",9), fg="#fff", bg="#16213e", selectcolor="#00ff88").pack(side="left")
        tk.Button(af, text="Backup Now", font=("Courier",9), fg="#000", bg="#00ff88",
                relief="raised", padx=10, pady=5, command=self._backup_full).pack(side="right")
        
        self.output = tk.Text(self.inner, font=("Courier",9), bg="#0a0a0a", fg="#00ff88", relief="flat", height=8)
        self.output.pack(fill="both", expand=True, padx=10, pady=5)
        self.status = self.add_status("Ready")

    def _backup_dir(self):
        d = os.path.expanduser("~/cyberlab_backups")
        os.makedirs(d, exist_ok=True)
        return d

    def _get_name(self):
        return self.backup_name.get().strip() or f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    def _create_archive(self, name, paths):
        path = os.path.join(self._backup_dir(), f"{name}.tar.gz")
        with tarfile.open(path, "w:gz") as tar:
            for p in paths:
                if os.path.exists(p):
                    tar.add(p, arcname=os.path.basename(p))
        
        # Generate checksum
        sha = hashlib.sha256(open(path,"rb").read()).hexdigest()
        with open(path + ".sha256", "w") as f:
            f.write(f"{sha}  {name}.tar.gz\n")
        
        size = os.path.getsize(path) // 1024
        self.output.insert("end", f"\n[+] Backup created: {name}.tar.gz ({size}KB)\n")
        self.output.insert("end", f"    SHA256: {sha[:16]}...\n")
        self.output.insert("end", f"    Path: {path}\n")
        self.output.see("end")
        self.status.config(text=f"Backup created: {name}.tar.gz ({size}KB)")
        return path

    def _backup_full(self):
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        paths = [
            os.path.join(base, "core"),
            os.path.join(base, "gui"),
            os.path.join(base, "modules"),
            os.path.join(base, "plugins"),
            os.path.join(base, "themes"),
            os.path.join(base, "config"),
            os.path.join(base, "database"),
            os.path.join(base, "launcher.py"),
            os.path.join(base, "setup.py"),
        ]
        self._create_archive(self._get_name(), paths)

    def _backup_config(self):
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self._create_archive(self._get_name() + "_config", [os.path.join(base, "config")])

    def _backup_projects(self):
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self._create_archive(self._get_name() + "_projects", [os.path.join(base, "projects")])

    def _backup_tools(self):
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        paths = [os.path.join(base, d) for d in ["core/tools.py","core/tool_args.py","core/tool_args_data.py","modules","plugins"]]
        self._create_archive(self._get_name() + "_tools", [p for p in paths if os.path.exists(p)])

    def _backup_themes(self):
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self._create_archive(self._get_name() + "_themes", [os.path.join(base, "themes")])

    def _restore_backup(self, path):
        if not os.path.exists(path): return
        if messagebox.askyesno("Restore", f"Restore {os.path.basename(path)}?\nThis will overwrite current files."):
            base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            with tarfile.open(path, "r:gz") as tar:
                tar.extractall(path=base)
            self.output.insert("end", f"\n[+] Restored from {os.path.basename(path)}\n")
            self.status.config(text="Restore complete - restart CyberLab")

    def _restore_selected(self):
        path = self.restore_path.get().strip()
        if not path or not os.path.exists(path):
            messagebox.showwarning("Warning", "Select a backup file first")
            return
        self._restore_backup(path)

    def _verify_backup(self):
        path = self.restore_path.get().strip()
        if not path or not os.path.exists(path): return
        
        sha_path = path + ".sha256"
        if os.path.exists(sha_path):
            with open(sha_path) as f:
                expected = f.read().split()[0]
            actual = hashlib.sha256(open(path,"rb").read()).hexdigest()
            if expected == actual:
                self.output.insert("end", "\n[+] Backup integrity VERIFIED\n")
            else:
                self.output.insert("end", "\n[!] Backup integrity FAILED - file may be corrupted\n")
        else:
            self.output.insert("end", "\n[!] No checksum file found\n")
        self.output.see("end")

    def _delete_backup(self, path):
        if messagebox.askyesno("Delete", f"Delete {os.path.basename(path)}?"):
            os.remove(path)
            sha = path + ".sha256"
            if os.path.exists(sha): os.remove(sha)
            self.output.insert("end", f"\n[-] Deleted {os.path.basename(path)}\n")
            self._refresh()

    def _export_zip(self):
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path = os.path.expanduser(f"~/cyberlab_full_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip")
        subprocess.run(f"cd {base} && zip -r {path} . -x 'projects/*' 'logs/*' 'cache/*' 'tmp/*' '*.db'", shell=True)
        self.output.insert("end", f"\n[+] Exported to {path}\n")
        messagebox.showinfo("Exported", f"Saved to {path}")

    def _export_projects(self):
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path = os.path.expanduser(f"~/cyberlab_projects_{datetime.now().strftime('%Y%m%d')}.zip")
        subprocess.run(f"cd {base} && zip -r {path} projects/", shell=True)
        messagebox.showinfo("Exported", f"Saved to {path}")

    def _export_plugins(self):
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path = os.path.expanduser(f"~/cyberlab_plugins_{datetime.now().strftime('%Y%m%d')}.zip")
        subprocess.run(f"cd {base} && zip -r {path} plugins/", shell=True)
        messagebox.showinfo("Exported", f"Saved to {path}")

    def _export_themes(self):
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path = os.path.expanduser(f"~/cyberlab_themes_{datetime.now().strftime('%Y%m%d')}.zip")
        subprocess.run(f"cd {base} && zip -r {path} themes/", shell=True)
        messagebox.showinfo("Exported", f"Saved to {path}")

    def _export_database(self):
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        db_path = os.path.join(base, "database", "cyberlab.db")
        if os.path.exists(db_path):
            path = os.path.expanduser(f"~/cyberlab_db_{datetime.now().strftime('%Y%m%d')}.sqlite")
            shutil.copy2(db_path, path)
            messagebox.showinfo("Exported", f"Saved to {path}")

    def _export_wordlists(self):
        wl_dir = os.path.expanduser("~/wordlists")
        if os.path.exists(wl_dir):
            path = os.path.expanduser(f"~/cyberlab_wordlists_{datetime.now().strftime('%Y%m%d')}.zip")
            subprocess.run(f"cd ~ && zip -r {path} wordlists/", shell=True)
            messagebox.showinfo("Exported", f"Saved to {path}")

    def _refresh(self):
        for w in self.inner.winfo_children(): w.destroy()
        self.build_content()
