import os

def check():
    config = {}
    config["MongoDB"] = {
        "uri": os.getenv("MONGODB_URI", "mongodb://localhost:27017"),
        "name": os.getenv("MONGODB_NAME", "OpenLoop"),
    }
    config["Customize"] = {
        "name": "OpenLoop",
        "theme": "primary"
    }
    config["Plugins"] = {
        "identity": "cloud"
    }

    return config

if __name__=="__main__":
    # This is for debug, nothing much
    x = check()
    print(dict(x["Settings"]))