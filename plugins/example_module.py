"""
Example Future Module - Copy this template for new modules.
Shows how BaseModule makes everything scrollable and responsive.
"""
from gui.base_module import BaseModule
import tkinter as tk

class ExampleModule(BaseModule):
    """My new module - inherits scroll, sections, cards, all for free"""
    
    def build_content(self):
        # Title
        self.add_title("My New Module", "Description of what this does")
        
        # Collapsible section 1
        def section1_content(parent):
            self.create_card("Card Title", "Card details here", "#00ff88")
            self.add_button("Click Me", lambda: print("Clicked"), "#00ccff")
            self.add_entry("Input:", "default value")
        
        self.add_section("Section One", section1_content, "📦", default_open=True)
        
        # Collapsible section 2
        def section2_content(parent):
            for i in range(10):
                self.create_card(f"Item {i}", f"Details for item {i}")
        
        self.add_section("Items List", section2_content, "📋")
        
        # Collapsible section 3
        def section3_content(parent):
            self.add_text(height=5)
            self.add_status("Ready")
        
        self.add_section("Output", section3_content, "📄")
