#!/bin/bash
# CyberLab Pro - Linux Installer

echo "🛡️  CyberLab Pro - Linux Installation"
echo "======================================"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 required. Install: sudo apt install python3"
    exit 1
fi

# Check tkinter
python3 -c "import tkinter" 2>/dev/null || {
    echo "📦 Installing tkinter..."
    sudo apt install python3-tk -y
}

# Install to /opt
INSTALL_DIR="/opt/cyberlab"
sudo mkdir -p "$INSTALL_DIR"
sudo cp -r . "$INSTALL_DIR"
sudo chmod -R 755 "$INSTALL_DIR"

# Create desktop entry
cp cyberlab.desktop ~/.local/share/applications/cyberlab.desktop 2>/dev/null
cp cyberlab.desktop ~/Desktop/cyberlab.desktop 2>/dev/null

# Create symlink
sudo ln -sf "$INSTALL_DIR/launcher.py" /usr/local/bin/cyberlab
sudo chmod +x /usr/local/bin/cyberlab

echo ""
echo "✅ CyberLab Pro installed!"
echo "   Launch: cyberlab"
echo "   Or: python3 $INSTALL_DIR/launcher.py"
echo "   Desktop entry also created"
