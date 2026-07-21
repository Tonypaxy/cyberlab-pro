import subprocess
import tkinter as tk
from tkinter import ttk, messagebox
import os
import shutil

class PluginsManager:
    def __init__(self, parent, config, logger):
        self.parent = parent
        self.config = config
        self.logger = logger
        self.frame = tk.Frame(parent, bg='#1a1a2e')
        self.plugin_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'plugins')
    
    def build(self):
        self.frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        header = tk.Frame(self.frame, bg='#1a1a2e')
        header.pack(fill='x', pady=(0,10))
        
        tk.Label(header, text="🔌 Plugins", font=('Courier', 18, 'bold'),
                fg='#00ff88', bg='#1a1a2e').pack(side='left')
        
        btn_frame = tk.Frame(header, bg='#1a1a2e')
        btn_frame.pack(side='right')
        
        tk.Button(btn_frame, text="+ Create", font=('Courier', 9),
                fg='#000', bg='#00ff88', relief='flat', padx=10, pady=5,
                command=self._create_dialog).pack(side='left', padx=2)
        tk.Button(btn_frame, text="📁 Open Folder", font=('Courier', 9),
                fg='#000', bg='#00ccff', relief='flat', padx=10, pady=5,
                command=self._open_folder).pack(side='left', padx=2)
        tk.Button(btn_frame, text="🔄 Refresh", font=('Courier', 9),
                fg='#000', bg='#ffaa00', relief='flat', padx=10, pady=5,
                command=self._load).pack(side='left', padx=2)
        
        tk.Label(self.frame, text=f"Plugin directory: {self.plugin_dir}",
                font=('Courier', 8), fg='#666', bg='#1a1a2e').pack(anchor='w', pady=(0,10))
        
        self.list_frame = tk.Frame(self.frame, bg='#1a1a2e')
        self.list_frame.pack(fill='both', expand=True)
        self._load()
    
    def _load(self):
        for w in self.list_frame.winfo_children(): w.destroy()
        
        plugins = []
        if os.path.exists(self.plugin_dir):
            for item in os.listdir(self.plugin_dir):
                if item.endswith('.py') and item != '__init__.py':
                    plugins.append(item)
                elif os.path.isdir(os.path.join(self.plugin_dir, item)):
                    if os.path.exists(os.path.join(self.plugin_dir, item, '__init__.py')):
                        plugins.append(f"{item}/")
        
        if not plugins:
            tk.Label(self.list_frame, text="No plugins installed.\nClick '+ Create' to build one!",
                    font=('Courier', 11), fg='#666', bg='#1a1a2e', justify='center').pack(expand=True)
            return
        
        canvas = tk.Canvas(self.list_frame, bg='#1a1a2e', highlightthickness=0)
        scrollbar = tk.Scrollbar(self.list_frame, orient='vertical', command=canvas.yview)
        sf = tk.Frame(canvas, bg='#1a1a2e')
        sf.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.create_window((0,0), window=sf, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        for p in sorted(plugins):
            self._plugin_card(sf, p)
    
    def _plugin_card(self, parent, name):
        is_dir = name.endswith('/')
        clean_name = name.rstrip('/')
        icon = '📦' if is_dir else '🔌'
        
        card = tk.Frame(parent, bg='#16213e', relief='flat', bd=0)
        card.pack(fill='x', padx=5, pady=2)
        
        info = tk.Frame(card, bg='#16213e')
        info.pack(side='left', fill='x', expand=True, padx=15, pady=10)
        
        tk.Label(info, text=f"{icon} {clean_name}", font=('Courier', 10, 'bold'),
                fg='#00ff88', bg='#16213e').pack(anchor='w')
        
        # File size
        path = os.path.join(self.plugin_dir, name.rstrip('/'))
        if not is_dir:
            size = os.path.getsize(path)
            tk.Label(info, text=f"Size: {size:,} bytes", font=('Courier', 8),
                    fg='#888', bg='#16213e').pack(anchor='w')
        
        actions = tk.Frame(card, bg='#16213e')
        actions.pack(side='right', padx=15, pady=10)
        
        tk.Button(actions, text="▶ Load", font=('Courier', 9),
                fg='#000', bg='#00ff88', relief='flat', padx=12,
                command=lambda n=clean_name: self._load_plugin(n)).pack(pady=2)
        
        tk.Button(actions, text="✏️ Edit", font=('Courier', 9),
                fg='#000', bg='#00ccff', relief='flat', padx=12,
                command=lambda n=clean_name: self._edit_plugin(n)).pack(pady=2)
        
        tk.Button(actions, text="🗑️ Delete", font=('Courier', 9),
                fg='#fff', bg='#cc0000', relief='flat', padx=12,
                command=lambda n=clean_name: self._delete_plugin(n)).pack(pady=2)
    
    def _create_dialog(self):
        dialog = tk.Toplevel(self.parent, bg='#1a1a2e')
        dialog.title("Create Plugin"); dialog.geometry("550x450")
        
        tk.Label(dialog, text="Create New Plugin", font=('Courier', 14, 'bold'),
                fg='#00ff88', bg='#1a1a2e').pack(pady=15)
        
        tk.Label(dialog, text="Plugin Name:", font=('Courier', 10), fg='#fff', bg='#1a1a2e').pack()
        name_entry = tk.Entry(dialog, font=('Courier', 11), bg='#16213e', fg='#fff', relief='flat')
        name_entry.pack(fill='x', padx=20, pady=5); name_entry.insert(0, 'my_plugin')
        
        tk.Label(dialog, text="Description:", font=('Courier', 10), fg='#fff', bg='#1a1a2e').pack()
        desc_entry = tk.Entry(dialog, font=('Courier', 10), bg='#16213e', fg='#fff', relief='flat')
        desc_entry.pack(fill='x', padx=20, pady=5); desc_entry.insert(0, 'My custom plugin')
        
        tk.Label(dialog, text="Code:", font=('Courier', 10), fg='#fff', bg='#1a1a2e').pack()
        code = tk.Text(dialog, font=('Courier', 9), bg='#0a0a0a', fg='#00ff88', relief='flat', height=12)
        code.pack(fill='both', expand=True, padx=20, pady=5)
        code.insert('1.0', '''"""My Plugin for CyberLab Pro"""
import tkinter as tk

def run(parent, db, logger, config):
    """Main entry point - called when plugin loads"""
    frame = tk.Frame(parent, bg='#1a1a2e')
    frame.pack(fill='both', expand=True, padx=20, pady=20)
    
    tk.Label(frame, text="🔌 My Plugin", font=('Courier', 18, 'bold'),
            fg='#00ff88', bg='#1a1a2e').pack(pady=10)
    
    tk.Label(frame, text="This is a custom plugin!\\n\\n"
            "You can:\\n"
            "• Add custom tools\\n"
            "• Access the database\\n"
            "• Build full GUIs\\n"
            "• Integrate external scripts",
            font=('Courier', 10), fg='#aaa', bg='#1a1a2e', justify='left').pack(pady=10)
    
    def do_something():
        from tkinter import messagebox
        messagebox.showinfo("Plugin", "Hello from your plugin!")
    
    tk.Button(frame, text="Click Me", font=('Courier', 10, 'bold'),
            fg='#000', bg='#00ff88', relief='flat', padx=15, pady=8,
            command=do_something).pack(pady=10)
    
    return frame
''')
        
        def save():
            name = name_entry.get().strip()
            if not name: messagebox.showwarning("Warning", "Enter a name"); return
            fpath = os.path.join(self.plugin_dir, f"{name}.py")
            if os.path.exists(fpath):
                if not messagebox.askyesno("Overwrite", f"'{name}.py' exists. Overwrite?"): return
            with open(fpath, 'w') as f: f.write(code.get('1.0', 'end-1c'))
            self.logger.app_logger.info(f"Plugin created: {name}.py"); dialog.destroy()
            self._load(); messagebox.showinfo("Created", f"Plugin '{name}.py' saved!")
        
        tk.Button(dialog, text="💾 Save Plugin", font=('Courier', 10, 'bold'),
                fg='#000', bg='#00ff88', relief='flat', padx=20, pady=8, command=save).pack(pady=10)
    
    def _load_plugin(self, name):
        path = os.path.join(self.plugin_dir, f"{name}.py")
        if not os.path.exists(path):
            messagebox.showerror("Error", f"Plugin '{name}' not found"); return
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location(name, path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            if hasattr(module, 'run'):
                for w in self.frame.winfo_children(): w.destroy()
                tk.Button(self.frame, text="← Back to Plugins", font=('Courier', 10),
                        fg='#00ccff', bg='#1a1a2e', relief='flat', command=self.build).pack(anchor='w', pady=5)
                module.run(self.frame, self.parent, self.logger, self.config)
                self.logger.app_logger.info(f"Plugin loaded: {name}")
            else:
                messagebox.showwarning("Warning", f"Plugin '{name}' has no run() function")
        except Exception as e:
            messagebox.showerror("Plugin Error", str(e))
    
    def _edit_plugin(self, name):
        path = os.path.join(self.plugin_dir, f"{name}.py")
        if not os.path.exists(path):
            messagebox.showerror("Error", "Plugin not found"); return
        try:
            with open(path) as f: code = f.read()
        except: code = "# Error reading file"
        
        dialog = tk.Toplevel(self.parent, bg='#1a1a2e')
        dialog.title(f"Edit: {name}.py"); dialog.geometry("600x450")
        
        tk.Label(dialog, text=f"Editing: {name}.py", font=('Courier', 12, 'bold'),
                fg='#00ff88', bg='#1a1a2e').pack(pady=10)
        
        code_text = tk.Text(dialog, font=('Courier', 9), bg='#0a0a0a', fg='#00ff88', relief='flat')
        code_text.pack(fill='both', expand=True, padx=10, pady=5); code_text.insert('1.0', code)
        
        def save():
            with open(path, 'w') as f: f.write(code_text.get('1.0', 'end-1c'))
            dialog.destroy(); messagebox.showinfo("Saved", f"'{name}.py' updated!"); self._load()
        
        tk.Button(dialog, text="💾 Save Changes", font=('Courier', 10, 'bold'),
                fg='#000', bg='#00ff88', relief='flat', padx=20, pady=8, command=save).pack(pady=10)
    
    def _delete_plugin(self, name):
        path = os.path.join(self.plugin_dir, f"{name}.py")
        if not os.path.exists(path):
            # Check if directory
            dir_path = os.path.join(self.plugin_dir, name)
            if os.path.isdir(dir_path):
                path = dir_path
            else:
                messagebox.showerror("Error", "Plugin not found"); return
        
        if messagebox.askyesno("🗑️ Delete Plugin", 
                f"Permanently delete '{name}'?\n\nThis CANNOT be undone!\n\nFile: {path}"):
            try:
                if os.path.isdir(path):
                    shutil.rmtree(path)
                else:
                    os.remove(path)
                self.logger.app_logger.info(f"Plugin deleted: {name}")
                self._load()
                messagebox.showinfo("Deleted", f"Plugin '{name}' deleted!")
            except Exception as e:
                messagebox.showerror("Error", f"Could not delete: {e}")
    
    def _open_folder(self):
        os.makedirs(self.plugin_dir, exist_ok=True)
        try:
            if os.name == 'nt':
                os.startfile(self.plugin_dir)
            else:
                subprocess.Popen(['xdg-open', self.plugin_dir])
        except:
            messagebox.showinfo("Plugin Directory", f"Plugins folder:\n{self.plugin_dir}")
