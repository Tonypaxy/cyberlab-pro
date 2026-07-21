import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os
import json

class PermissionsView:
    def __init__(self, parent, permissions_manager, logger, notifier=None):
        self.parent = parent
        self.pm = permissions_manager
        self.logger = logger
        self.notifier = notifier
        self.frame = tk.Frame(parent, bg='#1a1a2e')
        self.status_labels = {}
    
    def build(self):
        self.frame.pack(fill='both', expand=True, padx=15, pady=15)
        
        tk.Label(self.frame, text="🔐 System Permissions", font=('Courier', 18, 'bold'),
                fg='#00ff88', bg='#1a1a2e').pack(anchor='w', pady=(0,5))
        
        # Check all via API
        storage_ok = self._check_storage()
        camera_ok = self._check_camera()
        root_ok = self._check_root()
        net_ok = self._check_network()
        
        # Storage
        self._create_card("💾 Storage", storage_ok,
                "termux-storage-get → Save files to shared storage",
                lambda: self._run_api("termux-storage-get .", "storage"))
        
        # Camera
        self._create_card("📷 Camera", camera_ok,
                "termux-camera-photo → Take photos for evidence",
                lambda: self._run_api("termux-camera-photo -c 0 /tmp/cyberlab_test.jpg", "camera"))
        
        # Root
        self._create_card("🔐 Root", root_ok,
                "su access for advanced scanning",
                lambda: self._run_api("su -c 'echo root_granted'", "root"))
        
        # Network
        self._create_card("🌐 Network", net_ok,
                "Internet connectivity",
                lambda: self._run_api("ping -c 2 8.8.8.8", "network"))
        
        # Termux API check
        api_ok = self._check_termux_api()
        self._create_card("📡 Termux:API", api_ok,
                "termux-api package for system integration",
                lambda: self._run_api("pkg install termux-api -y", "api"))
        
        # Buttons
        btn_frame = tk.Frame(self.frame, bg='#1a1a2e')
        btn_frame.pack(fill='x', pady=15)
        
        tk.Button(btn_frame, text="🔧 Grant All via API", font=('Courier', 12, 'bold'),
                fg='#000', bg='#00ff88', relief='flat', padx=20, pady=12,
                command=self._grant_all_via_api).pack(side='left', padx=5)
        
        tk.Button(btn_frame, text="🔄 Refresh", font=('Courier', 10),
                fg='#000', bg='#00ccff', relief='flat', padx=15, pady=12,
                command=self._refresh).pack(side='left', padx=5)
        
        # API Commands reference
        info = tk.LabelFrame(self.frame, text=" Termux:API Commands ", font=('Courier', 10, 'bold'),
                fg='#00ccff', bg='#16213e', padx=15, pady=10)
        info.pack(fill='both', expand=True, pady=10)
        
        api_cmds = """Available Termux:API commands:
• termux-storage-get <dir>     - Request storage permission
• termux-camera-photo <file>   - Take photo with camera
• termux-camera-info           - Camera information
• termux-battery-status        - Battery level & status
• termux-wifi-enable <bool>    - Toggle WiFi
• termux-wifi-connectioninfo   - WiFi network info
• termux-telephony-deviceinfo  - Device information
• termux-clipboard-get/set     - Clipboard access
• termux-notification          - Send notification
• termux-vibrate               - Vibrate device
• termux-toast                 - Show toast message
• termux-dialog                - Show native dialog
• termux-location              - GPS location (needs permission)

All run via: termux-api command [args]"""
        
        text = tk.Text(info, font=('Courier', 8), bg='#0a0a0a', fg='#00ff88',
                relief='flat', wrap='word', height=12)
        text.pack(fill='both', expand=True)
        text.insert('1.0', api_cmds)
        text.config(state='disabled')
    
    def _create_card(self, name, granted, description, fix_cmd):
        card = tk.Frame(self.frame, bg='#16213e', padx=15, pady=10)
        card.pack(fill='x', pady=2)
        
        header = tk.Frame(card, bg='#16213e')
        header.pack(fill='x')
        
        icon = "✅" if granted else "❌"
        color = "#00ff88" if granted else "#cc0000"
        
        tk.Label(header, text=f"{icon} {name}", font=('Courier', 11, 'bold'),
                fg=color, bg='#16213e').pack(side='left')
        
        if not granted:
            tk.Button(header, text="⚡ Grant via API", font=('Courier', 8, 'bold'),
                    fg='#000', bg='#00ff88', relief='flat', padx=10,
                    command=fix_cmd).pack(side='right')
        
        tk.Label(card, text=description, font=('Courier', 9),
                fg='#888', bg='#16213e').pack(anchor='w')
    
    def _run_api(self, command, perm_type):
        """Run Termux:API command and show result"""
        try:
            result = subprocess.run(command, shell=True, capture_output=True, 
                    text=True, timeout=15)
            
            output = result.stdout.strip() or result.stderr.strip()
            
            if result.returncode == 0:
                messagebox.showinfo("✅ Success", 
                        f"Permission granted!\n\nCommand: {command}\nOutput: {output[:200]}")
                if self.notifier:
                    self.notifier(f"{perm_type} permission granted", "success")
            else:
                messagebox.showwarning("⚠️ Denied", 
                        f"Permission denied or not available.\n\n{output[:200]}\n\n"
                        "Check Settings → Apps → Termux → Permissions")
                if self.notifier:
                    self.notifier(f"{perm_type} permission denied", "warning")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to run API command:\n{str(e)}")
        
        self._refresh()
    
    def _check_storage(self):
        """Check storage via API"""
        try:
            result = subprocess.run(['termux-storage-get', '.'],
                    capture_output=True, text=True, timeout=5)
            return result.returncode == 0
        except:
            # Fallback: check manually
            storage = '/data/data/com.termux/files/home/storage/shared'
            if os.path.exists(storage):
                try:
                    test = os.path.join(storage, '.test')
                    with open(test, 'w') as f:
                        f.write('ok')
                    os.remove(test)
                    return True
                except:
                    pass
            return False
    
    def _check_camera(self):
        """Check camera via API"""
        try:
            result = subprocess.run(['termux-camera-info'],
                    capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                try:
                    info = json.loads(result.stdout)
                    return len(info) > 0
                except:
                    pass
        except:
            pass
        
        # Fallback
        for p in ['/dev/video0', '/dev/video1']:
            if os.path.exists(p):
                return True
        return False
    
    def _check_root(self):
        try:
            result = subprocess.run(['su', '-c', 'echo ok'],
                    capture_output=True, text=True, timeout=5)
            return result.returncode == 0
        except:
            return False
    
    def _check_network(self):
        try:
            subprocess.run(['ping', '-c', '1', '-W', '2', '8.8.8.8'],
                    capture_output=True, timeout=3)
            return True
        except:
            return False
    
    def _check_termux_api(self):
        """Check if termux-api is installed"""
        try:
            result = subprocess.run(['pkg', 'list-installed', 'termux-api'],
                    capture_output=True, text=True, timeout=5)
            return 'termux-api' in result.stdout
        except:
            return False
    
    def _grant_all_via_api(self):
        """Grant all permissions using API"""
        commands = [
            "termux-storage-get .",
            "termux-camera-info",
            "ping -c 1 8.8.8.8"
        ]
        
        results = []
        for cmd in commands:
            try:
                result = subprocess.run(cmd, shell=True, capture_output=True, 
                        text=True, timeout=10)
                status = "✅" if result.returncode == 0 else "❌"
                results.append(f"{status} {cmd}")
            except:
                results.append(f"❌ {cmd}")
        
        messagebox.showinfo("API Results", 
                "Permission requests sent via Termux:API\n\n" + 
                "\n".join(results) +
                "\n\nIf denied, go to Settings → Apps → Termux → Permissions")
        
        if self.notifier:
            self.notifier("All API permissions requested", "info")
        self._refresh()
    
    def _refresh(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.build()
