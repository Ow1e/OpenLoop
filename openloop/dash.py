# Dashboard API System

from openloop.crossweb import *

class Dash_Manager:
    def __init__(self, shared) -> None:
        shared.flow["dash"] = self.generate
        self.vault = shared.vault
    
    def generate(self):
        dash = Row()
        dash.append(self.create_welcome())
        return dash.export()
        
    def create_welcome(self):
        user = self.vault.current_user()
        c = Card("Welcome Message", 5)
        c.append(Heading("Welcome to OpenLoop", 3))
        t = Text(f"You are signed in as user <b>{user['username']}</b>.")
        c.append(t)
        return c