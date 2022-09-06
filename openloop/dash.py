# Dashboard API System

from openloop.crossweb import *
import os

class Dash_Manager:
    def __init__(self, shared) -> None:
        shared.flow["dash"] = self.generate
        self.customs = []
        self.template()
    
    def template(self):
        self.customs.append(Heading("Dashboard", 0))
        data = [
            {"title": "CPU USAGE", "flow": "defaults.cpu", "color": "primary", "icon": "fas fa-microchip", "bar": True},
            {"title": "RAM USAGE", "flow": "defaults.ram_used", "color": "success", "icon": "fab fa-superpowers", "bar": True},
            {"title": "CPU TEMPERATURE", "flow": "defaults.cpu_temp", "color": "warning", "icon": "fas fa-fire-alt"},
            {"title": "SERVER TIME", "flow": "defaults.timec", "color": "info", "icon": "fas fa-hourglass"},
        ]
        for i in data:
            fet = Feature(i["title"], color=i["color"], inner="", icon=i["icon"], bar=("bar" in i))
            if "bar" in i:
                fet.add_flow(i["flow"], 1000, type="width")
            else:
                fet.add_flow(i["flow"])
            self.customs.append(fet)

    def generate(self):
        export = ""
        for i in self.customs:
            if type(i) == int or type(i) == str:
                export += str(i).replace("\n", "<br>")
            else:
                if "export" in dir(i):
                    export += i.export()
                else:
                    call = i()
                    if "export" in dir(call):
                        call = call.export()
                    export += call
        return export

    def clear(self):
        self.customs = []
        self.template()