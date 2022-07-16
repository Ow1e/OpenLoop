# Dashboard API System

from openloop.crossweb import *
import os

class Dash_Manager:
    def __init__(self, shared) -> None:
        shared.flow["dash"] = self.generate
        self.customs = []
        self.template()
        print(self.customs)
    
    def template(self):
        data = [
            {"title": "CPU USAGE", "flow": "defaults.cpu", "color": "primary", "icon": "fas fa-microchip", "bar": True},
            {"title": "RAM USAGE", "flow": "defaults.ram_used", "color": "success", "icon": "fab fa-superpowers", "bar": True},
            {"title": "CPU TEMPERATURE", "flow": "defaults.cpu_temp", "color": "danger", "icon": "fas fa-fire-alt"},
            {"title": "SERVER TIME", "flow": "defaults.timec", "color": "info", "icon": "fas fa-hourglass"},
        ]
        for i in data:
            fet = Feature(i["title"], color=i["color"], inner="", icon=i["icon"], bar=("bar" in i))
            if "bar" in i:
                fet.add_flow(i["flow"], 1000, type="width")
            else:
                fet.add_flow(i["flow"])
            self.customs.append(fet.export)

    def generate(self):
        p = Text()
        for i in self.customs:
            p.append(i())
        return p.export()

    def clear(self):
        self.customs = []
        self.template()