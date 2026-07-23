import tkinter as tk
from tkinter import ttk, messagebox
import subprocess, threading, os, shutil, hashlib, base64, binascii
from datetime import datetime
from gui.base_module import BaseModule

class CryptoToolkit(BaseModule):
    def __init__(self, parent, db, logger):
        super().__init__(parent)
        self.db = db; self.logger = logger

    def build_content(self):
        self.add_title("Cryptography Toolkit", "Encrypt, decrypt, hash, encode, crack, keys")
        
        tk.Label(self.inner, text="Input Text/File:", font=("Courier",10), fg="#fff", bg="#1a1a2e").pack(anchor="w", padx=10)
        self.input_text = tk.Text(self.inner, font=("Courier",9), bg="#0f3460", fg="#fff", relief="flat", height=5)
        self.input_text.pack(fill="x", padx=10, pady=3)
        
        tk.Label(self.inner, text="Key/Password:", font=("Courier",10), fg="#fff", bg="#1a1a2e").pack(anchor="w", padx=10)
        self.key_entry = tk.Entry(self.inner, font=("Courier",10), bg="#0f3460", fg="#fff", relief="flat", show="*")
        self.key_entry.pack(fill="x", padx=10, pady=3)
        
        bf = tk.Frame(self.inner, bg="#1a1a2e"); bf.pack(fill="x", padx=10, pady=5)
        
        tools = self._detect_tools()
        for name, func, color in tools:
            tk.Button(bf, text=name, font=("Courier",8), fg="#000", bg=color, relief="flat", padx=6,
                    command=func).pack(side="left", padx=2)
        
        self.output = tk.Text(self.inner, font=("Courier",9), bg="#0a0a0a", fg="#00ff88", relief="flat", height=12)
        self.output.pack(fill="both", expand=True, padx=10, pady=5)
        self.status = self.add_status(f"Ready - {len(tools)} crypto tools available")

    def _get_input(self): return self.input_text.get("1.0","end-1c").strip()
    def _get_key(self): return self.key_entry.get().strip()
    def _set_output(self, text):
        self.output.delete("1.0","end")
        self.output.insert("1.0", text)

    def _detect_tools(self):
        tools = []
        
        # === ENCODING ===
        tools.append(("Base64 Encode", self._b64_encode, "#00ccff"))
        tools.append(("Base64 Decode", self._b64_decode, "#00ccff"))
        tools.append(("Base32 Encode", self._b32_encode, "#00ccff"))
        tools.append(("Base32 Decode", self._b32_decode, "#00ccff"))
        tools.append(("Hex Encode", self._hex_encode, "#00ccff"))
        tools.append(("Hex Decode", self._hex_decode, "#00ccff"))
        tools.append(("URL Encode", self._url_encode, "#00ccff"))
        tools.append(("URL Decode", self._url_decode, "#00ccff"))
        tools.append(("Binary", self._binary, "#00ccff"))
        tools.append(("ROT13", self._rot13, "#00ccff"))
        tools.append(("ROT47", self._rot47, "#00ccff"))
        tools.append(("Morse Encode", self._morse_encode, "#00ccff"))
        tools.append(("Morse Decode", self._morse_decode, "#00ccff"))
        
        # === HASHING ===
        tools.append(("MD5", lambda: self._hash("md5"), "#ffaa00"))
        tools.append(("SHA1", lambda: self._hash("sha1"), "#ffaa00"))
        tools.append(("SHA256", lambda: self._hash("sha256"), "#ffaa00"))
        tools.append(("SHA512", lambda: self._hash("sha512"), "#ffaa00"))
        tools.append(("BLAKE2", lambda: self._hash("blake2b"), "#ffaa00"))
        tools.append(("CRC32", self._crc32, "#ffaa00"))
        tools.append(("All Hashes", self._all_hashes, "#ffaa00"))
        
        # === ENCRYPTION ===
        tools.append(("AES Encrypt", self._aes_encrypt, "#00ff88"))
        tools.append(("AES Decrypt", self._aes_decrypt, "#00ff88"))
        tools.append(("XOR Encrypt", self._xor_encrypt, "#00ff88"))
        tools.append(("XOR Decrypt", self._xor_decrypt, "#00ff88"))
        tools.append(("Fernet Encrypt", self._fernet_encrypt, "#00ff88"))
        tools.append(("Fernet Decrypt", self._fernet_decrypt, "#00ff88"))
        
        # === RSA ===
        tools.append(("RSA Generate", self._rsa_generate, "#ff00ff"))
        tools.append(("RSA Encrypt", self._rsa_encrypt, "#ff00ff"))
        tools.append(("RSA Decrypt", self._rsa_decrypt, "#ff00ff"))
        
        # === PGP/GPG ===
        if shutil.which("gpg"):
            tools.append(("GPG Encrypt", self._gpg_encrypt, "#bc8cff"))
            tools.append(("GPG Decrypt", self._gpg_decrypt, "#bc8cff"))
            tools.append(("GPG Sign", self._gpg_sign, "#bc8cff"))
            tools.append(("GPG Verify", self._gpg_verify, "#bc8cff"))
            tools.append(("GPG Key Gen", lambda: self._cmd("gpg --full-generate-key"), "#bc8cff"))
            tools.append(("GPG List Keys", lambda: self._cmd("gpg --list-keys"), "#bc8cff"))
        
        # === OPENSSL ===
        if shutil.which("openssl"):
            tools.append(("SSL Encrypt", self._ssl_encrypt, "#d2991d"))
            tools.append(("SSL Decrypt", self._ssl_decrypt, "#d2991d"))
            tools.append(("SSL Cert Info", self._ssl_cert, "#d2991d"))
            tools.append(("SSL Key Gen", lambda: self._cmd("openssl genrsa -out key.pem 2048"), "#d2991d"))
            tools.append(("SSL CSR Gen", self._ssl_csr, "#d2991d"))
        
        # === CRACKING ===
        tools.append(("Hash Identifier", self._hash_id, "#ff4444"))
        if shutil.which("john"):
            tools.append(("John Crack", self._john_crack, "#ff0000"))
        if shutil.which("hashcat"):
            tools.append(("Hashcat Crack", self._hashcat_crack, "#ff0000"))
        
        # === UTILITIES ===
        tools.append(("Random Key Gen", self._random_key, "#888888"))
        tools.append(("Password Strength", self._password_strength, "#888888"))
        tools.append(("File Hash", self._file_hash, "#888888"))
        tools.append(("Compare Hashes", self._compare_hash, "#888888"))
        
        return tools

    # === ENCODING ===
    def _b64_encode(self):
        try: self._set_output(base64.b64encode(self._get_input().encode()).decode())
        except Exception as e: self._set_output(f"[X] {e}")
    def _b64_decode(self):
        try: self._set_output(base64.b64decode(self._get_input()).decode())
        except Exception as e: self._set_output(f"[X] {e}")
    def _b32_encode(self):
        try: self._set_output(base64.b32encode(self._get_input().encode()).decode())
        except Exception as e: self._set_output(f"[X] {e}")
    def _b32_decode(self):
        try: self._set_output(base64.b32decode(self._get_input()).decode())
        except Exception as e: self._set_output(f"[X] {e}")
    def _hex_encode(self):
        try: self._set_output(binascii.hexlify(self._get_input().encode()).decode())
        except Exception as e: self._set_output(f"[X] {e}")
    def _hex_decode(self):
        try: self._set_output(binascii.unhexlify(self._get_input()).decode())
        except Exception as e: self._set_output(f"[X] {e}")
    def _url_encode(self):
        from urllib.parse import quote
        self._set_output(quote(self._get_input()))
    def _url_decode(self):
        from urllib.parse import unquote
        self._set_output(unquote(self._get_input()))
    def _binary(self):
        try: self._set_output(" ".join(format(ord(c),'08b') for c in self._get_input()))
        except: pass
    def _rot13(self):
        text = self._get_input()
        result = ""
        for c in text:
            if c.isalpha():
                base = ord('A') if c.isupper() else ord('a')
                result += chr((ord(c) - base + 13) % 26 + base)
            else: result += c
        self._set_output(result)
    def _rot47(self):
        text = self._get_input()
        result = ""
        for c in text:
            if 33 <= ord(c) <= 126:
                result += chr(33 + ((ord(c) - 33 + 47) % 94))
            else: result += c
        self._set_output(result)
    def _morse_encode(self):
        code = {'A':'.-','B':'-...','C':'-.-.','D':'-..','E':'.','F':'..-.','G':'--.','H':'....','I':'..','J':'.---','K':'-.-','L':'.-..','M':'--','N':'-.','O':'---','P':'.--.','Q':'--.-','R':'.-.','S':'...','T':'-','U':'..-','V':'...-','W':'.--','X':'-..-','Y':'-.--','Z':'--..','0':'-----','1':'.----','2':'..---','3':'...--','4':'....-','5':'.....','6':'-....','7':'--...','8':'---..','9':'----.',' ':'/','a':'.-','b':'-...','c':'-.-.','d':'-..','e':'.','f':'..-.','g':'--.','h':'....','i':'..','j':'.---','k':'-.-','l':'.-..','m':'--','n':'-.','o':'---','p':'.--.','q':'--.-','r':'.-.','s':'...','t':'-','u':'..-','v':'...-','w':'.--','x':'-..-','y':'-.--','z':'--..'}
        try: self._set_output(" ".join(code.get(c,'?') for c in self._get_input()))
        except: pass
    def _morse_decode(self):
        code = {'.-':'A','-...':'B','-.-.':'C','-..':'D','.':'E','..-.':'F','--.':'G','....':'H','..':'I','.---':'J','-.-':'K','.-..':'L','--':'M','-.':'N','---':'O','.--.':'P','--.-':'Q','.-.':'R','...':'S','-':'T','..-':'U','...-':'V','.--':'W','-..-':'X','-.--':'Y','--..':'Z','-----':'0','.----':'1','..---':'2','...--':'3','....-':'4','.....':'5','-....':'6','--...':'7','---..':'8','----.':'9','/':' '}
        try: self._set_output("".join(code.get(c,'?') for c in self._get_input().split()))
        except: pass

    # === HASHING ===
    def _hash(self, algo):
        try:
            h = hashlib.new(algo, self._get_input().encode())
            self._set_output(f"{algo.upper()}: {h.hexdigest()}")
        except Exception as e:
            self._set_output(f"[X] {e}")
    def _crc32(self):
        try:
            import zlib
            self._set_output(f"CRC32: {zlib.crc32(self._get_input().encode()):08x}")
        except: pass
    def _all_hashes(self):
        text = self._get_input().encode()
        result = ""
        for algo in ["md5","sha1","sha256","sha512","blake2b"]:
            try:
                h = hashlib.new(algo, text)
                result += f"{algo.upper()}: {h.hexdigest()}\n"
            except: pass
        self._set_output(result)

    # === ENCRYPTION ===
    def _xor_encrypt(self):
        text = self._get_input()
        key = self._get_key() or "cyberlab"
        result = "".join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(text))
        self._set_output(base64.b64encode(result.encode()).decode())
    def _xor_decrypt(self):
        try:
            text = base64.b64decode(self._get_input()).decode()
            key = self._get_key() or "cyberlab"
            result = "".join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(text))
            self._set_output(result)
        except: self._set_output("[X] Invalid base64 input")

    def _aes_encrypt(self):
        try:
            from Crypto.Cipher import AES
            from Crypto.Util.Padding import pad
            key = hashlib.sha256((self._get_key() or "cyberlab").encode()).digest()
            cipher = AES.new(key, AES.MODE_CBC)
            ct = cipher.encrypt(pad(self._get_input().encode(), AES.block_size))
            self._set_output(base64.b64encode(cipher.iv + ct).decode())
        except: self._set_output("[X] Install: pip install pycryptodome")
    def _aes_decrypt(self):
        try:
            from Crypto.Cipher import AES
            from Crypto.Util.Padding import unpad
            raw = base64.b64decode(self._get_input())
            key = hashlib.sha256((self._get_key() or "cyberlab").encode()).digest()
            iv, ct = raw[:16], raw[16:]
            cipher = AES.new(key, AES.MODE_CBC, iv)
            self._set_output(unpad(cipher.decrypt(ct), AES.block_size).decode())
        except: self._set_output("[X] Invalid input or wrong key")

    def _fernet_encrypt(self):
        try:
            from cryptography.fernet import Fernet
            key = base64.urlsafe_b64encode(hashlib.sha256((self._get_key() or "cyberlab").encode()).digest())
            f = Fernet(key)
            self._set_output(f.encrypt(self._get_input().encode()).decode())
        except: self._set_output("[X] Install: pip install cryptography")
    def _fernet_decrypt(self):
        try:
            from cryptography.fernet import Fernet
            key = base64.urlsafe_b64encode(hashlib.sha256((self._get_key() or "cyberlab").encode()).digest())
            f = Fernet(key)
            self._set_output(f.decrypt(self._get_input().encode()).decode())
        except: self._set_output("[X] Invalid input or wrong key")

    def _rsa_generate(self):
        try:
            from Crypto.PublicKey import RSA
            key = RSA.generate(2048)
            private = key.export_key().decode()
            public = key.publickey().export_key().decode()
            self._set_output(f"---PRIVATE KEY---\n{private}\n\n---PUBLIC KEY---\n{public}")
        except: self._set_output("[X] Install: pip install pycryptodome")
    def _rsa_encrypt(self):
        try:
            from Crypto.PublicKey import RSA
            from Crypto.Cipher import PKCS1_OAEP
            key = RSA.import_key(self._get_key() or self._get_input())
            cipher = PKCS1_OAEP.new(key.publickey())
            self._set_output(base64.b64encode(cipher.encrypt(self._get_input()[:200].encode())).decode())
        except: pass
    def _rsa_decrypt(self):
        try:
            from Crypto.PublicKey import RSA
            from Crypto.Cipher import PKCS1_OAEP
            key = RSA.import_key(self._get_key())
            cipher = PKCS1_OAEP.new(key)
            self._set_output(cipher.decrypt(base64.b64decode(self._get_input())).decode())
        except: pass

    def _gpg_encrypt(self): self._cmd(f"echo '{self._get_input()}' | gpg -c --passphrase '{self._get_key()}' --batch -q 2>/dev/null")
    def _gpg_decrypt(self): self._cmd(f"echo '{self._get_input()}' | gpg -d --passphrase '{self._get_key()}' --batch -q 2>/dev/null")
    def _gpg_sign(self): self._cmd(f"echo '{self._get_input()}' | gpg --sign --batch -q 2>/dev/null")
    def _gpg_verify(self): self._cmd(f"gpg --verify 2>/dev/null")

    def _ssl_encrypt(self):
        key = self._get_key() or "cyberlab"
        self._cmd(f"echo '{self._get_input()}' | openssl enc -aes-256-cbc -a -pass pass:{key} 2>/dev/null")
    def _ssl_decrypt(self):
        key = self._get_key() or "cyberlab"
        self._cmd(f"echo '{self._get_input()}' | openssl enc -d -aes-256-cbc -a -pass pass:{key} 2>/dev/null")
    def _ssl_cert(self): self._cmd(f"openssl x509 -in TARGET -text -noout 2>/dev/null || echo 'Paste cert path in target field'")
    def _ssl_csr(self): self._cmd("openssl req -new -newkey rsa:2048 -nodes -keyout key.pem -out csr.pem")

    def _hash_id(self):
        text = self._get_input()
        hlen = len(text)
        ids = []
        if hlen == 32 and all(c in '0123456789abcdef' for c in text.lower()): ids.append("MD5 / MD4 / NTLM")
        if hlen == 40: ids.append("SHA1 / MySQL5")
        if hlen == 64: ids.append("SHA256")
        if hlen == 128: ids.append("SHA512")
        if hlen == 60 and text.startswith("$2"): ids.append("Bcrypt")
        if hlen == 34 and text.startswith("$1$"): ids.append("MD5Crypt")
        if hlen == 98 and text.startswith("$6$"): ids.append("SHA512Crypt")
        if ":" in text and hlen == 65: ids.append("LM:NT")
        self._set_output("Possible types: " + (", ".join(ids) if ids else "Unknown"))

    def _john_crack(self):
        h = self._get_input()
        wl = self._get_key() or os.path.expanduser("~/wordlists/rockyou.txt")
        self._cmd(f"echo '{h}' > /tmp/hash.txt && john --wordlist={wl} /tmp/hash.txt 2>/dev/null && john --show /tmp/hash.txt")

    def _hashcat_crack(self):
        h = self._get_input()
        wl = self._get_key() or os.path.expanduser("~/wordlists/rockyou.txt")
        self._cmd(f"echo '{h}' > /tmp/hash.txt && hashcat -m 0 -a 0 /tmp/hash.txt {wl} --force 2>/dev/null")

    def _random_key(self):
        import secrets, string
        chars = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?"
        key = "".join(secrets.choice(chars) for _ in range(32))
        self._set_output(f"Random Key (32 chars):\n{key}")

    def _password_strength(self):
        pw = self._get_input()
        score = 0
        if len(pw) >= 8: score += 1
        if len(pw) >= 16: score += 1
        if re.search(r'[A-Z]', pw): score += 1
        if re.search(r'[a-z]', pw): score += 1
        if re.search(r'[0-9]', pw): score += 1
        if re.search(r'[^A-Za-z0-9]', pw): score += 1
        rating = ["Very Weak","Weak","Fair","Good","Strong","Very Strong","Excellent"][score]
        self._set_output(f"Password: {'*'*len(pw)}\nLength: {len(pw)}\nScore: {score}/6\nRating: {rating}")

    def _file_hash(self):
        f = self._get_input()
        if not os.path.exists(f):
            self._set_output("[X] File not found. Enter file path.")
            return
        result = ""
        for algo in ["md5","sha1","sha256"]:
            h = hashlib.new(algo)
            with open(f,"rb") as fh:
                while True:
                    chunk = fh.read(8192)
                    if not chunk: break
                    h.update(chunk)
            result += f"{algo.upper()}: {h.hexdigest()}\n"
        self._set_output(result)

    def _compare_hash(self):
        self._set_output("Enter hash in key field, file path in input field.\nChecks MD5/SHA1/SHA256 match.")
        h = self._get_key()
        f = self._get_input()
        if not os.path.exists(f): return
        for algo in ["md5","sha1","sha256"]:
            fh = hashlib.new(algo)
            with open(f,"rb") as fh2:
                while True:
                    chunk = fh2.read(8192)
                    if not chunk: break
                    fh.update(chunk)
            if fh.hexdigest() == h.lower():
                self._set_output(f"[MATCH] {algo.upper()}")
                return
        self._set_output("[NO MATCH]")

    def _cmd(self, cmd):
        self.output.insert("end", f"\n{'='*40}\n$ {cmd[:80]}\n{'='*40}\n\n")
        self.output.see("end")
        def do():
            try:
                p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                out = p.stdout.read()[:5000]
                self.frame.after(0, lambda: self.output.insert("end", out))
                self.frame.after(0, self.output.see("end"))
            except Exception as e:
                self.output.insert("end", f"\n[X] {e}\n")
        threading.Thread(target=do, daemon=True).start()
