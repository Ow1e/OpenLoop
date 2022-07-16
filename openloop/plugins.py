import os
import logging
import secrets
import requests
import datetime
from time import sleep
import ctypes
import openloop
from threading import Thread # Multiproccesing does not work, because of a issue with cpick
import threading
from datetime import datetime
import openloop.crossweb as crossweb

def convert_zones(datetype : datetime):
    rel = datetype
    now = datetime.utcnow()
    change = now-rel
    ans = ""
    
    days = change.days
    if days == 0:
        secs = change.total_seconds()
        if secs < 60: # Totals one minute
            return f"{int(secs)} second ago."
        elif secs < 3600: # Totals one hour
            return f"{int(secs/60)} minutes ago."
        elif int(secs/3600)==1:
            return "1 hour ago."
        else:
            return f"{int(secs/3600)} hours ago."
    elif days == 1:
        return "Yesterday"
    else:
        month = ["January", "Febuary", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"][rel.month]
        day = ["Monday", "Tuesday", "Wendsday", "Thursday", "Friday", "Saturday", "Sunday"][rel.weekday()]
        return f"{day}, {month} {rel.day} {rel.year}"

class CoreThread(Thread):
    """Thread for plugins with stop functionality"""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def get_id(self):
 
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id

    def stop(self, plugin = "Default"):
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
              ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
        logging.warning(f"The plugin thread was remotely turned off thread#{thread_id}/{plugin}")
    

class Enviroment:
    def __init__(self, path, src, shared, memory) -> None:
        self.name = path.split(".")[0]
        self.path = path
        self.hidden = False
        self.author = "Unknown"
        self.release = ""
        self.dash = shared.dash.customs
        self._threads = []
        self._devicedb = shared.database.db["devices"]
        self._streamdb = shared.database.db["streams"]

        if "Plugins" in shared.config:
            self.globalconfig = dict(shared.config["Plugins"])
        else:
            self.globalconfig = {"identity": "cloud", "_setup": False, "name": "No Name"}
        
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
            "server": (not "OpenLite" in shared.config),
            "shared": memory,
            "alerts": shared.alerts,
            "bootup": openloop.bootup,
            "convert_zones": convert_zones
        }
        
        for i in dir(crossweb):
            if not i.startswith("_"):
                env[i] = getattr(crossweb, i)
        try:
            exec(compile(src, path, "exec"), env, {})
        except Exception as e:
            shared.alerts.add(f"There was a error in {self.name}", "", "danger")
            logging.error("A error occured in {}".format(self.name), exc_info=e)

    def crossweb_example(self):
        p = crossweb.Page()
        p.append(crossweb.Heading(self.name, 0))
        c = crossweb.Card("About", 6)
        c.append("This is a default page, a developer can turn this place into their own dashboard!")
        p.append(c)
        return p.export()

    def build_thread(self, *args, **kwargs):
        thread = CoreThread(*args, **kwargs)
        self._threads.append(thread)
        return thread

    def stop_threads(self):
        for i in self._threads:
            i.stop(self.name)
            self._threads.remove(i)
            del i

    def sleep_agent(self, num):
        sleep(num)

    def stream(self, id, **kwargs):
        device = self._devicedb.find_one({"name": id})
        if device == None:
            return {"status": "incomplete", "reason": f"Could not find {id}"}
        else:
            package = {
                "device": device["_id"],
                "time": datetime.datetime.utcnow()
            }
            for i in kwargs:
                package[i] = kwargs[i]
            self._streamdb.insert_one(package)
            package["status"] = "complete"
            return package

    def get_stream(self, id):
        device = self._devicedb.find_one({"name": id})
        if device == None:
            return {"status": "incomplete", "reason": f"Could not find {id}"}
        else:
            return self._streamdb.find({"device": device["_id"]})


class Deployer:
    def __init__(self, shared) -> None:
        self._shared = shared
        self.deploy()
        
    def deploy(self) -> None:
        if not os.path.exists("plugins"): # Creates plugins folder if not done already
            os.mkdir("plugins")

        self._shared.dash.clear()

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

        logging.info("Reading Plugins from Mongo")
        if self._shared.database.working:
            for i in self._shared.database.db["plugins"].find():
                if i["filename"].endswith(".pyr"):
                    dealers["(MONGODB) "+i["filename"]] = i["contents"]
                else:
                    plugins["(MONGODB) "+i["filename"]] = i["contents"]
        else:
            logging.warning("OpenLoop Core could not load MongoDB plugins")

        logging.info("Initializing Dealers/Plugins")
        for i in dealers:
            self.enviroments.append(Enviroment(i, dealers[i], self._shared, self.dealer))
        for i in plugins:
            self.enviroments.append(Enviroment(i, plugins[i], self._shared, self.dealer))

    def shutdown(self):
        for i in self.enviroments:
            i.stop_threads()
            del i

        del self.enviroments
        del self.dealer

    def restart(self):
        logging.warning("Restarting OpenLoop plugins")
        self.shutdown()
        self.deploy()
        logging.warning("Restart of Plugins Complete")