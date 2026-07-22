"""
CyberLab Pro - Shared PTY Terminal Handler
All modules use this single powerful terminal for command execution.
"""
import os
import pty
import select
import subprocess
import threading
import signal

class PTYHandler:
    """Single shared PTY terminal used by all modules"""
    
    def __init__(self):
        self.processes = {}
        self.outputs = {}
        self.master_fds = {}
    
    def run_command(self, cmd, output_widget, on_complete=None, module_id=None):
        """Run a command in PTY and stream output to any tkinter Text widget"""
        # Try PTY first, fall back to subprocess
        try:
            return self._run_pty(cmd, output_widget, on_complete)
        except Exception as e:
            return self._run_fallback(cmd, output_widget, on_complete)
    
    def _run_pty(self, cmd, output_widget, on_complete=None):
        """Run using PTY"""
        try:
            master_fd, slave_fd = pty.openpty()
            
            process = subprocess.Popen(
                cmd,
                shell=True,
                stdout=slave_fd,
                stderr=slave_fd,
                stdin=slave_fd,
                text=True,
                bufsize=0,
                preexec_fn=os.setsid if hasattr(os, 'setsid') else None
            )
            
            os.close(slave_fd)
            
            # Store for management
            proc_id = id(output_widget)
            self.processes[proc_id] = process
            self.outputs[proc_id] = output_widget
            self.master_fds[proc_id] = master_fd
            
            def read_output():
                try:
                    while process.poll() is None:
                        ready, _, _ = select.select([master_fd], [], [], 0.1)
                        if ready:
                            data = os.read(master_fd, 4096)
                            if data:
                                text = data.decode('utf-8', errors='replace')
                                output_widget.after(0, lambda t=text: self._write(output_widget, t))
                    
                    # Read remaining
                    try:
                        while True:
                            data = os.read(master_fd, 4096)
                            if not data: break
                            text = data.decode('utf-8', errors='replace')
                            output_widget.after(0, lambda t=text: self._write(output_widget, t))
                    except:
                        pass
                    
                    os.close(master_fd)
                    
                    if on_complete:
                        output_widget.after(0, lambda: on_complete(process.returncode))
                    
                    # Cleanup
                    self.processes.pop(proc_id, None)
                    self.outputs.pop(proc_id, None)
                    self.master_fds.pop(proc_id, None)
                    
                except Exception as e:
                    if on_complete:
                        output_widget.after(0, lambda: on_complete(-1))
            
            threading.Thread(target=read_output, daemon=True).start()
            return process
            
        except Exception as e:
            # Fallback to subprocess
            return self._run_fallback(cmd, output_widget, on_complete)
    
    def _run_fallback(self, cmd, output_widget, on_complete=None):
        """Fallback using subprocess pipe"""
        process = subprocess.Popen(
            cmd, shell=True,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, bufsize=1
        )
        
        def read():
            for line in iter(process.stdout.readline, ''):
                output_widget.after(0, lambda l=line: output_widget.insert('end', l))
                output_widget.after(0, lambda: output_widget.see('end'))
            process.wait()
            if on_complete:
                output_widget.after(0, lambda: on_complete(process.returncode))
        
        threading.Thread(target=read, daemon=True).start()
        return process
    
    def _write(self, widget, text):
        """Write text to widget with ANSI handling"""
        # Strip ANSI codes for non-terminal outputs
        clean = ''
        i = 0
        while i < len(text):
            if text[i] == '\x1b' and i+1 < len(text) and text[i+1] == '[':
                end = text.find('m', i)
                if end > i:
                    i = end + 1
                else:
                    clean += text[i]
                    i += 1
            elif text[i] == '\r':
                i += 1  # Skip carriage returns
            else:
                clean += text[i]
                i += 1
        
        if clean:
            widget.insert('end', clean)
            widget.see('end')
            widget.update_idletasks()
    
    def kill_all(self):
        """Kill all running processes"""
        for proc_id, process in list(self.processes.items()):
            try:
                os.killpg(os.getpgid(process.pid), signal.SIGKILL)
            except:
                process.kill()
        self.processes.clear()
        self.outputs.clear()
        for fd in self.master_fds.values():
            try: os.close(fd)
            except: pass
        self.master_fds.clear()


# Global instance shared by all modules
shared_pty = PTYHandler()
