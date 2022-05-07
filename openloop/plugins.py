import os, sys
import logging
import openloop.crossweb as crossweb

def example():
    p = crossweb.Page()
    p.append(crossweb.Heading("My Plugin", 0))
    c = crossweb.Card("About", 6)
    c.append("This is a example of CrossWeb")
    p.append(c)

class Enviroment:
    def __init__(self, path, src, shared) -> None:
        self.shared = shared
        self.pages = {
            "index": example
        }

        env = {
            "io": self,
            "crossweb": crossweb
        }
        
        for i in dir(crossweb):
            if not i.startswith("_"):
                env[i] = getattr(crossweb, i)

        exec(compile(src, path, "exec"), env, {})

class Deployer:
    def __init__(self, shared) -> None:
        if not os.path.exists("plugins"): # Creates plugins folder if not done already
            os.mkdir("plugins")

        sources = {}
        self.enviroments = []

        logging.info("Reading Plugins")
        for i in os.listdir("plugins"): # Lists plugins and read them all, then sends them in a dict
            with open(i) as f:
                sources[i] = f.read()

        logging.info("Initializing Plugins")
        for i in sources:
            self.enviroments.append(Enviroment(i, sources[i], shared))