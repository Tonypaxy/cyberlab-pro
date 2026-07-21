#!/data/data/com.termux/files/usr/bin/bash
echo "🛡️  CyberLab Pro Installer"
echo "=========================="

if [ -d "/data/data/com.termux/files/usr" ]; then
    echo "📱 Termux detected"
    pkg update -y
    pkg install python python-tkinter git termux-api -y
else
    echo "💻 Linux detected"
    sudo apt update
    sudo apt install python3 python3-tk git -y
fi

python3 setup.py
echo ""
echo "✅ Done! Run: bash run.sh"
