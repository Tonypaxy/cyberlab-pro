import tkinter as tk
from tkinter import ttk, messagebox
import os
from datetime import datetime

class ProjectManager:
    def __init__(self, parent, db, logger, navigate_callback=None):
        self.parent = parent
        self.db = db
        self.logger = logger
        self.navigate_callback = navigate_callback
        self.frame = tk.Frame(parent, bg='#1a1a2e')
    
    def build(self):
        self.frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Header
        header = tk.Frame(self.frame, bg='#1a1a2e')
        header.pack(fill='x', pady=(0,10))
        
        tk.Label(header, text="Projects", font=('Courier', 18, 'bold'),
                fg='#00ff88', bg='#1a1a2e').pack(side='left')
        
        tk.Button(header, text="+ New Project", font=('Courier', 10),
                fg='#000', bg='#00ff88', relief='flat', padx=10, pady=5,
                command=self.new_project_dialog).pack(side='right')
        
        # Stats
        projects = self.db.get_all_projects()
        stats = tk.Frame(self.frame, bg='#16213e', padx=15, pady=10)
        stats.pack(fill='x', pady=(0,10))
        tk.Label(stats, text=f"Total Projects: {len(projects)}", font=('Courier', 10),
                fg='#00ccff', bg='#16213e').pack(side='left')
        
        # Projects list
        self.list_frame = tk.Frame(self.frame, bg='#16213e')
        self.list_frame.pack(fill='both', expand=True)
        
        self.refresh_list()
    
    def refresh_list(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()
        
        projects = self.db.get_all_projects()
        
        if not projects:
            tk.Label(self.list_frame, text="No projects yet.\nClick '+ New Project' to start.",
                    font=('Courier', 12), fg='#666', bg='#16213e',
                    justify='center').pack(expand=True)
            return
        
        # Canvas for scrolling
        canvas = tk.Canvas(self.list_frame, bg='#16213e', highlightthickness=0)
        scrollbar = tk.Scrollbar(self.list_frame, orient='vertical', command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg='#16213e')
        
        scroll_frame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.create_window((0,0), window=scroll_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        for project in projects:
            self._create_project_card(scroll_frame, project)
    
    def _create_project_card(self, parent, project):
        card = tk.Frame(parent, bg='#1a1a2e', relief='flat', bd=0)
        card.pack(fill='x', pady=3, padx=5)
        
        # Project info
        info = tk.Frame(card, bg='#1a1a2e')
        info.pack(side='left', fill='x', expand=True, padx=15, pady=10)
        
        tk.Label(info, text=f"📁 {project['name']}", font=('Courier', 12, 'bold'),
                fg='#00ff88', bg='#1a1a2e').pack(anchor='w')
        
        desc = project.get('description', '') or 'No description'
        tk.Label(info, text=desc[:60], font=('Courier', 9),
                fg='#aaa', bg='#1a1a2e').pack(anchor='w')
        
        created = project.get('created_at', 'Unknown')
        tk.Label(info, text=f"Created: {created[:19] if created else 'Unknown'}",
                font=('Courier', 8), fg='#666', bg='#1a1a2e').pack(anchor='w')
        
        # Check project contents
        proj_path = project.get('path', '')
        if proj_path and os.path.exists(proj_path):
            logs = os.path.join(proj_path, 'logs')
            evidence = os.path.join(proj_path, 'evidence')
            notes = os.path.join(proj_path, 'notes')
            log_count = len(os.listdir(logs)) if os.path.exists(logs) else 0
            ev_count = len(os.listdir(evidence)) if os.path.exists(evidence) else 0
            note_count = len(os.listdir(notes)) if os.path.exists(notes) else 0
            tk.Label(info, text=f"Logs: {log_count} | Evidence: {ev_count} | Notes: {note_count}",
                    font=('Courier', 8), fg='#555', bg='#1a1a2e').pack(anchor='w')
        
        # Actions
        actions = tk.Frame(card, bg='#1a1a2e')
        actions.pack(side='right', padx=15, pady=10)
        
        tk.Button(actions, text="Open", font=('Courier', 9, 'bold'),
                fg='#000', bg='#00ff88', relief='flat', padx=15, pady=3,
                command=lambda p=project: self.open_project(p)).pack(pady=2)
        
        tk.Button(actions, text="Delete", font=('Courier', 8),
                fg='#fff', bg='#cc0000', relief='flat', padx=15, pady=2,
                command=lambda p=project: self.delete_project(p)).pack(pady=2)
    
    def new_project_dialog(self):
        dialog = tk.Toplevel(self.parent, bg='#1a1a2e')
        dialog.title("New Project")
        dialog.geometry("450x300")
        dialog.resizable(False, False)
        
        tk.Label(dialog, text="Create New Project", font=('Courier', 14, 'bold'),
                fg='#00ff88', bg='#1a1a2e').pack(pady=20)
        
        tk.Label(dialog, text="Project Name:", font=('Courier', 10),
                fg='#fff', bg='#1a1a2e').pack()
        name_entry = tk.Entry(dialog, font=('Courier', 12), bg='#16213e',
                fg='#fff', insertbackground='#fff', relief='flat')
        name_entry.pack(pady=5, padx=20, fill='x')
        name_entry.focus()
        
        tk.Label(dialog, text="Description:", font=('Courier', 10),
                fg='#fff', bg='#1a1a2e').pack()
        desc_entry = tk.Entry(dialog, font=('Courier', 10), bg='#16213e',
                fg='#fff', insertbackground='#fff', relief='flat')
        desc_entry.pack(pady=5, padx=20, fill='x')
        
        def create():
            name = name_entry.get().strip()
            desc = desc_entry.get().strip()
            if name:
                proj_id = self.db.add_project(name, desc)
                if proj_id > 0:
                    self.logger.log_project_action(name, "created")
                    self.db.log_activity("project_created", name)
                    dialog.destroy()
                    self.refresh_list()
                    messagebox.showinfo("Success", f"Project '{name}' created!")
                else:
                    messagebox.showerror("Error", "Project name already exists!")
            else:
                messagebox.showwarning("Warning", "Enter a project name")
        
        tk.Button(dialog, text="Create Project", font=('Courier', 10, 'bold'),
                fg='#000', bg='#00ff88', relief='flat', padx=20, pady=10,
                command=create).pack(pady=20)
    
    def open_project(self, project):
        self.logger.log_project_action(project['name'], "opened")
        self.db.log_activity("project_opened", project['name'])
        
        # Show project overview
        for widget in self.frame.winfo_children():
            widget.destroy()
        
        # Back button
        tk.Button(self.frame, text="← Back to Projects", font=('Courier', 10),
                fg='#00ccff', bg='#1a1a2e', relief='flat',
                command=self.build).pack(anchor='w', pady=5)
        
        tk.Label(self.frame, text=f"📁 {project['name']}", font=('Courier', 18, 'bold'),
                fg='#00ff88', bg='#1a1a2e').pack(anchor='w', pady=(10,5))
        
        desc = project.get('description', '') or 'No description'
        tk.Label(self.frame, text=desc, font=('Courier', 10),
                fg='#aaa', bg='#1a1a2e').pack(anchor='w')
        
        # Quick links
        links_frame = tk.Frame(self.frame, bg='#1a1a2e')
        links_frame.pack(fill='x', pady=20)
        
        quick_actions = [
            ("🎯 Recon", "recon"),
            ("🌐 Network Scan", "network"),
            ("🌍 Web Scan", "web"),
            ("📝 Notes", "notes"),
            ("🔒 Evidence", "evidence"),
            ("📋 Reports", "reports")
        ]
        
        for text, cmd in quick_actions:
            btn = tk.Button(links_frame, text=text, font=('Courier', 10),
                    fg='#000', bg='#00ccff', relief='flat', padx=15, pady=8,
                    command=lambda c=cmd: self._navigate(c))
            btn.pack(side='left', padx=5)
        
        # Project contents
        proj_path = project.get('path', '')
        if proj_path and os.path.exists(proj_path):
            tk.Label(self.frame, text="Project Contents:", font=('Courier', 12, 'bold'),
                    fg='#00ccff', bg='#1a1a2e').pack(anchor='w', pady=(20,5))
            
            for folder in ['logs', 'evidence', 'notes', 'reports', 'screenshots', 'scripts', 'exports']:
                fpath = os.path.join(proj_path, folder)
                if os.path.exists(fpath):
                    count = len([f for f in os.listdir(fpath) if os.path.isfile(os.path.join(fpath, f))])
                    tk.Label(self.frame, text=f"  📂 {folder}: {count} files", font=('Courier', 9),
                            fg='#888', bg='#1a1a2e').pack(anchor='w')
    
    def _navigate(self, command):
        if self.navigate_callback:
            self.navigate_callback(command)
    
    def delete_project(self, project):
        if messagebox.askyesno("Delete Project", 
                f"Delete '{project['name']}' and all its data?\nThis cannot be undone!"):
            self.db.delete_project(project['id'])
            self.logger.log_project_action(project['name'], "deleted")
            self.db.log_activity("project_deleted", project['name'])
            self.refresh_list()
