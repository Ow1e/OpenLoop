from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from dateutil import tz
from werkzeug.security import generate_password_hash, check_password_hash
import sys, pymongo

def div_exponent(inter, div):
    running = True
    current = 0
    while running:
        current += div
        if current >= inter:
            running = False
            return (int((current-div)/div), inter-(current-div))
    
def convert_zones(datetype : datetime):
    rel = datetype
    now = datetime.utcnow()
    change = now-rel
    ans = ""
    
    minutes, seconds = div_exponent(change.seconds, 60)
    hours, none = div_exponent(minutes, 60)
    if minutes > 1 and hours == 0:
        return f"{minutes} minutes ago."
    elif minutes < 1 and hours == 0:
        return f"{seconds} seconds ago."
    else:
        return f"{hours} hour ago."

class Database:
    def __init__(self, shared) -> None:
        settings = dict(shared.config["MongoDB"])
        default = "mongodb+srv://<username>:<password>@<cluster-address>/test?retryWrites=true&w=majority"
        if settings.get("uri", default)==default:
            sys.exit("MongoDB is not configured!")
        else:
            try:
                client = pymongo.MongoClient(settings.get("uri"), serverSelectionTimeoutMS=5000)
            except:
                sys.exit("Invalid URI")

            try:
                self.info = client.server_info()
            except:
                sys.exit("Connection Error")

            self.client = client
            self.db = client[settings.get("name", "OpenLoop")]