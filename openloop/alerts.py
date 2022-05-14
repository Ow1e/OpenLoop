"""
Manage alerts with db
"""

from datetime import datetime

alert = """<a class="dropdown-item d-flex align-items-center" href="{}"><div class="me-3"><div class="bg-{} icon-circle"><i class="{} text-white"></i></div></div><div><span class="small text-gray-500">{}</span><p>{}</p></div></a>"""

class AlertManager:
    """This is loaded by the loader, it has properties of a list but automatically sets a export function to ReFlow"""
    def __init__(self, shared):
        shared.flow["alerts"] = {"inner": self.exp_html, "length": self.exp_len, "clear": self.clear}
        #self.append(Alert("#", "primary", "fas fa-tachometer-alt", "Today", "Wow it updated!!!!"))


    def exp_html(self):
        contents = ""
        for i in []:
            contents = i.export(alert)+contents
        return contents

    def exp_len(self):
        x = 0
        if x == 0:
            x = ""
        elif x > 9:
            x = "9+"
        return x

    def clear(self):
        pass