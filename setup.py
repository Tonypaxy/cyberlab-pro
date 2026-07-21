#!/usr/bin/env python3
"""CyberLab Pro - Installation Script"""
import os
import sys
import shutil
from pathlib import Path

def install():
    print("🛡️  CyberLab Pro Installer")
    print("=" * 50)
    
    # Directories
    home = Path.home()
    cyberlab_dir = home / "CyberLab"
    bin_dir = home / "bin"
    desktop_dir = home / ".local" / "share" / "applications"
    
    # Create bin directory
    bin_dir.mkdir(exist_ok=True)
    
    # Create launcher script
    launcher_path = bin_dir / "cyberlab"
    with open(launcher_path, 'w') as f:
        f.write(f'''#!/data/data/com.termux/files/usr/bin/bash
# CyberLab Pro Launcher
export DISPLAY=:0
cd {cyberlab_dir}
python3 launcher.py "$@"
''')
    launcher_path.chmod(0o755)
    print(f"✅ Created: {launcher_path}")
    
    # Create desktop entry
    desktop_dir.mkdir(parents=True, exist_ok=True)
    desktop_path = desktop_dir / "cyberlab.desktop"
    with open(desktop_path, 'w') as f:
        f.write(f'''[Desktop Entry]
Name=CyberLab Pro
Comment=Professional Cybersecurity Workspace
Exec={launcher_path}
Icon={cyberlab_dir}/assets/icon.png
Terminal=false
Type=Application
Categories=Security;Development;
StartupNotify=true
''')
    print(f"✅ Created: {desktop_path}")
    
    # Add to PATH if needed
    bashrc = home / ".bashrc"
    path_line = f'export PATH="$PATH:{bin_dir}"'
    if bashrc.exists():
        content = bashrc.read_text()
        if path_line not in content:
            with open(bashrc, 'a') as f:
                f.write(f'\n# CyberLab Pro\n{path_line}\n')
            print(f"✅ Added to PATH in .bashrc")
    
    # Create icon placeholder
    assets_dir = cyberlab_dir / "assets"
    assets_dir.mkdir(exist_ok=True)
    
    print("\n" + "=" * 50)
    print("✅ CyberLab Pro installed successfully!")
    print("=" * 50)
    print(f"\nLaunch from terminal: cyberlab")
    print(f"Or run: cd {cyberlab_dir} && python3 launcher.py")
    print(f"\nDesktop entry created for Termux:X11")
    print(f"Restart Termux or run: source ~/.bashrc")

if __name__ == "__main__":
    install()
