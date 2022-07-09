from time import sleep
import logging
from openloop.plugins import CoreThread
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
        self.live_worker = CoreThread(target=self.worker)
        self.live_worker.start()

    def check(self):
        try:
            self.info = self.client.server_info()
            return True
        except:
            self.info = {}
            logging.critical("MongoDB cannot connect")
            return False

    def worker(self):
        while True:
            sleep(10)
            self.working = self.check()