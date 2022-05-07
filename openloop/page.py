"""
OpenLoop built-in routes/render functions
"""

from openloop.crossweb import *
import openloop as openloop

def about():
    p = Page()
    p.append(Heading("About", 0))
    c = Card("Version", 7)
    title = Heading("OpenLoop")
    title.add_flow("defaults.version", 5000)
    c.append(title)
    c.append("Made with Flask")
    p.append(c)

    c = Card("Credits", 5)
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

def plugins(plugin_list):
    p = Page()
    p.append(Heading("Plugins", 0))
    c = Card("Plugin List", 12)
    table = Table()

    header = Table_Header()
    body = Table_Body()

    header_row = Table_Row()
    header_row.append(Table_Cell("Plugin Name"))
    header_row.append(Table_Cell("Plugin Location"))
    header.append(header_row)

    for i in plugin_list:
        row = Table_Row()
        row.append(Table_Cell(i.name))
        row.append(Table_Cell(i.path))
        body.append(row)
    
    table.append(header)
    table.append(body)
    if len(body) > 9:
        table.append(header)

    c.append("Note that on Plugin Startup plugin metadata is changed.")
    c.append(table)
    c.append("<b>This chart does not auto update</b>")
    p.append(c)
    
    return p.export()

