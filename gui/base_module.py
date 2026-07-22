"""
Base Module - Inherit this for all new modules.
Provides automatic scrollable content that stays in screen.
"""
import tkinter as tk

class BaseModule:
    """Base class for all CyberLab modules with built-in scroll"""
    
    def __init__(self, parent, bg='#1a1a2e'):
        self.parent = parent
        self.bg = bg
        
        # Outer frame (fills parent)
        self.frame = tk.Frame(parent, bg=bg)
        
        # Canvas with scroll
        self.canvas = tk.Canvas(self.frame, bg=bg, highlightthickness=0)
        self.v_scroll = tk.Scrollbar(self.frame, orient='vertical', command=self.canvas.yview)
        self.h_scroll = tk.Scrollbar(self.frame, orient='horizontal', command=self.canvas.xview)
        
        # Inner frame (where content goes)
        self.inner = tk.Frame(self.canvas, bg=bg)
        self.inner.bind('<Configure>', self._on_configure)
        self._win_id = self.canvas.create_window((0,0), window=self.inner, anchor='nw')
        
        self.canvas.configure(yscrollcommand=self.v_scroll.set, xscrollcommand=self.h_scroll.set)
        
        # Bind canvas resize
        self.canvas.bind('<Configure>', self._on_canvas_resize)
        
        # Mouse wheel
        self.canvas.bind('<MouseWheel>', self._on_mousewheel)
        self.canvas.bind('<Button-4>', self._on_mousewheel_up)
        self.canvas.bind('<Button-5>', self._on_mousewheel_down)
    
    def _on_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))
    
    def _on_canvas_resize(self, event):
        self.canvas.itemconfig(self._win_id, width=event.width)
    
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(-1 * (event.delta // 120), 'units')
    
    def _on_mousewheel_up(self, event):
        self.canvas.yview_scroll(-1, 'units')
    
    def _on_mousewheel_down(self, event):
        self.canvas.yview_scroll(1, 'units')
    
    def build(self):
        """Override this in subclasses"""
        self.frame.pack(fill='both', expand=True)
        self.canvas.pack(side='left', fill='both', expand=True)
        self.v_scroll.pack(side='right', fill='y')
        self.h_scroll.pack(side='bottom', fill='x')
        
        # Default content
        tk.Label(self.inner, text="Module Content", font=('Courier', 14),
                fg='#00ff88', bg=self.bg).pack(padx=20, pady=20)
    
    def clear(self):
        """Clear all content from inner frame"""
        for w in self.inner.winfo_children():
            w.destroy()
    
    def add_label(self, text, font=('Courier', 10), fg='#fff', **kwargs):
        """Add a wrapped label"""
        lbl = tk.Label(self.inner, text=text, font=font, fg=fg, bg=self.bg,
                      wraplength=self.canvas.winfo_width()-20, justify='left', **kwargs)
        lbl.pack(anchor='w', padx=10, pady=2)
        return lbl
    
    def add_button(self, text, command, color='#00ccff', **kwargs):
        """Add a button that fits"""
        btn = tk.Button(self.inner, text=text, font=('Courier', 9),
                       fg='#000', bg=color, relief='flat', command=command, **kwargs)
        btn.pack(padx=10, pady=2)
        return btn
    
    def add_card(self, title, details, color='#00ff88'):
        """Add a card with title and details"""
        card = tk.Frame(self.inner, bg='#16213e', padx=12, pady=8)
        card.pack(fill='x', padx=10, pady=3)
        tk.Label(card, text=title, font=('Courier', 10, 'bold'),
                fg=color, bg='#16213e', wraplength=self.canvas.winfo_width()-40).pack(anchor='w')
        if details:
            tk.Label(card, text=details, font=('Courier', 8),
                    fg='#888', bg='#16213e', wraplength=self.canvas.winfo_width()-40).pack(anchor='w')
        return card
