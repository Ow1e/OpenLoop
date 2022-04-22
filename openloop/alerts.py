alert = """<a class="dropdown-item d-flex align-items-center" href="{}"><div class="me-3"><div class="bg-{} icon-circle"><i class="{} text-white"></i></div></div><div><span class="small text-gray-500">{}</span><p>{}</p></div></a>"""

class Alert:
    def __init__(self, link, color, icon, date, contents) -> None:
        """Turns variables to formated text, represented as a string and a class"""
        self.link, self.color, self.icon, self.date, self.contents = link, color, icon, date, contents
        self.str_val = alert.format(link, color, icon, date, contents)

    def export(self):
        """Returns tuple of variables in order"""
        return (self.link, self.color, self.icon, self.date, self.contents)

class AlertManager(list):
    """This is loaded by the loader, it has properties of a list but automatically sets a export function to ReFlow"""
    def __init__(self, shared):
        super().__init__()
        shared.flow["alerts"] = {"inner": self.exp_html, "length": self.exp_len, "clear": self.clear}
        #self.append(Alert("#", "primary", "fas fa-tachometer-alt", "Today", "Wow it updated!!!!"))

    def exp_html(self):
        p = ""
        for i in self:
            p += i.str_val
        return p

    def exp_len(self):
        x = len(self)
        if x == 0:
            x = ""
        elif x > 9:
            x = "9+"
        return x

    def clear(self):
        super().__init__()