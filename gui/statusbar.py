import tkinter as tk

class StatusBar:
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg='#0f3460', height=25)
        self.status_text = tk.StringVar(value="Ready")
        self.tool_text = tk.StringVar(value="")
        
    def build(self):
        # Pack handled by launcher grid
        self.frame.grid_propagate(False)
        
        tk.Label(self.frame, textvariable=self.status_text, font=('Courier', 9),
                fg='#00ff88', bg='#0f3460').pack(side='left', padx=10)
        tk.Label(self.frame, textvariable=self.tool_text, font=('Courier', 9),
                fg='#aaa', bg='#0f3460').pack(side='right', padx=10)
    
    def set_status(self, text):
        self.status_text.set(text)
    
    def set_tool_info(self, text):
        self.tool_text.set(text)
