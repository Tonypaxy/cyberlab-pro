import tkinter as tk
from tkinter import ttk, messagebox
import os
from datetime import datetime

class ReportsModule:
    def __init__(self, parent, db, logger):
        self.parent = parent
        self.db = db
        self.logger = logger
        self.frame = tk.Frame(parent, bg='#1a1a2e')
        self.current_project = None
    
    def build(self):
        self.frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        header = tk.Frame(self.frame, bg='#1a1a2e')
        header.pack(fill='x', pady=(0,10))
        
        tk.Label(header, text="📋 Reports", font=('Courier', 18, 'bold'),
                fg='#00ff88', bg='#1a1a2e').pack(side='left')
        
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
            self.proj_menu.bind('<<ComboboxSelected>>', lambda e: self._load_reports())
            self._set_project(names[0])
        
        tk.Button(proj_frame, text="🔄 Refresh", font=('Courier', 9),
                fg='#000', bg='#00ccff', relief='flat', padx=10,
                command=self._load_reports).pack(side='right', padx=2)
        
        self.list_frame = tk.Frame(self.frame, bg='#1a1a2e')
        self.list_frame.pack(fill='both', expand=True)
        
        self._load_reports()
    
    def _set_project(self, name):
        projects = self.db.get_all_projects()
        for p in projects:
            if p['name'] == name:
                self.current_project = p
                break
    
    def _load_reports(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()
        
        if not self.current_project:
            tk.Label(self.list_frame, text="Select a project", font=('Courier', 12),
                    fg='#666', bg='#1a1a2e').pack(expand=True)
            return
        
        logs_dir = os.path.join(self.current_project['path'], 'logs')
        reports_dir = os.path.join(self.current_project['path'], 'reports')
        exports_dir = os.path.join(self.current_project['path'], 'exports')
        
        all_files = []
        for d in [logs_dir, reports_dir, exports_dir]:
            if os.path.exists(d):
                for f in os.listdir(d):
                    fp = os.path.join(d, f)
                    if os.path.isfile(fp):
                        all_files.append(fp)
        
        if not all_files:
            tk.Label(self.list_frame,
                    text="No reports yet.\nRun scans from Recon or Web tools.",
                    font=('Courier', 11), fg='#666', bg='#1a1a2e',
                    justify='center').pack(expand=True)
            # Export all button
            tk.Button(self.list_frame, text="📊 Generate Summary Report",
                    font=('Courier', 10), fg='#000', bg='#00ff88',
                    relief='flat', padx=15, pady=8,
                    command=self._export_summary).pack(pady=20)
            return
        
        canvas = tk.Canvas(self.list_frame, bg='#1a1a2e', highlightthickness=0)
        scrollbar = tk.Scrollbar(self.list_frame, orient='vertical', command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg='#1a1a2e')
        
        scroll_frame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.create_window((0,0), window=scroll_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Export all button
        btn_bar = tk.Frame(scroll_frame, bg='#1a1a2e')
        btn_bar.pack(fill='x', pady=5)
        tk.Button(btn_bar, text="📊 Export All as HTML", font=('Courier', 9),
                fg='#000', bg='#ffaa00', relief='flat', padx=10,
                command=self._export_all_html).pack(side='left', padx=2)
        tk.Button(btn_bar, text="📄 Export All as TXT", font=('Courier', 9),
                fg='#000', bg='#00ccff', relief='flat', padx=10,
                command=self._export_all_txt).pack(side='left', padx=2)
        
        for filepath in sorted(all_files, reverse=True):
            self._create_file_row(scroll_frame, filepath)
    
    def _create_file_row(self, parent, filepath):
        filename = os.path.basename(filepath)
        size = os.path.getsize(filepath)
        mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
        
        row = tk.Frame(parent, bg='#16213e', relief='flat', bd=0)
        row.pack(fill='x', pady=2, padx=5)
        
        info = tk.Frame(row, bg='#16213e')
        info.pack(side='left', fill='x', expand=True, padx=10, pady=8)
        
        icon = "📄" if filename.endswith('.txt') else "📊" if filename.endswith('.html') else "📎"
        tk.Label(info, text=f"{icon} {filename}", font=('Courier', 10, 'bold'),
                fg='#00ff88', bg='#16213e').pack(anchor='w')
        tk.Label(info, text=f"Size: {size:,}b | {mtime.strftime('%Y-%m-%d %H:%M')}",
                font=('Courier', 8), fg='#888', bg='#16213e').pack(anchor='w')
        
        actions = tk.Frame(row, bg='#16213e')
        actions.pack(side='right', padx=10)
        
        tk.Button(actions, text="View", font=('Courier', 8),
                fg='#000', bg='#00ccff', relief='flat', padx=8,
                command=lambda f=filepath: self._view_file(f)).pack(side='left', padx=2)
        
        tk.Button(actions, text="HTML", font=('Courier', 8),
                fg='#000', bg='#ffaa00', relief='flat', padx=8,
                command=lambda f=filepath: self._export_single_html(f)).pack(side='left', padx=2)
        
        tk.Button(actions, text="PDF", font=('Courier', 8),
                fg='#000', bg='#cc0000', relief='flat', padx=8,
                command=lambda f=filepath: self._export_single_pdf(f)).pack(side='left', padx=2)
    
    def _view_file(self, filepath):
        dialog = tk.Toplevel(self.parent, bg='#1a1a2e')
        dialog.title(os.path.basename(filepath))
        dialog.geometry("700x500")
        
        tk.Label(dialog, text=os.path.basename(filepath), font=('Courier', 12, 'bold'),
                fg='#00ff88', bg='#1a1a2e').pack(pady=10)
        
        text = tk.Text(dialog, font=('Courier', 9), bg='#0a0a0a', fg='#00ff88',
                relief='flat', wrap='word')
        text.pack(fill='both', expand=True, padx=10, pady=10)
        
        try:
            with open(filepath, 'r', errors='ignore') as f:
                text.insert('1.0', f.read())
        except:
            text.insert('1.0', f"[Cannot read: {filepath}]")
        
        text.config(state='disabled')
        tk.Button(dialog, text="Close", font=('Courier', 10),
                fg='#000', bg='#00ccff', relief='flat', padx=20, pady=5,
                command=dialog.destroy).pack(pady=10)
    
    def _export_single_html(self, filepath):
        try:
            with open(filepath, 'r', errors='ignore') as f:
                content = f.read()
        except:
            messagebox.showerror("Error", "Cannot read file")
            return
        
        html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<title>{os.path.basename(filepath)}</title>
<style>
body{{background:#0a0a0a;color:#00ff88;font-family:monospace;padding:20px;}}
pre{{background:#111;padding:15px;border-radius:5px;border:1px solid #00ff88;}}
h1{{color:#00ccff;}}.meta{{color:#666;font-size:12px;}}
</style></head><body>
<h1>🛡️ CyberLab Pro Report</h1>
<p class="meta">File: {os.path.basename(filepath)} | Date: {datetime.now()}</p>
<pre>{content}</pre>
</body></html>"""
        
        outpath = filepath.replace('.txt', '.html').replace('.log', '.html')
        with open(outpath, 'w') as f:
            f.write(html)
        
        self.logger.log_project_action(self.current_project['name'], f"exported_html: {os.path.basename(outpath)}")
        messagebox.showinfo("Exported", f"HTML saved:\n{outpath}")
        self._load_reports()
    
    def _export_single_pdf(self, filepath):
        """Export as PDF via HTML conversion"""
        html_path = filepath.replace('.txt', '.html').replace('.log', '.html')
        pdf_path = filepath.replace('.txt', '.pdf').replace('.log', '.pdf')
        
        # Generate HTML first
        try:
            with open(filepath, 'r', errors='ignore') as f:
                content = f.read()
        except:
            messagebox.showerror("Error", "Cannot read file")
            return
        
        html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<title>{os.path.basename(filepath)}</title>
<style>
body{{background:#fff;color:#000;font-family:monospace;padding:20px;}}
pre{{background:#f5f5f5;padding:15px;border:1px solid #ccc;}}
h1{{color:#333;}}
</style></head><body>
<h1>CyberLab Pro Report</h1>
<p>File: {os.path.basename(filepath)} | Date: {datetime.now()}</p>
<pre>{content}</pre>
</body></html>"""
        
        with open(html_path, 'w') as f:
            f.write(html)
        
        # Try wkhtmltopdf, then weasyprint, then fallback
        import subprocess
        converted = False
        
        for cmd in ['wkhtmltopdf', 'weasyprint']:
            try:
                subprocess.run([cmd, html_path, pdf_path], capture_output=True, timeout=30)
                if os.path.exists(pdf_path):
                    converted = True
                    break
            except:
                pass
        
        if converted:
            messagebox.showinfo("PDF Created", f"PDF saved:\n{pdf_path}")
        else:
            # Fallback: just rename HTML
            messagebox.showinfo("HTML Created", 
                    f"PDF converter not found.\nInstall wkhtmltopdf or weasyprint.\n\nHTML saved:\n{html_path}")
        
        self._load_reports()
    
    def _export_all_html(self):
        if not self.current_project:
            return
        
        logs_dir = os.path.join(self.current_project['path'], 'logs')
        reports_dir = os.path.join(self.current_project['path'], 'reports')
        
        all_content = ""
        for d in [logs_dir, reports_dir]:
            if os.path.exists(d):
                for f in sorted(os.listdir(d)):
                    fp = os.path.join(d, f)
                    if os.path.isfile(fp):
                        try:
                            with open(fp, 'r', errors='ignore') as fh:
                                content = fh.read()
                            all_content += f"<h2>{f}</h2><pre>{content[:5000]}</pre><hr>\n"
                        except:
                            pass
        
        html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<title>CyberLab Report - {self.current_project['name']}</title>
<style>
body{{background:#0a0a0a;color:#00ff88;font-family:monospace;padding:20px;}}
h1{{color:#00ccff;border-bottom:2px solid #00ff88;}}
h2{{color:#ffaa00;margin-top:30px;}}
pre{{background:#111;padding:15px;border-radius:5px;border:1px solid #333;white-space:pre-wrap;}}
hr{{border-color:#333;}}
.meta{{color:#666;font-size:12px;}}
</style></head><body>
<h1>🛡️ CyberLab Pro - Full Report</h1>
<p class="meta">Project: {self.current_project['name']} | Date: {datetime.now()}</p>
{all_content}
</body></html>"""
        
        outpath = os.path.join(self.current_project['path'], 'exports', f'full_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.html')
        os.makedirs(os.path.dirname(outpath), exist_ok=True)
        with open(outpath, 'w') as f:
            f.write(html)
        
        messagebox.showinfo("Exported", f"Full HTML report saved:\n{outpath}")
        self._load_reports()
    
    def _export_all_txt(self):
        if not self.current_project:
            return
        
        logs_dir = os.path.join(self.current_project['path'], 'logs')
        reports_dir = os.path.join(self.current_project['path'], 'reports')
        
        all_content = f"CyberLab Pro Report\n{'='*50}\n"
        all_content += f"Project: {self.current_project['name']}\n"
        all_content += f"Date: {datetime.now()}\n{'='*50}\n\n"
        
        for d in [logs_dir, reports_dir]:
            if os.path.exists(d):
                for f in sorted(os.listdir(d)):
                    fp = os.path.join(d, f)
                    if os.path.isfile(fp):
                        all_content += f"\n--- {f} ---\n"
                        try:
                            with open(fp, 'r', errors='ignore') as fh:
                                all_content += fh.read()[:10000]
                        except:
                            all_content += "[Error reading]\n"
        
        outpath = os.path.join(self.current_project['path'], 'exports', f'full_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt')
        os.makedirs(os.path.dirname(outpath), exist_ok=True)
        with open(outpath, 'w') as f:
            f.write(all_content)
        
        messagebox.showinfo("Exported", f"Full TXT report saved:\n{outpath}")
        self._load_reports()
    
    def _export_summary(self):
        """Generate summary report for project without scan data"""
        if not self.current_project:
            return
        
        html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<title>CyberLab Summary - {self.current_project['name']}</title>
<style>
body{{background:#0a0a0a;color:#00ff88;font-family:monospace;padding:40px;}}
h1{{color:#00ccff;border-bottom:2px solid #00ff88;padding-bottom:10px;}}
.card{{background:#111;border:1px solid #333;padding:20px;margin:10px 0;border-radius:5px;}}
.label{{color:#666;}}.value{{color:#00ff88;font-size:24px;}}
.footer{{margin-top:40px;color:#444;font-size:11px;text-align:center;}}
</style></head><body>
<h1>🛡️ CyberLab Pro - Project Summary</h1>
<div class="card">
<p class="label">Project Name</p><p class="value">{self.current_project['name']}</p>
<p class="label">Created</p><p>{self.current_project.get('created_at', 'N/A')}</p>
<p class="label">Description</p><p>{self.current_project.get('description', 'No description')}</p>
</div>
<p class="footer">Generated by CyberLab Pro v1.0 | {datetime.now()}</p>
</body></html>"""
        
        outpath = os.path.join(self.current_project['path'], 'exports', f'summary_{datetime.now().strftime("%Y%m%d_%H%M%S")}.html')
        os.makedirs(os.path.dirname(outpath), exist_ok=True)
        with open(outpath, 'w') as f:
            f.write(html)
        
        messagebox.showinfo("Exported", f"Summary report saved:\n{outpath}")
        self._load_reports()
