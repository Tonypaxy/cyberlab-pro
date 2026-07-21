"""Hello World Plugin for CyberLab Pro"""
import tkinter as tk

def run(parent, db, logger, config):
    """Main plugin entry point"""
    frame = tk.Frame(parent, bg='#1a1a2e')
    frame.pack(fill='both', expand=True, padx=20, pady=20)
    
    tk.Label(frame, text="🔌 Hello World Plugin", font=('Courier', 18, 'bold'),
            fg='#00ff88', bg='#1a1a2e').pack(pady=10)
    
    tk.Label(frame, text="This is a sample plugin for CyberLab Pro.\n\n"
            "Plugins can:\n"
            "• Add custom tools\n"
            "• Integrate external scripts\n"
            "• Create new workspaces\n"
            "• Access the database and logger\n"
            "• Build full GUI interfaces",
            font=('Courier', 10), fg='#aaa', bg='#1a1a2e',
            justify='left').pack(pady=10)
    
    # Example button that uses the database
    def show_projects():
        projects = db.get_all_projects()
        count = len(projects)
        from tkinter import messagebox
        messagebox.showinfo("Projects", f"Total projects: {count}")
    
    tk.Button(frame, text="Show Project Count", font=('Courier', 10),
            fg='#000', bg='#00ccff', relief='flat', padx=15, pady=8,
            command=show_projects).pack(pady=10)
    
    return frame
