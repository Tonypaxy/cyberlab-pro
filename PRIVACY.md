# Privacy Policy - CyberLab Pro

Last updated: July 2026

## Our Commitment

CyberLab Pro does NOT collect, store, transmit, or share any of your personal data. We have zero analytics, zero tracking, zero telemetry, and zero advertising. The app runs entirely on your device with no internet connection required for core functionality.

## What The App Does

CyberLab Pro is a local desktop application that runs on your phone or computer. It provides a graphical interface for security tools that you already have installed. Think of it like a window manager for your terminal tools. All processing happens on your device. Nothing leaves your device unless you explicitly run a tool that connects to a target you specify.

## Data On Your Device

The app creates these files on your device for functionality. Configuration files store your theme preference and window size in config/settings.json. Database files store your projects notes and activity history in database/cyberlab.db using SQLite. Log files record application events in logs/ folder for debugging. Project files store your scan results reports and evidence in projects/ folder. All these files stay on your device. You can delete them anytime by removing the cyberlab-pro folder.

## Permissions Explained

Storage permission is needed to save your projects reports and evidence files to your phone. Without storage permission the app cannot persist any data between sessions. The app only writes to its own folder at /data/data/com.termux/files/home/cyberlab-pro and your shared storage if you configure it.

Camera permission is optional and only used if you click the camera test in Permissions module. The app never accesses your camera automatically. You must explicitly trigger camera access.

Network permission is needed for security tools to scan targets you specify. The app itself does not make any network connections except when you run a tool that connects to a target. No data is sent to any server controlled by us.

Root access is optional and only used if your phone is rooted and you run tools that require root privileges like nmap OS detection or tcpdump. The app never requests root without your explicit action.

## Tool Execution

When you run a security tool through CyberLab Pro the tool executes locally on your device with the arguments you provide. The app does not modify inject or log your tool commands except for your own activity history stored locally. You are responsible for ensuring you have permission to scan any targets you specify.

## Data Deletion

To remove all data delete the cyberlab-pro folder from your device. cd ~ && rm -rf cyberlab-pro. This removes the app all configuration all projects all reports all evidence and all logs. Nothing remains on your device.

## Open Source

The complete source code is available at https://github.com/Tonypaxy/cyberlab-pro. You can review every line of code to verify there is no data collection. The app uses only Python standard library and tkinter. No third-party libraries that could track you.

## Contact

If you have questions about privacy open an issue on GitHub https://github.com/Tonypaxy/cyberlab-pro/issues

## Changes

This policy may update with new versions. Check the GitHub repository for the latest version.
