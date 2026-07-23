import tkinter as tk
from tkinter import ttk, messagebox
import subprocess, threading, os, shutil
from datetime import datetime
from gui.base_module import BaseModule

class StegoToolkit(BaseModule):
    def __init__(self, parent, db, logger):
        super().__init__(parent)
        self.db = db; self.logger = logger

    def build_content(self):
        self.add_title("Steganography Toolkit", "Hide and extract data in images, audio, video, text")
        
        tk.Label(self.inner, text="Target File:", font=("Courier",10), fg="#fff", bg="#1a1a2e").pack(anchor="w", padx=10)
        self.target_entry = tk.Entry(self.inner, font=("Courier",10), bg="#0f3460", fg="#fff", relief="flat")
        self.target_entry.pack(fill="x", padx=10, pady=3)
        self.target_entry.insert(0, "image.png")
        
        tk.Label(self.inner, text="Secret File (for embedding):", font=("Courier",10), fg="#fff", bg="#1a1a2e").pack(anchor="w", padx=10)
        self.secret_entry = tk.Entry(self.inner, font=("Courier",10), bg="#0f3460", fg="#fff", relief="flat")
        self.secret_entry.pack(fill="x", padx=10, pady=3)
        self.secret_entry.insert(0, "secret.txt")
        
        tk.Label(self.inner, text="Password (optional):", font=("Courier",10), fg="#fff", bg="#1a1a2e").pack(anchor="w", padx=10)
        self.pass_entry = tk.Entry(self.inner, font=("Courier",10), bg="#0f3460", fg="#fff", relief="flat", show="*")
        self.pass_entry.pack(fill="x", padx=10, pady=3)
        
        bf = tk.Frame(self.inner, bg="#1a1a2e"); bf.pack(fill="x", padx=10, pady=5)
        
        tools = self._detect_tools()
        for name, cmd, color in tools:
            tk.Button(bf, text=name, font=("Courier",8), fg="#000", bg=color, relief="flat", padx=6,
                    command=lambda c=cmd: self._run(c)).pack(side="left", padx=2)
        
        tk.Button(bf, text="STOP", font=("Courier",8,"bold"), fg="#fff", bg="#cc0000", relief="flat", padx=6,
                command=self._stop).pack(side="right", padx=2)
        
        self.output = tk.Text(self.inner, font=("Courier",9), bg="#0a0a0a", fg="#00ff88", relief="flat", height=15)
        self.output.pack(fill="both", expand=True, padx=10, pady=5)
        self.status = self.add_status(f"Ready - {len(tools)} stego tools detected")

    def _detect_tools(self):
        tools = []
        
        # === IMAGE STEGO ===
        if shutil.which("steghide"):
            tools.append(("Steghide Embed","steghide embed -cf FILE -ef SECRET -p PASS","#00ff88"))
            tools.append(("Steghide Extract","steghide extract -sf FILE -p PASS","#00ff88"))
            tools.append(("Steghide Info","steghide info FILE","#00ff88"))
        if shutil.which("zsteg"):
            tools.append(("Zsteg All","zsteg -a FILE","#ffaa00"))
            tools.append(("Zsteg LSB","zsteg FILE","#ffaa00"))
            tools.append(("Zsteg Extract","zsteg -E b1,rgb,lsb,xy FILE > extracted","#ffaa00"))
        if shutil.which("stegsolve"):
            tools.append(("Stegsolve","stegsolve FILE","#ff4444"))
        if shutil.which("stegcracker"):
            tools.append(("Stegcrack","stegcracker FILE wordlist.txt","#ff4444"))
        if shutil.which("stegoveritas"):
            tools.append(("Stegoveritas","stegoveritas.py FILE","#ff00ff"))
        if shutil.which("stegano"):
            tools.append(("Stegano LSB","stegano-lsb hide -i FILE -m 'secret' -o output.png","#bc8cff"))
            tools.append(("Stegano Reveal","stegano-lsb reveal -i FILE","#bc8cff"))
        if shutil.which("stegano-red"):
            tools.append(("Stegano Red","stegano-red hide -i FILE -m 'secret' -o output.png","#bc8cff"))
        if shutil.which("outguess"):
            tools.append(("Outguess","outguess -k PASS -d SECRET FILE output.jpg","#00ccff"))
            tools.append(("Outguess Extract","outguess -k PASS -r FILE extracted.txt","#00ccff"))
        if shutil.which("jsteg"):
            tools.append(("JSteg","jsteg hide FILE SECRET output.jpg","#00ccff"))
            tools.append(("JSteg Reveal","jsteg reveal FILE output.txt","#00ccff"))
        if shutil.which("jphide"):
            tools.append(("JPHide","jphide FILE output.jpg SECRET","#00ccff"))
        if shutil.which("jpseek"):
            tools.append(("JPSeek","jpseek FILE output.txt","#00ccff"))
        if shutil.which("f5"):
            tools.append(("F5 Embed","f5 -e SECRET FILE -p PASS output.jpg","#d2991d"))
            tools.append(("F5 Extract","f5 -x FILE -p PASS output.txt","#d2991d"))
        if shutil.which("openstego"):
            tools.append(("OpenStego","openstego embed -a LSB -mf SECRET -cf FILE -p PASS -sf output.png","#3fb950"))
        if shutil.which("stegspy"):
            tools.append(("StegSpy","stegspy FILE","#ff4444"))
        
        # === AUDIO STEGO ===
        if shutil.which("steghide"):
            tools.append(("Audio Embed","steghide embed -cf FILE -ef SECRET -p PASS","#ffaa00"))
            tools.append(("Audio Extract","steghide extract -sf FILE -p PASS","#ffaa00"))
        if shutil.which("deep-sound"):
            tools.append(("DeepSound","deep-sound","#ff8800"))
        if shutil.which("mp3stego"):
            tools.append(("MP3Stego","mp3stego -E SECRET -P PASS FILE output.mp3","#ff8800"))
            tools.append(("MP3Stego Decode","mp3stego -D -P PASS FILE","#ff8800"))
        if shutil.which("spectrology"):
            tools.append(("Spectrology","spectrology FILE output.wav","#bc8cff"))
        if shutil.which("wavsteg"):
            tools.append(("WavSteg","wavsteg -r FILE -o output.txt -n 2","#bc8cff"))
        
        # === VIDEO STEGO ===
        if shutil.which("ffmpeg"):
            tools.append(("FFmpeg Frame","ffmpeg -i FILE -vf fps=1 frames/%04d.png","#39c5cf"))
        if shutil.which("tcsteg"):
            tools.append(("TCSteg","tcsteg -i FILE -o output.mp4 -m 'secret'","#39c5cf"))
        
        # === TEXT STEGO ===
        if shutil.which("snow"):
            tools.append(("Snow Hide","snow -C -p PASS -m 'secret' FILE output.txt","#888888"))
            tools.append(("Snow Reveal","snow -C -p PASS FILE","#888888"))
        if shutil.which("stegano"):
            tools.append(("Text Hide","stegano-lsb-set hide -i FILE -m 'secret' -o output.txt","#888888"))
        if shutil.which("cloakify"):
            tools.append(("Cloakify","cloakify.py SECRET output.txt","#888888"))
            tools.append(("Decloakify","decloakify.py FILE output.txt","#888888"))
        
        # === PDF STEGO ===
        if shutil.which("pdf-parser"):
            tools.append(("PDF Parse","pdf-parser.py FILE","#ff4444"))
        if shutil.which("pdfid"):
            tools.append(("PDF ID","pdfid.py FILE","#ff4444"))
        if shutil.which("peepdf"):
            tools.append(("PeePDF","peepdf.py FILE","#ff4444"))
        
        # === NETWORK STEGO ===
        if shutil.which("steghide"):
            tools.append(("Pcap Hide","steghide embed -cf capture.pcap -ef SECRET","#58a6ff"))
        if shutil.which("netstego"):
            tools.append(("NetStego","netstego","#58a6ff"))
        
        # === DETECTION ===
        if shutil.which("stegdetect"):
            tools.append(("StegDetect","stegdetect FILE","#ff0000"))
            tools.append(("StegDetect All","stegdetect -tall FILE","#ff0000"))
        if shutil.which("stegseek"):
            tools.append(("StegSeek","stegseek FILE wordlist.txt","#ff0000"))
        if shutil.which("binwalk"):
            tools.append(("Binwalk","binwalk -Me FILE","#00ff88"))
        if shutil.which("foremost"):
            tools.append(("Foremost","foremost -i FILE -o output/","#00ff88"))
        if shutil.which("strings"):
            tools.append(("Strings","strings -n 8 FILE","#888888"))
        if shutil.which("exiftool"):
            tools.append(("ExifTool","exiftool FILE","#bc8cff"))
            tools.append(("ExifTool All","exiftool -a -G1 FILE","#bc8cff"))
        
        # === COVERT CHANNELS ===
        if shutil.which("pingtunnel"):
            tools.append(("ICMP Tunnel","pingtunnel -s SECRET FILE","#d2991d"))
        if shutil.which("dnscat2"):
            tools.append(("DNS Tunnel","dnscat2 --dns server=IP,port=53","#d2991d"))
        
        return tools

    def _run(self, cmd):
        target = self.target_entry.get().strip()
        secret = self.secret_entry.get().strip()
        password = self.pass_entry.get().strip()
        
        cmd = cmd.replace("FILE", target).replace("SECRET", secret).replace("PASS", password)
        
        self.output.insert("end", f"\n{'='*60}\n$ {cmd[:80]}\n{'='*60}\n\n")
        self.output.see("end")
        self.status.config(text=f"Running...")
        
        def do():
            try:
                p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                for line in p.stdout:
                    self.output.insert("end", line); self.output.see("end")
                p.wait()
                self.status.config(text=f"Done - Exit: {p.returncode}")
            except Exception as e:
                self.output.insert("end", f"\n[X] {e}\n")
        threading.Thread(target=do, daemon=True).start()

    def _stop(self):
        self.output.insert("end", "\n[STOPPED]\n")
        self.status.config(text="Stopped")
