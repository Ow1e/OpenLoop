num = 0.3
code = "Medway"
st_code = "2"
comb_code = str(num)+st_code
lite_api = "v1"

print(f"OpenLoop Core {num*10}:{st_code}")

import subprocess
def git_ver():
    x = subprocess.Popen(["git", "describe", "--tags"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    x.wait()
    if x.stderr.read() == b"":
        return x.stdout.read().decode().removesuffix("\n")
    else:
        return "There was a error contacting git"
