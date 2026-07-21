"""CyberLab Pro - Dynamic Tool Arguments System
Auto-detects arguments for all tools. Built-in args for 30+ tools.
Future installed tools auto-discover from --help output.
"""
import subprocess
import json
import os
from core.tool_args_data import BUILTIN_ARGS

class ToolArgsDatabase:
    def __init__(self, cache_dir=None):
        self.cache_dir = cache_dir or os.path.join(os.path.dirname(__file__), '..', 'cache')
        os.makedirs(self.cache_dir, exist_ok=True)
        self.cache_file = os.path.join(self.cache_dir, 'tool_args.json')
        self._load_cache()
    
    def _load_cache(self):
        self.cache = dict(BUILTIN_ARGS)
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file) as f:
                    cached = json.load(f)
                    self.cache.update(cached)
            except:
                pass
    
    def _save_cache(self):
        try:
            with open(self.cache_file, 'w') as f:
                json.dump(self.cache, f, indent=2)
        except:
            pass
    
    def get_args(self, tool_name):
        tool_name = tool_name.lower()
        if tool_name in self.cache:
            return self.cache[tool_name]
        discovered = self._discover_args(tool_name)
        if discovered:
            self.cache[tool_name] = discovered
            self._save_cache()
            return discovered
        return [("--help", "Show help")]
    
    def _discover_args(self, tool_name):
        try:
            result = subprocess.run(f"{tool_name} --help 2>&1 | head -80", shell=True,
                    capture_output=True, text=True, timeout=5)
            output = result.stdout.lower()
            args = []
            import re
            patterns = [r'(-\w{1,3})\s+(\w[\w\s]{2,35}?)', r'(--[\w-]+)\s+(\w[\w\s]{2,35}?)']
            seen = set()
            for pattern in patterns:
                for flag, desc in re.findall(pattern, output):
                    if flag not in seen and len(flag) > 1:
                        args.append((flag, desc.strip()[:35]))
                        seen.add(flag)
            return args[:20]
        except:
            return []
    
    def refresh_tool(self, tool_name):
        if tool_name in self.cache and tool_name not in BUILTIN_ARGS:
            del self.cache[tool_name]
        return self.get_args(tool_name)
    
    def discover_all_installed(self, tool_list):
        discovered_count = 0
        for tool_name in tool_list:
            if tool_name.lower() not in self.cache:
                args = self._discover_args(tool_name)
                if args and len(args) > 2:
                    self.cache[tool_name.lower()] = args
                    discovered_count += 1
        if discovered_count > 0:
            self._save_cache()
        return discovered_count
    
    def get_args_grouped(self, tool_name):
        args = self.get_args(tool_name)
        groups = {"Basic": [], "Attack/Brute": [], "Output": [], "Advanced": []}
        attack_kw = ['brute', 'attack', 'exploit', 'inject', 'tamper', 'dump', 'shell', 'pwn', 'spoof', 'flood', 'poison', 'crack', 'bypass']
        output_kw = ['-o', '--output', '-w', '--write', 'save', 'export', 'json', 'xml', 'html', 'csv']
        advanced_kw = ['proxy', 'tor', 'evasion', 'stealth', 'spoof', 'fragment', 'timeout', 'thread', 'delay', 'recursive', 'depth', 'rotate']
        for arg, desc in args:
            d = desc.lower()
            if any(k in d or k in arg.lower() for k in attack_kw): groups["Attack/Brute"].append((arg, desc))
            elif any(k in d or k in arg.lower() for k in output_kw): groups["Output"].append((arg, desc))
            elif any(k in d or k in arg.lower() for k in advanced_kw): groups["Advanced"].append((arg, desc))
            else: groups["Basic"].append((arg, desc))
        return {k: v for k, v in groups.items() if v}
    
    def get_all_tools(self):
        return list(self.cache.keys())
