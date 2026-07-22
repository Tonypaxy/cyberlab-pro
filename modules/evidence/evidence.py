import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import shutil
from datetime import datetime

class EvidenceModule:
    def __init__(self, parent, db, logger):
        self.parent = parent
        self.db = db
        self.logger = logger
        self.frame = tk.Frame(parent, bg='#1a1a2e')
        self.current_project = None
    
    def build(self):
        self.frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Header
        header = tk.Frame(self.frame, bg='#1a1a2e')
        header.pack(fill='x', pady=(0,10))
        
        tk.Label(header, text="Evidence Locker", font=('Courier', 18, 'bold'),
                fg='#00ff88', bg='#1a1a2e').pack(side='left')
        
        tk.Button(header, text="+ Add Evidence", font=('Courier', 10),
                fg='#000', bg='#00ff88', relief='flat', padx=10, pady=5,
                command=self._add_evidence).pack(side='right')
        
        # Project selector
        proj_frame = tk.Frame(self.frame, bg='#16213e', padx=10, pady=10)
        proj_frame.pack(fill='x', pady=5)
        
        tk.Label(proj_frame, text="Project:", font=('Courier', 10),
                fg='#fff', bg='#16213e').pack(side='left')
        
        self.project_var = tk.StringVar()
        projects = self.db.get_all_projects()
        names = [p['name'] for p in projects]
        if names:
            self.proj_menu = ttk.Combobox(proj_frame, textvariable=self.project_var,
                    values=names, font=('Courier', 10), state='readonly', width=25)
            self.proj_menu.pack(side='left', padx=10)
            self.proj_menu.set(names[0])
            self.proj_menu.bind('<<ComboboxSelected>>', lambda e: self._load_evidence())
            self._set_project(names[0])
        
        tk.Button(proj_frame, text="Refresh", font=('Courier', 9),
                fg='#000', bg='#00ccff', relief='flat', padx=10,
                command=self._load_evidence).pack(side='right')
        
        # Evidence grid
        self.evidence_frame = tk.Frame(self.frame, bg='#1a1a2e')
        self.evidence_frame.pack(fill='both', expand=True)
        
        self._load_evidence()
    
    def _set_project(self, name):
        projects = self.db.get_all_projects()
        for p in projects:
            if p['name'] == name:
                self.current_project = p
                break
    
    def _load_evidence(self):
        for widget in self.evidence_frame.winfo_children():
            widget.destroy()
        
        if not self.current_project:
            return
        
        evidence_dir = os.path.join(self.current_project['path'], 'evidence')
        screenshots_dir = os.path.join(self.current_project['path'], 'screenshots')
        
        all_evidence = []
        for d in [evidence_dir, screenshots_dir]:
            if os.path.exists(d):
                for f in os.listdir(d):
                    fp = os.path.join(d, f)
                    if os.path.isfile(fp):
                        all_evidence.append(fp)
        
        if not all_evidence:
            tk.Label(self.evidence_frame,
                    text="No evidence collected yet.\nClick '+ Add Evidence' to add files.",
                    font=('Courier', 11), fg='#666', bg='#1a1a2e',
                    justify='center').pack(expand=True)
            return
        
        # Display evidence items
        canvas = tk.Canvas(self.evidence_frame, bg='#1a1a2e', highlightthickness=0)
        scrollbar = tk.Scrollbar(self.evidence_frame, orient='vertical', command=canvas.yview)
        grid = tk.Frame(canvas, bg='#1a1a2e')
        
        grid.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.create_window((0,0), window=grid, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        row_frame = None
        for i, filepath in enumerate(sorted(all_evidence, reverse=True)):
            if i % 3 == 0:
                row_frame = tk.Frame(grid, bg='#1a1a2e')
                row_frame.pack(fill='x', pady=5)
            self._create_evidence_card(row_frame, filepath)
    
    def _create_evidence_card(self, parent, filepath):
        filename = os.path.basename(filepath)
        size = os.path.getsize(filepath)
        ext = os.path.splitext(filename)[1].lower()
        
        card = tk.Frame(parent, bg='#16213e', relief='flat', bd=1, width=200, height=150)
        card.pack(side='left', padx=5, fill='x', expand=True)
        card.pack_propagate(False)
        
        # Icon based on type
        icons = {'.txt': '📝', '.log': '📋', '.png': '🖼️', '.jpg': '📸',
                '.xml': '📊', '.json': '📊', '.html': '🌐', '.pdf': '📕'}
        icon = icons.get(ext, '📎')
        
        tk.Label(card, text=f"{icon} {filename[:20]}", font=('Courier', 9, 'bold'),
                fg='#00ff88', bg='#16213e', wraplength=180).pack(pady=(10,5), padx=5)
        tk.Label(card, text=f"{size:,} bytes", font=('Courier', 8),
                fg='#888', bg='#16213e').pack()
        tk.Label(card, text=f"Type: {ext or 'unknown'}", font=('Courier', 8),
                fg='#888', bg='#16213e').pack()
        
        btn_frame = tk.Frame(card, bg='#16213e')
        btn_frame.pack(pady=5)
        
        tk.Button(btn_frame, text="Open", font=('Courier', 8),
                fg='#000', bg='#00ccff', relief='flat', padx=5,
                command=lambda f=filepath: self._open_file(f)).pack(side='left', padx=2)
        tk.Button(btn_frame, text="Del", font=('Courier', 8),
                fg='#fff', bg='#cc0000', relief='flat', padx=5,
                command=lambda f=filepath: self._delete_file(f)).pack(side='left', padx=2)
    
    def _add_evidence(self):
        if not self.current_project:
            messagebox.showwarning("Warning", "Select a project first")
            return
        
        dialog = tk.Toplevel(self.parent, bg='#1a1a2e')
        dialog.title("Add Evidence")
        dialog.geometry("500x300")
        
        tk.Label(dialog, text="Add Evidence", font=('Courier', 14, 'bold'),
                fg='#00ff88', bg='#1a1a2e').pack(pady=15)
        
        # Note input
        tk.Label(dialog, text="Note/Description:", font=('Courier', 10),
                fg='#fff', bg='#1a1a2e').pack()
        note_entry = tk.Entry(dialog, font=('Courier', 11), bg='#16213e',
                fg='#fff', relief='flat')
        note_entry.pack(fill='x', padx=20, pady=10)
        
        def save_note():
            text = note_entry.get().strip()
            if text:
                evidence_dir = os.path.join(self.current_project['path'], 'evidence')
                os.makedirs(evidence_dir, exist_ok=True)
                fname = f"note_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                fpath = os.path.join(evidence_dir, fname)
                with open(fpath, 'w') as f:
                    f.write(f"Evidence Note\n{'='*40}\n")
                    f.write(f"Project: {self.current_project['name']}\n")
                    f.write(f"Date: {datetime.now()}\n")
                    f.write(f"{'='*40}\n\n")
                    f.write(text)
                self.logger.log_project_action(self.current_project['name'], f"evidence_added: {fname}")
                dialog.destroy()
                self._load_evidence()
                messagebox.showinfo("Added", "Evidence note saved!")
        
        tk.Button(dialog, text="Save Note", font=('Courier', 10, 'bold'),
                fg='#000', bg='#00ff88', relief='flat', padx=20, pady=8,
                command=save_note).pack(pady=10)
        
        tk.Label(dialog, text="— or —", font=('Courier', 10),
                fg='#666', bg='#1a1a2e').pack()
        
        def import_file():
            evidence_dir = os.path.join(self.current_project['path'], 'evidence')
            os.makedirs(evidence_dir, exist_ok=True)
            
            # Since Termux doesn't have file dialog, use manual path
            path_dialog = tk.Toplevel(dialog, bg='#1a1a2e')
            path_dialog.title("Import File")
            path_dialog.geometry("450x200")
            
            tk.Label(path_dialog, text="Enter file path to import:", font=('Courier', 10),
                    fg='#fff', bg='#1a1a2e').pack(pady=10)
            path_entry = tk.Entry(path_dialog, font=('Courier', 10), bg='#16213e',
                    fg='#fff', relief='flat')
            path_entry.pack(fill='x', padx=20, pady=10)
            path_entry.insert(0, '/data/data/com.termux/files/home/')
            
            def do_import():
                src = path_entry.get().strip()
                if os.path.isfile(src):
                    dst = os.path.join(evidence_dir, os.path.basename(src))
                    shutil.copy2(src, dst)
                    self.logger.log_project_action(self.current_project['name'], f"evidence_imported: {os.path.basename(src)}")
                    path_dialog.destroy()
                    dialog.destroy()
                    self._load_evidence()
                    messagebox.showinfo("Imported", f"File imported:\n{dst}")
                else:
                    messagebox.showerror("Error", "File not found!")
            
            tk.Button(path_dialog, text="Import", font=('Courier', 10, 'bold'),
                    fg='#000', bg='#00ccff', relief='flat', padx=20, pady=5,
                    command=do_import).pack(pady=10)
        
        tk.Button(dialog, text="Import File", font=('Courier', 10),
                fg='#000', bg='#00ccff', relief='flat', padx=20, pady=8,
                command=import_file).pack(pady=5)
    
    def _open_file(self, filepath):
        dialog = tk.Toplevel(self.parent, bg='#1a1a2e')
        dialog.title(os.path.basename(filepath))
        dialog.geometry("600x400")
        
        text = tk.Text(dialog, font=('Courier', 9), bg='#0a0a0a', fg='#00ff88',
                relief='flat', wrap='word')
        text.pack(fill='both', expand=True, padx=10, pady=10)
        
        try:
            with open(filepath, 'r', errors='ignore') as f:
                text.insert('1.0', f.read())
        except:
            text.insert('1.0', f"[Binary file - {os.path.getsize(filepath)} bytes]\n\nCannot preview binary files.")
        
        text.config(state='disabled')
        
        tk.Button(dialog, text="Close", font=('Courier', 10),
                fg='#000', bg='#00ccff', relief='flat', padx=20, pady=5,
                command=dialog.destroy).pack(pady=10)
    
    def _delete_file(self, filepath):
        if messagebox.askyesno("Delete", f"Delete {os.path.basename(filepath)}?"):
            try:
                os.remove(filepath)
                self._load_evidence()
            except Exception as e:
                messagebox.showerror("Error", str(e))
