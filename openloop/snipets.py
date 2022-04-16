alert = """
<a class="dropdown-item d-flex align-items-center" href="{}">
    <div class="me-3">
        <div class="bg-{} icon-circle"><i class="{} text-white"></i></div>
    </div>
    <div><span class="small text-gray-500">{}</span>
        <p>{}</p>
    </div>
</a>
"""

class Alert(str):
    def __init__(self, link, color, icon, date, contents) -> None:
        """Turns variables to formated text, represented as a string and a class"""
        self.link, self.color, self.icon, self.date, self.contents = link, color, icon, date, contents
        super().__init__()
        self.join(alert.format())

    def export(self):
        """Returns tuple of variables in order"""
        return (self.link, self.color, self.icon, self.date, self.contents)