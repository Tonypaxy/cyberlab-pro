import tkinter as tk

class NotificationManager:
    def __init__(self, parent):
        self.parent = parent
        self.notifications = []
        self.max_visible = 4
    
    def show(self, message, type="info", duration=3000):
        """Show a toast notification"""
        notif = Notification(self.parent, message, type, duration, self._on_dismiss)
        self.notifications.append(notif)
        
        # Limit visible notifications
        if len(self.notifications) > self.max_visible:
            old = self.notifications.pop(0)
            old.dismiss()
        
        notif.show()
    
    def _on_dismiss(self, notification):
        if notification in self.notifications:
            self.notifications.remove(notification)


class Notification:
    def __init__(self, parent, message, type, duration, on_dismiss):
        self.parent = parent
        self.message = message
        self.type = type
        self.duration = duration
        self.on_dismiss = on_dismiss
        self.window = None
        self.after_id = None
        
        self.colors = {
            "info": {"bg": "#0f3460", "fg": "#00ccff", "icon": "ℹ️"},
            "success": {"bg": "#0a3a0a", "fg": "#00ff88", "icon": "✅"},
            "warning": {"bg": "#3a3a00", "fg": "#ffaa00", "icon": "⚠️"},
            "error": {"bg": "#3a0000", "fg": "#ff4444", "icon": "❌"},
            "tool": {"bg": "#1a1a3a", "fg": "#cc88ff", "icon": "🔧"},
        }
    
    def show(self):
        self.window = tk.Toplevel(self.parent)
        self.window.overrideredirect(True)
        self.window.attributes('-topmost', True)
        
        colors = self.colors.get(self.type, self.colors["info"])
        
        # Calculate position (top-right stack)
        x = self.parent.winfo_rootx() + self.parent.winfo_width() - 320
        y = self.parent.winfo_rooty() + 60 + (len(self.parent.children) * 55)
        
        self.window.geometry(f"300x45+{x}+{y}")
        self.window.configure(bg=colors["bg"])
        
        # Border
        border = tk.Frame(self.window, bg=colors["fg"], padx=1, pady=1)
        border.pack(fill='both', expand=True)
        
        inner = tk.Frame(border, bg=colors["bg"])
        inner.pack(fill='both', expand=True)
        
        # Icon + message
        tk.Label(inner, text=colors["icon"], font=('Courier', 14),
                bg=colors["bg"]).pack(side='left', padx=(10,5))
        tk.Label(inner, text=self.message[:45], font=('Courier', 9),
                fg=colors["fg"], bg=colors["bg"], anchor='w').pack(side='left', padx=5)
        
        # Close button
        close_btn = tk.Label(inner, text="✕", font=('Courier', 10),
                fg=colors["fg"], bg=colors["bg"], cursor='hand2')
        close_btn.pack(side='right', padx=8)
        close_btn.bind('<Button-1>', lambda e: self.dismiss())
        
        # Auto dismiss
        self.after_id = self.window.after(self.duration, self.dismiss)
        
        # Click to dismiss
        inner.bind('<Button-1>', lambda e: self.dismiss())
    
    def dismiss(self):
        if self.after_id:
            self.window.after_cancel(self.after_id)
        if self.window:
            self.window.destroy()
            self.window = None
        self.on_dismiss(self)
