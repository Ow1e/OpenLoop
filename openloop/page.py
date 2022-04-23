"""
OpenLoop built-in routes/render functions
"""

from openloop.crossweb import Element, Page, Heading, Card
import openloop as openloop

def index():
    page = Page()
    text = Heading("Dashboard", 0)
    print(text.export())
    page.append(text)
    return page.export()

def about():
    p = Page()
    p.append(Heading("About", 0))
    c = Card("Version", 6)
    c.append(Heading(f"{openloop.num}-{openloop.code}"))
    c.append("Made with Flask")
    p.append(c)
    return p.export()

routes = {
    "about": about,
    "index": index
}