import threading
import time

class ServiceManager:
    def __init__(self, logger):
        self.logger = logger
        self.services = {}
        self._threads = {}
        self._running = False
    
    def register(self, name, func, interval=60):
        self.services[name] = {
            'func': func,
            'interval': interval,
            'status': 'stopped'
        }
    
    def start(self, name):
        if name in self.services and self.services[name]['status'] != 'running':
            service = self.services[name]
            service['status'] = 'running'
            self.logger.log_service(name, 'started')
            
            def run():
                while service['status'] == 'running':
                    try:
                        service['func']()
                    except Exception as e:
                        self.logger.log_error(f"service_{name}", e)
                    time.sleep(service['interval'])
            
            thread = threading.Thread(target=run, daemon=True)
            thread.start()
            self._threads[name] = thread
            return True
        return False
    
    def stop(self, name):
        if name in self.services:
            self.services[name]['status'] = 'stopped'
            self.logger.log_service(name, 'stopped')
            return True
        return False
    
    def stop_all(self):
        for name in self.services:
            self.stop(name)
    
    def get_status(self, name):
        return self.services.get(name, {}).get('status', 'unknown')
    
    def get_all(self):
        return {name: info['status'] for name, info in self.services.items()}
