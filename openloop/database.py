from datetime import datetime
from dateutil import tz
import logging
from werkzeug.security import generate_password_hash, check_password_hash
import sys, pymongo

class Database:
    def __init__(self, shared) -> None:
        settings = dict(shared.config["MongoDB"])
        default = "mongodb://localhost:27017"
        try:
            client = pymongo.MongoClient(settings.get("uri"), serverSelectionTimeoutMS=5000)
        except:
            sys.exit("Invalid URI")

        self.client = client
        self.db = client[settings.get("name", "OpenLoop")]

        try:
            self.info = client.server_info()
            self.working = True
        except:
            self.info = {}
            self.working = False
            logging.error("MongoDB cannot connect")