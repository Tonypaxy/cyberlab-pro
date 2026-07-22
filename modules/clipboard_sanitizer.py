import tkinter as tk
from tkinter import messagebox
import re
from gui.base_module import BaseModule

class ClipboardSanitizer(BaseModule):
    def __init__(self, parent, db, logger):
        super().__init__(parent)
        self.db = db
        self.logger = logger

    def build_content(self):
        self.add_title("Clipboard Sanitizer", "Remove sensitive data from text")
        tk.Label(self.inner, text="Paste text:", font=("Courier",10), fg="#fff", bg="#1a1a2e").pack(anchor="w", padx=10)
        self.input_text = tk.Text(self.inner, font=("Courier",9), bg="#0f3460", fg="#fff", relief="flat", height=8)
        self.input_text.pack(fill="x", padx=10, pady=5)
        bf = tk.Frame(self.inner, bg="#1a1a2e")
        bf.pack(fill="x", padx=10, pady=5)
        for t, c in [("Remove IPs",self._rm_ip),("Remove Emails",self._rm_email),("Remove URLs",self._rm_url),("Remove Passwords",self._rm_pass),("Remove Tokens",self._rm_token),("Sanitize All",self._sanitize)]:
            tk.Button(bf, text=t, font=("Courier",8), fg="#000", bg="#00ccff", relief="flat", padx=8, command=c).pack(side="left", padx=2)
        tk.Label(self.inner, text="Output:", font=("Courier",10), fg="#fff", bg="#1a1a2e").pack(anchor="w", padx=10, pady=(10,0))
        self.output_text = tk.Text(self.inner, font=("Courier",9), bg="#0a0a0a", fg="#00ff88", relief="flat", height=8)
        self.output_text.pack(fill="both", expand=True, padx=10, pady=5)
        obf = tk.Frame(self.inner, bg="#1a1a2e")
        obf.pack(fill="x", padx=10, pady=5)
        tk.Button(obf, text="Copy", font=("Courier",10,"bold"), fg="#000", bg="#00ff88", relief="raised", padx=15, pady=6, command=self._copy).pack(side="left", padx=3)
        tk.Button(obf, text="Clear", font=("Courier",10), fg="#fff", bg="#cc0000", relief="raised", padx=15, pady=6, command=self._clear).pack(side="left", padx=3)
        self.status_label = self.add_status("Ready")

    def _get(self): return self.input_text.get("1.0","end-1c")
    def _set(self, t): self.output_text.delete("1.0","end"); self.output_text.insert("1.0",t)
    def _rm_ip(self): t = self._get(); t = re.sub(r"\b(?:\d{1,3}\.){3}\d{1,3}\b","[IP]",t); self._set(t)
    def _rm_email(self): t = self._get(); t = re.sub(r"[\w.-]+@[\w.-]+\.\w+","[EMAIL]",t); self._set(t)
    def _rm_url(self): t = self._get(); t = re.sub(r"https?://\S+","[URL]",t); self._set(t)
    def _rm_pass(self): t = self._get(); t = re.sub(r"password[\s:=]+\S+","[PASS]",t,flags=re.I); self._set(t)
    def _rm_token(self): t = self._get(); t = re.sub(r"[\w-]{24,}\.[\w-]{6,}\.[\w-]{20,}","[TOKEN]",t); self._set(t)
    def _sanitize(self): t = self._get(); t = re.sub(r"\b(?:\d{1,3}\.){3}\d{1,3}\b","[IP]",t); t = re.sub(r"[\w.-]+@[\w.-]+\.\w+","[EMAIL]",t); t = re.sub(r"https?://\S+","[URL]",t); self._set(t)
    def _copy(self): t = self.output_text.get("1.0","end-1c"); self.frame.clipboard_clear(); self.frame.clipboard_append(t)
    def _clear(self): self.input_text.delete("1.0","end"); self.output_text.delete("1.0","end")