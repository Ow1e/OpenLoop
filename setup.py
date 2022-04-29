"""
Made by Cyclone
OpenLoop uses the open-source CC0 license.
"""

from openloop.database import Database
from openloop.config import check as configCheck
from configparser import ConfigParser
from flask import Flask


class Loader:
    def __init__(self) -> None:
        self.app = Flask(__name__)
        self.config = configCheck()
        self.database = Database(self)

def main():
    load = Loader()
    print("Loaded OpenLoop config module and database...")
    print("All updates require this script to be ran first to avoid SQL issues, in the future this will be automatic in the app loader")
    load.database.db.create_all()
    print("Created table(s)...")
    print("""
====================================================================================
   If you have a seperate database (SQL, Postgres, Oracle etc) go into config.ini
   and edit the sqlalchemy_uri, then rerun this script. 
====================================================================================
    """)

if __name__ == "__main__":
    main()