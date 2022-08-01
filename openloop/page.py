"""
OpenLoop built-in routes/render functions
"""

from openloop.crossweb import *
import openloop as openloop
import os

def about():
    p = Page()
    p.append(Heading("About", 0))

    row = Row()

    c = Card("Version", 5)
    title = Heading("OpenLoop")
    title.add_flow("defaults.version", 10000)
    c.append(title)
    c.append("Made with Flask")
    row.append(c)

    c = Card("Badges", 7)

    mongo = Link("https://www.mongodb.com")
    mongo.append(Image("/static/img/Mongo.png", 50))

    flask = Link("https://flask.palletsprojects.com")
    flask.append(Image("/static/img/Flask.png", 60))

    pwa = Link("https://web.dev/progressive-web-apps/")
    pwa.append(Image("/static/img/pwa.svg", 60))

    cyclone = Link("https://cyclone.biz")
    cyclone.append(Image("/static/img/CycloneWhite.png", 60))

    c.append(mongo)
    c.append(flask)
    c.append(pwa)
    c.append(cyclone)
    row.append(c)

    c = Card("Updates", 6)
    c.append(Text("By default, OpenLoop does not autoupdate but all versions of OpenLoop are generally compatable.", traditional=True))
    version = Code()
    version.add_flow("version", False)
    c.append(version)
    c.append("To update on a Linux system, SSH into the system and run a direct git pull from where OpenLoop is located. Then restart the OpenLoop service with systemd.")
    row.append(c)
    
    c = Card("Credits", 6)
    c.append(Code("""People who worked on and helped out with OpenLoop:
- Owen Shaule   (Lead Designer)
- Evan Taylor   (Project Manager)
- Minh Nyugen   (Help with Flow Defaults)
- Anthony Libby (Bug Tester)"""))
    c.append("Thanks to any other people helping and supporting this passion project.")
    row.append(c)
    p.append(row)

    return p.export()

def index():
    p = Page()
    p.append(Integrate("dash")) # Links to dash.py via flow
    return p.export()

def set_pl_redirects(plugin_list, flow):
    flow["redirects"]["plugins"] = {}
    for i in plugin_list:
        flow["redirects"]["plugins"][i.name] = f"/plugin/{i.name}"
            
def plugins(plugin_list):
    table = Table()

    header = Table_Header()
    body = Table_Body()

    header_row = Table_Row()
    header_row.append(Table_Cell("Plugin Name"))
    header_row.append(Table_Cell("Plugin Location"))
    header_row.append(Table_Cell("Plugin Page"))
    header.append(header_row)

    for i in plugin_list:
        row = Table_Row()
        row.append(Table_Cell(i.name))
        row.append(Table_Cell(i.path))
        btn_cell = Table_Cell()
        btn_cell.append(Button(text="Enter Page", flow="void", href=f"/plugin/{i.name}", icon="fas fa-sitemap"))
        row.append(btn_cell)
        body.append(row)

    table.append(header)
    table.append(body)
    if len(body) > 9:
        table.append(header)
    
    return table.export()

def plugins_view():
    p = Page()
    c = Card("Plugins", 7)
    chart = Div()
    chart.add_flow("pages.builtin.plugins")
    c.append("Plugin metadata updates every time a OpenLoop Core instance is restarted or a manual restart occurs")
    c.append(chart)
    c.append(Button(icon="fas fa-redo", color="danger", flow="void", text="Restart Plugins", href="/plugins/restart"))
    p.append(c)

    c = Card("Plugin API", 5)
    c.append(Text("See documentation "))
    c.append(Link("https://docs.cyclone.biz", "here"))
    p.append(c)
    return p.export()

def login_page():
    p = Page()
    p.append(Heading("OpenLoop Dashboard", 0))
    c = Card("Login Prompt", 6)

    form = HTML_Form("/auth/handle") # Goes to auth.py to manage
    
    username = Form_Element()
    username.append(Label("Username"))
    username.append(Input("username"))

    password = Form_Element()
    password.append(Label("Password"))
    password.append(Input("password", "password"))

    form.append(username)
    form.append(password)
    form.append(Form_Button("Login"))

    c.append(form)
    p.append(c)
    return p.export()
