from gui.scrollable_frame import create_scrollable
"""Wordlist Generator Module"""
import tkinter as tk
from tkinter import ttk, messagebox
import os
import itertools
import string

class WordlistGenerator:
    def __init__(self, parent, db, logger):
        self.parent = parent
        self.db = db
        self.logger = logger
        self.frame = tk.Frame(parent, bg='#1a1a2e')
    
    def build(self):
        self.frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        tk.Label(self.frame, text="📝 Wordlist Generator", font=('Courier', 18, 'bold'),
                fg='#00ff88', bg='#1a1a2e').pack(anchor='w', pady=(0,20))
        
        # Options
        opts = tk.LabelFrame(self.frame, text=" Generation Options ", font=('Courier', 10, 'bold'),
                fg='#00ccff', bg='#16213e', padx=15, pady=15)
        opts.pack(fill='x', pady=10)
        
        tk.Label(opts, text="Charset:", font=('Courier', 10), fg='#fff', bg='#16213e').pack(anchor='w')
        self.charset_var = tk.StringVar(value="lowercase")
        charsets = [
            ("Lowercase (a-z)", "lowercase"),
            ("Uppercase (A-Z)", "uppercase"),
            ("Digits (0-9)", "digits"),
            ("Lower+Digits", "lowerdigits"),
            ("All printable", "printable"),
            ("Custom", "custom")
        ]
        for text, val in charsets:
            tk.Radiobutton(opts, text=text, variable=self.charset_var, value=val,
                    font=('Courier', 9), fg='#aaa', bg='#16213e', selectcolor='#00ff88',
                    command=lambda: self._toggle_custom()).pack(anchor='w', pady=2)
        
        self.custom_entry = tk.Entry(opts, font=('Courier', 10), bg='#0f3460', fg='#fff', relief='flat')
        self.custom_entry.pack(fill='x', pady=5)
        self.custom_entry.insert(0, 'abc123!@#')
        self.custom_entry.config(state='disabled')
        
        tk.Label(opts, text="Min Length:", font=('Courier', 10), fg='#fff', bg='#16213e').pack(anchor='w', pady=(10,0))
        self.min_var = tk.IntVar(value=1)
        tk.Scale(opts, from_=1, to=15, variable=self.min_var, orient='horizontal',
                bg='#16213e', fg='#00ff88', troughcolor='#0f3460').pack(fill='x')
        
        tk.Label(opts, text="Max Length (15):", font=('Courier', 10), fg='#fff', bg='#16213e').pack(anchor='w')
        self.max_var = tk.IntVar(value=4)
        tk.Scale(opts, from_=1, to=15, variable=self.max_var, orient='horizontal',
                bg='#16213e', fg='#00ff88', troughcolor='#0f3460').pack(fill='x')
        
        # Generate button
        btn_frame = tk.Frame(self.frame, bg='#1a1a2e')
        btn_frame.pack(fill='x', pady=10)
        
        tk.Button(btn_frame, text="⚡ Generate Wordlist", font=('Courier', 12, 'bold'),
                fg='#000', bg='#00ff88', relief='flat', padx=20, pady=10,
                command=self._generate).pack(side='left', padx=5)
        
        self.count_label = tk.Label(btn_frame, text="", font=('Courier', 9), fg='#888', bg='#1a1a2e')
        self.count_label.pack(side='left', padx=10)
        
        # Output
        out = tk.LabelFrame(self.frame, text=" Output ", font=('Courier', 10, 'bold'),
                fg='#00ccff', bg='#16213e', padx=10, pady=10)
        out.pack(fill='both', expand=True, pady=10)
        
        self.output = tk.Text(out, font=('Courier', 9), bg='#0a0a0a', fg='#00ff88',
                relief='flat', wrap='word')
        self.output.pack(fill='both', expand=True)
    
    def _toggle_custom(self):
        if self.charset_var.get() == 'custom':
            self.custom_entry.config(state='normal')
        else:
            self.custom_entry.config(state='disabled')
    
    def _get_charset(self):
        choice = self.charset_var.get()
        sets = {
            'lowercase': string.ascii_lowercase,
            'uppercase': string.ascii_uppercase,
            'digits': string.digits,
            'lowerdigits': string.ascii_lowercase + string.digits,
            'printable': string.printable.strip(),
            'custom': self.custom_entry.get().strip()
        }
        return sets.get(choice, string.ascii_lowercase)
    
    def _generate(self):
        charset = self._get_charset()
        if not charset:
            messagebox.showwarning("Warning", "Enter a character set")
            return
        
        min_len = self.min_var.get()
        max_len = min(self.max_var.get(), 15)
        
        if min_len > max_len:
            messagebox.showwarning("Warning", "Min length must be <= max length")
            return
        
        self.output.delete('1.0', 'end')
        total = sum(len(charset)**i for i in range(min_len, max_len+1))
        
        if total > 100000:
            if not messagebox.askyesno("Large Wordlist", 
                    f"This will generate {total:,} words.\nContinue?"):
                return
        
        self.count_label.config(text=f"Generating {total:,} words...")
        self.output.update()
        
        count = 0
        for length in range(min_len, max_len+1):
            for combo in itertools.product(charset, repeat=length):
                word = ''.join(combo)
                self.output.insert('end', word + '\n')
                count += 1
                if count % 1000 == 0:
                    self.count_label.config(text=f"Generated: {count:,} / {total:,}")
                    self.output.see('end')
                    self.output.update()
        
        self.count_label.config(text=f"✅ Done! {count:,} words generated")
        self.logger.log_tool_execution("wordlist_gen", f"{count} words", "completed")
