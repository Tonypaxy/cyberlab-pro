import tkinter as tk
from tkinter import ttk, messagebox
import subprocess, threading, os, shutil, hashlib
from datetime import datetime
from gui.base_module import BaseModule

class ForensicToolkit(BaseModule):
    def __init__(self, parent, db, logger):
        super().__init__(parent)
        self.db = db; self.logger = logger

    def build_content(self):
        self.add_title("Forensic Toolkit", "Disk imaging, memory dump, file carving, recovery")
        
        tk.Label(self.inner, text="Target (device/file/image):", font=("Courier",10), fg="#fff", bg="#1a1a2e").pack(anchor="w", padx=10)
        self.target_entry = tk.Entry(self.inner, font=("Courier",10), bg="#0f3460", fg="#fff", relief="flat")
        self.target_entry.pack(fill="x", padx=10, pady=3)
        self.target_entry.insert(0, "/dev/block/mmcblk0")
        
        bf = tk.Frame(self.inner, bg="#1a1a2e"); bf.pack(fill="x", padx=10, pady=5)
        
        # Auto-detect forensic tools
        tools = self._detect_tools()
        for name, cmd, color in tools:
            tk.Button(bf, text=name, font=("Courier",8), fg="#000", bg=color, relief="flat", padx=6,
                    command=lambda c=cmd: self._run(c)).pack(side="left", padx=2)
        
        tk.Button(bf, text="STOP", font=("Courier",8,"bold"), fg="#fff", bg="#cc0000", relief="flat", padx=6,
                command=self._stop).pack(side="right", padx=2)
        
        self.output = tk.Text(self.inner, font=("Courier",9), bg="#0a0a0a", fg="#00ff88", relief="flat", height=15)
        self.output.pack(fill="both", expand=True, padx=10, pady=5)
        self.status = self.add_status(f"Ready - {len(tools)} forensic tools detected")

    def _detect_tools(self):
        tools = []
        target = self.target_entry.get().strip() or "/dev/sda"
        output_dir = os.path.expanduser("~/forensics")
        os.makedirs(output_dir, exist_ok=True)
        
        # Disk Imaging
        if shutil.which("dd"):
            tools.append(("DD Image","dd if=TARGET of=" + output_dir + "/image.dd bs=4M status=progress","#00ccff"))
            tools.append(("DD Forensics","dd if=TARGET of=" + output_dir + "/image.dd bs=512 conv=noerror,sync","#00ccff"))
        if shutil.which("dcfldd"):
            tools.append(("dcfldd Hash","dcfldd if=TARGET hash=md5,sha256 hashlog=" + output_dir + "/hash.log of=" + output_dir + "/image.dd","#00ccff"))
        if shutil.which("dc3dd"):
            tools.append(("dc3dd Image","dc3dd if=TARGET of=" + output_dir + "/image.dd hof=" + output_dir + "/image.dd","#00ccff"))
        if shutil.which("guymager"):
            tools.append(("Guymager","guymager","#ffaa00"))
        if shutil.which("ewfacquire"):
            tools.append(("EWF Acquire","ewfacquire TARGET -t " + output_dir + "/evidence","#ffaa00"))
        
        # Memory Forensics
        if shutil.which("volatility3") or shutil.which("vol"):
            tools.append(("Volatility3","vol -f TARGET windows.info","#ff4444"))
            tools.append(("Vol PSList","vol -f TARGET windows.pslist","#ff4444"))
            tools.append(("Vol Netscan","vol -f TARGET windows.netscan","#ff4444"))
            tools.append(("Vol Cmdline","vol -f TARGET windows.cmdline","#ff4444"))
        if shutil.which("volatility2") or shutil.which("volatility"):
            tools.append(("Volatility2","volatility -f TARGET imageinfo","#ff4444"))
        if shutil.which("lime"):
            tools.append(("LiME Capture","insmod lime.ko path=" + output_dir + "/mem.lime format=lime","#ff4444"))
        if shutil.which("avml"):
            tools.append(("AVML","avml " + output_dir + "/mem.avml","#ff4444"))
        if shutil.which("rekall"):
            tools.append(("Rekall","rekall -f TARGET pslist","#ff4444"))
        
        # File Carving
        if shutil.which("foremost"):
            tools.append(("Foremost","foremost -i TARGET -o " + output_dir + "/carved","#00ff88"))
        if shutil.which("scalpel"):
            tools.append(("Scalpel","scalpel TARGET -o " + output_dir + "/scalpel","#00ff88"))
        if shutil.which("photorec"):
            tools.append(("PhotoRec","photorec TARGET","#00ff88"))
        if shutil.which("testdisk"):
            tools.append(("TestDisk","testdisk TARGET","#ffaa00"))
        if shutil.which("bulk_extractor"):
            tools.append(("Bulk Extractor","bulk_extractor TARGET -o " + output_dir + "/bulk","#00ff88"))
        
        # Metadata Analysis
        if shutil.which("exiftool"):
            tools.append(("ExifTool","exiftool -r TARGET","#bc8cff"))
        if shutil.which("strings"):
            tools.append(("Strings","strings -n 8 TARGET","#888888"))
        if shutil.which("binwalk"):
            tools.append(("Binwalk","binwalk -Me TARGET","#ff00ff"))
        
        # Filesystem Analysis
        if shutil.which("fsstat"):
            tools.append(("FSStat","fsstat TARGET","#58a6ff"))
        if shutil.which("fls"):
            tools.append(("FLS List","fls -r TARGET","#58a6ff"))
        if shutil.which("icat"):
            tools.append(("ICAT Extract","icat TARGET INODE > " + output_dir + "/extracted","#58a6ff"))
        if shutil.which("tcpflow"):
            tools.append(("TCPFlow","tcpflow -r TARGET","#39c5cf"))
        
        # Timeline
        if shutil.which("mactime"):
            tools.append(("Mactime","mactime -b bodyfile -d","#d2991d"))
        if shutil.which("log2timeline"):
            tools.append(("Log2Timeline","log2timeline " + output_dir + "/timeline.plaso TARGET","#d2991d"))
        
        # Hash verification
        if shutil.which("md5sum") or shutil.which("md5"):
            tools.append(("MD5","md5sum TARGET","#666666"))
        if shutil.which("sha256sum") or shutil.which("sha256"):
            tools.append(("SHA256","sha256sum TARGET","#666666"))
        
        # Disk Utils
        if shutil.which("fdisk"):
            tools.append(("FDisk","fdisk -l TARGET","#888888"))
        if shutil.which("parted"):
            tools.append(("Parted","parted TARGET print","#888888"))
        if shutil.which("mount"):
            tools.append(("Mount RO","mount -o ro,noexec TARGET /mnt/forensics","#888888"))
        
        # Anti-Forensics Detection
        if shutil.which("chkrootkit"):
            tools.append(("Chkrootkit","chkrootkit","#ff4444"))
        if shutil.which("rkhunter"):
            tools.append(("Rkhunter","rkhunter --check","#ff4444"))
        
        # Auto-detect future forensic tools
        for path in os.environ.get("PATH","").split(":"):
            try:
                for f in os.listdir(path):
                    fpath = os.path.join(path,f)
                    if os.access(fpath, os.X_OK) and f not in [t[1].split()[0] for t in tools]:
                        try:
                            r = subprocess.run([f,"--help"], capture_output=True, text=True, timeout=3)
                            h = (r.stdout + r.stderr).lower()
                            if any(kw in h for kw in ["forensic","carving","recovery","imaging","memory dump","file system","partition","extract","evidence","analysis"]):
                                known = ["dd","dcfldd","dc3dd","guymager","ewfacquire","volatility3","vol","volatility2","volatility","lime","avml","rekall","foremost","scalpel","photorec","testdisk","bulk_extractor","exiftool","strings","binwalk","fsstat","fls","icat","tcpflow","mactime","log2timeline","md5sum","sha256sum","fdisk","parted","mount","chkrootkit","rkhunter"]
                                if f not in known:
                                    tools.append((f" {f.title()}","{f} TARGET","#666666"))
                        except: pass
            except: pass
        
        return tools

    def _run(self, cmd):
        target = self.target_entry.get().strip()
        if not target: return
        cmd = cmd.replace("TARGET", target)
        
        self.output.insert("end", f"\n{'='*60}\n$ {cmd[:80]}\n{'='*60}\n\n")
        self.output.see("end")
        self.status.config(text=f"Running: {cmd.split()[0]}...")
        
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
