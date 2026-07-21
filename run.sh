#!/data/data/com.termux/files/usr/bin/bash
# CyberLab Pro Launcher
export DISPLAY=:0
cd "$(dirname "$0")"
python3 launcher.py "$@"
