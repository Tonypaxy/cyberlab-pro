"""
CyberLab Pro - Universal Data Locker
Auto-detects and stores valuable data from ALL tools during hacking.
Credentials, hashes, tokens, URLs, IPs, ports, vulnerabilities, emails, subdomains.
One centralized storage for everything found during pentesting.
"""
import tkinter as tk
from tkinter import ttk, messagebox
import os
import json
import re
from datetime import datetime
import threading

class CredentialLocker:
    def __init__(self, parent, db, logger):
        self.parent = parent
        self.db = db
        self.logger = logger
        self.frame = tk.Frame(parent, bg='#1a1a2e')
        self.current_project = None
        self.auto_detect_enabled = True
        self._init_db()
    
    def _init_db(self):
        """Create all data storage tables"""
        tables = [
            '''CREATE TABLE IF NOT EXISTS credentials (
                id INTEGER PRIMARY KEY AUTOINCREMENT, project_id INTEGER, tool TEXT,
                target TEXT, username TEXT, password TEXT, email TEXT, phone TEXT,
                token TEXT, cookie TEXT, url TEXT, ip_address TEXT, user_agent TEXT,
                extra_data TEXT, source TEXT, campaign TEXT,
                found_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, notes TEXT,
                FOREIGN KEY (project_id) REFERENCES projects (id))''',
            
            '''CREATE TABLE IF NOT EXISTS discovered_hashes (
                id INTEGER PRIMARY KEY AUTOINCREMENT, project_id INTEGER, tool TEXT,
                hash_value TEXT, hash_type TEXT, cracked_value TEXT,
                target TEXT, file_path TEXT, found_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (project_id) REFERENCES projects (id))''',
            
            '''CREATE TABLE IF NOT EXISTS discovered_hosts (
                id INTEGER PRIMARY KEY AUTOINCREMENT, project_id INTEGER, tool TEXT,
                ip_address TEXT, hostname TEXT, ports TEXT, services TEXT,
                os_info TEXT, mac_address TEXT, status TEXT DEFAULT 'up',
                found_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (project_id) REFERENCES projects (id))''',
            
            '''CREATE TABLE IF NOT EXISTS discovered_urls (
                id INTEGER PRIMARY KEY AUTOINCREMENT, project_id INTEGER, tool TEXT,
                url TEXT, status_code INTEGER, content_type TEXT, title TEXT,
                parameters TEXT, vulnerable BOOLEAN DEFAULT 0,
                found_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (project_id) REFERENCES projects (id))''',
            
            '''CREATE TABLE IF NOT EXISTS discovered_emails (
                id INTEGER PRIMARY KEY AUTOINCREMENT, project_id INTEGER, tool TEXT,
                email TEXT, source TEXT, domain TEXT, verified BOOLEAN DEFAULT 0,
                found_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (project_id) REFERENCES projects (id))''',
            
            '''CREATE TABLE IF NOT EXISTS discovered_subdomains (
                id INTEGER PRIMARY KEY AUTOINCREMENT, project_id INTEGER, tool TEXT,
                subdomain TEXT, ip_address TEXT, status_code INTEGER,
                found_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (project_id) REFERENCES projects (id))''',
            
            '''CREATE TABLE IF NOT EXISTS discovered_vulns (
                id INTEGER PRIMARY KEY AUTOINCREMENT, project_id INTEGER, tool TEXT,
                vuln_name TEXT, severity TEXT, description TEXT, cve_id TEXT,
                cvss_score REAL, target TEXT, url TEXT, remediation TEXT,
                found_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (project_id) REFERENCES projects (id))''',
            
            '''CREATE TABLE IF NOT EXISTS phishing_campaigns (
                id INTEGER PRIMARY KEY AUTOINCREMENT, project_id INTEGER,
                name TEXT, target_site TEXT, template TEXT, landing_page TEXT,
                emails_sent INTEGER DEFAULT 0, clicks INTEGER DEFAULT 0,
                credentials_captured INTEGER DEFAULT 0,
                started_at TIMESTAMP, ended_at TIMESTAMP, status TEXT DEFAULT 'active',
                FOREIGN KEY (project_id) REFERENCES projects (id))''',
            
            '''CREATE TABLE IF NOT EXISTS tool_output_cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT, project_id INTEGER,
                tool TEXT, command TEXT, output_summary TEXT, valuable_data TEXT,
                executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (project_id) REFERENCES projects (id))'''
        ]
        
        for table in tables:
            try:
                self.db.cursor.execute(table)
            except:
                pass
        self.db.conn.commit()
    
    def build(self):
        for w in self.frame.winfo_children(): w.destroy()
        self.frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Auto-select first project if none selected
        if not self.current_project:
            projects = self.db.get_all_projects()
            if projects:
                self.current_project = projects[0]
        
        # Header
        header = tk.Frame(self.frame, bg='#1a1a2e')
        header.pack(fill='x', pady=(0,10))
        
        tk.Label(header, text="💎 Universal Data Locker", font=('Courier', 18, 'bold'),
                fg='#ff4488', bg='#1a1a2e').pack(side='left')
        
        tk.Button(header, text="+ Add Data", font=('Courier', 9),
                fg='#000', bg='#00ff88', relief='raised', padx=10,
                command=self._add_data_dialog).pack(side='right', padx=2)
        tk.Button(header, text="📥 Import", font=('Courier', 9),
                fg='#000', bg='#ffaa00', relief='raised', padx=10,
                command=self._import_data).pack(side='right', padx=2)
        tk.Button(header, text="📤 Export All", font=('Courier', 9),
                fg='#000', bg='#00ccff', relief='raised', padx=10,
                command=self._export_all).pack(side='right', padx=2)
        tk.Button(header, text="🗑 Clear All", font=('Courier', 9),
                fg='#fff', bg='#cc0000', relief='raised', padx=10,
                command=self._clear_all).pack(side='right', padx=2)
        
        # Project selector
        proj_frame = tk.Frame(self.frame, bg='#16213e', padx=10, pady=8)
        proj_frame.pack(fill='x', pady=5)
        
        tk.Label(proj_frame, text="Project:", font=('Courier', 10), fg='#fff', bg='#16213e').pack(side='left')
        self.project_var = tk.StringVar()
        projects = self.db.get_all_projects()
        names = [p['name'] for p in projects]
        if names:
            self.proj_menu = ttk.Combobox(proj_frame, textvariable=self.project_var,
                    values=names, font=('Courier', 10), state='readonly', width=25)
            self.proj_menu.pack(side='left', padx=10)
            self.proj_menu.set(names[0])
            self._set_project(names[0])
            self.proj_menu.bind('<<ComboboxSelected>>', lambda e: self._refresh())
        
        # Auto-detect toggle
        self.auto_var = tk.BooleanVar(value=True)
        tk.Checkbutton(proj_frame, text="Auto-detect", variable=self.auto_var,
                font=('Courier', 9), fg='#888', bg='#16213e', selectcolor='#00ff88',
                command=lambda: setattr(self, 'auto_detect_enabled', self.auto_var.get())).pack(side='right', padx=10)
        
        tk.Button(proj_frame, text="🔄 Refresh", font=('Courier', 9),
                fg='#000', bg='#00ccff', relief='flat', padx=10,
                command=self._refresh).pack(side='right')
        
        # Search bar
        search_frame = tk.Frame(self.frame, bg='#1a1a2e')
        search_frame.pack(fill='x', pady=5)
        self.search_entry = tk.Entry(search_frame, font=('Courier', 10), bg='#16213e', fg='#fff', relief='flat')
        self.search_entry.pack(side='left', fill='x', expand=True)
        self.search_entry.insert(0, 'Search all data...')
        self.search_entry.bind('<Return>', lambda e: self._refresh())
        tk.Button(search_frame, text="🔍", font=('Courier', 10),
                fg='#000', bg='#00ccff', relief='flat', padx=10,
                command=self._refresh).pack(side='right')
        
        # Category tabs
        self.notebook = ttk.Notebook(self.frame)
        self.notebook.pack(fill='both', expand=True)
        
        style = ttk.Style()
        style.configure('TNotebook', background='#1a1a2e')
        style.configure('TNotebook.Tab', background='#16213e', foreground='#00ccff', padding=[10,4])
        style.map('TNotebook.Tab', background=[('selected', '#0f3460')], foreground=[('selected', '#00ff88')])
        
        self.tabs = {
            'creds': ('🔑 Credentials', self._load_credentials),
            'hashes': ('#️⃣ Hashes', self._load_hashes),
            'hosts': ('🖥️ Hosts/Ports', self._load_hosts),
            'urls': ('🔗 URLs/Endpoints', self._load_urls),
            'emails': ('📧 Emails', self._load_emails),
            'subdomains': ('🌐 Subdomains', self._load_subdomains),
            'vulns': ('⚠️ Vulnerabilities', self._load_vulns),
            'campaigns': ('📊 Campaigns', self._load_campaigns),
        }
        
        self.tab_frames = {}
        for key, (label, loader) in self.tabs.items():
            frame = tk.Frame(self.notebook, bg='#1a1a2e')
            self.notebook.add(frame, text=f'  {label}  ')
            self.tab_frames[key] = {'frame': frame, 'loader': loader}
        
        # Stats bar
        self.stats_label = tk.Label(self.frame, text="", font=('Courier', 9),
                fg='#888', bg='#1a1a2e')
        self.stats_label.pack(fill='x', pady=3)
        
        self._refresh()
    
    def _set_project(self, name):
        projects = self.db.get_all_projects()
        for p in projects:
            if p['name'] == name:
                self.current_project = p
                break
    
    def _refresh(self):
        if not hasattr(self, 'current_project') or not self.current_project:
            return
        
        # Load all tabs
        for key, tab_data in self.tab_frames.items():
            for w in tab_data['frame'].winfo_children():
                w.destroy()
            tab_data['loader'](tab_data['frame'])
        
        # Update stats
        self._update_stats()
    
    def _search_filter(self, table, fields):
        """Build search query"""
        search = self.search_entry.get().strip()
        if not search or search == 'Search all data...':
            self.db.cursor.execute(f'SELECT * FROM {table} WHERE project_id = ? ORDER BY found_at DESC LIMIT 200',
                    (self.current_project['id'],))
        else:
            conditions = ' OR '.join([f'{f} LIKE ?' for f in fields])
            params = [self.current_project['id']] + [f'%{search}%'] * len(fields)
            self.db.cursor.execute(f'SELECT * FROM {table} WHERE project_id = ? AND ({conditions}) ORDER BY found_at DESC LIMIT 200',
                    params)
        return [dict(row) for row in self.db.cursor.fetchall()]
    
    def _create_scrollable_list(self, parent):
        """Create a scrollable list frame"""
        canvas = tk.Canvas(parent, bg='#1a1a2e', highlightthickness=0)
        scrollbar = tk.Scrollbar(parent, orient='vertical', command=canvas.yview)
        sf = tk.Frame(canvas, bg='#1a1a2e')
        sf.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.create_window((0,0), window=sf, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        return sf
    
    def _data_card(self, parent, data, fields, title_key='title', color='#00ff88', on_view=None, on_copy=None, on_delete=None):
        """Create a standardized data card"""
        card = tk.Frame(parent, bg='#16213e', relief='flat', bd=0)
        card.pack(fill='x', padx=5, pady=2)
        
        info = tk.Frame(card, bg='#16213e')
        info.pack(side='left', fill='x', expand=True, padx=12, pady=8)
        
        # Title line
        title = data.get(title_key, 'Unknown') if title_key in data else 'Entry'
        tk.Label(info, text=str(title)[:60], font=('Courier', 10, 'bold'),
                fg=color, bg='#16213e').pack(anchor='w')
        
        # Details line
        detail_parts = []
        for f in fields:
            val = data.get(f, '')
            if val:
                detail_parts.append(f"{f}: {str(val)[:30]}")
        if detail_parts:
            tk.Label(info, text=' | '.join(detail_parts[:4]), font=('Courier', 8),
                    fg='#888', bg='#16213e').pack(anchor='w')
        
        # Time
        if data.get('found_at'):
            tk.Label(info, text=str(data['found_at'])[:19], font=('Courier', 7),
                    fg='#555', bg='#16213e').pack(anchor='w')
        
        actions = tk.Frame(card, bg='#16213e')
        actions.pack(side='right', padx=12, pady=8)
        
        if on_view:
            tk.Button(actions, text="👁", font=('Courier', 8), fg='#000', bg='#00ccff', relief='flat', padx=6,
                    command=on_view).pack(side='left', padx=1)
        if on_copy:
            tk.Button(actions, text="📋", font=('Courier', 8), fg='#000', bg='#ffaa00', relief='flat', padx=6,
                    command=on_copy).pack(side='left', padx=1)
        if on_delete:
            tk.Button(actions, text="🗑", font=('Courier', 8), fg='#fff', bg='#cc0000', relief='flat', padx=6,
                    command=on_delete).pack(side='left', padx=1)
    
    # === LOADERS FOR EACH CATEGORY ===
    
    def _load_credentials(self, parent):
        sf = self._create_scrollable_list(parent)
        creds = self._search_filter('credentials', ['username', 'password', 'email', 'target', 'tool', 'url'])
        
        if not creds:
            tk.Label(sf, text="No credentials yet", font=('Courier', 10), fg='#666', bg='#1a1a2e').pack(pady=20)
            return
        
        for c in creds:
            self._data_card(sf, c, ['username', 'password', 'email', 'target'], 'username', '#00ff88',
                on_view=lambda d=c: self._view_detail('Credentials', d),
                on_copy=lambda d=c: self._copy_text(f"{d.get('username','')}:{d.get('password','')}"),
                on_delete=lambda d=c: self._delete_entry('credentials', d['id']))
    
    def _load_hashes(self, parent):
        sf = self._create_scrollable_list(parent)
        hashes = self._search_filter('discovered_hashes', ['hash_value', 'hash_type', 'cracked_value', 'target'])
        
        if not hashes:
            tk.Label(sf, text="No hashes discovered", font=('Courier', 10), fg='#666', bg='#1a1a2e').pack(pady=20)
            return
        
        for h in hashes:
            self._data_card(sf, h, ['hash_type', 'cracked_value', 'target'], 'hash_value', '#ff4488',
                on_view=lambda d=h: self._view_detail('Hash', d),
                on_copy=lambda d=h: self._copy_text(d.get('hash_value','')),
                on_delete=lambda d=h: self._delete_entry('discovered_hashes', d['id']))
    
    def _load_hosts(self, parent):
        sf = self._create_scrollable_list(parent)
        hosts = self._search_filter('discovered_hosts', ['ip_address', 'hostname', 'ports', 'services', 'os_info'])
        
        if not hosts:
            tk.Label(sf, text="No hosts discovered", font=('Courier', 10), fg='#666', bg='#1a1a2e').pack(pady=20)
            return
        
        for h in hosts:
            self._data_card(sf, h, ['hostname', 'ports', 'services', 'os_info'], 'ip_address', '#58a6ff',
                on_view=lambda d=h: self._view_detail('Host', d),
                on_copy=lambda d=h: self._copy_text(f"{d.get('ip_address','')} {d.get('hostname','')}"),
                on_delete=lambda d=h: self._delete_entry('discovered_hosts', d['id']))
    
    def _load_urls(self, parent):
        sf = self._create_scrollable_list(parent)
        urls = self._search_filter('discovered_urls', ['url', 'title', 'parameters', 'status_code'])
        
        if not urls:
            tk.Label(sf, text="No URLs discovered", font=('Courier', 10), fg='#666', bg='#1a1a2e').pack(pady=20)
            return
        
        for u in urls:
            self._data_card(sf, u, ['status_code', 'title', 'parameters'], 'url', '#d2991d',
                on_view=lambda d=u: self._view_detail('URL', d),
                on_copy=lambda d=u: self._copy_text(d.get('url','')),
                on_delete=lambda d=u: self._delete_entry('discovered_urls', d['id']))
    
    def _load_emails(self, parent):
        sf = self._create_scrollable_list(parent)
        emails = self._search_filter('discovered_emails', ['email', 'source', 'domain'])
        
        if not emails:
            tk.Label(sf, text="No emails discovered", font=('Courier', 10), fg='#666', bg='#1a1a2e').pack(pady=20)
            return
        
        for e in emails:
            self._data_card(sf, e, ['source', 'domain'], 'email', '#bc8cff',
                on_copy=lambda d=e: self._copy_text(d.get('email','')),
                on_delete=lambda d=e: self._delete_entry('discovered_emails', d['id']))
    
    def _load_subdomains(self, parent):
        sf = self._create_scrollable_list(parent)
        subs = self._search_filter('discovered_subdomains', ['subdomain', 'ip_address'])
        
        if not subs:
            tk.Label(sf, text="No subdomains discovered", font=('Courier', 10), fg='#666', bg='#1a1a2e').pack(pady=20)
            return
        
        for s in subs:
            self._data_card(sf, s, ['ip_address', 'status_code'], 'subdomain', '#39c5cf',
                on_delete=lambda d=s: self._delete_entry('discovered_subdomains', d['id']))
    
    def _load_vulns(self, parent):
        sf = self._create_scrollable_list(parent)
        vulns = self._search_filter('discovered_vulns', ['vuln_name', 'severity', 'cve_id', 'target', 'description'])
        
        if not vulns:
            tk.Label(sf, text="No vulnerabilities found", font=('Courier', 10), fg='#666', bg='#1a1a2e').pack(pady=20)
            return
        
        for v in vulns:
            sev_color = {'CRITICAL': '#ff0000', 'HIGH': '#ff4444', 'MEDIUM': '#ffaa00', 'LOW': '#00ff88', 'INFO': '#00ccff'}
            color = sev_color.get(v.get('severity', '').upper(), '#ffaa00')
            self._data_card(sf, v, ['severity', 'cve_id', 'target'], 'vuln_name', color,
                on_view=lambda d=v: self._view_detail('Vulnerability', d),
                on_delete=lambda d=v: self._delete_entry('discovered_vulns', d['id']))
    
    def _load_campaigns(self, parent):
        sf = self._create_scrollable_list(parent)
        self.db.cursor.execute('SELECT * FROM phishing_campaigns WHERE project_id = ? ORDER BY started_at DESC',
                (self.current_project['id'],))
        campaigns = [dict(row) for row in self.db.cursor.fetchall()]
        
        if not campaigns:
            tk.Label(sf, text="No campaigns", font=('Courier', 10), fg='#666', bg='#1a1a2e').pack(pady=20)
            tk.Button(sf, text="+ New Campaign", font=('Courier', 10), fg='#000', bg='#00ff88',
                    relief='raised', padx=15, pady=5, command=self._new_campaign).pack(pady=10)
            return
        
        for c in campaigns:
            self._data_card(sf, c, ['target_site', 'emails_sent', 'clicks', 'credentials_captured'], 'name', '#ffaa00',
                on_delete=lambda d=c: self._delete_entry('phishing_campaigns', d['id']))
    
    def _update_stats(self):
        """Update statistics bar"""
        tables = ['credentials', 'discovered_hashes', 'discovered_hosts', 'discovered_urls',
                  'discovered_emails', 'discovered_subdomains', 'discovered_vulns']
        counts = {}
        for table in tables:
            self.db.cursor.execute(f'SELECT COUNT(*) FROM {table} WHERE project_id = ?',
                    (self.current_project['id'],))
            counts[table] = self.db.cursor.fetchone()[0]
        
        total = sum(counts.values())
        parts = [f"Total: {total}"]
        for k, v in counts.items():
            if v > 0:
                parts.append(f"{k.split('_')[1]}: {v}")
        self.stats_label.config(text=' | '.join(parts))
    
    def _view_detail(self, title, data):
        dialog = tk.Toplevel(self.parent, bg='#1a1a2e')
        dialog.title(f"{title} Details"); dialog.geometry("450x400")
        
        tk.Label(dialog, text=f"{title} Details", font=('Courier', 14, 'bold'),
                fg='#00ff88', bg='#1a1a2e').pack(pady=10)
        
        text = tk.Text(dialog, font=('Courier', 10), bg='#0a0a0a', fg='#00ff88', relief='flat')
        text.pack(fill='both', expand=True, padx=10, pady=10)
        
        for k, v in data.items():
            if v and k != 'id' and k != 'project_id':
                text.insert('end', f"{k}: {v}\n")
        
        text.config(state='disabled')
        tk.Button(dialog, text="Close", font=('Courier', 10), fg='#fff', bg='#666',
                relief='raised', padx=15, pady=5, command=dialog.destroy).pack(pady=5)
    
    def _delete_entry(self, table, entry_id):
        if messagebox.askyesno("Delete", "Delete this entry permanently?"):
            self.db.cursor.execute(f'DELETE FROM {table} WHERE id = ?', (entry_id,))
            self.db.conn.commit()
            self._refresh()
    
    def _clear_all(self):
        if not self.current_project: return
        if messagebox.askyesno("⚠️ Clear All", "Delete ALL data for this project?\n\nThis CANNOT be undone!"):
            tables = ['credentials', 'discovered_hashes', 'discovered_hosts', 'discovered_urls',
                      'discovered_emails', 'discovered_subdomains', 'discovered_vulns', 'phishing_campaigns']
            for table in tables:
                self.db.cursor.execute(f'DELETE FROM {table} WHERE project_id = ?', (self.current_project['id'],))
            self.db.conn.commit()
            self._refresh()
    
    def _copy_text(self, text):
        try:
            self.frame.clipboard_clear()
            self.frame.clipboard_append(str(text))
        except:
            pass
    
    def _add_data_dialog(self):
        if not self.current_project: return
        
        dialog = tk.Toplevel(self.parent, bg='#1a1a2e')
        dialog.title("Add Data Entry"); dialog.geometry("500x550")
        
        tk.Label(dialog, text="Add Data Entry", font=('Courier', 14, 'bold'),
                fg='#00ff88', bg='#1a1a2e').pack(pady=10)
        
        # Category selector
        tk.Label(dialog, text="Type:", font=('Courier', 10), fg='#fff', bg='#1a1a2e').pack(anchor='w', padx=20)
        cat_var = tk.StringVar(value='creds')
        cats = {'creds': 'Credentials', 'hashes': 'Hash', 'hosts': 'Host/Port', 'urls': 'URL', 'emails': 'Email', 'subdomains': 'Subdomain', 'vulns': 'Vulnerability'}
        for key, label in cats.items():
            tk.Radiobutton(dialog, text=label, variable=cat_var, value=key,
                    font=('Courier', 9), fg='#aaa', bg='#1a1a2e', selectcolor='#00ff88').pack(anchor='w', padx=40)
        
        # Fields
        tk.Label(dialog, text="Value:", font=('Courier', 10), fg='#fff', bg='#1a1a2e').pack(anchor='w', padx=20)
        val_entry = tk.Text(dialog, font=('Courier', 10), bg='#16213e', fg='#fff', relief='flat', height=8)
        val_entry.pack(fill='x', padx=20, pady=5)
        
        tk.Label(dialog, text="Tool/Source:", font=('Courier', 10), fg='#fff', bg='#1a1a2e').pack(anchor='w', padx=20)
        tool_entry = tk.Entry(dialog, font=('Courier', 10), bg='#16213e', fg='#fff', relief='flat')
        tool_entry.pack(fill='x', padx=20, pady=5)
        tool_entry.insert(0, 'manual')
        
        tk.Label(dialog, text="Target:", font=('Courier', 10), fg='#fff', bg='#1a1a2e').pack(anchor='w', padx=20)
        target_entry = tk.Entry(dialog, font=('Courier', 10), bg='#16213e', fg='#fff', relief='flat')
        target_entry.pack(fill='x', padx=20, pady=5)
        
        tk.Label(dialog, text="Notes:", font=('Courier', 10), fg='#fff', bg='#1a1a2e').pack(anchor='w', padx=20)
        notes_entry = tk.Entry(dialog, font=('Courier', 10), bg='#16213e', fg='#fff', relief='flat')
        notes_entry.pack(fill='x', padx=20, pady=5)
        
        def save():
            cat = cat_var.get()
            val = val_entry.get('1.0', 'end-1c').strip()
            tool = tool_entry.get().strip()
            target = target_entry.get().strip()
            notes = notes_entry.get().strip()
            
            if not val: return
            
            table_map = {
                'creds': ('credentials', {'username': val, 'tool': tool, 'target': target, 'notes': notes}),
                'hashes': ('discovered_hashes', {'hash_value': val, 'tool': tool, 'target': target}),
                'hosts': ('discovered_hosts', {'ip_address': val, 'tool': tool}),
                'urls': ('discovered_urls', {'url': val, 'tool': tool, 'target': target}),
                'emails': ('discovered_emails', {'email': val, 'tool': tool, 'source': target}),
                'subdomains': ('discovered_subdomains', {'subdomain': val, 'tool': tool}),
                'vulns': ('discovered_vulns', {'vuln_name': val, 'tool': tool, 'target': target}),
            }
    
    def _import_data(self):
        if not self.current_project: return
        dialog = tk.Toplevel(self.parent, bg='#1a1a2e')
        dialog.title("Import Data"); dialog.geometry("500x300")
        tk.Label(dialog, text="Paste tool output to auto-extract data:", font=('Courier', 10),
                fg='#fff', bg='#1a1a2e').pack(pady=5)
        text = tk.Text(dialog, font=('Courier', 9), bg='#16213e', fg='#fff', relief='flat', height=12)
        text.pack(fill='both', expand=True, padx=10, pady=5)
        def extract():
            content = text.get('1.0', 'end-1c')
            found = 0
            for email in set(re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', content)):
                try:
                    self.db.cursor.execute('INSERT INTO discovered_emails (project_id, email, source) VALUES (?, ?, ?)',
                            (self.current_project['id'], email, 'imported'))
                    found += 1
                except: pass
            for ip in set(re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', content)):
                try:
                    self.db.cursor.execute('INSERT INTO discovered_hosts (project_id, ip_address, tool) VALUES (?, ?, ?)',
                            (self.current_project['id'], ip, 'imported'))
                    found += 1
                except: pass
            for url in set(re.findall(r'https?://[^\s<>"\']+', content)):
                try:
                    self.db.cursor.execute('INSERT INTO discovered_urls (project_id, url, tool) VALUES (?, ?, ?)',
                            (self.current_project['id'], url[:500], 'imported'))
                    found += 1
                except: pass
            self.db.conn.commit()
            dialog.destroy()
            self._refresh()
            messagebox.showinfo("Import Complete", f"Extracted {found} items!")
        tk.Button(dialog, text="Auto-Extract", font=('Courier', 10, 'bold'),
                fg='#000', bg='#00ff88', relief='raised', padx=15, pady=8,
                command=extract).pack(pady=10)
        tk.Button(dialog, text="Cancel", font=('Courier', 10),
                fg='#fff', bg='#666', relief='raised', padx=15, pady=5,
                command=dialog.destroy).pack(pady=5)
    
    def _export_all(self):
        if not self.current_project: return
        export_dir = os.path.join(self.current_project['path'], 'exports')
        os.makedirs(export_dir, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        all_data = {}
        for table in ['credentials', 'discovered_hashes', 'discovered_hosts', 'discovered_urls',
                      'discovered_emails', 'discovered_subdomains', 'discovered_vulns']:
            self.db.cursor.execute(f'SELECT * FROM {table} WHERE project_id = ?', (self.current_project['id'],))
            all_data[table] = [dict(row) for row in self.db.cursor.fetchall()]
        json_path = os.path.join(export_dir, f'data_{ts}.json')
        with open(json_path, 'w') as f: json.dump(all_data, f, indent=2, default=str)
        messagebox.showinfo("Exported", f"Data exported to:\n{json_path}")
    
    def auto_store(self, tool_name, output_text, command=""):
        if not self.auto_detect_enabled or not self.current_project: return 0
        found = 0
        for email in set(re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', output_text)):
            try:
                self.db.cursor.execute('INSERT INTO discovered_emails (project_id, email, source, tool) VALUES (?, ?, ?, ?)',
                        (self.current_project['id'], email, 'auto', tool_name))
                found += 1
            except: pass
        for ip in set(re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', output_text)):
            if ip not in ('0.0.0.0','255.255.255.255','127.0.0.1'):
                try:
                    self.db.cursor.execute('INSERT INTO discovered_hosts (project_id, ip_address, tool) VALUES (?, ?, ?)',
                            (self.current_project['id'], ip, tool_name))
                    found += 1
                except: pass
        for u, p in set(re.findall(r'([\w.-]{3,}):([\w.@#$%^&*!]{3,})', output_text)):
            try:
                self.db.cursor.execute('INSERT INTO credentials (project_id, username, password, tool, target) VALUES (?, ?, ?, ?, ?)',
                        (self.current_project['id'], u, p, tool_name, 'auto'))
                found += 1
            except: pass
        for url in set(re.findall(r'https?://[^\s<>"\']+', output_text)):
            try:
                self.db.cursor.execute('INSERT INTO discovered_urls (project_id, url, tool) VALUES (?, ?, ?)',
                        (self.current_project['id'], url[:500], tool_name))
                found += 1
            except: pass
        for h in set(re.findall(r'\b[a-fA-F0-9]{32}\b', output_text)):
            try:
                self.db.cursor.execute('INSERT INTO discovered_hashes (project_id, hash_value, hash_type, tool) VALUES (?, ?, ?, ?)',
                        (self.current_project['id'], h, 'MD5', tool_name))
                found += 1
            except: pass
        if found > 0:
            self.db.conn.commit()
            self.logger.log_project_action(self.current_project['name'], f"auto_stored: {found} from {tool_name}")
        return found
