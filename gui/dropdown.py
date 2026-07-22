"""
CyberLab Pro - Dropdown Component
Use this in ANY module to create collapsible sections.
Just like Tool Center's category expand/collapse.
"""
import tkinter as tk

class Dropdown:
    """A collapsible dropdown section usable in any module.
    
    Usage:
        dropdown = Dropdown(parent, "Title", icon="📦")
        dropdown.add_item("Item 1", callback)
        dropdown.add_item("Item 2", callback)
        # Or add custom widgets:
        dropdown.add_widget(my_button)
    """
    
    def __init__(self, parent, title, icon='', bg='#16213e', fg='#00ccff', default_open=False):
        self.parent = parent
        self.title = title
        self.icon = icon
        self.bg = bg
        self.fg = fg
        self.is_open = default_open
        self.items = []
        self.widgets = []
        
        # Container
        self.container = tk.Frame(parent, bg=parent.cget('bg') if hasattr(parent, 'cget') else '#1a1a2e')
        self.container.pack(fill='x', padx=5, pady=1)
        
        # Header button
        self.header = tk.Button(self.container, text=self._get_text(),
                font=('Courier', 10, 'bold'), fg=fg, bg=bg,
                relief='flat', anchor='w', padx=10, pady=6,
                command=self.toggle)
        self.header.pack(fill='x')
        
        # Content frame
        self.content = tk.Frame(self.container, bg=parent.cget('bg') if hasattr(parent, 'cget') else '#1a1a2e')
        if self.is_open:
            self.content.pack(fill='x', padx=15, pady=(0,5))
            self._render_content()
    
    def _get_text(self):
        arrow = '▼' if self.is_open else '▶'
        return f"{arrow} {self.icon} {self.title}"
    
    def toggle(self):
        self.is_open = not self.is_open
        self.header.config(text=self._get_text())
        if self.is_open:
            self.content.pack(fill='x', padx=15, pady=(0,5))
            self._render_content()
        else:
            for w in self.content.winfo_children():
                w.destroy()
            self.content.pack_forget()
    
    def _render_content(self):
        for w in self.content.winfo_children():
            w.destroy()
        for widget in self.widgets:
            widget.pack(fill='x', pady=1)
    
    def add_item(self, text, callback=None, fg='#fff', icon=''):
        """Add a clickable item"""
        btn = tk.Button(self.content, text=f"{icon} {text}", font=('Courier', 9),
                fg=fg, bg='#16213e', relief='flat', anchor='w', padx=10, pady=3,
                command=callback)
        self.widgets.append(btn)
        if self.is_open:
            btn.pack(fill='x', pady=1)
        return btn
    
    def add_widget(self, widget):
        """Add any tkinter widget"""
        self.widgets.append(widget)
        if self.is_open:
            widget.pack(fill='x', pady=1)
        return widget
    
    def add_row(self, left_text, right_widget=None):
        """Add a row with text on left, widget on right"""
        row = tk.Frame(self.content, bg='#16213e')
        tk.Label(row, text=left_text, font=('Courier', 9), fg='#aaa', bg='#16213e').pack(side='left', padx=5, pady=3)
        if right_widget:
            right_widget.pack(side='right', padx=5)
        self.widgets.append(row)
        if self.is_open:
            row.pack(fill='x', pady=1)
        return row


class DropdownGroup:
    """A group of dropdowns - only one open at a time (accordion)"""
    
    def __init__(self, parent):
        self.parent = parent
        self.dropdowns = []
    
    def add(self, title, icon='', bg='#16213e', fg='#00ccff'):
        """Add a dropdown to the group"""
        dd = Dropdown(self.parent, title, icon, bg, fg)
        # Make it accordion-style
        orig_toggle = dd.toggle
        def new_toggle():
            for d in self.dropdowns:
                if d != dd and d.is_open:
                    d.toggle()
            orig_toggle()
        dd.toggle = new_toggle
        self.dropdowns.append(dd)
        return dd
