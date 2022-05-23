# Dashboard API System

from crossweb import Element

class Dashboard(Element):
    def __init__(self):
        super().__init__()
        self.outer = "<div>{}</div>"

class Dash_Manager:
    def __init__(self) -> None:
        self.show_stats = True
        self.dash = Dashboard()
        