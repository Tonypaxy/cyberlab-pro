import tkinter as tk
from tkinter import ttk, messagebox
import os, json, hashlib, base64, secrets, threading
from datetime import datetime
from gui.base_module import BaseModule

class PasswordManager(BaseModule):
    def __init__(self, parent, db, logger):
        super().__init__(parent)
        self.db = db; self.logger = logger
        self.master_key = None
        self.vault_file = os.path.expanduser("~/cyberlab_vault.json")
        self.entries = []

    def build_content(self):
        self.add_title("Password Manager", "Encrypted vault for pentest credentials & keys")
        
        if not self.master_key:
            self._show_unlock()
        else:
            self._show_vault()

    def _show_unlock(self):
        tk.Label(self.inner, text="Master Password:", font=("Courier",10), fg="#fff", bg="#1a1a2e").pack(anchor="w", padx=10, pady=(20,0))
        self.master_entry = tk.Entry(self.inner, font=("Courier",11), bg="#0f3460", fg="#fff", relief="flat", show="*")
        self.master_entry.pack(fill="x", padx=10, pady=3)
        self.master_entry.bind("<Return>", lambda e: self._unlock())
        
        bf = tk.Frame(self.inner, bg="#1a1a2e"); bf.pack(fill="x", padx=10, pady=10)
        tk.Button(bf, text="Unlock Vault", font=("Courier",10,"bold"), fg="#000", bg="#00ff88",
                relief="raised", padx=20, pady=8, command=self._unlock).pack(side="left", padx=5)
        tk.Button(bf, text="Create New Vault", font=("Courier",10), fg="#000", bg="#ffaa00",
                relief="raised", padx=20, pady=8, command=self._create_vault).pack(side="left", padx=5)
        
        if os.path.exists(self.vault_file):
            tk.Label(self.inner, text=f"Vault exists: {self.vault_file}", font=("Courier",8), fg="#888", bg="#1a1a2e").pack(pady=5)
        else:
            tk.Label(self.inner, text="No vault found. Create new vault to start.", font=("Courier",9), fg="#888", bg="#1a1a2e").pack(pady=5)
        
        self.status = self.add_status("Enter master password to unlock")

    def _create_vault(self):
        password = self.master_entry.get().strip()
        if not password or len(password) < 8:
            messagebox.showwarning("Warning", "Password must be at least 8 characters")
            return
        
        if os.path.exists(self.vault_file):
            if not messagebox.askyesno("Overwrite", "Vault already exists. Overwrite?"): return
        
        self.master_key = password
        self.entries = []
        self._save_vault()
        messagebox.showinfo("Created", "New vault created!")
        self._refresh()

    def _unlock(self):
        password = self.master_entry.get().strip()
        if not password: return
        
        if not os.path.exists(self.vault_file):
            messagebox.showwarning("Warning", "No vault found. Create one first.")
            return
        
        try:
            with open(self.vault_file, "r") as f:
                data = json.load(f)
            
            salt = base64.b64decode(data["salt"])
            key = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100000)
            stored_key = base64.b64decode(data["key"])
            
            if key != stored_key:
                messagebox.showerror("Error", "Wrong password!")
                return
            
            self.master_key = password
            self.entries = data.get("entries", [])
            self._refresh()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to unlock: {e}")

    def _save_vault(self):
        salt = secrets.token_bytes(32)
        key = hashlib.pbkdf2_hmac("sha256", self.master_key.encode(), salt, 100000)
        
        data = {
            "salt": base64.b64encode(salt).decode(),
            "key": base64.b64encode(key).decode(),
            "entries": self.entries,
            "updated": str(datetime.now())
        }
        
        with open(self.vault_file, "w") as f:
            json.dump(data, f, indent=2)

    def _encrypt(self, text):
        if not self.master_key: return text
        result = []
        for i, c in enumerate(text):
            kc = self.master_key[i % len(self.master_key)]
            result.append(chr(ord(c) ^ ord(kc)))
        return base64.b64encode("".join(result).encode()).decode()

    def _decrypt(self, encoded):
        if not self.master_key: return encoded
        try:
            text = base64.b64decode(encoded).decode()
            result = []
            for i, c in enumerate(text):
                kc = self.master_key[i % len(self.master_key)]
                result.append(chr(ord(c) ^ ord(kc)))
            return "".join(result)
        except:
            return "[Decryption failed]"

    def _show_vault(self):
        for w in self.inner.winfo_children(): w.destroy()
        self.add_title("Password Manager", f"Vault unlocked - {len(self.entries)} entries")
        
        bf = tk.Frame(self.inner, bg="#1a1a2e"); bf.pack(fill="x", padx=10, pady=5)
        tk.Button(bf, text="+ Add Entry", font=("Courier",9,"bold"), fg="#000", bg="#00ff88",
                relief="raised", padx=12, pady=6, command=self._add_entry).pack(side="left", padx=3)
        tk.Button(bf, text="Generate Password", font=("Courier",9), fg="#000", bg="#00ccff",
                relief="raised", padx=12, pady=6, command=self._generate_password).pack(side="left", padx=3)
        tk.Button(bf, text="Lock Vault", font=("Courier",9), fg="#fff", bg="#cc0000",
                relief="raised", padx=12, pady=6, command=self._lock).pack(side="right", padx=3)
        tk.Button(bf, text="Export", font=("Courier",9), fg="#000", bg="#ffaa00",
                relief="raised", padx=12, pady=6, command=self._export).pack(side="right", padx=3)
        
        # Search
        sf = tk.Frame(self.inner, bg="#16213e", padx=10, pady=5)
        sf.pack(fill="x", padx=10, pady=5)
        self.search_entry = tk.Entry(sf, font=("Courier",10), bg="#0f3460", fg="#fff", relief="flat")
        self.search_entry.pack(fill="x")
        self.search_entry.insert(0, "Search entries...")
        self.search_entry.bind("<Return>", lambda e: self._display_entries())
        tk.Button(sf, text="🔍", font=("Courier",10), fg="#000", bg="#00ccff", relief="flat", padx=10,
                command=self._display_entries).pack(side="right")
        
        self.entries_frame = tk.Frame(self.inner, bg="#1a1a2e")
        self.entries_frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.status = self.add_status(f"{len(self.entries)} entries stored")
        self._display_entries()

    def _display_entries(self):
        for w in self.entries_frame.winfo_children(): w.destroy()
        search = self.search_entry.get().strip() if hasattr(self, 'search_entry') else ""
        if search == "Search entries...": search = ""
        
        filtered = self.entries
        if search:
            filtered = [e for e in self.entries if search.lower() in str(e).lower()]
        
        if not filtered:
            tk.Label(self.entries_frame, text="No entries found", font=("Courier",10), fg="#888", bg="#1a1a2e").pack(pady=20)
            return
        
        for i, entry in enumerate(filtered):
            card = tk.Frame(self.entries_frame, bg="#16213e", padx=10, pady=6)
            card.pack(fill="x", pady=2)
            
            h = tk.Frame(card, bg="#16213e"); h.pack(fill="x")
            title = self._decrypt(entry.get("title", "???"))
            tk.Label(h, text=title, font=("Courier",10,"bold"), fg="#00ff88", bg="#16213e").pack(side="left")
            
            category = self._decrypt(entry.get("category", ""))
            if category:
                tk.Label(h, text=f"[{category}]", font=("Courier",8), fg="#888", bg="#16213e").pack(side="left", padx=5)
            
            ts = entry.get("created", "")
            if ts: tk.Label(h, text=ts[:19], font=("Courier",7), fg="#666", bg="#16213e").pack(side="right")
            
            url = self._decrypt(entry.get("url", ""))
            if url: tk.Label(card, text=url[:60], font=("Courier",8), fg="#58a6ff", bg="#16213e").pack(anchor="w")
            
            bf2 = tk.Frame(card, bg="#16213e"); bf2.pack(fill="x")
            tk.Button(bf2, text="View", font=("Courier",7), fg="#000", bg="#00ccff", relief="flat", padx=6,
                    command=lambda e=entry: self._view_entry(e)).pack(side="left", padx=1)
            tk.Button(bf2, text="Copy Pass", font=("Courier",7), fg="#000", bg="#ffaa00", relief="flat", padx=6,
                    command=lambda e=entry: self._copy_pass(e)).pack(side="left", padx=1)
            tk.Button(bf2, text="Delete", font=("Courier",7), fg="#fff", bg="#cc0000", relief="flat", padx=6,
                    command=lambda e=entry: self._delete_entry(e)).pack(side="left", padx=1)

    def _add_entry(self):
        d = tk.Toplevel(self.frame, bg="#1a1a2e"); d.title("Add Entry"); d.geometry("450x500")
        tk.Label(d, text="Add Password Entry", font=("Courier",14,"bold"), fg="#00ff88", bg="#1a1a2e").pack(pady=10)
        
        fields = [
            ("Title:", "title", ""),
            ("URL/Host:", "url", ""),
            ("Username:", "username", ""),
            ("Password:", "password", ""),
            ("API Key/Token:", "token", ""),
            ("SSH Key Path:", "ssh_key", ""),
            ("Category:", "category", "client/root/admin/service"),
            ("Notes:", "notes", ""),
        ]
        entries = {}
        for label, key, default in fields:
            tk.Label(d, text=label, font=("Courier",9), fg="#aaa", bg="#1a1a2e").pack(anchor="w", padx=20)
            show = "*" if key == "password" else ""
            e = tk.Entry(d, font=("Courier",10), bg="#16213e", fg="#fff", relief="flat", show=show)
            e.pack(fill="x", padx=20, pady=2)
            if default: e.insert(0, default)
            entries[key] = e
        
        def save():
            entry = {}
            for key, widget in entries.items():
                val = widget.get().strip()
                entry[key] = self._encrypt(val) if val else ""
            entry["created"] = str(datetime.now())
            self.entries.append(entry)
            self._save_vault()
            d.destroy()
            self._refresh()
        
        tk.Button(d, text="Save Entry", font=("Courier",10,"bold"), fg="#000", bg="#00ff88",
                relief="raised", padx=20, pady=8, command=save).pack(pady=15)

    def _view_entry(self, entry):
        d = tk.Toplevel(self.frame, bg="#1a1a2e"); d.title("View Entry"); d.geometry("450x400")
        tk.Label(d, text="Entry Details", font=("Courier",14,"bold"), fg="#00ff88", bg="#1a1a2e").pack(pady=10)
        
        t = tk.Text(d, font=("Courier",10), bg="#0a0a0a", fg="#00ff88", relief="flat", height=15)
        t.pack(fill="both", expand=True, padx=10, pady=10)
        
        for key in ["title","url","username","password","token","ssh_key","category","notes"]:
            val = self._decrypt(entry.get(key,""))
            if val:
                t.insert("end", f"{key.upper()}: {val}\n")
                t.insert("end", "-"*40 + "\n")
        t.config(state="disabled")
        
        bf = tk.Frame(d, bg="#1a1a2e"); bf.pack(pady=5)
        tk.Button(bf, text="Copy Username", font=("Courier",9), fg="#000", bg="#00ccff", relief="flat", padx=10, pady=5,
                command=lambda: self._copy(self._decrypt(entry.get("username","")))).pack(side="left", padx=2)
        tk.Button(bf, text="Copy Password", font=("Courier",9), fg="#000", bg="#ffaa00", relief="flat", padx=10, pady=5,
                command=lambda: self._copy(self._decrypt(entry.get("password","")))).pack(side="left", padx=2)
        tk.Button(bf, text="Close", font=("Courier",9), fg="#fff", bg="#666", relief="flat", padx=10, pady=5,
                command=d.destroy).pack(side="left", padx=2)

    def _copy_pass(self, entry):
        password = self._decrypt(entry.get("password",""))
        self._copy(password)
        messagebox.showinfo("Copied", "Password copied to clipboard")

    def _copy(self, text):
        try: self.frame.clipboard_clear(); self.frame.clipboard_append(text)
        except: pass

    def _delete_entry(self, entry):
        if messagebox.askyesno("Delete", "Delete this entry?"):
            self.entries.remove(entry)
            self._save_vault()
            self._display_entries()

    def _generate_password(self):
        chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-=[]{}|;:,.<>?"
        password = "".join(secrets.choice(chars) for _ in range(24))
        self._copy(password)
        messagebox.showinfo("Generated", f"24-char password generated and copied!\n\n{password[:8]}...")

    def _lock(self):
        self.master_key = None
        self.entries = []
        self._refresh()

    def _export(self):
        if not self.entries: return
        path = os.path.expanduser(f"~/cyberlab_export_{datetime.now().strftime('%Y%m%d')}.csv")
        with open(path, "w") as f:
            f.write("Title,URL,Username,Password,Token,Category,Notes\n")
            for e in self.entries:
                row = ",".join(self._decrypt(e.get(k,"")) for k in ["title","url","username","password","token","category","notes"])
                f.write(row + "\n")
        messagebox.showinfo("Exported", f"Saved to {path}\n\nWARNING: File is UNENCRYPTED!")

    def _refresh(self):
        for w in self.inner.winfo_children(): w.destroy()
        self.build_content()
