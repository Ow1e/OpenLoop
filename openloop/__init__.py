from datetime import datetime

num = 0.5
code = "Kepler"
st_code = "1"
comb_code = str(num)+st_code
lite_api = "v1f"
bootup = datetime.utcnow()

ascii = """________                            .____                             
\_____  \  ______    ____    ____   |    |     ____    ____  ______   
 /   |   \ \____ \ _/ __ \  /    \  |    |    /  _ \  /  _ \ \____ \  
/    |    \|  |_> >\  ___/ |   |  \ |    |___(  <_> )(  <_> )|  |_> > 
\_______  /|   __/  \___  >|___|  / |_______ \\____/  \____/ |   __/  
        \/ |__|         \/      \/          \/               |__|     
To learn more about OpenLoop, check out the docs https://docs.cyclone.biz"""

print(f"OpenLoop Core {num*10}:{st_code}")

import subprocess
def git_ver():
    try:
        x = subprocess.Popen("git describe --tags", stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        x.wait()
        if x.stderr.read() == b"":
            return x.stdout.read().decode().removesuffix("\n")
        else:
            return "There was a error contacting git"
    except:
        return "There was a error calling the shell"

cache_gitver = git_ver()