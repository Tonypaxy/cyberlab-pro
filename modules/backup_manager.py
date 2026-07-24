import tkinter as tk
from tkinter import ttk, messagebox
import subprocess, threading, os, shutil, tarfile, hashlib, json, zipfile
from datetime import datetime

class BackupManager:
    def __init__(self, parent, db, logger):
        self.parent = parent; self.db = db; self.logger = logger
        self.frame = tk.Frame(parent, bg='#1a1a2e')
        self.backup_dir = os.path.expanduser('~/cyberlab_backups')
        os.makedirs(self.backup_dir, exist_ok=True)
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def build(self):
        self.frame.pack(fill='both', expand=True)
        
        header = tk.Frame(self.frame, bg='#1a1a2e')
        header.pack(fill='x', padx=10, pady=5)
        tk.Label(header, text="Backup & Restore", font=('Courier',16,'bold'), fg='#00ff88', bg='#1a1a2e').pack(side='left')
        tk.Label(header, text=f"Dir: {self.backup_dir}", font=('Courier',7), fg='#888', bg='#1a1a2e').pack(side='right')
        
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
        
        # === CREATE BACKUP ===
        sf1 = tk.LabelFrame(inner, text=" Create Backup ", font=('Courier',10,'bold'), fg='#00ff88', bg='#16213e', padx=10, pady=8)
        sf1.pack(fill='x', padx=10, pady=5)
        
        tk.Label(sf1, text="Backup Name:", font=('Courier',9), fg='#fff', bg='#16213e').pack(anchor='w')
        self.name_entry = tk.Entry(sf1, font=('Courier',10), bg='#0f3460', fg='#fff', relief='flat')
        self.name_entry.pack(fill='x', pady=3)
        self.name_entry.insert(0, f"cyberlab_backup_{datetime.now().strftime('%Y%m%d_%H%M')}")
        
        bf1 = tk.Frame(sf1, bg='#16213e'); bf1.pack(fill='x', pady=5)
        backups = [
            ("Full System", self._backup_full, "#00ff88", "Everything: core, gui, modules, plugins, themes, config, database, launcher"),
            ("Config Only", self._backup_config, "#00ccff", "Settings, API keys, favorites"),
            ("Projects", self._backup_projects, "#ffaa00", "All user projects with reports"),
            ("Tools & Plugins", self._backup_tools, "#bc8cff", "Tool data, plugins, custom scripts"),
            ("Themes", self._backup_themes, "#d2991d", "All 6 theme files"),
            ("Database", self._backup_database, "#ff4444", "SQLite database with all tables"),
            ("Wordlists", self._backup_wordlists, "#3fb950", "Downloaded and generated wordlists"),
        ]
        for name, func, color, desc in backups:
            row = tk.Frame(bf1, bg='#16213e'); row.pack(fill='x', pady=1)
            tk.Button(row, text=name, font=('Courier',9,'bold'), fg='#000', bg=color, relief='raised', padx=10, pady=4, command=func).pack(side='left')
            tk.Label(row, text=desc[:60], font=('Courier',7), fg='#888', bg='#16213e').pack(side='left', padx=5)
        
        # === RESTORE ===
        sf2 = tk.LabelFrame(inner, text=" Restore Backup ", font=('Courier',10,'bold'), fg='#ffaa00', bg='#16213e', padx=10, pady=8)
        sf2.pack(fill='x', padx=10, pady=5)
        self._list_backups(sf2)
        
        # === AUTO BACKUP ===
        sf3 = tk.LabelFrame(inner, text=" Auto Backup ", font=('Courier',10,'bold'), fg='#00ccff', bg='#16213e', padx=10, pady=8)
        sf3.pack(fill='x', padx=10, pady=5)
        self.auto_var = tk.BooleanVar(value=False)
        tk.Checkbutton(sf3, text="Auto-backup on exit", variable=self.auto_var, font=('Courier',9),
                fg='#fff', bg='#16213e', selectcolor='#00ff88').pack(anchor='w')
        tk.Label(sf3, text="Creates full backup automatically when you close CyberLab", font=('Courier',7), fg='#888', bg='#16213e').pack(anchor='w', padx=20)
        
        # === EXPORT ===
        sf4 = tk.LabelFrame(inner, text=" Export/Share ", font=('Courier',10,'bold'), fg='#bc8cff', bg='#16213e', padx=10, pady=8)
        sf4.pack(fill='x', padx=10, pady=5)
        ef = tk.Frame(sf4, bg='#16213e'); ef.pack(fill='x', pady=3)
        exports = [
            ("Export All ZIP", self._export_zip, "#00ff88"),
            ("Export Database", self._export_db, "#ff4444"),
            ("Export Wordlists", self._export_wordlists, "#3fb950"),
            ("Export Projects", self._export_projects, "#ffaa00"),
        ]
        for name, func, color in exports:
            tk.Button(ef, text=name, font=('Courier',9), fg='#000', bg=color, relief='flat', padx=10, pady=4, command=func).pack(side='left', padx=2)
        
        # === STATUS ===
        self.status_label = tk.Label(inner, text="Ready", font=('Courier',8), fg='#888', bg='#1a1a2e')
        self.status_label.pack(anchor='w', padx=10, pady=5)
        self.output = tk.Text(inner, font=('Courier',8), bg='#0a0a0a', fg='#00ff88', relief='flat', height=6)
        self.output.pack(fill='x', padx=10, pady=3)
        tk.Label(inner, text="", bg='#1a1a2e').pack()

    def _get_name(self):
        return self.name_entry.get().strip() or f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    def _create_tar(self, name, paths):
        path = os.path.join(self.backup_dir, f"{name}.tar.gz")
        with tarfile.open(path, 'w:gz') as tar:
            for p in paths:
                if os.path.exists(p):
                    arcname = p.replace(self.base_dir, '').lstrip('/')
                    tar.add(p, arcname=arcname or os.path.basename(p))
        sha = hashlib.sha256(open(path,'rb').read()).hexdigest()
        with open(path + '.sha256', 'w') as f: f.write(f"{sha}  {name}.tar.gz\n")
        size = os.path.getsize(path) // 1024
        return path, size, sha

    def _backup_full(self):
        name = self._get_name()
        paths = [os.path.join(self.base_dir, d) for d in ['core','gui','modules','plugins','themes','config','database']]
        paths += [os.path.join(self.base_dir, f) for f in ['launcher.py','setup.py','README.md'] if os.path.exists(os.path.join(self.base_dir, f))]
        path, size, sha = self._create_tar(name, paths)
        self._log(f"[+] Full backup: {name}.tar.gz ({size}KB)\n    SHA256: {sha[:16]}...")

    def _backup_config(self):
        path, size, sha = self._create_tar(self._get_name() + '_config', [os.path.join(self.base_dir, 'config')])
        self._log(f"[+] Config backup: ({size}KB)")

    def _backup_projects(self):
        path, size, sha = self._create_tar(self._get_name() + '_projects', [os.path.join(self.base_dir, 'projects')])
        self._log(f"[+] Projects backup: ({size}KB)")

    def _backup_tools(self):
        paths = [os.path.join(self.base_dir, d) for d in ['core/tools.py','core/tool_args.py','core/tool_args_data.py','modules','plugins'] if os.path.exists(os.path.join(self.base_dir, d))]
        path, size, sha = self._create_tar(self._get_name() + '_tools', paths)
        self._log(f"[+] Tools backup: ({size}KB)")

    def _backup_themes(self):
        path, size, sha = self._create_tar(self._get_name() + '_themes', [os.path.join(self.base_dir, 'themes')])
        self._log(f"[+] Themes backup: ({size}KB)")

    def _backup_database(self):
        db_path = os.path.join(self.base_dir, 'database', 'cyberlab.db')
        if os.path.exists(db_path):
            dest = os.path.join(self.backup_dir, f"{self._get_name()}_db.sqlite")
            shutil.copy2(db_path, dest)
            self._log(f"[+] Database backup: {os.path.getsize(dest)//1024}KB")

    def _backup_wordlists(self):
        wl_dir = os.path.expanduser('~/wordlists')
        if os.path.exists(wl_dir):
            path, size, sha = self._create_tar(self._get_name() + '_wordlists', [wl_dir])
            self._log(f"[+] Wordlists backup: ({size}KB)")

    def _list_backups(self, parent):
        for w in parent.winfo_children():
            if isinstance(w, tk.Frame) and w != parent.winfo_children()[0]:
                w.destroy()
        
        backups = sorted([f for f in os.listdir(self.backup_dir) if f.endswith('.tar.gz') or f.endswith('.sqlite')], reverse=True)
        if not backups:
            tk.Label(parent, text="No backups yet", font=('Courier',9), fg='#888', bg='#16213e').pack(pady=5)
            return
        
        tk.Label(parent, text=f"Existing backups ({len(backups)}):", font=('Courier',9), fg='#fff', bg='#16213e').pack(anchor='w')
        
        for f in backups[:15]:
            path = os.path.join(self.backup_dir, f)
            size = os.path.getsize(path) // 1024
            date = datetime.fromtimestamp(os.path.getmtime(path)).strftime('%Y-%m-%d %H:%M')
            sha_path = path + '.sha256'
            verified = "✓" if os.path.exists(sha_path) else "?"
            
            row = tk.Frame(parent, bg='#16213e'); row.pack(fill='x', pady=1, padx=5)
            tk.Label(row, text=f, font=('Courier',8), fg='#00ff88', bg='#16213e', width=30, anchor='w').pack(side='left', padx=5)
            tk.Label(row, text=f"{size}KB | {date} | {verified}", font=('Courier',7), fg='#888', bg='#16213e').pack(side='left', padx=5)
            
            bf = tk.Frame(row, bg='#16213e'); bf.pack(side='right')
            tk.Button(bf, text='Restore', font=('Courier',7), fg='#000', bg='#ffaa00', relief='flat', padx=6,
                    command=lambda p=path: self._restore(p)).pack(side='left', padx=1)
            tk.Button(bf, text='Verify', font=('Courier',7), fg='#000', bg='#00ccff', relief='flat', padx=6,
                    command=lambda p=path: self._verify(p)).pack(side='left', padx=1)
            tk.Button(bf, text='Del', font=('Courier',7), fg='#fff', bg='#cc0000', relief='flat', padx=6,
                    command=lambda p=path: self._delete_backup(p)).pack(side='left', padx=1)

    def _restore(self, path):
        if not messagebox.askyesno('Restore', f'Restore {os.path.basename(path)}?\nThis OVERWRITES current files.\n\nA backup of current state will be made first.'): return
        
        # Backup current state first
        self._backup_full()
        
        if path.endswith('.sqlite'):
            dest = os.path.join(self.base_dir, 'database', 'cyberlab.db')
            shutil.copy2(path, dest)
        else:
            with tarfile.open(path, 'r:gz') as tar: tar.extractall(path=self.base_dir)
        
        self._log(f"[+] Restored from {os.path.basename(path)}\n    Restart CyberLab to apply changes.")
        messagebox.showinfo('Restored', 'Restore complete. Restart CyberLab.')

    def _verify(self, path):
        sha_path = path + '.sha256'
        if os.path.exists(sha_path):
            with open(sha_path) as f:
                expected = f.read().split()[0]
            actual = hashlib.sha256(open(path,'rb').read()).hexdigest()
            if expected == actual:
                self._log(f"[✓] Integrity VERIFIED: {os.path.basename(path)}")
                messagebox.showinfo('Verified', 'Backup integrity verified!')
            else:
                self._log(f"[!] Integrity FAILED: {os.path.basename(path)}")
                messagebox.showerror('Failed', 'Backup may be corrupted!')
        else:
            self._log(f"[?] No checksum file for {os.path.basename(path)}")

    def _delete_backup(self, path):
        if messagebox.askyesno('Delete', f'Delete {os.path.basename(path)}?'):
            os.remove(path)
            sha = path + '.sha256'
            if os.path.exists(sha): os.remove(sha)
            self._log(f"[-] Deleted {os.path.basename(path)}")
            self.build()

    def _export_zip(self):
        path = os.path.expanduser(f"~/cyberlab_export_{datetime.now().strftime('%Y%m%d_%H%M')}.zip")
        subprocess.run(f'cd {self.base_dir} && zip -r {path} . -x "projects/*" "logs/*" "cache/*" "tmp/*" "*.db" "cyberlab_backups/*"', shell=True)
        self._log(f"[+] Exported: {path}")

    def _export_db(self):
        dbp = os.path.join(self.base_dir, 'database', 'cyberlab.db')
        if os.path.exists(dbp):
            path = os.path.expanduser(f"~/cyberlab_db_{datetime.now().strftime('%Y%m%d')}.sqlite")
            shutil.copy2(dbp, path)
            self._log(f"[+] DB exported: {path}")

    def _export_wordlists(self):
        wl = os.path.expanduser('~/wordlists')
        if os.path.exists(wl):
            path = os.path.expanduser(f"~/cyberlab_wordlists_{datetime.now().strftime('%Y%m%d')}.zip")
            subprocess.run(f'cd ~ && zip -r {path} wordlists/', shell=True)
            self._log(f"[+] Wordlists exported: {path}")

    def _export_projects(self):
        path = os.path.expanduser(f"~/cyberlab_projects_{datetime.now().strftime('%Y%m%d')}.zip")
        subprocess.run(f'cd {self.base_dir} && zip -r {path} projects/', shell=True)
        self._log(f"[+] Projects exported: {path}")

    def _log(self, text):
        self.output.insert('end', text + '\n'); self.output.see('end')
        self.status_label.config(text=text[:80])
