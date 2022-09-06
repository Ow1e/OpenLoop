"""
Manage alerts with db
"""

from datetime import datetime
from time import sleep

from openloop.time import convert_zones
from openloop.plugins import CoreThread

alert = """<a class="dropdown-item d-flex align-items-center" href="{}"><div class="me-3"><div class="bg-{} icon-circle"><i class="{} text-white"></i></div></div><div><span class="small text-gray-500">{}</span><p>{}</p></div></a>"""

def div_exponent(inter, div):
    running = True
    current = 0
    while running:
        current += div
        if current >= inter:
            running = False
            return (int((current-div)/div), inter-(current-div))

class AlertManager:
    """This is loaded by the loader, it has properties of a list but automatically sets a export function to ReFlow"""
    def __init__(self, shared):
        self.db = shared.database.db["alerts"]
        self._cache = ""
        self._length = 0
        shared.flow["alerts"] = {"inner": self.get, "length": self.get_len, "clear": self.clear}
        self.database_on = shared.database.working
        self.worker_thread = CoreThread(target=self.worker)
        self.worker_thread.start()
        #self.append(Alert("#", "primary", "fas fa-tachometer-alt", "Today", "Wow it updated!!!!"))

    def exp_html(self):
        contents = ""
        if self.database_on:
            try:
                for i in self.db.find():
                    contents += alert.format(i["link"], i["color"], i["icon"], convert_zones(i["date"]), i["text"])
            except:
                contents += alert.format("", "danger", i["icon"], "Right now", "Alerts error!")
        else:
            contents += alert.format("", "danger", i["icon"], "Right now", "MongoDB is not online!")
        return contents

    def worker(self):
        while True:
            sleep(1)
            if self.database_on:
                self._cache = self.exp_html()
                self._length = len(list(self.db.find()))

    def add(self, text, link = "#", color = "primary", icon = "fas fa-tachometer-alt", date = datetime.utcnow()):
        if self.database_on:
            pkg = {
                "text": text,
                "link": link,
                "color": color,
                "icon": icon,
                "date": date
            }
            self.db.insert_one(pkg)

    def get_len(self):
        x = self._length
        if x == 0:
            x = ""
        elif x > 9:
            x = "9+"
        return x

    def get(self):
        return self._cache

    def clear(self):
        self.db.delete_many({})