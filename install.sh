#!/bin/bash
echo "🛡️  CyberLab Pro - One-Command Install"
echo "========================================"

if [ -d "/data/data/com.termux/files/usr" ]; then
    echo "📱 Detected Termux"
    pkg update -y
    pkg install python python-tkinter git termux-api -y
else
    echo "💻 Detected Linux"
    sudo apt update
    sudo apt install python3 python3-tk git curl -y
fi

python3 setup.py
echo ""
echo "✅ Installation complete!"
echo "Run: cyberlab"
