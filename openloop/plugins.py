import os, sys
import logging
import secrets
import sched
import time
import requests
import openloop.crossweb as crossweb

class Enviroment:
    def __init__(self, path, src, shared, memory) -> None:
        self.name = path.split(".")[0]
        self.path = path
        self.hidden = False
        
        self.secret = secrets.token_urlsafe(16) # This is so other plugins cannot edit/transmit to others

        shared.flow["plugins"][self.secret] = {}
        self.flow = shared.flow["plugins"][self.secret]
        self.flow_path = f"plugins.{self.secret}"
        
        self.pages = {
            "index": self.crossweb_example
        }

        env = {
            "plugin": self,
            "crossweb": crossweb,
            "requests": requests,
            "flow": self.flow,
            "server": True,
            "shared": memory
        }
        
        for i in dir(crossweb):
            if not i.startswith("_"):
                env[i] = getattr(crossweb, i)
        try:
            exec(compile(src, path, "exec"), env, {})
        except Exception as e:
            logging.error("A error occured in {}".format(self.name), exc_info=e)

    def crossweb_example(self):
        p = crossweb.Page()
        p.append(crossweb.Heading(self.name, 0))
        c = crossweb.Card("About", 6)
        c.append("This is a default page, a developer can turn this place into their own dashboard!")
        p.append(c)
        return p.export()

    def create_loop(self):
        # Thanks to https://stackoverflow.com/questions/474528/what-is-the-best-way-to-repeatedly-execute-a-function-every-x-seconds
        return sched.scheduler(time.time, time.sleep)

class Deployer:
    def __init__(self, shared) -> None:
        if not os.path.exists("plugins"): # Creates plugins folder if not done already
            os.mkdir("plugins")

        plugins = {} # Plugin Sources
        dealers = {} # Plugin Extentions
        self.dealer = {} # For memory share between different plugins
        self.enviroments = []

        logging.info("Reading Plugins")
        for i in os.listdir("plugins"): # Lists plugins and read them all, then sends them in a dict
            with open(f"plugins/{i}") as f:
                if i.endswith(".pyr"):
                    dealers[i] = f.read()
                else:
                    plugins[i] = f.read()

        logging.info("Initializing Dealers/Plugins")
        for i in dealers:
            self.enviroments.append(Enviroment(i, dealers[i], shared, self.dealer))
        for i in plugins:
            self.enviroments.append(Enviroment(i, plugins[i], shared, self.dealer))