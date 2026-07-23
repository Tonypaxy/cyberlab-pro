"""
CyberLab Pro - Resource Manager
Handles large-scale operations: task queuing, memory limits, timeout control
"""
import threading, queue, time, os, gc
from datetime import datetime

class ResourceManager:
    def __init__(self, logger):
        self.logger = logger
        self.task_queue = queue.Queue(maxsize=100)
        self.active_tasks = {}
        self.max_concurrent = 3  # Max simultaneous scans
        self.memory_limit_mb = 500  # Warning threshold
        self.output_limit = 50000  # Max lines in terminal output
        self.running = True
        self._start_worker()
    
    def _start_worker(self):
        def worker():
            while self.running:
                try:
                    task = self.task_queue.get(timeout=1)
                    if task:
                        self._execute_task(task)
                except queue.Empty:
                    continue
                except Exception as e:
                    self.logger.log_error("resource_manager", e)
        threading.Thread(target=worker, daemon=True).start()
    
    def _execute_task(self, task):
        """Execute a task with resource monitoring"""
        task_id = task.get("id", str(time.time()))
        self.active_tasks[task_id] = {"started": datetime.now(), "status": "running"}
        
        try:
            # Check memory before starting
            mem = self._get_memory_usage()
            if mem > self.memory_limit_mb:
                self.logger.app_logger.warning(f"High memory usage: {mem}MB - queuing task")
                time.sleep(2)
            
            # Execute with timeout
            func = task.get("func")
            kwargs = task.get("kwargs", {})
            timeout = task.get("timeout", 300)
            
            result = func(**kwargs) if func else None
            self.active_tasks[task_id]["status"] = "completed"
            self.active_tasks[task_id]["result"] = result
            
        except Exception as e:
            self.active_tasks[task_id]["status"] = "failed"
            self.active_tasks[task_id]["error"] = str(e)
        
        # Cleanup
        gc.collect()
    
    def submit(self, func, timeout=300, **kwargs):
        """Submit a task to the queue"""
        task_id = str(time.time())
        task = {"id": task_id, "func": func, "timeout": timeout, "kwargs": kwargs}
        
        # If under concurrent limit, execute immediately
        if len(self.active_tasks) < self.max_concurrent:
            self.task_queue.put(task)
        else:
            self.task_queue.put(task)
            self.logger.app_logger.info(f"Task {task_id} queued - {self.task_queue.qsize()} pending")
        
        return task_id
    
    def get_status(self, task_id):
        """Get task status"""
        return self.active_tasks.get(task_id, {"status": "unknown"})
    
    def cancel(self, task_id):
        """Cancel a queued task"""
        if task_id in self.active_tasks:
            self.active_tasks[task_id]["status"] = "cancelled"
    
    def _get_memory_usage(self):
        """Get current memory usage in MB"""
        try:
            with open("/proc/self/status") as f:
                for line in f:
                    if "VmRSS" in line:
                        return int(line.split()[1]) // 1024
        except: pass
        return 0
    
    def get_active_count(self):
        return len([t for t in self.active_tasks.values() if t["status"] == "running"])
    
    def get_queue_size(self):
        return self.task_queue.qsize()
    
    def set_limits(self, max_concurrent=None, memory_limit=None):
        """Configure resource limits"""
        if max_concurrent: self.max_concurrent = max_concurrent
        if memory_limit: self.memory_limit_mb = memory_limit
    
    def stop(self):
        self.running = False
