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

def offline():
    p = Page()
    c = Card("Offline Mode", 6)
    h = Heading()
    h.append(Icon("fas fa-cloud fa-1x text-gray-300"))
    h.append("  OpenLoop is offline!")
    c.append(h)
    c.append("You are currently running under a PWA, but your internet is disconnected.")
    p.append(c)
    return p.export()

def index():
    p = Page()
    p.append(Heading("Dashboard", 0))
    row = Row()
    data = [
        {"title": "CPU USAGE", "flow": "defaults.cpu", "color": "primary", "icon": "fas fa-microchip"},
        {"title": "RAM USAGE", "flow": "defaults.ram_used", "color": "success", "icon": "fab fa-superpowers"},
        {"title": "CPU TEMPERATURE", "flow": "defaults.cpu_temp", "color": "danger", "icon": "fas fa-fire-alt"},
        {"title": "SERVER TIME", "flow": "defaults.timec", "color": "info", "icon": "fas fa-hourglass"},
    ]
    for i in data:
        fet = Feature(i["title"], color=i["color"], inner="", icon=i["icon"])
        fet.add_flow(i["flow"], 1000)
        row.append(fet)
    p.append(row)
    return p.export()

routes = {
    "about": about,
    "index": index,
    "offline": offline
}