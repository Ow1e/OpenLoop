from time import sleep
import logging
from openloop.plugins import CoreThread
from datetime import datetime
import sys, pymongo

class Database:
    def __init__(self, shared) -> None:
        settings = dict(shared.config["MongoDB"])
        default = "mongodb://localhost:27017"
        try:
            client = pymongo.MongoClient(settings.get("uri", default), serverSelectionTimeoutMS=5000)
        except:
            sys.exit("Invalid URI")

        self.client = client
        self.db = client[settings.get("name", "OpenLoop")]
        self.working = self.check()

        if self.working:
            identity = shared.config["Identity"]

            group = self.db["groups"].find_one({"name": identity["group"]})
            if group == None:
                group = self.db["groups"].insert_one({"name": identity["group"]})
                group = group.inserted_id
            else:
                group = group["_id"]

            self.myquery = query = {"name": identity["name"], "group": group}
            res = self.db["instances"].find_one(query)
            if res == None:
                self.db["instances"].insert_one({"name": identity["name"], "group": group, "ping": datetime.utcnow()})
                res = self.db["instances"].find_one(query)

            self.identity = res

        self.live_worker = CoreThread(target=self.worker)
        self.live_worker.start()

    def check(self, thread = False):
        try:
            self.info = self.client.server_info()

            if thread:
                self.db["instances"].update_one(self.myquery, {"$set": {"ping": datetime.utcnow()}})
            return True
        except:
            self.info = {}
            logging.critical("MongoDB cannot connect")
            return False

    def worker(self):
        while True:
            sleep(10)
            self.working = self.check(True)