"""
OpenLoop built-in routes/render functions
"""

from openloop.crossweb import *
import openloop as openloop

def about():
    p = Page()
    p.append(Heading("About", 0))
    c = Card("Version", 6)
    title = Heading("OpenLoop")
    title.add_flow("defaults.version", 5000)
    c.append(title)
    c.append("Made with Flask")
    p.append(c)
    return p.export()

def index():
    p = Page()
    p.append(Heading("Dashboard", 0))
    row = Row()
    for i, color in enumerate(["primary", "success", "danger", "warning"]):
        row.append(Feature("SHEESH", color=color, inner=i+1))
    p.append(row)
    return p.export()

routes = {
    "about": about,
    "index": index
}