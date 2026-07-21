import tkinter as tk
from tkinter import ttk, messagebox
import os

class PluginsManager:
    def __init__(self, parent, config, logger):
        self.parent = parent
        self.config = config
        self.logger = logger
        self.frame = tk.Frame(parent, bg='#1a1a2e')
        self.plugin_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'plugins')
    
    def build(self):
        self.frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Header
        header = tk.Frame(self.frame, bg='#1a1a2e')
        header.pack(fill='x', pady=(0,10))
        
        tk.Label(header, text="Plugins", font=('Courier', 18, 'bold'),
                fg='#00ff88', bg='#1a1a2e').pack(side='left')
        
        tk.Button(header, text="+ New Plugin", font=('Courier', 10),
                fg='#000', bg='#00ff88', relief='flat', padx=10, pady=5,
                command=self._create_plugin_dialog).pack(side='right')
        
        # Info
        info_frame = tk.Frame(self.frame, bg='#16213e', padx=15, pady=10)
        info_frame.pack(fill='x', pady=(0,10))
        tk.Label(info_frame, text="Plugins extend CyberLab with custom tools and modules.",
                font=('Courier', 9), fg='#aaa', bg='#16213e').pack(anchor='w')
        tk.Label(info_frame, text=f"Plugin directory: {self.plugin_dir}",
                font=('Courier', 8), fg='#666', bg='#16213e').pack(anchor='w')
        
        # Plugin list
        self.list_frame = tk.Frame(self.frame, bg='#1a1a2e')
        self.list_frame.pack(fill='both', expand=True)
        
        self._load_plugins()
    
    def _load_plugins(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()
        
        plugins = []
        if os.path.exists(self.plugin_dir):
            for item in os.listdir(self.plugin_dir):
                if item.endswith('.py') and item != '__init__.py':
                    plugins.append(item)
                elif os.path.isdir(os.path.join(self.plugin_dir, item)):
                    init_file = os.path.join(self.plugin_dir, item, '__init__.py')
                    if os.path.exists(init_file):
                        plugins.append(f"{item}/")
        
        if not plugins:
            tk.Label(self.list_frame,
                    text="No plugins installed.\n\nPlugins are Python scripts that extend CyberLab.\nClick '+ New Plugin' to create one, or add .py files to:\nplugins/",
                    font=('Courier', 10), fg='#666', bg='#1a1a2e',
                    justify='center').pack(expand=True)
            return
        
        for plugin in sorted(plugins):
            self._create_plugin_row(plugin)
    
    def _create_plugin_row(self, plugin_name):
        row = tk.Frame(self.list_frame, bg='#16213e', relief='flat', bd=0)
        row.pack(fill='x', pady=2)
        
        is_dir = plugin_name.endswith('/')
        icon = '📦' if is_dir else '🔌'
        name = plugin_name.rstrip('/')
        
        info = tk.Frame(row, bg='#16213e')
        info.pack(side='left', fill='x', expand=True, padx=15, pady=10)
        
        tk.Label(info, text=f"{icon} {name}", font=('Courier', 10, 'bold'),
                fg='#00ff88', bg='#16213e').pack(anchor='w')
        
        # Check plugin metadata
        plugin_path = os.path.join(self.plugin_dir, plugin_name.rstrip('/'))
        if not is_dir:
            try:
                size = os.path.getsize(plugin_path)
                tk.Label(info, text=f"Size: {size:,} bytes", font=('Courier', 8),
                        fg='#888', bg='#16213e').pack(anchor='w')
            except:
                pass
        
        # Actions
        actions = tk.Frame(row, bg='#16213e')
        actions.pack(side='right', padx=15, pady=10)
        
        tk.Button(actions, text="Load", font=('Courier', 9),
                fg='#000', bg='#00ff88', relief='flat', padx=12,
                command=lambda n=name: self._load_plugin(n)).pack(side='left', padx=2)
        
        tk.Button(actions, text="Edit", font=('Courier', 9),
                fg='#000', bg='#00ccff', relief='flat', padx=12,
                command=lambda n=name: self._edit_plugin(n)).pack(side='left', padx=2)
        
        tk.Button(actions, text="Del", font=('Courier', 9),
                fg='#fff', bg='#cc0000', relief='flat', padx=12,
                command=lambda n=name: self._delete_plugin(n)).pack(side='left', padx=2)
    
    def _create_plugin_dialog(self):
        dialog = tk.Toplevel(self.parent, bg='#1a1a2e')
        dialog.title("Create Plugin")
        dialog.geometry("500x400")
        
        tk.Label(dialog, text="Create New Plugin", font=('Courier', 14, 'bold'),
                fg='#00ff88', bg='#1a1a2e').pack(pady=15)
        
        tk.Label(dialog, text="Plugin Name:", font=('Courier', 10),
                fg='#fff', bg='#1a1a2e').pack()
        name_entry = tk.Entry(dialog, font=('Courier', 11), bg='#16213e',
                fg='#fff', relief='flat')
        name_entry.pack(fill='x', padx=20, pady=5)
        name_entry.insert(0, 'my_plugin')
        
        tk.Label(dialog, text="Description:", font=('Courier', 10),
                fg='#fff', bg='#1a1a2e').pack()
        desc_entry = tk.Entry(dialog, font=('Courier', 10), bg='#16213e',
                fg='#fff', relief='flat')
        desc_entry.pack(fill='x', padx=20, pady=5)
        desc_entry.insert(0, 'My custom plugin')
        
        tk.Label(dialog, text="Plugin Code:", font=('Courier', 10),
                fg='#fff', bg='#1a1a2e').pack()
        code_text = tk.Text(dialog, font=('Courier', 9), bg='#0a0a0a', fg='#00ff88',
                relief='flat', wrap='word', height=10)
        code_text.pack(fill='both', expand=True, padx=20, pady=5)
        code_text.insert('1.0', '''"""My Plugin - CyberLab Pro"""
import tkinter as tk

def run(parent, db, logger, config):
    """Main plugin entry point"""
    frame = tk.Frame(parent, bg='#1a1a2e')
    frame.pack(fill='both', expand=True)
    tk.Label(frame, text="Hello from my plugin!",
            font=('Courier', 14), fg='#00ff88',
            bg='#1a1a2e').pack(expand=True)
    return frame
''')
        
        def save():
            name = name_entry.get().strip()
            code = code_text.get('1.0', 'end-1c')
            if not name:
                messagebox.showwarning("Warning", "Enter a plugin name")
                return
            
            fname = f"{name}.py"
            fpath = os.path.join(self.plugin_dir, fname)
            
            if os.path.exists(fpath):
                if not messagebox.askyesno("Overwrite", f"Plugin '{fname}' exists. Overwrite?"):
                    return
            
            with open(fpath, 'w') as f:
                f.write(code)
            
            self.logger.app_logger.info(f"Plugin created: {fname}")
            dialog.destroy()
            self._load_plugins()
            messagebox.showinfo("Created", f"Plugin '{fname}' saved!")
        
        tk.Button(dialog, text="Save Plugin", font=('Courier', 10, 'bold'),
                fg='#000', bg='#00ff88', relief='flat', padx=20, pady=8,
                command=save).pack(pady=10)
    
    def _load_plugin(self, name):
        plugin_path = os.path.join(self.plugin_dir, f"{name}.py")
        if not os.path.exists(plugin_path):
            messagebox.showerror("Error", f"Plugin '{name}' not found")
            return
        
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location(name, plugin_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            if hasattr(module, 'run'):
                for widget in self.frame.winfo_children():
                    widget.destroy()
                
                tk.Button(self.frame, text="← Back to Plugins", font=('Courier', 10),
                        fg='#00ccff', bg='#1a1a2e', relief='flat',
                        command=self.build).pack(anchor='w', pady=5)
                
                module.run(self.frame, self.parent, self.logger, self.config)
                self.logger.app_logger.info(f"Plugin executed: {name}")
            else:
                messagebox.showwarning("Warning", f"Plugin '{name}' has no run() function")
        except Exception as e:
            messagebox.showerror("Plugin Error", str(e))
            self.logger.log_error(f"plugin_{name}", e)
    
    def _edit_plugin(self, name):
        plugin_path = os.path.join(self.plugin_dir, f"{name}.py")
        if not os.path.exists(plugin_path):
            messagebox.showerror("Error", "Plugin file not found")
            return
        
        try:
            with open(plugin_path, 'r') as f:
                code = f.read()
        except:
            code = "# Error reading file"
        
        dialog = tk.Toplevel(self.parent, bg='#1a1a2e')
        dialog.title(f"Edit: {name}.py")
        dialog.geometry("600x450")
        
        tk.Label(dialog, text=f"Editing: {name}.py", font=('Courier', 12, 'bold'),
                fg='#00ff88', bg='#1a1a2e').pack(pady=10)
        
        code_text = tk.Text(dialog, font=('Courier', 9), bg='#0a0a0a', fg='#00ff88',
                relief='flat', wrap='word')
        code_text.pack(fill='both', expand=True, padx=10, pady=5)
        code_text.insert('1.0', code)
        
        def save():
            new_code = code_text.get('1.0', 'end-1c')
            with open(plugin_path, 'w') as f:
                f.write(new_code)
            dialog.destroy()
            messagebox.showinfo("Saved", f"Plugin '{name}.py' updated!")
        
        tk.Button(dialog, text="Save Changes", font=('Courier', 10, 'bold'),
                fg='#000', bg='#00ff88', relief='flat', padx=20, pady=8,
                command=save).pack(pady=10)
    
    def _delete_plugin(self, name):
        plugin_path = os.path.join(self.plugin_dir, f"{name}.py")
        if os.path.exists(plugin_path):
            if messagebox.askyesno("Delete Plugin", f"Delete '{name}.py' permanently?"):
                os.remove(plugin_path)
                self.logger.app_logger.info(f"Plugin deleted: {name}.py")
                self._load_plugins()
