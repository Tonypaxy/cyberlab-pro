import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class NotePad:
    def __init__(self, parent, db, logger):
        self.parent = parent
        self.db = db
        self.logger = logger
        self.frame = tk.Frame(parent, bg='#1a1a2e')
        self.current_project = None
        self.current_note = None
    
    def build(self):
        self.frame.pack(fill='both', expand=True)
        
        # Main layout - split into project selector and editor
        self.left_panel = tk.Frame(self.frame, bg='#16213e', width=200)
        self.left_panel.pack(side='left', fill='y')
        self.left_panel.pack_propagate(False)
        
        self.right_panel = tk.Frame(self.frame, bg='#1a1a2e')
        self.right_panel.pack(side='left', fill='both', expand=True)
        
        self._build_project_selector()
        self._build_editor()
    
    def _build_project_selector(self):
        tk.Label(self.left_panel, text="Projects", font=('Courier', 12, 'bold'),
                fg='#00ff88', bg='#16213e').pack(pady=10, padx=5)
        
        self.project_list = tk.Listbox(self.left_panel, bg='#0f3460', fg='#fff',
                font=('Courier', 9), selectbackground='#00ff88', selectforeground='#000',
                relief='flat', borderwidth=0)
        self.project_list.pack(fill='both', expand=True, padx=5, pady=5)
        self.project_list.bind('<<ListboxSelect>>', self._on_project_select)
        
        projects = self.db.get_all_projects()
        for p in projects:
            self.project_list.insert('end', p['name'])
    
    def _build_editor(self):
        if not self.current_project:
            tk.Label(self.right_panel, text="Select a project to start taking notes",
                    font=('Courier', 12), fg='#666', bg='#1a1a2e').pack(expand=True)
            return
        
        # Notes list sidebar within editor
        notes_frame = tk.Frame(self.right_panel, bg='#16213e', width=180)
        notes_frame.pack(side='left', fill='y')
        notes_frame.pack_propagate(False)
        
        tk.Label(notes_frame, text="Notes", font=('Courier', 10, 'bold'),
                fg='#00ff88', bg='#16213e').pack(pady=5)
        
        tk.Button(notes_frame, text="+ New", font=('Courier', 9),
                fg='#000', bg='#00ff88', relief='flat', padx=5,
                command=self._new_note).pack(pady=2, padx=5, fill='x')
        
        self.notes_list = tk.Listbox(notes_frame, bg='#0f3460', fg='#fff',
                font=('Courier', 9), selectbackground='#00ff88', selectforeground='#000',
                relief='flat', borderwidth=0)
        self.notes_list.pack(fill='both', expand=True, padx=5, pady=5)
        self.notes_list.bind('<<ListboxSelect>>', self._on_note_select)
        
        # Editor area
        editor_frame = tk.Frame(self.right_panel, bg='#1a1a2e')
        editor_frame.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        
        self.title_entry = tk.Entry(editor_frame, font=('Courier', 12, 'bold'),
                bg='#16213e', fg='#00ff88', insertbackground='#fff', relief='flat')
        self.title_entry.pack(fill='x', pady=(0,5))
        self.title_entry.insert(0, "Note title...")
        
        self.content_text = tk.Text(editor_frame, font=('Courier', 10),
                bg='#0a0a0a', fg='#fff', insertbackground='#00ff88',
                relief='flat', wrap='word', undo=True)
        self.content_text.pack(fill='both', expand=True)
        
        btn_frame = tk.Frame(editor_frame, bg='#1a1a2e')
        btn_frame.pack(fill='x', pady=(5,0))
        
        tk.Button(btn_frame, text="Save", font=('Courier', 10, 'bold'),
                fg='#000', bg='#00ff88', relief='flat', padx=15,
                command=self._save_note).pack(side='right', padx=2)
        
        self._refresh_notes_list()
    
    def _on_project_select(self, event):
        selection = self.project_list.curselection()
        if selection:
            project_name = self.project_list.get(selection[0])
            projects = self.db.get_all_projects()
            for p in projects:
                if p['name'] == project_name:
                    self.current_project = p
                    break
            self._rebuild_editor()
    
    def _rebuild_editor(self):
        for widget in self.right_panel.winfo_children():
            widget.destroy()
        self._build_editor()
    
    def _refresh_notes_list(self):
        self.notes_list.delete(0, 'end')
        if self.current_project:
            notes = self.db.get_project_notes(self.current_project['id'])
            for note in notes:
                self.notes_list.insert('end', note['title'])
    
    def _on_note_select(self, event):
        selection = self.notes_list.curselection()
        if selection and self.current_project:
            title = self.notes_list.get(selection[0])
            notes = self.db.get_project_notes(self.current_project['id'])
            for note in notes:
                if note['title'] == title:
                    self.current_note = note
                    self.title_entry.delete(0, 'end')
                    self.title_entry.insert(0, note['title'])
                    self.content_text.delete('1.0', 'end')
                    self.content_text.insert('1.0', note['content'] or '')
                    break
    
    def _new_note(self):
        self.current_note = None
        self.title_entry.delete(0, 'end')
        self.title_entry.insert(0, "New Note")
        self.content_text.delete('1.0', 'end')
    
    def _save_note(self):
        if not self.current_project:
            messagebox.showwarning("Warning", "Select a project first")
            return
        
        title = self.title_entry.get().strip()
        content = self.content_text.get('1.0', 'end-1c')
        
        if not title:
            messagebox.showwarning("Warning", "Enter a title")
            return
        
        if self.current_note:
            # Update existing
            self.db.cursor.execute(
                "UPDATE notes SET title=?, content=?, updated_at=CURRENT_TIMESTAMP WHERE id=?",
                (title, content, self.current_note['id'])
            )
            self.db.conn.commit()
        else:
            # New note
            self.db.add_note(self.current_project['id'], title, content)
        
        self.logger.log_project_action(self.current_project['name'], f"note_saved: {title}")
        self._refresh_notes_list()
        messagebox.showinfo("Saved", f"Note '{title}' saved!")
