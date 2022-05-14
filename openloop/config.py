import os
from configparser import ConfigParser

def check():
    config = ConfigParser()

    if not os.path.exists("config.ini"):
        config["Settings"] = {
            "mongodb": "mongodb+srv://<username>:<password>@<cluster-address>/test?retryWrites=true&w=majority"
        }
        with open("config.ini", "w") as f:
            config.write(f)

    config.read("config.ini")
    return config

if __name__=="__main__":
    # This is for debug, nothing much
    x = check()
    print(dict(x["Settings"]))