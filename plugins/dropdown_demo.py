"""
Demo: How to use Dropdown in ANY module.
This gives you the same collapsible behavior as Tool Center.
"""
from gui.base_module import BaseModule
from gui.dropdown import Dropdown, DropdownGroup
import tkinter as tk

class DropdownDemo(BaseModule):
    def build_content(self):
        self.add_title("Dropdown Demo")
        
        # Single dropdown
        recon = Dropdown(self.inner, "Recon Tools", "🎯", default_open=True)
        recon.add_item("nmap", lambda: print("nmap"), "#00ff88")
        recon.add_item("gobuster", lambda: print("gobuster"), "#00ff88")
        recon.add_item("sqlmap", lambda: print("sqlmap"), "#00ff88")
        
        # Add custom widget to dropdown
        btn = tk.Button(recon.content, text="Custom Button", font=('Courier', 9),
                fg='#000', bg='#00ff88', relief='flat')
        recon.add_widget(btn)
        
        # Another dropdown
        web = Dropdown(self.inner, "Web Tools", "🌍")
        web.add_item("curl", None, "#00ccff")
        web.add_item("wpscan", None, "#00ccff")
        web.add_row("Target:", tk.Entry(web.content, font=('Courier', 9), bg='#0f3460', fg='#fff'))
        
        # Accordion group (only one open at a time)
        network = Dropdown(self.inner, "Network", "🌐")
        network.add_item("ping", None)
        network.add_item("nmap", None)
        network.add_item("netcat", None)
        
        # Nested dropdown
        advanced = Dropdown(self.inner, "Advanced", "⚙️")
        sub = Dropdown(advanced.content, "Sub Category", "📦", '#0f3460', '#ffaa00')
        sub.add_item("Tool A", None)
        sub.add_item("Tool B", None)
