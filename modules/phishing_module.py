
import tkinter as tk
from tkinter import ttk, messagebox
import os, subprocess, threading
from gui.base_module import BaseModule
from gui.dropdown import Dropdown

class PhishingModule(BaseModule):
    def __init__(self, parent, db, logger, detector):
        super().__init__(parent)
        self.db = db
        self.logger = logger
        self.detector = detector

    def build_content(self):
        self.add_title("Phishing Tools", "Social engineering and phishing frameworks")
        
        tools = self.detector.detected.get("phishing_social", [])
        if not tools:
            self.create_card("No phishing tools detected", "Install: setoolkit, zphisher, gophish, evilginx2", "#ffaa00")
        
        for tool in tools:
            def make_content(parent, t=tool):
                args = self._get_args(t["name"])
                for arg, desc in args:
                    card = tk.Frame(parent, bg="#16213e", padx=10, pady=6)
                    card.pack(fill="x", pady=1)
                    h = tk.Frame(card, bg="#16213e")
                    h.pack(fill="x")
                    tk.Label(h, text=arg[:25], font=("Courier",9,"bold"), fg="#00ff88", bg="#16213e").pack(side="left")
                    tk.Label(h, text=desc[:35], font=("Courier",8), fg="#888", bg="#16213e").pack(side="left", padx=5)
                    tk.Button(h, text="Run", font=("Courier",7), fg="#000", bg="#00ff88", relief="flat", padx=6,
                            command=lambda a=arg: self._run(t["command"] + " " + a)).pack(side="right", padx=1)
            self.add_section(tool["name"], make_content, "hook")
        
        self.output = tk.Text(self.inner, font=("Courier",9), bg="#0a0a0a", fg="#00ff88", relief="flat", height=10)
        self.output.pack(fill="both", expand=True, padx=10, pady=5)
        self.status = self.add_status("Ready")

    def _get_args(self, name):
        db = {
            "setoolkit": [("-s","Social engineering"),("-p","Phishing vectors"),("-w","Website vectors"),("-q","Quick track"),("-m","Mass mailer"),("-c","Credential harvester"),("-t","Tabnabbing"),("-j","Java applet")],
            "zphisher": [("-p","Pick page"),("-t","Tunnel option"),("-o","Open port"),("-l","Localhost"),("--ngrok","Ngrok tunnel")],
            "blackeye": [("-p","Pick page"),("-t","Tunnel"),("-s","Server")],
            "gophish": [("--port 3333","Admin port"),("--config config.json","Config file"),("-v","Verbose")],
            "evilginx2": [("-p phishlet","Phishlet name"),("-t target.com","Target"),("-g group","Phishlet group"),("--debug","Debug")],
            "modlishka": [("-config config.json","Config"),("-proxy target.com","Proxy"),("-port 443","Port")],
            "muraena": [("-config config.toml","Config"),("-phish phish.toml","Phish config"),("-t target.com","Target")],
            "socialfish": [("-u","Update"),("-c","Check creds"),("-r","Run server"),("-p 8080","Port"),("--ssl","Enable SSL")],
        }
        return db.get(name, [("--help","Show help")])

    def _run(self, cmd):
        self.output.insert("end", "\n$ " + cmd + "\n" + "="*40 + "\n")
        self.output.see("end")
        self.status.config(text="Running...")
        def do():
            try:
                p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                for line in p.stdout:
                    self.output.insert("end", line); self.output.see("end")
                p.wait()
                self.output.insert("end", "\n[Exit: " + str(p.returncode) + "]\n")
                self.status.config(text="Done")
            except Exception as e:
                self.output.insert("end", "\n[X] " + str(e) + "\n")
        threading.Thread(target=do, daemon=True).start()
