"""
OpenLoop built-in routes/render functions
"""

from openloop.crossweb import Element, Page, Heading, Card
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

routes = {
    "about": about
}