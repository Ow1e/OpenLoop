from datetime import datetime

num = 0.3
code = "Discovery"
st_code = "4"
comb_code = str(num)+st_code
lite_api = "v1f"
bootup = datetime.now()

print(f"OpenLoop Core {num*10}:{st_code}")

import subprocess
def git_ver():
    try:
        x = subprocess.Popen(["git", "describe", "--tags"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        x.wait()
        if x.stderr.read() == b"":
            return x.stdout.read().decode().removesuffix("\n")
        else:
            return "There was a error contacting git"
    except:
        return "There was a error calling the shell"