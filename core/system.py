import os
import time
import subprocess

class SystemMonitor:
    def __init__(self):
        self._cpu_count = os.cpu_count() or 4
        self._last_cpu_stats = None
    
    def get_cpu_usage(self):
        try:
            with open('/proc/stat', 'r') as f:
                line = f.readline()
                values = list(map(int, line.split()[1:]))
                if self._last_cpu_stats:
                    prev_idle = self._last_cpu_stats[3] + self._last_cpu_stats[4]
                    idle = values[3] + values[4]
                    prev_total = sum(self._last_cpu_stats)
                    total = sum(values)
                    total_diff = total - prev_total
                    idle_diff = idle - prev_idle
                    if total_diff > 0:
                        usage = (total_diff - idle_diff) / total_diff * 100
                        self._last_cpu_stats = values
                        return round(usage, 1)
                self._last_cpu_stats = values
                return 0.0
        except:
            return 0.0
    
    def get_ram_usage(self):
        try:
            with open('/proc/meminfo', 'r') as f:
                meminfo = {}
                for line in f:
                    parts = line.split(':')
                    if len(parts) == 2:
                        key = parts[0].strip()
                        value = int(parts[1].strip().split()[0])
                        meminfo[key] = value
                total = meminfo.get('MemTotal', 0) / 1024
                free = meminfo.get('MemFree', 0) / 1024
                buffers = meminfo.get('Buffers', 0) / 1024
                cached = meminfo.get('Cached', 0) / 1024
                available = free + buffers + cached
                used = total - available
                return {
                    'total': round(total, 1),
                    'used': round(used, 1),
                    'free': round(available, 1),
                    'percent': round((used / total * 100) if total > 0 else 0, 1)
                }
        except:
            return {'total': 0, 'used': 0, 'free': 0, 'percent': 0}
    
    def get_battery_info(self):
        """Get battery info from multiple possible paths"""
        battery_paths = [
            '/sys/class/power_supply/battery',
            '/sys/class/power_supply/BAT0',
            '/sys/class/power_supply/BAT1',
            '/sys/class/power_supply/bms',
            '/sys/class/power_supply/ac',
            '/sys/class/power_supply/usb'
        ]
        
        for path in battery_paths:
            try:
                if os.path.exists(path):
                    cap_file = os.path.join(path, 'capacity')
                    stat_file = os.path.join(path, 'status')
                    health_file = os.path.join(path, 'health')
                    
                    capacity = None
                    status = 'Unknown'
                    
                    if os.path.exists(cap_file):
                        with open(cap_file) as f:
                            capacity = int(f.read().strip())
                    
                    if os.path.exists(stat_file):
                        with open(stat_file) as f:
                            status = f.read().strip()
                    
                    # If we found capacity, return it
                    if capacity is not None and capacity > 0:
                        return {
                            'capacity': capacity,
                            'status': status,
                            'charging': status in ['Charging', 'Full']
                        }
            except:
                pass
        
        # Fallback: try Termux API
        try:
            result = subprocess.run(['termux-battery-status'], 
                    capture_output=True, text=True, timeout=3)
            if result.returncode == 0:
                import json
                data = json.loads(result.stdout)
                return {
                    'capacity': data.get('percentage', 0),
                    'status': data.get('status', 'Unknown'),
                    'charging': data.get('status') == 'CHARGING'
                }
        except:
            pass
        
        # Last fallback: check if charging
        try:
            for path in ['/sys/class/power_supply/usb/online', '/sys/class/power_supply/ac/online']:
                if os.path.exists(path):
                    with open(path) as f:
                        online = int(f.read().strip())
                        return {
                            'capacity': 50,  # Unknown but charging
                            'status': 'Charging' if online else 'Battery',
                            'charging': bool(online)
                        }
        except:
            pass
        
        return None
    
    def get_network_info(self):
        """Detect network connectivity"""
        interfaces = []
        
        # Check common interface names
        possible_ifaces = [
            'wlan0', 'wlan1', 'eth0', 'eth1', 'rmnet0', 'rmnet1',
            'rmnet_data0', 'rmnet_data1', 'ccmni0', 'ccmni1',
            'p2p0', 'lo', 'dummy0', 'sit0', 'tun0', 'ppp0'
        ]
        
        for iface in possible_ifaces:
            path = f'/sys/class/net/{iface}/operstate'
            if os.path.exists(path):
                try:
                    with open(path) as f:
                        state = f.read().strip()
                        if state == 'up' and iface != 'lo':
                            interfaces.append(iface)
                except:
                    pass
        
        # If no interfaces found via sysfs, try ip command
        if not interfaces:
            try:
                result = subprocess.run(['ip', 'link', 'show', 'up'], 
                        capture_output=True, text=True, timeout=5)
                for line in result.stdout.split('\n'):
                    if ': ' in line and 'lo:' not in line:
                        iface = line.split(':')[1].strip().split('@')[0]
                        if iface:
                            interfaces.append(iface)
            except:
                pass
        
        # Final fallback: ping test
        connected = len([i for i in interfaces if i != 'lo']) > 0
        
        if not connected:
            try:
                subprocess.run(['ping', '-c', '1', '-W', '2', '8.8.8.8'],
                        capture_output=True, timeout=3)
                connected = True
            except:
                pass
        
        return {
            'connected': connected,
            'interfaces': interfaces if interfaces else ['unknown']
        }
    
    def get_storage_info(self):
        try:
            stat = os.statvfs('/data/data/com.termux/files/home')
        except:
            try:
                stat = os.statvfs(os.path.expanduser('~'))
            except:
                return {'total': 0, 'used': 0, 'free': 0, 'percent': 0}
        
        total = (stat.f_blocks * stat.f_frsize) / (1024**3)
        free = (stat.f_bfree * stat.f_frsize) / (1024**3)
        used = total - free
        
        return {
            'total': round(total, 2),
            'used': round(used, 2),
            'free': round(free, 2),
            'percent': round((used / total * 100) if total > 0 else 0, 1)
        }
    
    def get_running_services(self):
        """Count running security tools/services"""
        services = 0
        tool_processes = [
            'nmap', 'gobuster', 'sqlmap', 'hydra', 'nikto', 'dirb',
            'wpscan', 'ffuf', 'amass', 'subfinder', 'httpx', 'msfconsole',
            'aircrack-ng', 'tcpdump', 'wireshark', 'tshark', 'bettercap',
            'metasploit', 'beef', 'burpsuite', 'john', 'hashcat'
        ]
        
        try:
            result = subprocess.run(['ps', 'aux'], capture_output=True, text=True, timeout=5)
            for proc in tool_processes:
                if proc in result.stdout.lower():
                    services += 1
        except:
            pass
        
        return services
    
    def get_summary(self):
        return {
            'cpu': self.get_cpu_usage(),
            'ram': self.get_ram_usage(),
            'battery': self.get_battery_info(),
            'network': self.get_network_info(),
            'storage': self.get_storage_info(),
            'services': self.get_running_services(),
            'timestamp': time.time()
        }
