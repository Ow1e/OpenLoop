import os
from configparser import ConfigParser
import os

def check():
    config = ConfigParser()

    if not os.path.exists("config.ini"):
        config["MongoDB"] = {
            "uri": "mongodb://localhost:27017",
            "name": "OpenLoop",
        }
        config["Customize"] = {
            "name": "OpenLoop",
            "theme": "primary"
        }
        config["Plugins"] = {
            "identity": "cloud"
        }
    
        with open("config.ini", "w") as f:
            config.write(f)

    config.read("config.ini")

    if os.environ.get("mongodb_uri")!=None:
        config["MongoDB"]["uri"] = os.environ.get("mongodb_uri")
    if os.environ.get("mongodb_name")!=None:
        config["MongoDB"]["name"] = os.environ.get("mongodb_name")

    if os.environ.get("customize_name")!=None:
        config["Customize"]["name"] = os.environ.get("customize_name")
    if os.environ.get("customize_theme")!=None:
        config["Customize"]["theme"] = os.environ.get("customize_theme")

    return config

if __name__=="__main__":
    # This is for debug, nothing much
    x = check()
    print(dict(x["Settings"]))