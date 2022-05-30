# Dashboard API System

from openloop.crossweb import *
import os

class Dash_Manager:
    def __init__(self, shared) -> None:
        shared.flow["dash"] = self.generate
        self.vault = shared.vault
    
    def generate(self):
        dash = Row()
        dash.append(self.create_welcome())
        dash.append(self.create_system())
        return dash.export()
        
    def create_welcome(self):
        user = self.vault.current_user()
        c = Card("Welcome Message", 5)
        c.append(Heading("Welcome to OpenLoop", 3))
        t = Text(f"You are signed in as user <b>{user['username']}</b>.")
        c.append(t)
        return c

    def create_system(self):
        c = Card("System Information", 7)
        c.append(Heading("System Information", 3))
        if os.getenv("I_AM_HEROKU"):
            c.append(Text("<b>Running on Heroku Web Server</b>", color="primary"))
        elif os.getenv("CYCLONE_MANUFACTURE"):
            c.append(Text("<b>Running on a supported device from Cyclone</b>", color="info"))
        elif os.getenv("OPENLOOP_MANUFACTURE"):
            c.append(Text("<b>Running on a 3rd party supported device</b>", color="warning"))
        else:
            c.append(Text("<b>Running on a self hosted device</b>", color="danger"))
        return c