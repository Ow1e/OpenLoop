from openloop.crossweb import package as cross_pack
import os, sys

class Enviroment:
    def __init__(self, path, src, shared) -> None:
        self.shared = shared

        env = {
            "io": self
        }

        for i in cross_pack:
            env[i] = cross_pack[i]
        
        exec(compile(src, path, "exec"), env, {})

class Deployer:
    if not os.path.exists("plugins"): # Creates plugins folder if not done already
        os.mkdir("plugins")

    sources = {}

    for i in os.listdir("plugins"): # Lists plugins and read them all, then sends them in a dict
        with open(i) as f:
            sources[i] = f.read()