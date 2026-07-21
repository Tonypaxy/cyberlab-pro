#!/usr/bin/env python3
"""Generate CyberLab Pro icon in multiple formats"""
import os
import struct
import zlib

ICON_DIR = os.path.dirname(os.path.abspath(__file__))

def create_ico():
    """Create a simple ICO file (32x32)"""
    width, height = 32, 32
    
    # Create pixel data (shield shape with green on dark background)
    pixels = []
    for y in range(height):
        row = []
        for x in range(width):
            cx, cy = 15.5, 16
            # Shield shape
            if 4 <= y <= 28 and abs(x - cx) < (14 - abs(y - 16) * 0.4):
                # Green shield
                if abs(x - cx) > 12 or y < 5 or y > 27:
                    row.extend([0, 200, 100, 255])  # Border
                else:
                    row.extend([10, 30, 20, 255])  # Body
            elif y > 12 and y < 20 and abs(x - cx) < 4:
                row.extend([0, 255, 136, 255])  # Center mark
            else:
                row.extend([5, 10, 20, 255])  # Background
        pixels.append(row)
    
    # Save as PNG (which can be used as icon)
    save_png(pixels, width, height, 'icon.png')
    print(f"✅ Created: {os.path.join(ICON_DIR, 'icon.png')}")

def save_png(pixels, width, height, filename):
    """Save pixel data as PNG file"""
    def create_chunk(chunk_type, data):
        chunk = chunk_type + data
        crc = struct.pack('>I', zlib.crc32(chunk) & 0xffffffff)
        return struct.pack('>I', len(data)) + chunk + crc
    
    # PNG signature
    signature = b'\x89PNG\r\n\x1a\n'
    
    # IHDR chunk
    ihdr_data = struct.pack('>IIBBBBB', width, height, 8, 6, 0, 0, 0)
    ihdr = create_chunk(b'IHDR', ihdr_data)
    
    # IDAT chunk
    raw_data = b''
    for row in pixels:
        raw_data += b'\x00'  # No filter
        for i in range(0, len(row), 4):
            raw_data += bytes(row[i:i+4])
    
    compressed = zlib.compress(raw_data)
    idat = create_chunk(b'IDAT', compressed)
    
    # IEND chunk
    iend = create_chunk(b'IEND', b'')
    
    with open(os.path.join(ICON_DIR, filename), 'wb') as f:
        f.write(signature + ihdr + idat + iend)

def create_svg():
    """Create SVG icon"""
    svg = '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0a0e1a"/>
      <stop offset="100%" stop-color="#1a1a2e"/>
    </linearGradient>
    <linearGradient id="shield" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#00ff88"/>
      <stop offset="100%" stop-color="#00cc66"/>
    </linearGradient>
  </defs>
  
  <!-- Background -->
  <rect width="64" height="64" rx="12" fill="url(#bg)"/>
  
  <!-- Shield -->
  <path d="M32 8 L46 14 L46 30 C46 42 32 54 32 54 C32 54 18 42 18 30 L18 14 Z" 
        fill="none" stroke="url(#shield)" stroke-width="2.5"/>
  
  <!-- Inner shield -->
  <path d="M32 14 L42 18 L42 30 C42 39 32 48 32 48 C32 48 22 39 22 30 L22 18 Z" 
        fill="#0a1a0f" stroke="#00ff88" stroke-width="1"/>
  
  <!-- CL text -->
  <text x="32" y="34" text-anchor="middle" fill="#00ff88" 
        font-family="monospace" font-size="10" font-weight="bold">CL</text>
  
  <!-- Corner accents -->
  <circle cx="12" cy="12" r="2" fill="#00ff88" opacity="0.5"/>
  <circle cx="52" cy="12" r="2" fill="#00ff88" opacity="0.5"/>
  <circle cx="12" cy="52" r="2" fill="#00ff88" opacity="0.5"/>
  <circle cx="52" cy="52" r="2" fill="#00ff88" opacity="0.5"/>
</svg>'''
    
    with open(os.path.join(ICON_DIR, 'icon.svg'), 'w') as f:
        f.write(svg)
    print(f"✅ Created: {os.path.join(ICON_DIR, 'icon.svg')}")

def create_xpm():
    """Create XPM icon for tkinter"""
    xpm = """/* XPM */
static char * cyberlab_xpm[] = {
"32 32 5 1",
"  c #0a0e1a",
". c #1a1a2e",
"+ c #00ff88",
"@ c #0f3460",
"# c #16213e",
"                                ",
"             .....              ",
"           ..+++++..            ",
"         ..+++++++++..          ",
"        .+++++++++++++.         ",
"       .+++++.....+++++.        ",
"      .+++++.     .+++++.       ",
"      .++++.       .++++.       ",
"     .++++.         .++++.      ",
"     .++++           ++++.      ",
"     .+++.    .++.    .+++.     ",
"     .+++.    .++.    .+++.     ",
"     .+++.    .++.    .+++.     ",
"     .++++           ++++.      ",
"     .++++.         .++++.      ",
"      .++++.       .++++.       ",
"      .+++++.     .+++++.       ",
"       .+++++.....+++++.        ",
"        .+++++++++++++.         ",
"         ..+++++++++..          ",
"           ..+++++..            ",
"             .....              ",
"                                ",
"                                ",
"                                ",
"                                ",
"                                ",
"                                ",
"                                ",
"                                ",
"                                ",
"                                "};"""
    
    with open(os.path.join(ICON_DIR, 'icon.xpm'), 'w') as f:
        f.write(xpm)
    print(f"✅ Created: {os.path.join(ICON_DIR, 'icon.xpm')}")

def create_desktop_entry():
    """Create .desktop file with icon path"""
    icon_path = os.path.join(ICON_DIR, 'icon.png')
    desktop = f"""[Desktop Entry]
Name=CyberLab Pro
Comment=Professional Cybersecurity Workspace
Exec=python3 {os.path.join(os.path.dirname(ICON_DIR), 'launcher.py')}
Icon={icon_path}
Terminal=false
Type=Application
Categories=Security;Development;System;
Keywords=cybersecurity;pentest;recon;network;hacking;tools;
StartupNotify=true
StartupWMClass=cyberlab-pro
"""
    
    desktop_path = os.path.join(os.path.dirname(ICON_DIR), 'cyberlab.desktop')
    with open(desktop_path, 'w') as f:
        f.write(desktop)
    print(f"✅ Created: {desktop_path}")

if __name__ == '__main__':
    create_ico()
    create_svg()
    create_xpm()
    create_desktop_entry()
    print("\n✅ All icons generated!")
