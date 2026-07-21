# 🛡️ CyberLab Pro v1.0

Professional Cybersecurity Workspace for Android Termux+X11 and Linux Desktop. Works on any phone from 1GB RAM to flagship devices.

---

## Check Your Phone Environment First

Open Termux and run this command to see your phone specifications. cat /proc/cpuinfo | grep -E "model|Processor|Hardware" && free -h && df -h /data. This shows your CPU model RAM size and free storage so you know what tools your phone can handle.

---

## Phone Categories - What Works On Your Device

### Low-End Phones with 1GB to 2GB RAM like Itel Tecno old Samsung J series old Xiaomi Redmi 5A Nokia 1

These phones have 32-bit ARM Cortex-A7 or A53 processors with 4 cores. Storage is usually 16GB or 32GB with 4GB to 8GB free. Android version is usually 8 to 10 Go edition. Screen is 5 to 5.5 inches with 480p or 720p resolution. Termux runs well but heavy tools will freeze or crash.

Tools that work reliably are nmap with -F flag for fast scans takes about 2 minutes per host ping and traceroute for network testing dig and whois for DNS reconnaissance curl for HTTP requests netcat for port connections sqlmap with --batch flag for automated injection takes 5 to 10 minutes per URL dirb with wordlists under 5000 lines hydra with single username and small password lists under 1000 entries python3 for custom scripts git for cloning repositories john with rockyou truncated to 10000 lines takes about 30 minutes hashcat with -O optimized flag for dictionary attacks.

Tools that will NOT work are nmap -p- full port scans will timeout after 10 minutes gobuster with wordlists over 5000 lines will freeze the phone metasploit needs minimum 4GB RAM to load amass enumeration uses over 2GB RAM and crashes ffuf with large wordlists causes out of memory error go-based tools like subfinder httpx assetfinder gau waybackurls need compilation which fails on 32-bit ARM john with full rockyou txt takes 6 hours plus hashcat with rules needs GPU acceleration tcpdump packet capture fills storage in minutes running two tools simultaneously causes system freeze.

Recommended settings for low-end phones use AMOLED theme to save battery set nmap timing to -T2 slow but stable limit all wordlists to maximum 5000 lines close all apps before scanning keep phone plugged into charger use WiFi instead of mobile data for stable connection enable storage permission for saving results run only one tool at a time monitor RAM in dashboard if it goes above 90 percent stop all tools and clear terminal output do not use SOC monitoring it consumes extra resources disable notifications to save CPU cycles keep screen brightness at minimum.

### Mid-Range Phones with 3GB to 4GB RAM like Samsung A series A20 A30 A50 Redmi Note 8 9 10 Realme 5 6 7 Moto G series G7 G8 G9 Nokia 5 6 7

These phones have 64-bit ARM Cortex-A73 or A55 processors with 8 cores. Storage is 32GB to 128GB with 10GB to 30GB free. Android version is 10 to 13 with full features. Screen is 6 to 6.5 inches with 1080p resolution. Termux runs smoothly and most tools work without issues.

Tools that work well are everything from low-end plus nmap full port scans -p- with -T4 timing takes about 15 minutes gobuster with wordlists up to 50000 lines nikto full web scan takes 10 minutes wpscan WordPress enumeration takes 5 minutes whatweb technology detection takes 2 minutes sqlmap full with --dump --tables --columns takes 20 minutes hydra with user lists and password lists up to 10000 entries john with full rockyou txt takes about 1 hour hashcat with basic rules and dictionary attacks metasploit auxiliary modules and some exploits subfinder and assetfinder for subdomain discovery httpx for live host probing gau and waybackurls for URL history discovery tcpdump for packet capture with filters netcat for shells and file transfers ffuf with 100 threads and wordlists up to 50000 lines all programming tools python go ruby perl php node gcc make can run two tools simultaneously if RAM stays below 80 percent.

Tools to be careful with are metasploit exploits need timing and patience amass full enumeration takes 30 minutes plus and uses 2GB RAM hashcat with complex rules slows the phone noticeably running three or more tools simultaneously causes lag and heat go-based tool compilation takes 5 to 10 minutes but works large wordlist generation above 100000 lines causes slowdown tcpdump with -vv verbose flag on busy network fills memory nikto with all plugins enabled takes 30 minutes.

Recommended settings use Dark or Ocean theme set nmap timing to -T4 fast but stable set gobuster and ffuf threads to 50 to 100 keep at least 1GB RAM free close social media and video apps use WiFi 5GHz band for faster scanning keep phone in cool place avoid direct sunlight keep charger connected for long scans enable all permissions for full functionality use SOC monitoring to watch resources during scans.

### Flagship Phones with 6GB to 12GB RAM like Samsung S series S20 S21 S22 S23 S24 OnePlus 8 9 10 11 Google Pixel 6 7 8 Xiaomi 12 13 14 series Sony Xperia 1 5 series Asus ROG Phone

These phones have 64-bit Snapdragon 8 series or Tensor or Dimensity 9000 processors with 8 cores. Storage is 128GB to 512GB with plenty free. Android version is 13 to 14 with all features. Screen is 6.5 to 6.8 inches with 1440p AMOLED display. Termux runs like a desktop Linux machine with no limitations.

Everything works without restrictions. nmap full port scans -p- with -T5 timing takes 5 minutes gobuster with massive wordlists over 1 million lines nikto with all plugins full scan takes 5 minutes wpscan full enumeration with API token sqlmap with all options and tamper scripts hydra with massive user and password lists john with all modes and full rockyou hashcat with full rules masks and combinator attacks metasploit full framework with all exploits payloads and auxiliary modules amass full passive and active enumeration with all sources subfinder with all APIs configured httpx with all probes and screenshots gau and waybackurls with full history extraction ffuf with 200 threads and unlimited wordlists tcpdump full packet capture without filters netcat with all options all go tools compile in under a minute burpsuite community edition if installed docker containers if configured custom wordlist generation up to millions of entries can run 4 or more tools simultaneously with no lag.

No restrictions at all. Your phone equals a laptop in capability. Only limits are battery life and heat generation during extended operations.

Recommended settings use any theme you prefer maximum performance on all tools keep phone plugged into fast charger use phone cooling fan for extended operations exceeding 1 hour store wordlists on internal storage for faster access enable all permissions including root if available use SOC monitoring to track long operations can leave running overnight for full enumeration tasks.

---

## Installation Methods

### Method 1 Android Phone with Termux and Termux:X11 from F-Droid

Step 1 Install F-Droid. Download from https://f-droid.org on your phone browser. Open the downloaded APK file and allow installation from unknown sources when prompted. Open F-Droid and wait for repository update to complete about 2 minutes.

Step 2 Install required apps. In F-Droid search for Termux and install it this gives you a Linux terminal on Android. Search for Termux:X11 and install it this provides the X11 display server needed to show GUI applications. Search for Termux:API and install it this allows accessing Android hardware like camera storage and sensors. These three apps together create a complete Linux desktop environment on your phone.

Step 3 Setup Termux. Open the Termux app you will see a black terminal with white text. Type pkg update && pkg upgrade -y this updates all packages to latest versions takes 3 to 5 minutes depending on internet speed. Type pkg install x11-repo -y this adds the repository containing X11 packages. Type pkg install python python-tkinter git termux-api -y this installs Python for running the app tkinter for the graphical interface git for downloading the project termux-api for Android integration. Type termux-setup-storage this triggers Android permission popup tap Allow to grant storage access if you deny the app cannot save projects or reports.

Step 4 Start Termux:X11. Open the Termux:X11 app from your phone app drawer it shows a blank screen with a settings icon in top right corner. Do not close this app press the home button or use recent apps to switch back to Termux while keeping Termux:X11 running in background. In Termux type termux-x11 :0 & this starts the X11 display server as a background process. Type export DISPLAY=:0 this tells graphical applications where to render their windows. You must do these two commands every time you restart Termux or after rebooting your phone.

Step 5 Download and Launch CyberLab. Type git clone https://github.com/Tonypaxy/cyberlab-pro.git this downloads the entire project about 2MB in size. Type cd cyberlab-pro to enter the project folder. Type python3 setup.py this creates necessary directories and configuration files. Type python3 launcher.py to start the application you should see a splash screen with shield logo followed by the main dashboard with system statistics. First launch takes about 5 seconds subsequent launches are faster.

Step 6 Create Quick Launch Alias. Type echo 'alias cyberlab="cd ~/cyberlab-pro && export DISPLAY=:0 && python3 launcher.py"' >> ~/.bashrc this adds a shortcut command to your bash configuration. Type source ~/.bashrc to reload the configuration. Now anytime you open Termux just type cyberlab and press enter the entire app launches with a single word.

### Method 2 FluxLinux Optional Advanced Setup

FluxLinux is a proot-distro that runs a full Linux distribution inside Termux without root. It gives you access to Linux package managers like apt with thousands of packages. This is optional and only needed if you want to use Linux-specific tools that are not available in Termux repositories.

Why use FluxLinux. Some security tools are only packaged for Debian Ubuntu or Kali Linux and not available in Termux pkg. FluxLinux gives you access to apt-get install with the full Debian repository. You can install tools like burpsuite zaproxy wireshark that are not in Termux. FluxLinux shares the same kernel as Termux so performance is similar. The downside is it uses about 500MB extra storage for the Linux filesystem.

Install FluxLinux. In Termux type pkg install proot-distro -y this installs the proot container manager. Type proot-distro install ubuntu this downloads and installs Ubuntu about 300MB download takes 5 to 15 minutes depending on internet. After installation type proot-distro login ubuntu this enters the Ubuntu environment you will see root@localhost prompt.

Setup inside FluxLinux. Type apt update && apt upgrade -y this updates Ubuntu packages. Type apt install python3 python3-tk git curl nmap -y this installs Python and required tools. Type apt install x11-apps -y this installs X11 support for GUI. Type exit to return to Termux.

Install CyberLab inside FluxLinux. From Termux type proot-distro login ubuntu to enter FluxLinux again. Type git clone https://github.com/Tonypaxy/cyberlab-pro.git to download the project inside the Ubuntu filesystem. Type cd cyberlab-pro && python3 setup.py to configure. To launch from Termux with Termux:X11 running type proot-distro login ubuntu -- bash -c "export DISPLAY=:0 && cd ~/cyberlab-pro && python3 launcher.py". This runs the app inside FluxLinux but displays on Termux:X11.

When to use FluxLinux versus Termux direct. Use Termux direct for most tasks it is faster uses less storage and has 40 plus tools available via pkg and pip. Use FluxLinux when you need apt-get tools like burpsuite zaproxy wireshark or when a Python pip package fails to compile in Termux. FluxLinux adds complexity so only use it if you specifically need Debian packages.

### Method 3 Linux Desktop Ubuntu Debian Kali Parrot Arch Fedora

For Ubuntu Debian Kali Parrot open terminal and type sudo apt update && sudo apt install python3 python3-tk git curl -y this installs all requirements. Type git clone https://github.com/Tonypaxy/cyberlab-pro.git to download the project. Type cd cyberlab-pro && bash install_linux.sh this installs the app creates a desktop entry and adds cyberlab command to your PATH. Type cyberlab to launch or find CyberLab Pro in your applications menu under Security or Development category.

For Arch Linux or Manjaro open terminal and type sudo pacman -Syu && sudo pacman -S python tk git this installs requirements. Type git clone https://github.com/Tonypaxy/cyberlab-pro.git to download. Type cd cyberlab-pro && python3 launcher.py to launch.

For Fedora open terminal and type sudo dnf update && sudo dnf install python3 python3-tkinter git this installs requirements. Type git clone https://github.com/Tonypaxy/cyberlab-pro.git to download. Type cd cyberlab-pro && python3 launcher.py to launch.

### Method 4 One Command Install Any Platform

Type curl -sSL https://raw.githubusercontent.com/Tonypaxy/cyberlab-pro/main/install.sh | bash this downloads and runs the installer automatically. Works on Termux and all Linux distributions. You still need Termux:X11 running on Android.

---

## All Features Explained

Dashboard shows real-time system statistics CPU percentage RAM usage and percentage disk free space in gigabytes battery level with charging status network connectivity status number of installed tools number of projects with active project name recent activity log and installed tools by category with quick action buttons for New Scan Terminal Reports Projects Notes.

Projects creates organized folders for each security engagement with subdirectories for reports evidence notes logs scripts screenshots exports each project shows creation date and file counts open project shows quick links to Recon Network Web Notes Evidence Reports modules with back navigation.

Tool Center displays 40 plus security tools grouped into 8 categories Recon Web Network Credentials Wireless Forensics Programming Exploitation each tool shows name command path version installed tools have green checkmark and Run and Help buttons available tools have gray icon and Install buttons with pkg pip options clicking Run opens dialog with dynamic argument buttons based on tool help output clicking an argument button adds it to command field Execute runs the tool and shows real-time output with Stop button.

Recon Workspace provides target input field with quick scan buttons for Nmap Fast Nmap Service Nmap All Ports Nmap Scripts DNS Lookup Whois Ping Traceroute each scan runs in background thread and shows output in real-time results save to project logs folder automatically Stop All button kills all running scans.

Network Tools includes Ping Traceroute Netcat Listen Netcat Connect ARP Table Netstat DNS Lookup Curl each with target input and Run button output shows in embedded terminal with syntax highlighting.

Web Tools includes cURL GET cURL Headers cURL Full WhatWeb Nikto SQLMap Dirb WPScan each with target URL input and Execute button installed tools are clickable uninstalled tools are grayed out output shows in real-time.

SOC Dashboard monitors system resources continuously with Start Stop Monitoring button shows CPU RAM Disk Network status as large color-coded cards alerts trigger when CPU exceeds 80 percent RAM exceeds 90 percent Disk below 1GB free live log shows timestamped system readings.

Reports shows all scan outputs and log files for selected project each file shows name size date with View Export HTML Export PDF buttons Export All as HTML or TXT generates full project report with dark theme styling.

Evidence Locker stores evidence files per project Add Evidence button creates note or imports files from phone storage each item shows icon type size with Open and Delete buttons.

Notes provides project-based note taking with project selector on left notes list and title content editor on right Save button stores to database New button creates blank note.

Terminal is full bash shell with command history arrow keys cd pwd clear commands no timeout handles long operations Kill button stops processes Clear button resets output.

Plugins manages custom Python extensions Create button opens editor with template code each plugin shows name size status Load runs the plugin Edit opens code editor Delete removes permanently Open Folder opens plugin directory in file manager.

Wordlist Generator creates custom wordlists with charset selection lowercase uppercase digits custom min and max length up to 15 Generate button creates wordlist with progress count.

Permissions shows storage camera root network status with Grant buttons Auto-Fix All button requests all permissions via Termux API instructions show manual fix steps for Android settings.

Settings provides theme selector with 6 options Dark AMOLED Matrix Light Cyberpunk Ocean radio buttons apply theme instantly window size configuration auto-save toggle notifications toggle about section with version info.

---

## Themes Available

Dark theme is default with deep navy background and green accents good for daytime use and most readable. AMOLED theme uses pure black background with green accents saves battery on OLED screens best for night use. Matrix theme uses black background with classic green text like the movie terminal aesthetic for hackers. Light theme uses white background with dark text for bright environments and outdoor use. Cyberpunk theme uses deep purple background with neon pink and cyan accents futuristic aesthetic. Ocean theme uses dark blue background with teal accents calm professional look.

---

## Troubleshooting

Blank screen or no module named tkinter means graphics library missing install with pkg install python-tkinter -y on Termux or sudo apt install python3-tk -y on Linux.

DISPLAY not set error means X11 server not running start with termux-x11 :0 & and export DISPLAY=:0 make sure Termux:X11 app is open in background.

Storage permission denied means Android blocked access run termux-setup-storage and tap Allow on popup or go to Settings Apps Termux Permissions Files and Media and enable.

Tools not detected means they are not installed run pkg install nmap hydra curl -y and pip install sqlmap then click Refresh in Tool Center or restart app.

App crashes on startup means corrupted files delete and clone fresh with cd ~ && rm -rf cyberlab-pro && git clone https://github.com/Tonypaxy/cyberlab-pro.git.

Phone gets hot during scans means too much CPU usage reduce scan speed with -T2 flag close other apps use AMOLED theme keep phone in cool place plug in charger.

Termux:X11 shows black screen means display server crashed run pkill termux-x11 then restart with termux-x11 :0 & and export DISPLAY=:0.

Slow performance on low-end phone means insufficient RAM close all apps use AMOLED theme limit wordlists to 1000 lines run one tool at a time disable SOC monitoring.

---

## License

MIT License free to use modify and distribute. Built for security professionals who need mobile penetration testing capabilities.

GitHub https://github.com/Tonypaxy/cyberlab-pro

---

## Privacy

CyberLab Pro collects ZERO data. No analytics no tracking no telemetry no ads no network calls to any server. Everything runs locally on your device. The app never connects to the internet unless you explicitly run a security tool that connects to a target you specify. All files stay on your phone in the cyberlab-pro folder. Delete the folder and everything is gone. Source code is open for you to verify. Read full privacy policy in PRIVACY.md file.

## Permissions The App Requests

Storage permission is needed only to save your projects reports and evidence files locally on your phone. Camera permission is optional only used if you manually test camera in the Permissions module. Network permission is needed for security tools to scan targets you specify. Root access is optional only used if your phone is rooted and you run root-required tools. The app never uses any permission automatically without your action. You control everything.

## How The App Works

CyberLab Pro is a GUI wrapper for your existing security tools. It does not install tools by itself it detects what you already have. When you click Run on nmap the app executes nmap on your device and shows the output in a window same as running it in terminal but with a nicer interface. The app organizes your work into projects with folders for reports evidence notes. Everything is stored in SQLite database locally. The app uses Python tkinter for graphics which is built into Python with no extra downloads. No cloud no subscription no login required.
