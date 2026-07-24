import subprocess, json, os

class ToolArgsDatabase:
    def __init__(self, cache_dir=None):
        self.cache_dir = cache_dir or os.path.join(os.path.dirname(__file__), '..', 'cache')
        os.makedirs(self.cache_dir, exist_ok=True)
        self.cache_file = os.path.join(self.cache_dir, 'tool_args.json')
        self.cache = {}
        self._load_parts()
        self._load_cache()

    def _load_parts(self):
        from core.tool_args_part1 import BUILTIN_ARGS as p1
        from core.tool_args_part2 import BUILTIN_ARGS as p2
        from core.tool_args_part3 import BUILTIN_ARGS as p3
        from core.tool_args_part4 import BUILTIN_ARGS as p4
        from core.tool_args_part5 import BUILTIN_ARGS as p5
        from core.tool_args_part6 import BUILTIN_ARGS as p6
        from core.tool_args_part7 import BUILTIN_ARGS as p7
        self.cache.update(p1); self.cache.update(p2); self.cache.update(p3)
        self.cache.update(p4); self.cache.update(p5); self.cache.update(p6); self.cache.update(p7)

    def _load_cache(self):
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file) as f:
                    self.cache.update(json.load(f))
            except: pass

    def _save_cache(self):
        with open(self.cache_file, 'w') as f:
            json.dump(self.cache, f, indent=2)

    def get_args(self, tool_name):
        tool_name = tool_name.lower()
        if tool_name in self.cache: return self.cache[tool_name]
        discovered = self._discover_args(tool_name)
        if discovered:
            self.cache[tool_name] = discovered
            self._save_cache()
            return discovered
        return [("--help", "Show help")]

    def _discover_args(self, tool_name):
        try:
            r = subprocess.run(f"{tool_name} --help 2>&1 | head -60", shell=True,
                    capture_output=True, text=True, timeout=5)
            import re
            args = []
            for p in [r'(-\w{1,3})\s+(\w[\w\s]{2,30}?)', r'(--[\w-]+)\s+(\w[\w\s]{2,30}?)']:
                for flag, desc in re.findall(p, r.stdout.lower()):
                    if flag not in [a[0] for a in args]:
                        args.append((flag, desc.strip()[:30]))
            return args[:15]
        except: return []

    def get_all_tools(self): return list(self.cache.keys())
