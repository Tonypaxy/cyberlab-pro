
import tkinter as tk
from tkinter import ttk, messagebox
import json, os, threading, subprocess, time
from datetime import datetime
from gui.base_module import BaseModule

class MacroRecorder(BaseModule):
    def __init__(self, parent, db, logger):
        super().__init__(parent)
        self.db = db
        self.logger = logger
        self.macros = []
        self.recording = False
        self.playing = False
        self.current_macro = []
        self.macro_dir = os.path.expanduser("~/cyberlab_macros")
        os.makedirs(self.macro_dir, exist_ok=True)
        self._load_macros()

    def _load_macros(self):
        self.macros = []
        for f in os.listdir(self.macro_dir):
            if f.endswith(".json"):
                try:
                    with open(os.path.join(self.macro_dir, f)) as fh:
                        self.macros.append(json.load(fh))
                except: pass

    def build_content(self):
        self.add_title("Macro Recorder", "Record and replay sequences of commands for automation")
        
        # Record section
        def rec_content(parent):
            tk.Label(parent, text="Step Command:", font=("Courier",10), fg="#fff", bg="#1a1a2e").pack(anchor="w")
            self.cmd_entry = tk.Entry(parent, font=("Courier",10), bg="#0f3460", fg="#fff", relief="flat")
            self.cmd_entry.pack(fill="x", pady=3)
            self.cmd_entry.bind("<Return>", lambda e: self._add_step())
            
            bf = tk.Frame(parent, bg="#1a1a2e")
            bf.pack(fill="x", pady=5)
            tk.Button(bf, text="Add Step", font=("Courier",9), fg="#000", bg="#00ccff", relief="flat", padx=10, command=self._add_step).pack(side="left", padx=2)
            tk.Button(bf, text="Start Recording", font=("Courier",9,"bold"), fg="#000", bg="#ff0000", relief="flat", padx=10, command=self._toggle_recording).pack(side="left", padx=2)
            tk.Button(bf, text="Clear Steps", font=("Courier",9), fg="#fff", bg="#cc0000", relief="flat", padx=10, command=self._clear_steps).pack(side="left", padx=2)
            
            self.steps_label = tk.Label(parent, text="No steps added", font=("Courier",9), fg="#888", bg="#1a1a2e")
            self.steps_label.pack(anchor="w", pady=3)
            
            tk.Label(parent, text="Macro Name:", font=("Courier",10), fg="#fff", bg="#1a1a2e").pack(anchor="w", pady=(10,0))
            self.name_entry = tk.Entry(parent, font=("Courier",10), bg="#0f3460", fg="#fff", relief="flat")
            self.name_entry.pack(fill="x", pady=3)
            self.name_entry.insert(0, "my_macro")
            
            tk.Button(parent, text="Save Macro", font=("Courier",10,"bold"), fg="#000", bg="#00ff88", relief="raised", padx=15, pady=6, command=self._save_macro).pack(pady=10)
        
        self.add_section("Create Macro", rec_content, "record", default_open=True)
        
        # Saved macros
        def saved_content(parent):
            if not self.macros:
                tk.Label(parent, text="No saved macros", font=("Courier",9), fg="#888", bg="#1a1a2e").pack(pady=10)
            for macro in self.macros:
                card = tk.Frame(parent, bg="#16213e", padx=10, pady=8)
                card.pack(fill="x", pady=2)
                h = tk.Frame(card, bg="#16213e")
                h.pack(fill="x")
                tk.Label(h, text=macro.get("name","Unnamed"), font=("Courier",10,"bold"), fg="#00ff88", bg="#16213e").pack(side="left")
                tk.Label(h, text=str(len(macro.get("steps",[]))) + " steps", font=("Courier",8), fg="#888", bg="#16213e").pack(side="right")
                bf = tk.Frame(card, bg="#16213e")
                bf.pack(fill="x")
                tk.Button(bf, text="Play", font=("Courier",8), fg="#000", bg="#00ff88", relief="flat", padx=8, command=lambda m=macro: self._play_macro(m)).pack(side="left", padx=1)
                tk.Button(bf, text="Edit", font=("Courier",8), fg="#000", bg="#00ccff", relief="flat", padx=8, command=lambda m=macro: self._edit_macro(m)).pack(side="left", padx=1)
                tk.Button(bf, text="Delete", font=("Courier",8), fg="#fff", bg="#cc0000", relief="flat", padx=8, command=lambda m=macro: self._delete_macro(m)).pack(side="left", padx=1)
        
        self.add_section("Saved Macros", saved_content, "play", default_open=True)
        
        # Output
        self.output = tk.Text(self.inner, font=("Courier",9), bg="#0a0a0a", fg="#00ff88", relief="flat", height=8)
        self.output.pack(fill="both", expand=True, padx=10, pady=5)
        self.status = self.add_status("Ready - Add commands and save as macro")

    def _add_step(self):
        cmd = self.cmd_entry.get().strip()
        if not cmd: return
        self.current_macro.append({"command": cmd, "delay": 1})
        self.cmd_entry.delete(0, "end")
        self.steps_label.config(text=str(len(self.current_macro)) + " steps: " + ", ".join(s["command"][:20] for s in self.current_macro[-5:]))

    def _toggle_recording(self):
        self.recording = not self.recording
        msg = "RECORDING - commands will be captured" if self.recording else "Recording stopped"
        self.output.insert("end", "\n[*] " + msg + "\n")
        self.status.config(text=msg)

    def _clear_steps(self):
        self.current_macro = []
        self.steps_label.config(text="No steps added")

    def _save_macro(self):
        name = self.name_entry.get().strip()
        if not name: messagebox.showwarning("Warning", "Enter macro name"); return
        if not self.current_macro: messagebox.showwarning("Warning", "Add at least one step"); return
        
        macro = {
            "name": name,
            "steps": self.current_macro,
            "created": str(datetime.now()),
            "description": ""
        }
        fpath = os.path.join(self.macro_dir, name + ".json")
        with open(fpath, "w") as f: json.dump(macro, f, indent=2)
        self._load_macros()
        self.current_macro = []
        self.steps_label.config(text="No steps added")
        messagebox.showinfo("Saved", "Macro saved: " + name)
        self._refresh()

    def _play_macro(self, macro):
        if self.playing:
            messagebox.showwarning("Warning", "Already playing a macro")
            return
        self.playing = True
        self.output.insert("end", "\n[*] Playing macro: " + macro["name"] + " (" + str(len(macro["steps"])) + " steps)\n")
        self.output.see("end")
        
        def do():
            for i, step in enumerate(macro["steps"]):
                if not self.playing: break
                cmd = step["command"]
                delay = step.get("delay", 1)
                self.output.insert("end", "\n$ " + cmd + "\n")
                self.output.see("end")
                self.status.config(text="Step " + str(i+1) + "/" + str(len(macro["steps"])) + ": " + cmd[:40])
                try:
                    p = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
                    self.output.insert("end", p.stdout[-500:] if p.stdout else "(no output)\n")
                    if p.stderr: self.output.insert("end", p.stderr[-200:])
                except Exception as e:
                    self.output.insert("end", "[X] " + str(e) + "\n")
                self.output.see("end")
                time.sleep(delay)
            self.output.insert("end", "\n[*] Macro complete\n")
            self.status.config(text="Macro complete")
            self.playing = False
        threading.Thread(target=do, daemon=True).start()

    def _edit_macro(self, macro):
        self.current_macro = macro["steps"]
        self.name_entry.delete(0, "end")
        self.name_entry.insert(0, macro["name"])
        self.steps_label.config(text=str(len(self.current_macro)) + " steps loaded for editing")
        self.status.config(text="Editing: " + macro["name"] + " - modify and Save Macro")

    def _delete_macro(self, macro):
        if messagebox.askyesno("Delete", "Delete macro '" + macro["name"] + "'?"):
            fpath = os.path.join(self.macro_dir, macro["name"] + ".json")
            if os.path.exists(fpath): os.remove(fpath)
            self._load_macros()
            self._refresh()

    def _refresh(self):
        for w in self.inner.winfo_children(): w.destroy()
        self.build_content()
