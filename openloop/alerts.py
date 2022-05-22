"""
Manage alerts with db
"""

from datetime import datetime

alert = """<a class="dropdown-item d-flex align-items-center" href="{}"><div class="me-3"><div class="bg-{} icon-circle"><i class="{} text-white"></i></div></div><div><span class="small text-gray-500">{}</span><p>{}</p></div></a>"""

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

    if minutes == 0 and hours == 0:
        return f"{seconds} seconds ago."
    elif minutes == 1 and hours == 0:
        return f"{minutes} minute ago."
    elif hours == 0:
        return f"{minutes} minutes ago."
    else:
        return f"{hours} hours ago."

class AlertManager:
    """This is loaded by the loader, it has properties of a list but automatically sets a export function to ReFlow"""
    def __init__(self, shared):
        self.db = shared.database.db["alerts"]
        shared.flow["alerts"] = {"inner": self.exp_html, "length": self.exp_len, "clear": self.clear}
        #self.append(Alert("#", "primary", "fas fa-tachometer-alt", "Today", "Wow it updated!!!!"))

    def exp_html(self):
        contents = ""
        for i in self.db.find():
            contents += alert.format(i["link"], i["color"], i["icon"], convert_zones(i["date"]), i["text"])
        return contents

    def add(self, text, link = "#", color = "primary", icon = "fas fa-tachometer-alt", date = datetime.utcnow()):
        pkg = {
            "text": text,
            "link": link,
            "color": color,
            "icon": icon,
            "date": date
        }
        self.db.insert_one(pkg)

    def exp_len(self):
        x = len(list(self.db.find()))
        if x == 0:
            x = ""
        elif x > 9:
            x = "9+"
        return x

    def clear(self):
        self.db.delete_many({})