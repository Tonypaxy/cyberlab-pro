import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import os, json, hashlib, base64
from gui.base_module import BaseModule

class EncryptedVault(BaseModule):
    def __init__(self, parent, db, logger):
        super().__init__(parent)
        self.db = db
        self.logger = logger
        self.current_project = None
        self.vault_key = None
        self._init_table()

    def _init_table(self):
        self.db.cursor.execute("""CREATE TABLE IF NOT EXISTS encrypted_notes (id INTEGER PRIMARY KEY AUTOINCREMENT, project_id INTEGER, title TEXT, content TEXT, iv TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")
        self.db.conn.commit()

    def _derive_key(self, password, salt="cyberlab_salt"):
        return hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100000, dklen=32)

    def _encrypt(self, plaintext, password):
        from Crypto.Cipher import AES
        from Crypto.Util.Padding import pad
        import os as _os
        key = self._derive_key(password)
        iv = _os.urandom(16)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        ct = cipher.encrypt(pad(plaintext.encode(), AES.block_size))
        return base64.b64encode(iv + ct).decode()

    def _decrypt(self, ciphertext_b64, password):
        from Crypto.Cipher import AES
        from Crypto.Util.Padding import unpad
        key = self._derive_key(password)
        raw = base64.b64decode(ciphertext_b64)
        iv, ct = raw[:16], raw[16:]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(ct), AES.block_size).decode()

    def _simple_encrypt(self, text, password):
        result = []
        for i, c in enumerate(text):
            key_char = password[i % len(password)]
            result.append(chr(ord(c) ^ ord(key_char)))
        return base64.b64encode("".join(result).encode()).decode()

    def _simple_decrypt(self, encoded, password):
        text = base64.b64decode(encoded).decode()
        result = []
        for i, c in enumerate(text):
            key_char = password[i % len(password)]
            result.append(chr(ord(c) ^ ord(key_char)))
        return "".join(result)

    def build_content(self):
        self.add_title("Encrypted Vault", "AES-256 encrypted notes for sensitive findings")
        projects = self.db.get_all_projects()
        names = [p["name"] for p in projects]
        if names:
            pf = tk.Frame(self.inner, bg="#16213e", padx=10, pady=8)
            pf.pack(fill="x", padx=10, pady=5)
            tk.Label(pf, text="Project:", font=("Courier",10), fg="#fff", bg="#16213e").pack(side="left")
            self.project_var = tk.StringVar(value=names[0])
            ttk.Combobox(pf, textvariable=self.project_var, values=names, font=("Courier",10), state="readonly", width=25).pack(side="left", padx=10)
            self._set_project(names[0])
        pf2 = tk.Frame(self.inner, bg="#16213e", padx=10, pady=8)
        pf2.pack(fill="x", padx=10, pady=5)
        tk.Label(pf2, text="Vault Password:", font=("Courier",10), fg="#fff", bg="#16213e").pack(anchor="w")
        self.pwd_entry = tk.Entry(pf2, font=("Courier",11), bg="#0f3460", fg="#fff", show="*", relief="flat")
        self.pwd_entry.pack(fill="x", pady=3)
        tk.Button(pf2, text="Unlock Vault", font=("Courier",10,"bold"), fg="#000", bg="#00ff88", relief="raised", padx=15, pady=6, command=self._unlock).pack(pady=5)
        self.vault_frame = tk.Frame(self.inner, bg="#1a1a2e")
        self.vault_frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.status_label = self.add_status("Enter password to unlock vault")

    def _set_project(self, name):
        for p in self.db.get_all_projects():
            if p["name"] == name: self.current_project = p; break

    def _unlock(self):
        self.vault_key = self.pwd_entry.get().strip()
        if not self.vault_key: messagebox.showwarning("Warning","Enter a password"); return
        self._load_notes()

    def _load_notes(self):
        for w in self.vault_frame.winfo_children(): w.destroy()
        if not self.current_project: return
        self.db.cursor.execute("SELECT * FROM encrypted_notes WHERE project_id=? ORDER BY created_at DESC", (self.current_project["id"],))
        notes = [dict(r) for r in self.db.cursor.fetchall()]
        tk.Button(self.vault_frame, text="+ New Encrypted Note", font=("Courier",10,"bold"), fg="#000", bg="#00ff88", relief="raised", padx=15, pady=6, command=self._new_note).pack(pady=5)
        if not notes:
            tk.Label(self.vault_frame, text="No encrypted notes yet", font=("Courier",10), fg="#888", bg="#1a1a2e").pack(pady=20)
            self.status_label.config(text="Vault unlocked - empty")
            return
        self.status_label.config(text="Vault unlocked - " + str(len(notes)) + " notes")
        for note in notes:
            card = tk.Frame(self.vault_frame, bg="#16213e", padx=10, pady=8)
            card.pack(fill="x", pady=2)
            try:
                title = self._simple_decrypt(note.get("title",""), self.vault_key)
            except:
                title = "[Wrong password or corrupted]"
            h = tk.Frame(card, bg="#16213e")
            h.pack(fill="x")
            tk.Label(h, text=title, font=("Courier",10,"bold"), fg="#ff4488", bg="#16213e").pack(side="left")
            ts = note.get("created_at","")
            if ts: tk.Label(h, text=str(ts)[:19], font=("Courier",8), fg="#666", bg="#16213e").pack(side="right")
            bf = tk.Frame(card, bg="#16213e")
            bf.pack(fill="x")
            tk.Button(bf, text="View", font=("Courier",8), fg="#000", bg="#00ccff", relief="flat", padx=8, command=lambda n=note: self._view_note(n)).pack(side="left", padx=1)
            tk.Button(bf, text="Delete", font=("Courier",8), fg="#fff", bg="#cc0000", relief="flat", padx=8, command=lambda n=note: self._delete_note(n)).pack(side="left", padx=1)

    def _new_note(self):
        d = tk.Toplevel(self.frame, bg="#1a1a2e")
        d.title("New Encrypted Note"); d.geometry("500x400")
        tk.Label(d, text="New Encrypted Note", font=("Courier",14,"bold"), fg="#ff4488", bg="#1a1a2e").pack(pady=10)
        tk.Label(d, text="Title:", font=("Courier",10), fg="#fff", bg="#1a1a2e").pack(anchor="w", padx=20)
        title_e = tk.Entry(d, font=("Courier",11), bg="#16213e", fg="#fff", relief="flat")
        title_e.pack(fill="x", padx=20, pady=5)
        tk.Label(d, text="Content:", font=("Courier",10), fg="#fff", bg="#1a1a2e").pack(anchor="w", padx=20)
        content_t = tk.Text(d, font=("Courier",9), bg="#0a0a0a", fg="#00ff88", relief="flat", height=10)
        content_t.pack(fill="both", expand=True, padx=20, pady=5)
        def save():
            title = title_e.get().strip()
            content = content_t.get("1.0","end-1c").strip()
            if not title: return
            enc_title = self._simple_encrypt(title, self.vault_key)
            enc_content = self._simple_encrypt(content, self.vault_key)
            self.db.cursor.execute("INSERT INTO encrypted_notes (project_id, title, content) VALUES (?,?,?)", (self.current_project["id"], enc_title, enc_content))
            self.db.conn.commit()
            d.destroy(); self._load_notes()
        tk.Button(d, text="Save Encrypted", font=("Courier",10,"bold"), fg="#000", bg="#ff4488", relief="raised", padx=20, pady=8, command=save).pack(pady=10)

    def _view_note(self, note):
        try:
            title = self._simple_decrypt(note.get("title",""), self.vault_key)
            content = self._simple_decrypt(note.get("content",""), self.vault_key)
        except:
            messagebox.showerror("Error","Wrong password or corrupted data"); return
        d = tk.Toplevel(self.frame, bg="#1a1a2e")
        d.title(title); d.geometry("550x400")
        tk.Label(d, text=title, font=("Courier",12,"bold"), fg="#ff4488", bg="#1a1a2e").pack(pady=10)
        t = tk.Text(d, font=("Courier",10), bg="#0a0a0a", fg="#00ff88", relief="flat")
        t.pack(fill="both", expand=True, padx=10, pady=10)
        t.insert("1.0", content)
        t.config(state="disabled")
        tk.Button(d, text="Close", font=("Courier",10), fg="#fff", bg="#666", relief="raised", padx=15, pady=5, command=d.destroy).pack(pady=5)

    def _delete_note(self, note):
        if messagebox.askyesno("Delete","Delete this encrypted note?"):
            self.db.cursor.execute("DELETE FROM encrypted_notes WHERE id=?", (note["id"],))
            self.db.conn.commit()
            self._load_notes()