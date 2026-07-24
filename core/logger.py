import logging
import os
from datetime import datetime
from pathlib import Path
from logging.handlers import RotatingFileHandler

class CyberLogger:
    def __init__(self, base_dir=None):
        self.base_dir = Path(base_dir or Path(__file__).parent.parent)
        self.logs_dir = self.base_dir / "logs"
        self.logs_dir.mkdir(exist_ok=True)
        self.app_logger = None
        self.tools_logger = None
        self.projects_logger = None
        self.error_logger = None
        self._setup_loggers()
    
    def _create_handler(self, filename):
        handler = RotatingFileHandler(self.logs_dir / filename, maxBytes=5*1024*1024, backupCount=3)
        handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        return handler
    
    def _setup_loggers(self):
        self.app_logger = logging.getLogger("cyberlab.app")
        self.app_logger.addHandler(self._create_handler("application.log"))
        self.tools_logger = logging.getLogger("cyberlab.tools")
        self.tools_logger.addHandler(self._create_handler("tools.log"))
        self.projects_logger = logging.getLogger("cyberlab.projects")
        self.projects_logger.addHandler(self._create_handler("projects.log"))
        self.error_logger = logging.getLogger("cyberlab.errors")
        self.error_logger.addHandler(self._create_handler("errors.log"))
    
    def log_startup(self):
        self.app_logger.info("CyberLab Pro Shutting Down")
        self.app_logger.info("CyberLab Pro Shutting Down")
        self.app_logger.info("="*50)
        self.app_logger.info("CyberLab Pro Started")
    
    def log_error(self, module, error):
        self.error_logger.error(f"[{module}] {str(error)}")

    def log_tool_execution(self, tool, command, status):
        self.tools_logger.info(f"Tool: {tool} | Cmd: {command} | Status: {status}")
