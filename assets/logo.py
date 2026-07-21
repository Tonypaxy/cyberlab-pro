#!/usr/bin/env python3
"""Generate CyberLab Pro logo"""
import os

LOGO_ASCII = r"""
  ██████╗██╗   ██╗██████╗ ███████╗██████╗ ██╗      █████╗ ██████╗ 
 ██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗██║     ██╔══██╗██╔══██╗
 ██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝██║     ███████║██████╔╝
 ██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗██║     ██╔══██║██╔══██╗
 ╚██████╗   ██║   ██████╔╝███████╗██║  ██║███████╗██║  ██║██████╔╝
  ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═════╝ 
  ┌──────────────────────────────────────────────────────────────┐
  │  🛡️  Professional Cybersecurity Workspace for Termux:X11  🛡️  │
  │         Optimized for ARM 32-bit | Offline-First           │
  └──────────────────────────────────────────────────────────────┘
"""

SMALL_LOGO = """
╔══════════════════════╗
║   🛡️ CYBERLAB PRO   ║
║      v1.0.0         ║
║  Termux Workspace   ║
╚══════════════════════╝
"""

ICON_SHIELD = """
   ╔═══════╗
   ║  🛡️   ║
   ║ C L P ║
   ╚═══════╝
"""

def print_logo():
    print(LOGO_ASCII)

def print_small():
    print(SMALL_LOGO)

def print_icon():
    print(ICON_SHIELD)

if __name__ == "__main__":
    print_logo()
