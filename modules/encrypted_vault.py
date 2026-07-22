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
        self.db.cursor.execute("""CREATE TABLE IF NOT EXISTS encrypted_notes 
            (id INTEGER PRIMARY KEY AUTOINCREMENT, project_id INTEGER, title TEXT, 
             content TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")
        self.db.conn.commit()

    def _encrypt(self, text, password):
        result = []
        for i, c in enumerate(text):
            key_char = password[i % len(password)]
            result.append(chr(ord(c) ^ ord(key_char)))
        return base64.b64encode("".join(result).encode()).decode()

    def _decrypt(self, encoded, password):
        try:
            text = base64.b64decode(encoded).decode()
            result = []
            for i, c in enumerate(text):
                key_char = password[i % len(password)]
                result.append(chr(ord(c) ^ ord(key_char)))
            return "".join(result)
        except:
            return None

    def build_content(self):
        self.add_title("Encrypted Vault", "Password-protected notes and files")
        
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
        self.pwd_entry.bind("<Return>", lambda e: self._unlock())
        
        bf = tk.Frame(pf2, bg="#16213e")
        bf.pack(fill="x", pady=5)
        tk.Button(bf, text="Unlock Vault", font=("Courier",10,"bold"), fg="#000", bg="#00ff88",
                relief="raised", padx=15, pady=6, command=self._unlock).pack(side="left", padx=3)
        tk.Button(bf, text="Encrypt File", font=("Courier",10), fg="#000", bg="#ffaa00",
                relief="raised", padx=15, pady=6, command=self._encrypt_file).pack(side="left", padx=3)
        tk.Button(bf, text="Decrypt File", font=("Courier",10), fg="#000", bg="#cc88ff",
                relief="raised", padx=15, pady=6, command=self._decrypt_file).pack(side="left", padx=3)

        self.vault_frame = tk.Frame(self.inner, bg="#1a1a2e")
        self.vault_frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.status_label = self.add_status("Enter password and click Unlock Vault")

    def _set_project(self, name):
        for p in self.db.get_all_projects():
            if p["name"] == name: self.current_project = p; break

    def _unlock(self):
        self.vault_key = self.pwd_entry.get().strip()
        if not self.vault_key:
            messagebox.showwarning("Warning", "Enter a password")
            return
        self._load_notes()

    def _load_notes(self):
        for w in self.vault_frame.winfo_children(): w.destroy()
        if not self.current_project: return
        
        tk.Button(self.vault_frame, text="+ New Encrypted Note", font=("Courier",10,"bold"),
                fg="#000", bg="#00ff88", relief="raised", padx=15, pady=6,
                command=self._new_note).pack(pady=5)

        self.db.cursor.execute("SELECT * FROM encrypted_notes WHERE project_id=? ORDER BY created_at DESC",
                (self.current_project["id"],))
        notes = [dict(r) for r in self.db.cursor.fetchall()]

        if not notes:
            tk.Label(self.vault_frame, text="No encrypted notes yet", font=("Courier",10),
                    fg="#888", bg="#1a1a2e").pack(pady=20)
            self.status_label.config(text="Vault unlocked - empty")
            return

        self.status_label.config(text="Vault unlocked - " + str(len(notes)) + " notes")
        for note in notes:
            title = self._decrypt(note.get("title",""), self.vault_key)
            if title is None:
                title = "[Wrong password]"
            
            card = tk.Frame(self.vault_frame, bg="#16213e", padx=10, pady=8)
            card.pack(fill="x", pady=2)
            h = tk.Frame(card, bg="#16213e")
            h.pack(fill="x")
            tk.Label(h, text=title, font=("Courier",10,"bold"), fg="#ff4488", bg="#16213e").pack(side="left")
            ts = note.get("created_at","")
            if ts: tk.Label(h, text=str(ts)[:19], font=("Courier",8), fg="#666", bg="#16213e").pack(side="right")
            bf = tk.Frame(card, bg="#16213e")
            bf.pack(fill="x")
            tk.Button(bf, text="View", font=("Courier",8), fg="#000", bg="#00ccff", relief="flat", padx=8,
                    command=lambda n=note: self._view_note(n)).pack(side="left", padx=1)
            tk.Button(bf, text="Delete", font=("Courier",8), fg="#fff", bg="#cc0000", relief="flat", padx=8,
                    command=lambda n=note: self._delete_note(n)).pack(side="left", padx=1)

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
            enc_title = self._encrypt(title, self.vault_key)
            enc_content = self._encrypt(content, self.vault_key)
            self.db.cursor.execute("INSERT INTO encrypted_notes (project_id, title, content) VALUES (?,?,?)",
                    (self.current_project["id"], enc_title, enc_content))
            self.db.conn.commit()
            d.destroy()
            self._load_notes()
        tk.Button(d, text="Save Encrypted", font=("Courier",10,"bold"), fg="#000", bg="#ff4488",
                relief="raised", padx=20, pady=8, command=save).pack(pady=10)

    def _view_note(self, note):
        title = self._decrypt(note.get("title",""), self.vault_key)
        content = self._decrypt(note.get("content",""), self.vault_key)
        if title is None:
            messagebox.showerror("Error", "Wrong password or corrupted data")
            return
        d = tk.Toplevel(self.frame, bg="#1a1a2e")
        d.title(title); d.geometry("550x400")
        tk.Label(d, text=title, font=("Courier",12,"bold"), fg="#ff4488", bg="#1a1a2e").pack(pady=10)
        t = tk.Text(d, font=("Courier",10), bg="#0a0a0a", fg="#00ff88", relief="flat")
        t.pack(fill="both", expand=True, padx=10, pady=10)
        t.insert("1.0", content)
        t.config(state="disabled")
        tk.Button(d, text="Close", font=("Courier",10), fg="#fff", bg="#666", relief="raised", padx=15, pady=5, command=d.destroy).pack(pady=5)

    def _delete_note(self, note):
        if messagebox.askyesno("Delete", "Delete this encrypted note?"):
            self.db.cursor.execute("DELETE FROM encrypted_notes WHERE id=?", (note["id"],))
            self.db.conn.commit()
            self._load_notes()

    def _encrypt_file(self):
        password = self.pwd_entry.get().strip()
        if not password:
            messagebox.showwarning("Warning", "Enter a password first")
            return
        d = tk.Toplevel(self.frame, bg="#1a1a2e")
        d.title("Encrypt File"); d.geometry("500x300")
        tk.Label(d, text="Encrypt File", font=("Courier",14,"bold"), fg="#ffaa00", bg="#1a1a2e").pack(pady=10)
        tk.Label(d, text="File path:", font=("Courier",10), fg="#fff", bg="#1a1a2e").pack(anchor="w", padx=20)
        path_e = tk.Entry(d, font=("Courier",10), bg="#16213e", fg="#fff", relief="flat")
        path_e.pack(fill="x", padx=20, pady=5)
        tk.Label(d, text="Output (leave blank for .enc):", font=("Courier",10), fg="#fff", bg="#1a1a2e").pack(anchor="w", padx=20)
        out_e = tk.Entry(d, font=("Courier",10), bg="#16213e", fg="#fff", relief="flat")
        out_e.pack(fill="x", padx=20, pady=5)
        def encrypt():
            fpath = path_e.get().strip()
            if not fpath or not os.path.isfile(fpath):
                messagebox.showerror("Error", "File not found"); return
            out_path = out_e.get().strip() or fpath + ".enc"
            try:
                with open(fpath, "rb") as f:
                    data = f.read()
                text = base64.b64encode(data).decode()
                encrypted = self._encrypt(text, password)
                with open(out_path, "w") as f:
                    f.write(encrypted)
                messagebox.showinfo("Done", "File encrypted: " + out_path)
                d.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        tk.Button(d, text="Encrypt File", font=("Courier",10,"bold"), fg="#000", bg="#ffaa00",
                relief="raised", padx=15, pady=8, command=encrypt).pack(pady=10)

    def _decrypt_file(self):
        password = self.pwd_entry.get().strip()
        if not password:
            messagebox.showwarning("Warning", "Enter a password first")
            return
        d = tk.Toplevel(self.frame, bg="#1a1a2e")
        d.title("Decrypt File"); d.geometry("500x300")
        tk.Label(d, text="Decrypt File", font=("Courier",14,"bold"), fg="#cc88ff", bg="#1a1a2e").pack(pady=10)
        tk.Label(d, text="Encrypted file path:", font=("Courier",10), fg="#fff", bg="#1a1a2e").pack(anchor="w", padx=20)
        path_e = tk.Entry(d, font=("Courier",10), bg="#16213e", fg="#fff", relief="flat")
        path_e.pack(fill="x", padx=20, pady=5)
        tk.Label(d, text="Output (leave blank for original):", font=("Courier",10), fg="#fff", bg="#1a1a2e").pack(anchor="w", padx=20)
        out_e = tk.Entry(d, font=("Courier",10), bg="#16213e", fg="#fff", relief="flat")
        out_e.pack(fill="x", padx=20, pady=5)
        def decrypt():
            fpath = path_e.get().strip()
            if not fpath or not os.path.isfile(fpath):
                messagebox.showerror("Error", "File not found"); return
            out_path = out_e.get().strip() or fpath.replace(".enc", "")
            try:
                with open(fpath, "r") as f:
                    encrypted = f.read()
                decrypted = self._decrypt(encrypted, password)
                if decrypted is None:
                    messagebox.showerror("Error", "Wrong password or corrupted file"); return
                data = base64.b64decode(decrypted)
                with open(out_path, "wb") as f:
                    f.write(data)
                messagebox.showinfo("Done", "File decrypted: " + out_path)
                d.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        tk.Button(d, text="Decrypt File", font=("Courier",10,"bold"), fg="#000", bg="#cc88ff",
                relief="raised", padx=15, pady=8, command=decrypt).pack(pady=10)
