"""CyberLab Pro - Shared Scrollable Frame with Horizontal & Vertical Scroll"""
import tkinter as tk

class ScrollableFrame:
    """A frame with both horizontal and vertical scrollbars"""
    
    def __init__(self, parent, bg='#1a1a2e', width=None, height=None):
        self.parent = parent
        self.bg = bg
        
        # Container frame
        self.container = tk.Frame(parent, bg=bg, width=width, height=height)
        
        # Horizontal scrollbar
        self.h_scroll = tk.Scrollbar(self.container, orient='horizontal')
        self.h_scroll.pack(side='bottom', fill='x')
        
        # Vertical scrollbar
        self.v_scroll = tk.Scrollbar(self.container, orient='vertical')
        self.v_scroll.pack(side='right', fill='y')
        
        # Canvas
        self.canvas = tk.Canvas(self.container, bg=bg, highlightthickness=0,
                xscrollcommand=self.h_scroll.set, yscrollcommand=self.v_scroll.set)
        self.canvas.pack(side='left', fill='both', expand=True)
        
        self.h_scroll.config(command=self.canvas.xview)
        self.v_scroll.config(command=self.canvas.yview)
        
        # Inner frame
        self.inner = tk.Frame(self.canvas, bg=bg)
        self.inner.bind('<Configure>', self._on_configure)
        self.canvas.create_window((0, 0), window=self.inner, anchor='nw')
        
        # Bind mouse wheel
        self.canvas.bind('<MouseWheel>', self._on_mousewheel)
        self.canvas.bind('<Button-4>', self._on_mousewheel)
        self.canvas.bind('<Button-5>', self._on_mousewheel)
        self.canvas.bind('<Shift-MouseWheel>', self._on_shift_mousewheel)
    
    def _on_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))
    
    def _on_mousewheel(self, event):
        if event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-1, 'units')
        elif event.num == 5 or event.delta < 0:
            self.canvas.yview_scroll(1, 'units')
    
    def _on_shift_mousewheel(self, event):
        if event.delta > 0:
            self.canvas.xview_scroll(-1, 'units')
        else:
            self.canvas.xview_scroll(1, 'units')
    
    def pack(self, **kwargs):
        self.container.pack(**kwargs)
    
    def pack_forget(self):
        self.container.pack_forget()
    
    def destroy(self):
        self.container.destroy()
    
    def winfo_children(self):
        return self.inner.winfo_children()
    
    def update(self):
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))
