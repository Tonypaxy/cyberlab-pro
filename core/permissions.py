#!/usr/bin/env python3
"""CyberLab Pro - Permission Manager"""
import os
import subprocess
import tkinter as tk
from tkinter import messagebox

class PermissionManager:
    def __init__(self, logger):
        self.logger = logger
        self.is_termux = os.path.exists('/data/data/com.termux/files/usr/bin/bash')
        self.has_root = False
        self.has_storage = False
        self.permissions_granted = []
    
    def check_all(self):
        """Check all available permissions"""
        results = {}
        
        if self.is_termux:
            results['termux_storage'] = self._check_termux_storage()
            results['root_access'] = self._check_root()
            results['network'] = self._check_network()
            results['camera'] = self._check_camera()
        else:
            results['root_access'] = self._check_root()
            results['network'] = self._check_network()
            results['sudo'] = self._check_sudo()
        
        return results
    
    def _check_termux_storage(self):
        """Check if Termux has storage permission"""
        storage_path = '/data/data/com.termux/files/home/storage'
        return os.path.exists(storage_path) and os.path.islink(storage_path)
    
    def _check_root(self):
        """Check if root access is available"""
        try:
            result = subprocess.run(['su', '-c', 'id'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                self.has_root = True
                return True
        except:
            pass
        
        # Check alternative
        try:
            result = subprocess.run(['which', 'su'], capture_output=True, text=True)
            if result.returncode == 0 and result.stdout.strip():
                self.has_root = True
                return True
        except:
            pass
        
        return False
    
    def _check_network(self):
        """Check network access"""
        try:
            import socket
            socket.create_connection(('8.8.8.8', 53), timeout=3)
            return True
        except:
            return False
    
    def _check_camera(self):
        """Check camera access"""
        camera_paths = ['/dev/video0', '/dev/video1']
        for path in camera_paths:
            if os.path.exists(path):
                return True
        return False
    
    def _check_sudo(self):
        """Check sudo access on Linux"""
        try:
            result = subprocess.run(['sudo', '-n', 'true'], capture_output=True, timeout=3)
            return result.returncode == 0
        except:
            return False
    
    def request_termux_storage(self):
        """Request storage permission for Termux"""
        if not self.is_termux:
            return True
        
        if self._check_termux_storage():
            return True
        
        try:
            subprocess.run(['termux-setup-storage'], capture_output=True, timeout=10)
            return self._check_termux_storage()
        except:
            return False
    
    def request_root(self):
        """Request root access"""
        try:
            result = subprocess.run(['su', '-c', 'echo root_ok'], capture_output=True, text=True, timeout=10)
            if 'root_ok' in result.stdout:
                self.has_root = True
                return True
        except:
            pass
        return False
    
    def run_as_root(self, command):
        """Run command as root if available"""
        if self.has_root:
            try:
                result = subprocess.run(['su', '-c', command], capture_output=True, text=True, timeout=30)
                return result.returncode == 0, result.stdout + result.stderr
            except Exception as e:
                return False, str(e)
        return False, "Root not available"
    
    def show_permission_dialog(self, parent):
        """Show permission status and request dialog"""
        dialog = tk.Toplevel(parent, bg='#1a1a2e')
        dialog.title("🔐 Permissions")
        dialog.geometry("450x400")
        
        tk.Label(dialog, text="🔐 System Permissions", font=('Courier', 14, 'bold'),
                fg='#00ff88', bg='#1a1a2e').pack(pady=15)
        
        checks = self.check_all()
        
        # Storage
        storage_frame = tk.Frame(dialog, bg='#16213e', padx=10, pady=8)
        storage_frame.pack(fill='x', padx=15, pady=5)
        
        storage_ok = checks.get('termux_storage', True)
        icon = "✅" if storage_ok else "❌"
        tk.Label(storage_frame, text=f"{icon} Storage Access", font=('Courier', 10, 'bold'),
                fg='#00ff88' if storage_ok else '#cc0000', bg='#16213e').pack(side='left')
        
        if not storage_ok and self.is_termux:
            tk.Button(storage_frame, text="Grant", font=('Courier', 8),
                    fg='#000', bg='#00ff88', relief='flat', padx=8,
                    command=lambda: self._grant_and_refresh(dialog, 'storage')).pack(side='right')
        
        # Root
        root_frame = tk.Frame(dialog, bg='#16213e', padx=10, pady=8)
        root_frame.pack(fill='x', padx=15, pady=5)
        
        root_ok = checks.get('root_access', False)
        icon = "✅" if root_ok else "⚠️"
        tk.Label(root_frame, text=f"{icon} Root Access", font=('Courier', 10, 'bold'),
                fg='#00ff88' if root_ok else '#ffaa00', bg='#16213e').pack(side='left')
        
        if not root_ok:
            tk.Button(root_frame, text="Request", font=('Courier', 8),
                    fg='#000', bg='#ffaa00', relief='flat', padx=8,
                    command=lambda: self._grant_and_refresh(dialog, 'root')).pack(side='right')
        
        # Network
        net_frame = tk.Frame(dialog, bg='#16213e', padx=10, pady=8)
        net_frame.pack(fill='x', padx=15, pady=5)
        
        net_ok = checks.get('network', False)
        icon = "✅" if net_ok else "❌"
        tk.Label(net_frame, text=f"{icon} Network Access", font=('Courier', 10, 'bold'),
                fg='#00ff88' if net_ok else '#cc0000', bg='#16213e').pack(side='left')
        
        # Info
        info_frame = tk.Frame(dialog, bg='#1a1a2e')
        info_frame.pack(fill='x', padx=15, pady=15)
        
        info_text = "Permissions needed for:\n"
        info_text += "• Storage: Save reports, projects, evidence\n"
        info_text += "• Root: nmap -O, tcpdump, airmon-ng\n"
        info_text += "• Network: Scanning, updates, web tools"
        
        tk.Label(info_frame, text=info_text, font=('Courier', 9),
                fg='#888', bg='#1a1a2e', justify='left').pack()
        
        tk.Button(dialog, text="Close", font=('Courier', 10),
                fg='#000', bg='#00ccff', relief='flat', padx=20, pady=8,
                command=dialog.destroy).pack(pady=10)
    
    def _grant_and_refresh(self, dialog, perm_type):
        if perm_type == 'storage':
            self.request_termux_storage()
            messagebox.showinfo("Storage", "Storage permission requested.\nCheck Termux and grant if prompted.")
        elif perm_type == 'root':
            if self.request_root():
                messagebox.showinfo("Root", "Root access granted!")
            else:
                messagebox.showwarning("Root", "Root access denied or not available.")
        dialog.destroy()
