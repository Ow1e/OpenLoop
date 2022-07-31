from app import app

# This just has a cool banner, nothing else really

front = """\u001b[34m________                            \u001b[36m.____                             
\u001b[34m\_____  \  ______    ____    ____   \u001b[36m|    |     ____    ____  ______   
\u001b[34m /   |   \ \____ \ _/ __ \  /    \  \u001b[36m|    |    /  _ \  /  _ \ \____ \  
\u001b[34m/    |    \|  |_> >\  ___/ |   |  \ \u001b[36m|    |___(  <_> )(  <_> )|  |_> > 
\u001b[34m\_______  /|   __/  \___  >|___|  / \u001b[36m|_______ \\____/  \____/ |   __/  
\u001b[34m        \/ |__|         \/      \/  \u001b[36m        \/               |__|     
\u001b[34;1mTo learn more about OpenLoop, check out the docs https://docs.cyclone.biz
"""

for i in front.splitlines():
    print("\u001b[0m", i, "\u001b[0m")