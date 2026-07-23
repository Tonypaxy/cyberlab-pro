import tkinter as tk
from tkinter import ttk, messagebox
import subprocess, threading, os, shutil
from datetime import datetime
from gui.base_module import BaseModule

class ReverseEngineering(BaseModule):
    def __init__(self, parent, db, logger):
        super().__init__(parent)
        self.db = db; self.logger = logger
        self.output_dir = os.path.expanduser("~/re_output")
        os.makedirs(self.output_dir, exist_ok=True)

    def build_content(self):
        self.add_title("Reverse Engineering", "Binary analysis, disassembly, decompilation, patching")
        
        tk.Label(self.inner, text="Target Binary:", font=("Courier",10), fg="#fff", bg="#1a1a2e").pack(anchor="w", padx=10)
        self.file_entry = tk.Entry(self.inner, font=("Courier",10), bg="#0f3460", fg="#fff", relief="flat")
        self.file_entry.pack(fill="x", padx=10, pady=3)
        self.file_entry.insert(0, os.path.expanduser("~/target_binary"))
        
        bf = tk.Frame(self.inner, bg="#1a1a2e"); bf.pack(fill="x", padx=10, pady=5)
        
        tools = self._detect_tools()
        for name, func, color in tools:
            tk.Button(bf, text=name, font=("Courier",8), fg="#000", bg=color, relief="flat", padx=6,
                    command=func).pack(side="left", padx=2)
        
        tk.Button(bf, text="FULL RE", font=("Courier",8,"bold"), fg="#fff", bg="#cc0000",
                relief="flat", padx=8, command=self._full_re).pack(side="right", padx=2)
        tk.Button(bf, text="STOP", font=("Courier",8,"bold"), fg="#fff", bg="#cc0000",
                relief="flat", padx=8, command=self._stop).pack(side="right", padx=2)
        
        self.output = tk.Text(self.inner, font=("Courier",9), bg="#0a0a0a", fg="#00ff88", relief="flat", height=15)
        self.output.pack(fill="both", expand=True, padx=10, pady=5)
        self.status = self.add_status(f"Ready - {len(tools)} RE tools detected")

    def _get_file(self):
        return self.file_entry.get().strip()

    def _detect_tools(self):
        tools = []
        f = "FILE"
        
        # === DISASSEMBLERS ===
        if shutil.which("objdump"):
            tools.append(("Objdump -d", lambda: self._cmd(f"objdump -d {f} | head -500"), "#00ccff"))
            tools.append(("Objdump -s", lambda: self._cmd(f"objdump -s {f} | head -200"), "#00ccff"))
            tools.append(("Objdump -t", lambda: self._cmd(f"objdump -t {f}"), "#00ccff"))
            tools.append(("Objdump Full", lambda: self._cmd(f"objdump -x {f} | head -300"), "#00ccff"))
        if shutil.which("ndisasm"):
            tools.append(("NDisasm", lambda: self._cmd(f"ndisasm -b 32 {f} | head -500"), "#00ccff"))
        if shutil.which("capstone-tool"):
            tools.append(("Capstone", lambda: self._cmd(f"capstone-tool -d {f} | head -500"), "#00ccff"))
        if shutil.which("udcli"):
            tools.append(("Udis86", lambda: self._cmd(f"udcli -32 {f} | head -500"), "#00ccff"))
        if shutil.which("zydis"):
            tools.append(("Zydis", lambda: self._cmd(f"zydis -64 {f} | head -500"), "#00ccff"))
        
        # === DECOMPILERS ===
        if shutil.which("ghidra"):
            tools.append(("Ghidra Headless", lambda: self._cmd(f"ghidra-headless {os.path.dirname(f)} {os.path.basename(f)} -import {f}"), "#ffaa00"))
        if shutil.which("radare2"):
            tools.append(("Radare2 Analyze", self._run_radare2, "#ff8800"))
            tools.append(("Radare2 Decompile", lambda: self._cmd(f"r2 -A -q -c 'pdg' {f} | head -500"), "#ff8800"))
            tools.append(("Radare2 Strings", lambda: self._cmd(f"r2 -q -c 'izz' {f} | head -200"), "#ff8800"))
            tools.append(("Radare2 Functions", lambda: self._cmd(f"r2 -q -c 'afl' {f}"), "#ff8800"))
        if shutil.which("rizin"):
            tools.append(("Rizin", lambda: self._cmd(f"rizin -A -q -c 'pdg' {f} | head -500"), "#ff8800"))
        if shutil.which("iaito"):
            tools.append(("Iaito GUI","iaito","#ff8800"))
        if shutil.which("retdec"):
            tools.append(("RetDec", lambda: self._cmd(f"retdec-decompiler {f} -o {self.output_dir}/retdec.c"), "#ffaa00"))
        if shutil.which("snowman"):
            tools.append(("Snowman", lambda: self._cmd(f"snowman {f}"), "#ffaa00"))
        
        # === HEX EDITORS ===
        if shutil.which("hexdump"):
            tools.append(("Hexdump", lambda: self._cmd(f"hexdump -C {f} | head -200"), "#888888"))
        if shutil.which("xxd"):
            tools.append(("XXD", lambda: self._cmd(f"xxd {f} | head -200"), "#888888"))
        if shutil.which("hexedit"):
            tools.append(("Hexedit", lambda: self._cmd(f"hexedit {f}"), "#888888"))
        
        # === BINARY INFO ===
        if shutil.which("file"):
            tools.append(("File Type", lambda: self._cmd(f"file {f}"), "#58a6ff"))
        if shutil.which("size"):
            tools.append(("Size", lambda: self._cmd(f"size {f}"), "#58a6ff"))
        if shutil.which("readelf"):
            tools.append(("ReadELF Header", lambda: self._cmd(f"readelf -h {f}"), "#58a6ff"))
            tools.append(("ReadELF Sections", lambda: self._cmd(f"readelf -S {f}"), "#58a6ff"))
            tools.append(("ReadELF Symbols", lambda: self._cmd(f"readelf -s {f} | head -200"), "#58a6ff"))
            tools.append(("ReadELF Relocs", lambda: self._cmd(f"readelf -r {f}"), "#58a6ff"))
        if shutil.which("nm"):
            tools.append(("NM Symbols", lambda: self._cmd(f"nm -C {f} | head -200"), "#58a6ff"))
        if shutil.which("ldd"):
            tools.append(("LDD Dependencies", lambda: self._cmd(f"ldd {f}"), "#58a6ff"))
        if shutil.which("strace"):
            tools.append(("Strace", lambda: self._cmd(f"strace -f {f} 2>&1 | head -200"), "#d2991d"))
        if shutil.which("ltrace"):
            tools.append(("Ltrace", lambda: self._cmd(f"ltrace {f} 2>&1 | head -200"), "#d2991d"))
        
        # === PATCHING ===
        if shutil.which("radare2"):
            tools.append(("NOP Patch", lambda: self._cmd(f"r2 -w -q -c 'wx 9090909090' {f}"), "#ff4444"))
        if shutil.which("patchelf"):
            tools.append(("PatchELF", lambda: self._cmd(f"patchelf --set-interpreter /lib/ld.so {f}"), "#ff4444"))
        
        # === ANDROID RE ===
        if shutil.which("apktool"):
            tools.append(("APKTool Decode", lambda: self._cmd(f"apktool d {f} -o {self.output_dir}/apktool -f"), "#3fb950"))
        if shutil.which("jadx"):
            tools.append(("JADX Decompile", lambda: self._cmd(f"jadx -d {self.output_dir}/jadx {f}"), "#3fb950"))
        if shutil.which("dex2jar"):
            tools.append(("DEX2JAR", lambda: self._cmd(f"d2j-dex2jar {f} -o {self.output_dir}/output.jar"), "#3fb950"))
        if shutil.which("androguard"):
            tools.append(("Androguard", lambda: self._cmd(f"androguard analyze {f}"), "#3fb950"))
        
        # === .NET RE ===
        if shutil.which("ilspy"):
            tools.append(("ILSpy", lambda: self._cmd(f"ilspycmd {f} -o {self.output_dir}/ilspy"), "#bc8cff"))
        if shutil.which("dnspy"):
            tools.append(("dnSpy","dnspy","#bc8cff"))
        if shutil.which("monodis"):
            tools.append(("Monodis", lambda: self._cmd(f"monodis {f} | head -300"), "#bc8cff"))
        
        # === PYTHON RE ===
        if shutil.which("uncompyle6"):
            tools.append(("Uncompyle6", lambda: self._cmd(f"uncompyle6 {f}"), "#ff00ff"))
        if shutil.which("pycdc"):
            tools.append(("PyCDC", lambda: self._cmd(f"pycdc {f}"), "#ff00ff"))
        
        # === CRYPTO ===
        if shutil.which("hash-identifier"):
            tools.append(("Hash ID", lambda: self._cmd(f"hash-identifier"), "#ff4444"))
        if shutil.which("cyberchef"):
            tools.append(("CyberChef","cyberchef","#39c5cf"))
        
        # === SYSCALL ===
        if shutil.which("strace"):
            tools.append(("Syscalls", lambda: self._cmd(f"strace -c {f} 2>&1 | head -100"), "#d2991d"))
        
        return tools

    def _cmd(self, cmd):
        file = self._get_file()
        if not os.path.exists(file):
            messagebox.showerror("Error", "File not found: " + file); return
        cmd = cmd.replace("FILE", file)
        self.output.insert("end", f"\n{'='*60}\n$ {cmd[:100]}\n{'='*60}\n\n")
        self.output.see("end")
        self.status.config(text="Running...")
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

    def _run_radare2(self):
        file = self._get_file()
        if not os.path.exists(file): return
        self._cmd(f"r2 -A -q -c 'aaa; afl; pdf @main; izz' {file} 2>/dev/null | head -500")

    def _full_re(self):
        for name, func, _ in self._detect_tools()[:15]:
            self.frame.after(500, func)

    def _stop(self):
        self.output.insert("end", "\n[STOPPED]\n")
        self.status.config(text="Stopped")
