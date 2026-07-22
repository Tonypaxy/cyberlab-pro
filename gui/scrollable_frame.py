"""
Shared ScrollableFrame - Used by ALL modules for consistent scrolling.
Import and use create_scrollable() in any module that needs scrolling.

Usage:
    from gui.scrollable_frame import create_scrollable
    
    # In your build method:
    scroll_frame, canvas = create_scrollable(self.frame, '#1a1a2e')
    
    # Add your widgets to scroll_frame (not self.frame)
    for item in items:
        tk.Label(scroll_frame, text=item).pack()
    
    # That's it - horizontal + vertical scroll + mouse wheel all work
"""
import tkinter as tk

def create_scrollable(parent, bg='#1a1a2e', height=None, width=None):
    """Create a fully scrollable frame with both scrollbars and mouse wheel support.
    
    Args:
        parent: Parent tkinter widget
        bg: Background color
        height: Optional fixed height
        width: Optional fixed width
    
    Returns:
        (inner_frame, canvas): Tuple of inner frame (add widgets here) and canvas
    """
    # Container
    container = tk.Frame(parent, bg=bg, height=height, width=width)
    container.pack(fill='both', expand=True)
    container.grid_rowconfigure(0, weight=1)
    container.grid_columnconfigure(0, weight=1)
    
    # Canvas
    canvas = tk.Canvas(container, bg=bg, highlightthickness=0)
    
    # Scrollbars
    v_scroll = tk.Scrollbar(container, orient='vertical', command=canvas.yview)
    h_scroll = tk.Scrollbar(container, orient='horizontal', command=canvas.xview)
    
    # Inner frame where all content goes
    inner = tk.Frame(canvas, bg=bg)
    
    # Configure scrolling
    def _configure(event):
        canvas.configure(scrollregion=canvas.bbox('all'))
    inner.bind('<Configure>', _configure)
    
    # Create window
    window_id = canvas.create_window((0, 0), window=inner, anchor='nw')
    
    # Set canvas width to match inner frame
    def _set_width(event):
        canvas.itemconfig(window_id, width=event.width)
    canvas.bind('<Configure>', _set_width)
    
    # Connect scrollbars
    canvas.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
    
    # Grid layout
    canvas.grid(row=0, column=0, sticky='nsew')
    v_scroll.grid(row=0, column=1, sticky='ns')
    h_scroll.grid(row=1, column=0, sticky='ew')
    
    # Mouse wheel scrolling (cross-platform)
    def _on_mousewheel(event):
        if event.delta:
            canvas.yview_scroll(-1 * (event.delta // 120), 'units')
        elif event.num == 4:
            canvas.yview_scroll(-1, 'units')
        elif event.num == 5:
            canvas.yview_scroll(1, 'units')
    
    def _on_shift_mousewheel(event):
        if event.delta:
            canvas.xview_scroll(-1 * (event.delta // 120), 'units')
    
    canvas.bind('<MouseWheel>', _on_mousewheel)
    canvas.bind('<Button-4>', _on_mousewheel)
    canvas.bind('<Button-5>', _on_mousewheel)
    canvas.bind('<Shift-MouseWheel>', _on_shift_mousewheel)
    
    # Bind all mouse events to canvas for proper scroll focus
    canvas.bind('<Enter>', lambda e: canvas.focus_set())
    
    return inner, canvas


def create_scrollable_text(parent, bg='#1a1a2e', fg='#00ff88', font=('Courier', 10), height=None):
    """Create a scrollable Text widget with both scrollbars.
    
    Returns:
        (text_widget, container_frame): Tuple of Text widget and container
    """
    container = tk.Frame(parent, bg=bg, height=height)
    container.pack(fill='both', expand=True)
    container.grid_rowconfigure(0, weight=1)
    container.grid_columnconfigure(0, weight=1)
    
    # Text widget
    text = tk.Text(container, font=font, bg='#0a0a0a', fg=fg, 
                   insertbackground=fg, relief='flat', wrap='word')
    
    # Scrollbars
    v_scroll = tk.Scrollbar(container, orient='vertical', command=text.yview)
    h_scroll = tk.Scrollbar(container, orient='horizontal', command=text.xview)
    
    text.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
    
    text.grid(row=0, column=0, sticky='nsew')
    v_scroll.grid(row=0, column=1, sticky='ns')
    h_scroll.grid(row=1, column=0, sticky='ew')
    
    return text, container


def create_scrollable_listbox(parent, bg='#1a1a2e', fg='#fff', font=('Courier', 10)):
    """Create a scrollable Listbox with both scrollbars.
    
    Returns:
        (listbox, container_frame): Tuple of Listbox and container
    """
    container = tk.Frame(parent, bg=bg)
    container.pack(fill='both', expand=True)
    container.grid_rowconfigure(0, weight=1)
    container.grid_columnconfigure(0, weight=1)
    
    listbox = tk.Listbox(container, font=font, bg='#0f3460', fg=fg,
                         selectbackground='#00ff88', selectforeground='#000',
                         relief='flat', borderwidth=0)
    
    v_scroll = tk.Scrollbar(container, orient='vertical', command=listbox.yview)
    h_scroll = tk.Scrollbar(container, orient='horizontal', command=listbox.xview)
    
    listbox.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
    
    listbox.grid(row=0, column=0, sticky='nsew')
    v_scroll.grid(row=0, column=1, sticky='ns')
    h_scroll.grid(row=1, column=0, sticky='ew')
    
    return listbox, container
