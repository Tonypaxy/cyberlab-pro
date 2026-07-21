"""CyberLab Pro - Project Core Operations"""
import os
import shutil
from datetime import datetime
from pathlib import Path

class ProjectCore:
    def __init__(self, database, logger):
        self.db = database
        self.logger = logger
    
    def create(self, name, description=""):
        """Create a new project with full directory structure"""
        base = Path(__file__).parent.parent
        proj_path = base / "projects" / name
        
        # Create directories
        dirs = ['reports', 'evidence', 'notes', 'logs', 'scripts', 'screenshots', 'exports']
        for d in dirs:
            (proj_path / d).mkdir(parents=True, exist_ok=True)
        
        # Create project README
        readme = proj_path / "README.md"
        readme.write_text(f"""# {name}
**Created:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Description:** {description}

## Structure
- `reports/` - Scan reports and outputs
- `evidence/` - Collected evidence files
- `notes/` - Project notes
- `logs/` - Tool execution logs
- `scripts/` - Custom scripts
- `screenshots/` - Screenshots
- `exports/` - Exported data
""")
        
        # Save to database
        proj_id = self.db.add_project(name, description)
        self.logger.log_project_action(name, "created")
        return proj_id
    
    def delete(self, project_id):
        """Delete project and all its files"""
        project = self.db.get_project(project_id)
        if project:
            proj_path = Path(project['path'])
            if proj_path.exists():
                shutil.rmtree(proj_path)
            self.db.delete_project(project_id)
            self.logger.log_project_action(project['name'], "deleted")
            return True
        return False
    
    def export(self, project_id, export_dir):
        """Export project to directory"""
        project = self.db.get_project(project_id)
        if not project:
            return False
        
        proj_path = Path(project['path'])
        export_path = Path(export_dir) / project['name']
        
        if proj_path.exists():
            shutil.copytree(proj_path, export_path)
            self.logger.log_project_action(project['name'], f"exported to {export_dir}")
            return True
        return False
    
    def get_stats(self, project_id):
        """Get project statistics"""
        project = self.db.get_project(project_id)
        if not project:
            return {}
        
        proj_path = Path(project['path'])
        stats = {
            'name': project['name'],
            'created': project.get('created_at'),
            'files': 0,
            'reports': 0,
            'evidence': 0,
            'notes': 0,
            'total_size': 0
        }
        
        if proj_path.exists():
            for f in proj_path.rglob('*'):
                if f.is_file():
                    stats['files'] += 1
                    stats['total_size'] += f.stat().st_size
                    parent = f.parent.name
                    if parent == 'reports':
                        stats['reports'] += 1
                    elif parent == 'evidence':
                        stats['evidence'] += 1
                    elif parent == 'notes':
                        stats['notes'] += 1
        
        return stats
