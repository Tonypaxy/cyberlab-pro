import sqlite3
import os
import json
from pathlib import Path

class Database:
    def __init__(self, db_path=None):
        self.base_dir = Path(__file__).parent.parent
        self.db_path = db_path or str(self.base_dir / "database" / "cyberlab.db")
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self._create_tables()
    
    def _create_tables(self):
        self.cursor.executescript("""
            CREATE TABLE IF NOT EXISTS projects (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE, description TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, path TEXT);
            CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY AUTOINCREMENT, project_id INTEGER, title TEXT, content TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
            CREATE TABLE IF NOT EXISTS tools (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE, category TEXT, version TEXT, path TEXT);
            CREATE TABLE IF NOT EXISTS activity (id INTEGER PRIMARY KEY AUTOINCREMENT, action TEXT, details TEXT, timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
            CREATE TABLE IF NOT EXISTS sessions (id INTEGER PRIMARY KEY AUTOINCREMENT, session_data TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
        """)
        self.conn.commit()
    
    def add_project(self, name, description=""):
        projects_dir = self.base_dir / "projects" / name
        projects_dir.mkdir(parents=True, exist_ok=True)
        for sub in ["reports", "evidence", "notes", "logs"]:
            (projects_dir / sub).mkdir(exist_ok=True)
        self.cursor.execute("INSERT INTO projects (name, description, path) VALUES (?, ?, ?)", (name, description, str(projects_dir)))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def get_all_projects(self):
        self.cursor.execute("SELECT * FROM projects ORDER BY created_at DESC")
        return [dict(row) for row in self.cursor.fetchall()]
    
    def log_activity(self, action, details=""):
        self.cursor.execute("INSERT INTO activity (action, details) VALUES (?, ?)", (action, details))
        self.conn.commit()
    
    def close(self):
        if self.conn:
            self.conn.close()

    def get_project_notes(self, project_id):
        self.cursor.execute('SELECT * FROM notes WHERE project_id = ? ORDER BY updated_at DESC', (project_id,))
        return [dict(row) for row in self.cursor.fetchall()]
    
    def add_note(self, project_id, title, content):
        self.cursor.execute(
            'INSERT INTO notes (project_id, title, content) VALUES (?, ?, ?)',
            (project_id, title, content)
        )
        self.conn.commit()
        return self.cursor.lastrowid
    
    def delete_project(self, project_id):
        try:
            self.cursor.execute('DELETE FROM notes WHERE project_id = ?', (project_id,))
            self.cursor.execute('DELETE FROM reports WHERE project_id = ?', (project_id,))
            self.cursor.execute('DELETE FROM evidence WHERE project_id = ?', (project_id,))
            self.cursor.execute('DELETE FROM projects WHERE id = ?', (project_id,))
            self.conn.commit()
            return True
        except:
            return False

    def save_session(self, session_data):
        import json
        self.cursor.execute('INSERT INTO sessions (session_data) VALUES (?)', (json.dumps(session_data),))
        self.conn.commit()
    
    def get_last_session(self):
        self.cursor.execute('SELECT session_data FROM sessions ORDER BY created_at DESC LIMIT 1')
        row = self.cursor.fetchone()
        if row:
            import json
            try:
                return json.loads(row[0])
            except:
                pass
        return None

    def get_recent_activity(self, limit=10):
        self.cursor.execute('SELECT * FROM activity ORDER BY timestamp DESC LIMIT ?', (limit,))
        return [dict(row) for row in self.cursor.fetchall()]
    
    def log_activity(self, action, details=""):
        self.cursor.execute('INSERT INTO activity (action, details) VALUES (?, ?)', (action, details))
        self.conn.commit()
