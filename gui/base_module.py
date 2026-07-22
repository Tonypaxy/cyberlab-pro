"""
CyberLab Pro - Universal Base Module
EVERY module must inherit this. Provides:
- Horizontal + Vertical scroll
- Collapsible sections
- Consistent styling
- Responsive layout that fits any screen
"""
import tkinter as tk

class BaseModule:
    """Base class for ALL CyberLab modules.
    
    Usage:
        class MyModule(BaseModule):
            def build_content(self):
                self.add_section("Section 1", [
                    self.create_card("Title", "Details"),
                ])
    """
    
    def __init__(self, parent, bg='#1a1a2e'):
        self.parent = parent
        self.bg = bg
        self.frame = tk.Frame(parent, bg=bg)
        self.sections = {}
    
    def build(self):
        """Build the module - DO NOT OVERRIDE. Override build_content() instead."""
        self.frame.pack(fill='both', expand=True)
        
        # Canvas with dual scroll
        self.canvas = tk.Canvas(self.frame, bg=self.bg, highlightthickness=0)
        self.v_bar = tk.Scrollbar(self.frame, orient='vertical', command=self.canvas.yview)
        self.h_bar = tk.Scrollbar(self.frame, orient='horizontal', command=self.canvas.xview)
        
        self.inner = tk.Frame(self.canvas, bg=self.bg)
        self.inner.bind('<Configure>', self._on_configure)
        self._win_id = self.canvas.create_window((0,0), window=self.inner, anchor='nw')
        
        self.canvas.bind('<Configure>', self._on_resize)
        self.canvas.configure(yscrollcommand=self.v_bar.set, xscrollcommand=self.h_bar.set)
        
        self.canvas.pack(side='left', fill='both', expand=True)
        self.v_bar.pack(side='right', fill='y')
        self.h_bar.pack(side='bottom', fill='x')
        
        # Mouse scroll
        self.canvas.bind('<MouseWheel>', lambda e: self.canvas.yview_scroll(-e.delta//120, 'units'))
        self.canvas.bind('<Button-4>', lambda e: self.canvas.yview_scroll(-1, 'units'))
        self.canvas.bind('<Button-5>', lambda e: self.canvas.yview_scroll(1, 'units'))
        
        # Build content
        self.build_content()
    
    def _on_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))
    
    def _on_resize(self, event):
        self.canvas.itemconfig(self._win_id, width=event.width)
    
    def build_content(self):
        """Override this - add your content here"""
        self.add_title("Module Title")
    
    # === BUILDING BLOCKS ===
    
    def add_title(self, text, subtitle=None):
        """Add module title"""
        f = tk.Frame(self.inner, bg=self.bg)
        f.pack(fill='x', padx=10, pady=(10,5))
        tk.Label(f, text=text, font=('Courier', 18, 'bold'), fg='#00ff88', bg=self.bg).pack(anchor='w')
        if subtitle:
            tk.Label(f, text=subtitle, font=('Courier', 9), fg='#888', bg=self.bg).pack(anchor='w')
    
    def add_section(self, title, content_func, icon='', default_open=False):
        """Add a collapsible section.
        
        Args:
            title: Section title
            content_func: Function that takes (parent_frame) and adds widgets
            icon: Emoji icon
            default_open: Start expanded?
        """
        section_id = title.lower().replace(' ', '_')
        is_open = self.sections.get(section_id, default_open)
        
        # Header
        header = tk.Frame(self.inner, bg='#16213e', cursor='hand2')
        header.pack(fill='x', padx=10, pady=2)
        
        arrow = '▼' if is_open else '▶'
        btn = tk.Button(header, text=f"{arrow} {icon} {title}",
                font=('Courier', 10, 'bold'), fg='#00ccff', bg='#16213e',
                relief='flat', anchor='w', padx=10, pady=6,
                command=lambda: self._toggle_section(section_id, content_func, icon))
        btn.pack(fill='x')
        
        # Content
        content_frame = tk.Frame(self.inner, bg=self.bg)
        if is_open:
            content_frame.pack(fill='x', padx=20, pady=(0,5))
            content_func(content_frame)
        
        self.sections[section_id] = {'open': is_open, 'frame': content_frame}
    
    def _toggle_section(self, section_id, content_func, icon):
        """Toggle section open/close"""
        if section_id in self.sections:
            self.sections[section_id]['open'] = not self.sections[section_id]['open']
        # Rebuild
        for w in self.inner.winfo_children():
            w.destroy()
        self.sections = {}
        self.build_content()
    
    def create_card(self, title, details='', color='#00ff88'):
        """Create a card widget"""
        card = tk.Frame(self.inner, bg='#16213e', padx=12, pady=8)
        card.pack(fill='x', padx=10, pady=2)
        if title:
            tk.Label(card, text=title, font=('Courier', 10, 'bold'),
                    fg=color, bg='#16213e', wraplength=self.canvas.winfo_width()-60).pack(anchor='w')
        if details:
            tk.Label(card, text=details, font=('Courier', 8),
                    fg='#888', bg='#16213e', wraplength=self.canvas.winfo_width()-60).pack(anchor='w')
        return card
    
    def create_row(self, items, bg='#16213e'):
        """Create a horizontal row of items"""
        row = tk.Frame(self.inner, bg=bg)
        row.pack(fill='x', padx=10, pady=1)
        for item in items:
            if isinstance(item, str):
                tk.Label(row, text=item, font=('Courier', 9),
                        fg='#fff', bg=bg, wraplength=self.canvas.winfo_width()-40).pack(side='left', padx=5)
            else:
                item.pack(side='left', padx=2)
        return row
    
    def create_grid(self, items, cols=3):
        """Create a grid of items"""
        grid = tk.Frame(self.inner, bg=self.bg)
        grid.pack(fill='x', padx=10, pady=5)
        for i, item in enumerate(items):
            row = i // cols
            col = i % cols
            if isinstance(item, str):
                tk.Label(grid, text=item, font=('Courier', 9), fg='#fff', bg=self.bg).grid(row=row, column=col, padx=5, pady=2, sticky='w')
            else:
                item.grid(row=row, column=col, padx=5, pady=2, sticky='ew')
        return grid
    
    def add_button(self, text, command, color='#00ccff', side='left'):
        """Add a button"""
        btn = tk.Button(self.inner, text=text, font=('Courier', 9),
                fg='#000', bg=color, relief='raised', padx=10, pady=5, command=command)
        btn.pack(side=side, padx=3, pady=3)
        return btn
    
    def add_entry(self, label, default='', password=False):
        """Add a labeled entry field"""
        f = tk.Frame(self.inner, bg=self.bg)
        f.pack(fill='x', padx=10, pady=3)
        tk.Label(f, text=label, font=('Courier', 9), fg='#888', bg=self.bg).pack(anchor='w')
        show = '*' if password else ''
        e = tk.Entry(f, font=('Courier', 10), bg='#0f3460', fg='#fff', show=show, relief='flat')
        e.pack(fill='x', pady=2)
        if default:
            e.insert(0, default)
        return e
    
    def add_text(self, height=10):
        """Add a text area"""
        t = tk.Text(self.inner, font=('Courier', 9), bg='#0a0a0a', fg='#00ff88',
                relief='flat', wrap='word', height=height)
        t.pack(fill='both', expand=True, padx=10, pady=5)
        return t
    
    def add_status(self, text):
        """Add status bar"""
        s = tk.Label(self.inner, text=text, font=('Courier', 8), fg='#666', bg=self.bg)
        s.pack(fill='x', padx=10, pady=3)
        return s
