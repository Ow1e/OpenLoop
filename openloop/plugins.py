import os, sys
import logging
import openloop.crossweb as crossweb

class Enviroment:
    def __init__(self, path, src, shared) -> None:
        self.shared = shared
        self.name = path.split(".")[0]
        self.path = path
        
        self.refresh = 5000
        self.pages = {
            "index": self.crossweb_example
        }

        env = {
            "plugin": self,
            "crossweb": crossweb
        }
        
        for i in dir(crossweb):
            if not i.startswith("_"):
                env[i] = getattr(crossweb, i)

        exec(compile(src, path, "exec"), env, {})

    def crossweb_example(self):
        p = crossweb.Page()
        p.append(crossweb.Heading(self.name, 0))
        c = crossweb.Card("About", 6)
        c.append("This is a default page, a developer can turn this place into their own dashboard!")
        p.append(c)
        return p.export()

class Deployer:
    def __init__(self, shared) -> None:
        if not os.path.exists("plugins"): # Creates plugins folder if not done already
            os.mkdir("plugins")

        sources = {}
        self.enviroments = []

        logging.info("Reading Plugins")
        for i in os.listdir("plugins"): # Lists plugins and read them all, then sends them in a dict
            with open(f"plugins/{i}") as f:
                sources[i] = f.read()
                globals()

        logging.info("Initializing Plugins")
        for i in sources:
            self.enviroments.append(Enviroment(i, sources[i], shared))