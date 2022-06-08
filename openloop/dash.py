# Dashboard API System

from openloop.crossweb import *
import os

class Dash_Manager:
    def __init__(self, shared) -> None:
        shared.flow["dash"] = self.generate
        self.vault = shared.vault
    
    def generate(self):
        dash = Row() # Theoretical, its really nothing
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
        c.append("Running on a self hosted device.")
        return c