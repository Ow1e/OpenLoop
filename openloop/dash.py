# Dashboard API System

from openloop.crossweb import *
import os

class Dash_Manager:
    def __init__(self, shared) -> None:
        shared.flow["dash"] = self.generate
        self.customs = []
    
    def generate(self):
        p = Text()
        for i in self.customs:
            p.append(i())
        return p.export()

    def clear(self):
        self.customs = []