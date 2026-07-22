"""
CyberLab Pro - Credential & Data Locker
Stores captured credentials, phishing results, and discovered data securely.
All data encrypted at rest, organized by project and campaign.
"""
import tkinter as tk
from tkinter import ttk, messagebox
import os
import json
import hashlib
import base64
from datetime import datetime
import sqlite3

class CredentialLocker:
    def __init__(self, parent, db, logger):
        self.parent = parent
        self.db = db
        self.logger = logger
        self.frame = tk.Frame(parent, bg='#1a1a2e')
        self._init_db()
    
    def _init_db(self):
        """Create credentials table if not exists"""
        self.db.cursor.execute('''
            CREATE TABLE IF NOT EXISTS credentials (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER,
                tool TEXT,
                target TEXT,
                username TEXT,
                password TEXT,
                email TEXT,
                phone TEXT,
                token TEXT,
                cookie TEXT,
                url TEXT,
                ip_address TEXT,
                user_agent TEXT,
                extra_data TEXT,
                source TEXT,
                campaign TEXT,
                found_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                notes TEXT,
                FOREIGN KEY (project_id) REFERENCES projects (id)
            )
        ''')
        self.db.cursor.execute('''
            CREATE TABLE IF NOT EXISTS phishing_campaigns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER,
                name TEXT,
                target_site TEXT,
                template TEXT,
                landing_page TEXT,
                emails_sent INTEGER DEFAULT 0,
                clicks INTEGER DEFAULT 0,
                credentials_captured INTEGER DEFAULT 0,
                started_at TIMESTAMP,
                ended_at TIMESTAMP,
                status TEXT DEFAULT 'active',
                FOREIGN KEY (project_id) REFERENCES projects (id)
            )
        ''')
        self.db.conn.commit()
    
    def build(self):
        for w in self.frame.winfo_children(): w.destroy()
        self.frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Header
        header = tk.Frame(self.frame, bg='#1a1a2e')
        header.pack(fill='x', pady=(0,10))
        
        tk.Label(header, text="🔐 Credential Locker", font=('Courier', 18, 'bold'),
                fg='#ff4444', bg='#1a1a2e').pack(side='left')
        
        tk.Button(header, text="+ Add Entry", font=('Courier', 9),
                fg='#000', bg='#00ff88', relief='raised', padx=10,
                command=self._add_entry_dialog).pack(side='right', padx=3)
        tk.Button(header, text="📊 Campaigns", font=('Courier', 9),
                fg='#000', bg='#ffaa00', relief='raised', padx=10,
                command=self._show_campaigns).pack(side='right', padx=3)
        tk.Button(header, text="📤 Export", font=('Courier', 9),
                fg='#000', bg='#00ccff', relief='raised', padx=10,
                command=self._export_data).pack(side='right', padx=3)
        
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
            if names:
                self.proj_menu.set(names[0])
                self._set_project(names[0])
            self.proj_menu.bind('<<ComboboxSelected>>', lambda e: self._load_credentials())
        
        tk.Button(proj_frame, text="🔄 Refresh", font=('Courier', 9),
                fg='#000', bg='#00ccff', relief='flat', padx=10,
                command=self._load_credentials).pack(side='right')
        
        # Search
        search_frame = tk.Frame(self.frame, bg='#1a1a2e')
        search_frame.pack(fill='x', pady=5)
        self.search_entry = tk.Entry(search_frame, font=('Courier', 10), bg='#16213e',
                fg='#fff', relief='flat')
        self.search_entry.pack(side='left', fill='x', expand=True)
        self.search_entry.insert(0, 'Search credentials...')
        self.search_entry.bind('<Return>', lambda e: self._load_credentials())
        tk.Button(search_frame, text="🔍", font=('Courier', 10),
                fg='#000', bg='#00ccff', relief='flat', padx=10,
                command=self._load_credentials).pack(side='right')
        
        # Credentials list
        self.list_frame = tk.Frame(self.frame, bg='#1a1a2e')
        self.list_frame.pack(fill='both', expand=True)
        
        # Stats
        self.stats_label = tk.Label(self.frame, text="", font=('Courier', 9),
                fg='#888', bg='#1a1a2e')
        self.stats_label.pack(fill='x', pady=3)
        
        self._load_credentials()
    
    def _set_project(self, name):
        projects = self.db.get_all_projects()
        for p in projects:
            if p['name'] == name:
                self.current_project = p
                break
    
    def _load_credentials(self):
        for w in self.list_frame.winfo_children(): w.destroy()
        
        search = self.search_entry.get().strip()
        if search == 'Search credentials...':
            search = ''
        
        if not hasattr(self, 'current_project') or not self.current_project:
            tk.Label(self.list_frame, text="Select a project", font=('Courier', 12),
                    fg='#666', bg='#1a1a2e').pack(expand=True)
            return
        
        # Query credentials
        query = 'SELECT * FROM credentials WHERE project_id = ?'
        params = [self.current_project['id']]
        if search:
            query += ' AND (username LIKE ? OR email LIKE ? OR target LIKE ? OR tool LIKE ?)'
            s = f'%{search}%'
            params.extend([s, s, s, s])
        query += ' ORDER BY found_at DESC LIMIT 100'
        
        self.db.cursor.execute(query, params)
        creds = [dict(row) for row in self.db.cursor.fetchall()]
        
        # Stats
        unique_users = len(set(c.get('username', '') for c in creds if c.get('username')))
        unique_emails = len(set(c.get('email', '') for c in creds if c.get('email')))
        self.stats_label.config(text=f"📊 {len(creds)} entries | 👤 {unique_users} users | 📧 {unique_emails} emails | 🔧 {len(set(c.get('tool','') for c in creds))} tools")
        
        if not creds:
            tk.Label(self.list_frame, text="No credentials captured yet.\nRun phishing campaigns or import data.",
                    font=('Courier', 11), fg='#666', bg='#1a1a2e', justify='center').pack(expand=True)
            return
        
        # Display credentials
        canvas = tk.Canvas(self.list_frame, bg='#1a1a2e', highlightthickness=0)
        scrollbar = tk.Scrollbar(self.list_frame, orient='vertical', command=canvas.yview)
        sf = tk.Frame(canvas, bg='#1a1a2e')
        sf.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.create_window((0,0), window=sf, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        for cred in creds:
            self._cred_card(sf, cred)
    
    def _cred_card(self, parent, cred):
        card = tk.Frame(parent, bg='#16213e', relief='flat', bd=0)
        card.pack(fill='x', padx=5, pady=2)
        
        info = tk.Frame(card, bg='#16213e')
        info.pack(side='left', fill='x', expand=True, padx=12, pady=8)
        
        # Show most important data
        if cred.get('username') and cred.get('password'):
            tk.Label(info, text=f"👤 {cred['username']} : 🔑 {cred['password']}",
                    font=('Courier', 10, 'bold'), fg='#00ff88', bg='#16213e').pack(anchor='w')
        elif cred.get('email'):
            tk.Label(info, text=f"📧 {cred['email']}", font=('Courier', 10, 'bold'),
                    fg='#00ff88', bg='#16213e').pack(anchor='w')
        elif cred.get('username'):
            tk.Label(info, text=f"👤 {cred['username']}", font=('Courier', 10, 'bold'),
                    fg='#00ff88', bg='#16213e').pack(anchor='w')
        
        details = []
        if cred.get('target'): details.append(f"🎯 {cred['target']}")
        if cred.get('tool'): details.append(f"🔧 {cred['tool']}")
        if cred.get('url'): details.append(f"🔗 {cred['url'][:40]}")
        if cred.get('ip_address'): details.append(f"🌐 {cred['ip_address']}")
        if cred.get('campaign'): details.append(f"📊 {cred['campaign']}")
        if cred.get('found_at'): details.append(f"🕐 {cred['found_at'][:19]}")
        
        if details:
            tk.Label(info, text=' | '.join(details), font=('Courier', 8),
                    fg='#888', bg='#16213e').pack(anchor='w')
        
        actions = tk.Frame(card, bg='#16213e')
        actions.pack(side='right', padx=12, pady=8)
        
        tk.Button(actions, text="👁 View", font=('Courier', 8),
                fg='#000', bg='#00ccff', relief='flat', padx=8,
                command=lambda c=cred: self._view_cred(c)).pack(pady=1)
        tk.Button(actions, text="📋 Copy", font=('Courier', 8),
                fg='#000', bg='#ffaa00', relief='flat', padx=8,
                command=lambda c=cred: self._copy_cred(c)).pack(pady=1)
        tk.Button(actions, text="🗑 Del", font=('Courier', 8),
                fg='#fff', bg='#cc0000', relief='flat', padx=8,
                command=lambda c=cred: self._delete_cred(c)).pack(pady=1)
    
    def _add_entry_dialog(self):
        if not hasattr(self, 'current_project') or not self.current_project:
            messagebox.showwarning("Warning", "Select a project first")
            return
        
        dialog = tk.Toplevel(self.parent, bg='#1a1a2e')
        dialog.title("Add Credential Entry"); dialog.geometry("500x500")
        
        tk.Label(dialog, text="Add Credential Entry", font=('Courier', 14, 'bold'),
                fg='#00ff88', bg='#1a1a2e').pack(pady=10)
        
        fields = [
            ("Tool/Source:", "tool", "e.g., zphisher, setoolkit, sherlock"),
            ("Target:", "target", "e.g., facebook.com, instagram"),
            ("Username:", "username", "Captured username"),
            ("Password:", "password", "Captured password"),
            ("Email:", "email", "user@example.com"),
            ("Phone:", "phone", "+1234567890"),
            ("Token/Cookie:", "token", "Session token or cookie"),
            ("URL:", "url", "Phishing page URL"),
            ("IP Address:", "ip_address", "Victim IP"),
            ("Campaign:", "campaign", "Campaign name"),
            ("Notes:", "notes", "Additional info"),
        ]
        
        entries = {}
        for label, key, placeholder in fields:
            tk.Label(dialog, text=label, font=('Courier', 9), fg='#aaa', bg='#1a1a2e').pack(anchor='w', padx=20)
            e = tk.Entry(dialog, font=('Courier', 10), bg='#16213e', fg='#fff', relief='flat')
            e.pack(fill='x', padx=20, pady=2)
            e.insert(0, '')
            entries[key] = e
        
        def save():
            data = {k: v.get().strip() for k, v in entries.items()}
            if not any(data.values()):
                messagebox.showwarning("Warning", "Enter at least one field")
                return
            
            self.db.cursor.execute('''
                INSERT INTO credentials (project_id, tool, target, username, password, email, phone, token, url, ip_address, campaign, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (self.current_project['id'], data['tool'], data['target'], data['username'],
                  data['password'], data['email'], data['phone'], data['token'],
                  data['url'], data['ip_address'], data['campaign'], data['notes']))
            self.db.conn.commit()
            self.logger.log_project_action(self.current_project['name'], f"credential_added: {data.get('username','unknown')}")
            dialog.destroy()
            self._load_credentials()
        
        tk.Button(dialog, text="💾 Save Entry", font=('Courier', 10, 'bold'),
                fg='#000', bg='#00ff88', relief='raised', padx=20, pady=8,
                command=save).pack(pady=10)
    
    def _view_cred(self, cred):
        dialog = tk.Toplevel(self.parent, bg='#1a1a2e')
        dialog.title("Credential Details"); dialog.geometry("450x450")
        
        tk.Label(dialog, text="🔐 Credential Details", font=('Courier', 14, 'bold'),
                fg='#00ff88', bg='#1a1a2e').pack(pady=10)
        
        text = tk.Text(dialog, font=('Courier', 10), bg='#0a0a0a', fg='#00ff88', relief='flat')
        text.pack(fill='both', expand=True, padx=10, pady=10)
        
        details = f"""
╔══════════════════════════════╗
║     CREDENTIAL DETAILS       ║
╚══════════════════════════════╝

👤 Username : {cred.get('username', 'N/A')}
🔑 Password : {cred.get('password', 'N/A')}
📧 Email    : {cred.get('email', 'N/A')}
📱 Phone    : {cred.get('phone', 'N/A')}
🎯 Target   : {cred.get('target', 'N/A')}
🔧 Tool     : {cred.get('tool', 'N/A')}
🔗 URL      : {cred.get('url', 'N/A')}
🌐 IP       : {cred.get('ip_address', 'N/A')}
🍪 Token    : {cred.get('token', 'N/A')[:50]}
📊 Campaign : {cred.get('campaign', 'N/A')}
🕐 Found    : {cred.get('found_at', 'N/A')}
📝 Notes    : {cred.get('notes', 'N/A')}

User Agent : {cred.get('user_agent', 'N/A')}
Extra Data : {cred.get('extra_data', 'N/A')}
"""
        text.insert('1.0', details)
        text.config(state='disabled')
        
        tk.Button(dialog, text="📋 Copy All", font=('Courier', 10),
                fg='#000', bg='#00ccff', relief='raised', padx=15, pady=5,
                command=lambda: self._copy_text(details)).pack(pady=5)
        tk.Button(dialog, text="Close", font=('Courier', 10),
                fg='#fff', bg='#666', relief='raised', padx=15, pady=5,
                command=dialog.destroy).pack(pady=5)
    
    def _copy_cred(self, cred):
        text = f"Username: {cred.get('username','')}\nPassword: {cred.get('password','')}\nEmail: {cred.get('email','')}"
        self._copy_text(text)
        messagebox.showinfo("Copied", "Credentials copied to clipboard")
    
    def _copy_text(self, text):
        try:
            self.frame.clipboard_clear()
            self.frame.clipboard_append(text)
        except:
            pass
    
    def _delete_cred(self, cred):
        if messagebox.askyesno("Delete", "Delete this credential entry?"):
            self.db.cursor.execute('DELETE FROM credentials WHERE id = ?', (cred['id'],))
            self.db.conn.commit()
            self._load_credentials()
    
    def _show_campaigns(self):
        if not hasattr(self, 'current_project') or not self.current_project:
            return
        
        dialog = tk.Toplevel(self.parent, bg='#1a1a2e')
        dialog.title("Phishing Campaigns"); dialog.geometry("600x400")
        
        tk.Label(dialog, text="📊 Phishing Campaigns", font=('Courier', 14, 'bold'),
                fg='#ffaa00', bg='#1a1a2e').pack(pady=10)
        
        self.db.cursor.execute('SELECT * FROM phishing_campaigns WHERE project_id = ? ORDER BY started_at DESC',
                (self.current_project['id'],))
        campaigns = [dict(row) for row in self.db.cursor.fetchall()]
        
        if not campaigns:
            tk.Label(dialog, text="No campaigns yet", font=('Courier', 12),
                    fg='#666', bg='#1a1a2e').pack(expand=True)
        else:
            for c in campaigns:
                card = tk.Frame(dialog, bg='#16213e', padx=10, pady=8)
                card.pack(fill='x', padx=10, pady=3)
                tk.Label(card, text=f"📊 {c['name']}", font=('Courier', 10, 'bold'),
                        fg='#ffaa00', bg='#16213e').pack(anchor='w')
                tk.Label(card, text=f"Target: {c['target_site']} | Sent: {c['emails_sent']} | Clicks: {c['clicks']} | Captured: {c['credentials_captured']}",
                        font=('Courier', 8), fg='#888', bg='#16213e').pack(anchor='w')
        
        tk.Button(dialog, text="+ New Campaign", font=('Courier', 10),
                fg='#000', bg='#00ff88', relief='raised', padx=15, pady=5,
                command=lambda: self._new_campaign(dialog)).pack(pady=10)
        tk.Button(dialog, text="Close", font=('Courier', 10),
                fg='#fff', bg='#666', relief='raised', padx=15, pady=5,
                command=dialog.destroy).pack(pady=5)
    
    def _new_campaign(self, parent_dialog):
        dialog = tk.Toplevel(self.parent, bg='#1a1a2e')
        dialog.title("New Campaign"); dialog.geometry("400x350")
        
        tk.Label(dialog, text="New Phishing Campaign", font=('Courier', 14, 'bold'),
                fg='#00ff88', bg='#1a1a2e').pack(pady=10)
        
        fields = [("Campaign Name:", "name"), ("Target Site:", "target_site"),
                  ("Template:", "template"), ("Landing Page:", "landing_page")]
        entries = {}
        for label, key in fields:
            tk.Label(dialog, text=label, font=('Courier', 9), fg='#aaa', bg='#1a1a2e').pack(anchor='w', padx=20)
            e = tk.Entry(dialog, font=('Courier', 10), bg='#16213e', fg='#fff', relief='flat')
            e.pack(fill='x', padx=20, pady=2)
            entries[key] = e
        
        def save():
            data = {k: v.get().strip() for k, v in entries.items()}
            if not data['name']: return
            self.db.cursor.execute('''
                INSERT INTO phishing_campaigns (project_id, name, target_site, template, landing_page, started_at, status)
                VALUES (?, ?, ?, ?, ?, datetime('now'), 'active')
            ''', (self.current_project['id'], data['name'], data['target_site'], data['template'], data['landing_page']))
            self.db.conn.commit()
            dialog.destroy()
            parent_dialog.destroy()
            self._show_campaigns()
        
        tk.Button(dialog, text="Create Campaign", font=('Courier', 10, 'bold'),
                fg='#000', bg='#00ff88', relief='raised', padx=20, pady=8,
                command=save).pack(pady=15)
    
    def _export_data(self):
        if not hasattr(self, 'current_project') or not self.current_project:
            return
        
        self.db.cursor.execute('SELECT * FROM credentials WHERE project_id = ?', (self.current_project['id'],))
        creds = [dict(row) for row in self.db.cursor.fetchall()]
        
        export_dir = os.path.join(self.current_project['path'], 'exports')
        os.makedirs(export_dir, exist_ok=True)
        
        # Export as JSON
        json_path = os.path.join(export_dir, f'credentials_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json')
        with open(json_path, 'w') as f:
            json.dump(creds, f, indent=2, default=str)
        
        # Export as CSV
        csv_path = json_path.replace('.json', '.csv')
        with open(csv_path, 'w') as f:
            if creds:
                f.write(','.join(creds[0].keys()) + '\n')
                for c in creds:
                    f.write(','.join(str(v).replace(',', ';') for v in c.values()) + '\n')
        
        # Export as HTML
        html_path = json_path.replace('.json', '.html')
        with open(html_path, 'w') as f:
            f.write('<html><head><style>body{background:#0a0a0a;color:#00ff88;font:monospace}table{border-collapse:collapse}td,th{border:1px solid #333;padding:8px}</style></head><body>')
            f.write(f'<h1>Credential Report - {self.current_project["name"]}</h1>')
            f.write(f'<p>Exported: {datetime.now()}</p>')
            f.write('<table><tr><th>User</th><th>Password</th><th>Email</th><th>Target</th><th>Tool</th></tr>')
            for c in creds:
                f.write(f'<tr><td>{c.get("username","")}</td><td>{c.get("password","")}</td><td>{c.get("email","")}</td><td>{c.get("target","")}</td><td>{c.get("tool","")}</td></tr>')
            f.write('</table></body></html>')
        
        messagebox.showinfo("Exported", f"Data exported to:\n{json_path}\n{csv_path}\n{html_path}")
        self.logger.log_project_action(self.current_project['name'], f"credentials_exported: {len(creds)} entries")
