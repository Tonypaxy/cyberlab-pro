from gui.scrollable_frame import create_scrollable
import tkinter as tk
from tkinter import ttk, messagebox
import os
import shutil
import subprocess
import importlib.util

class PluginsManager:
    def __init__(self, parent, config, logger):
        self.parent = parent
        self.config = config
        self.logger = logger
        self.frame = tk.Frame(parent, bg='#1a1a2e')
        self.plugin_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'plugins')
        os.makedirs(self.plugin_dir, exist_ok=True)
    
    def build(self):
        for w in self.frame.winfo_children(): w.destroy()
        self.frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        header = tk.Frame(self.frame, bg='#1a1a2e')
        header.pack(fill='x', pady=(0,10))
        tk.Label(header, text="🔌 Plugins", font=('Courier', 18, 'bold'),
                fg='#00ff88', bg='#1a1a2e').pack(side='left')
        
        btn_frame = tk.Frame(header, bg='#1a1a2e')
        btn_frame.pack(side='right')
        
        tk.Button(btn_frame, text="+ Create", font=('Courier', 9),
                fg='#000', bg='#00ff88', relief='raised', padx=10, pady=5,
                command=self._create_dialog).pack(side='left', padx=3)
        
        # Open Folder - fixed with direct command
        tk.Button(btn_frame, text="📁 Open Folder", font=('Courier', 9),
                fg='#000', bg='#00ccff', relief='raised', padx=10, pady=5,
                command=self._open_folder).pack(side='left', padx=3)
        
        tk.Button(btn_frame, text="🔄 Refresh", font=('Courier', 9),
                fg='#000', bg='#ffaa00', relief='raised', padx=10, pady=5,
                command=self._load).pack(side='left', padx=3)
        
        tk.Label(self.frame, text=f"📂 {self.plugin_dir}", font=('Courier', 8),
                fg='#666', bg='#1a1a2e').pack(anchor='w', pady=(0,10))
        
        self.list_frame = tk.Frame(self.frame, bg='#1a1a2e')
        self.list_frame.pack(fill='both', expand=True)
        self._load()
    
    def _get_plugins(self):
        plugins = []
        if os.path.exists(self.plugin_dir):
            for item in os.listdir(self.plugin_dir):
                path = os.path.join(self.plugin_dir, item)
                if item.endswith('.py') and item != '__init__.py':
                    name = item[:-3]
                    has_run = self._check_has_run(path)
                    plugins.append({'name': name, 'path': path, 'size': os.path.getsize(path), 'has_run': has_run, 'type': 'file'})
                elif os.path.isdir(path) and not item.startswith('__'):
                    init = os.path.join(path, '__init__.py')
                    if os.path.exists(init):
                        has_run = self._check_has_run(init)
                        plugins.append({'name': item, 'path': path, 'size': 0, 'has_run': has_run, 'type': 'package'})
        return sorted(plugins, key=lambda p: p['name'])
    
    def _check_has_run(self, filepath):
        try:
            with open(filepath) as f:
                return 'def run(' in f.read()
        except:
            return False
    
    def _load(self):
        for w in self.list_frame.winfo_children(): w.destroy()
        plugins = self._get_plugins()
        if not plugins:
            tk.Label(self.list_frame, text="No plugins installed.\nClick '+ Create' to build one!",
                    font=('Courier', 11), fg='#666', bg='#1a1a2e', justify='center').pack(expand=True)
            return
        for p in plugins:
            self._card(p)
    
    def _card(self, plugin):
        name = plugin['name']
        icon = '📦' if plugin['type'] == 'package' else '🔌'
        has_run = plugin['has_run']
        status = "✅ Ready" if has_run else "⚠️ No run()"
        status_color = "#00ff88" if has_run else "#ffaa00"
        
        card = tk.Frame(self.list_frame, bg='#16213e', relief='flat', bd=0)
        card.pack(fill='x', padx=5, pady=2)
        
        info = tk.Frame(card, bg='#16213e')
        info.pack(side='left', fill='x', expand=True, padx=12, pady=8)
        
        tk.Label(info, text=f"{icon} {name}", font=('Courier', 10, 'bold'),
                fg='#00ff88', bg='#16213e').pack(anchor='w')
        tk.Label(info, text=status, font=('Courier', 8), fg=status_color, bg='#16213e').pack(anchor='w')
        if plugin['size'] > 0:
            tk.Label(info, text=f"{plugin['size']:,} bytes", font=('Courier', 8), fg='#666', bg='#16213e').pack(anchor='w')
        
        actions = tk.Frame(card, bg='#16213e')
        actions.pack(side='right', padx=12, pady=8)
        
        if has_run:
            tk.Button(actions, text="▶ Load", font=('Courier', 8),
                    fg='#000', bg='#00ff88', relief='raised', padx=10, pady=3,
                    command=lambda n=name: self._load_plugin(n)).pack(pady=2)
        
        tk.Button(actions, text="✏️ Edit", font=('Courier', 8),
                fg='#000', bg='#00ccff', relief='raised', padx=10, pady=3,
                command=lambda n=name: self._edit_plugin(n)).pack(pady=2)
        
        def make_delete(n):
            return lambda: self._delete_plugin(n)
        
        tk.Button(actions, text="🗑️ Delete", font=('Courier', 8),
                fg='#fff', bg='#cc0000', relief='raised', padx=10, pady=3,
                command=make_delete(name)).pack(pady=2)
    
    def _create_dialog(self):
        d = tk.Toplevel(self.parent, bg='#1a1a2e')
        d.title("Create Plugin"); d.geometry("500x400")
        tk.Label(d, text="Create New Plugin", font=('Courier', 14, 'bold'), fg='#00ff88', bg='#1a1a2e').pack(pady=15)
        tk.Label(d, text="Name:", font=('Courier', 10), fg='#fff', bg='#1a1a2e').pack()
        name_e = tk.Entry(d, font=('Courier', 11), bg='#16213e', fg='#fff', relief='flat')
        name_e.pack(fill='x', padx=20, pady=5); name_e.insert(0, 'my_plugin')
        tk.Label(d, text="Code:", font=('Courier', 10), fg='#fff', bg='#1a1a2e').pack()
        code = tk.Text(d, font=('Courier', 9), bg='#0a0a0a', fg='#00ff88', relief='flat', height=12)
        code.pack(fill='both', expand=True, padx=20, pady=5)
        code.insert('1.0', '"""My Plugin"""\nimport tkinter as tk\n\ndef run(parent, db, logger, config):\n    frame = tk.Frame(parent, bg="#1a1a2e")\n    frame.pack(fill="both", expand=True)\n    tk.Label(frame, text="Hello!", fg="#00ff88", bg="#1a1a2e", font=("Courier", 14)).pack(expand=True)\n    return frame\n')
        def save():
            name = name_e.get().strip()
            if not name: messagebox.showwarning("Warning", "Enter name"); return
            c = code.get('1.0', 'end-1c')
            if 'def run(' not in c: messagebox.showwarning("Warning", "Add def run() function!"); return
            with open(os.path.join(self.plugin_dir, f"{name}.py"), 'w') as f: f.write(c)
            d.destroy(); self._load()
        tk.Button(d, text="Save", font=('Courier', 10, 'bold'), fg='#000', bg='#00ff88', relief='raised', padx=20, pady=8, command=save).pack(pady=15)
    
    def _load_plugin(self, name):
        path = os.path.join(self.plugin_dir, f"{name}.py")
        if not os.path.exists(path):
            pkg = os.path.join(self.plugin_dir, name, '__init__.py')
            if os.path.exists(pkg): path = pkg
            else: messagebox.showerror("Error", f"Not found: {name}"); return
        try:
            spec = importlib.util.spec_from_file_location(name, path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            if hasattr(mod, 'run'):
                for w in self.frame.winfo_children(): w.destroy()
                tk.Button(self.frame, text="← Back", font=('Courier', 10), fg='#00ccff', bg='#1a1a2e', relief='raised', command=self.build).pack(anchor='w', pady=5)
                mod.run(self.frame, self.parent, self.logger, self.config)
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def _edit_plugin(self, name):
        path = os.path.join(self.plugin_dir, f"{name}.py")
        if not os.path.exists(path): path = os.path.join(self.plugin_dir, name, '__init__.py')
        if not os.path.exists(path): messagebox.showerror("Error", "Not found"); return
        with open(path) as f: code = f.read()
        d = tk.Toplevel(self.parent, bg='#1a1a2e')
        d.title(f"Edit: {name}"); d.geometry("550x400")
        t = tk.Text(d, font=('Courier', 9), bg='#0a0a0a', fg='#00ff88', relief='flat')
        t.pack(fill='both', expand=True, padx=10, pady=10); t.insert('1.0', code)
        def save():
            with open(path, 'w') as f: f.write(t.get('1.0', 'end-1c'))
            d.destroy(); self._load()
        tk.Button(d, text="Save", font=('Courier', 10, 'bold'), fg='#000', bg='#00ff88', relief='raised', padx=20, pady=8, command=save).pack(pady=10)
    
    def _delete_plugin(self, name):
        path = os.path.join(self.plugin_dir, f"{name}.py")
        if not os.path.exists(path):
            dir_path = os.path.join(self.plugin_dir, name)
            if os.path.isdir(dir_path): path = dir_path
            else: messagebox.showerror("Error", "Not found"); return
        if messagebox.askyesno("Delete", f"Delete '{name}' permanently?"):
            try:
                if os.path.isdir(path): shutil.rmtree(path)
                else: os.remove(path)
                self._load()
                messagebox.showinfo("Deleted", f"'{name}' deleted!")
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def _open_folder(self):
        """Open plugin folder - works on Termux and Linux"""
        import webbrowser
        folder = self.plugin_dir
        
        # Try multiple methods
        opened = False
        
        # Method 1: webbrowser (works cross-platform)
        try:
            webbrowser.open(f'file://{folder}')
            opened = True
        except:
            pass
        
        # Method 2: xdg-open (Linux)
        if not opened:
            try:
                subprocess.Popen(['xdg-open', folder], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                opened = True
            except:
                pass
        
        # Method 3: termux-open (Termux)
        if not opened:
            try:
                subprocess.Popen(['termux-open', folder], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                opened = True
            except:
                pass
        
        # Method 4: Show path in dialog
        if not opened:
            messagebox.showinfo("Plugin Folder", f"Plugins location:\n\n{folder}\n\nOpen this in your file manager.")
        else:
            messagebox.showinfo("Opened", f"Opening: {folder}", parent=self.frame)
