"""
Universal Scrollable Module - Use this for ALL modules.
Just wrap your build code inside make_scrollable().
"""
import tkinter as tk

class ScrolledModule:
    """Makes any module scrollable both ways with 2 lines of code.
    
    Usage:
        class MyModule(ScrolledModule):
            def build_content(self, inner):
                # Add your widgets to 'inner' frame
                tk.Label(inner, text="Content").pack()
    """
    def __init__(self, parent, bg='#1a1a2e'):
        self.parent = parent
        self.bg = bg
        self.frame = tk.Frame(parent, bg=bg)
    
    def build(self):
        self.frame.pack(fill='both', expand=True)
        
        # Canvas
        canvas = tk.Canvas(self.frame, bg=self.bg, highlightthickness=0)
        v_bar = tk.Scrollbar(self.frame, orient='vertical', command=canvas.yview)
        h_bar = tk.Scrollbar(self.frame, orient='horizontal', command=canvas.xview)
        
        # Inner content frame
        inner = tk.Frame(canvas, bg=self.bg)
        inner.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        win = canvas.create_window((0,0), window=inner, anchor='nw')
        
        # Resize inner to match canvas width
        def _resize(event):
            canvas.itemconfig(win, width=event.width)
        canvas.bind('<Configure>', _resize)
        
        canvas.configure(yscrollcommand=v_bar.set, xscrollcommand=h_bar.set)
        
        # Layout
        canvas.pack(side='left', fill='both', expand=True)
        v_bar.pack(side='right', fill='y')
        h_bar.pack(side='bottom', fill='x')
        
        # Mouse scroll
        canvas.bind('<MouseWheel>', lambda e: canvas.yview_scroll(-e.delta//120, 'units'))
        canvas.bind('<Button-4>', lambda e: canvas.yview_scroll(-1, 'units'))
        canvas.bind('<Button-5>', lambda e: canvas.yview_scroll(1, 'units'))
        
        # Build content in inner frame
        self.build_content(inner)
    
    def build_content(self, inner):
        """Override this - add widgets to 'inner'"""
        tk.Label(inner, text="Module", font=('Courier', 14), fg='#00ff88', bg=self.bg).pack(pady=20)


def make_scrollable(frame, bg='#1a1a2e'):
    """Quick wrapper: returns (canvas, inner, v_bar, h_bar)"""
    canvas = tk.Canvas(frame, bg=bg, highlightthickness=0)
    v_bar = tk.Scrollbar(frame, orient='vertical', command=canvas.yview)
    h_bar = tk.Scrollbar(frame, orient='horizontal', command=canvas.xview)
    
    inner = tk.Frame(canvas, bg=bg)
    inner.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
    win = canvas.create_window((0,0), window=inner, anchor='nw')
    
    canvas.bind('<Configure>', lambda e: canvas.itemconfig(win, width=e.width))
    canvas.configure(yscrollcommand=v_bar.set, xscrollcommand=h_bar.set)
    
    canvas.pack(side='left', fill='both', expand=True)
    v_bar.pack(side='right', fill='y')
    h_bar.pack(side='bottom', fill='x')
    
    canvas.bind('<MouseWheel>', lambda e: canvas.yview_scroll(-e.delta//120, 'units'))
    canvas.bind('<Button-4>', lambda e: canvas.yview_scroll(-1, 'units'))
    canvas.bind('<Button-5>', lambda e: canvas.yview_scroll(1, 'units'))
    
    return canvas, inner, v_bar, h_bar
