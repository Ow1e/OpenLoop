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
    body = Table_Body()

    for i in plugin_list:
        row = Table_Row()
        row.append(Table_Cell(i.name))
        row.append(Table_Cell(i.path))
        btn_cell = Table_Cell()
        btn_cell.append(Button(text="Enter Page", flow="void", href=f"/plugin/{i.name}", icon="fas fa-sitemap"))
        row.append(btn_cell)
        body.append(row)

    return body.export()

def plugins_view():
    p = Page()
    p.append(Heading("Plugins", 0))
    c = Card("Plugins Online", 7)
    table = Table()
    header = Table_Header()
    body = Table_Body()

    header_row = Table_Row()
    header_row.append(Table_Cell("Plugin Name"))
    header_row.append(Table_Cell("Plugin Location"))
    header_row.append(Table_Cell("Plugin Page"))
    header.append(header_row)

    body.add_flow("pages.plugins.mylist")

    table.append(body)
    table.append(header)

    c.append("Plugin metadata updates every time a OpenLoop Core instance is restarted or a manual restart occurs")
    c.append(table)
    c.append(Button(icon="fas fa-redo", color="danger", flow="pages.plugins.restart", text="Restart Plugins"))
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

def welcome_page():
    p = Page()
    p.append(Heading("OpenLoop Wizzard", 0))
    c = Card("Register Account", 6)

    form = HTML_Form("/auth/handle") # Goes to auth.py to manage
    
    username = Form_Element()
    username.append(Label("Username"))
    username.append(Input("username", required=True))

    password = Form_Element()
    password.append(Label("Password"))
    password.append(Input("password", required=True))

    form.append(username)
    form.append(password)
    form.append(Form_Button("Register"))

    c.append(form)
    p.append(c)

    c = Card("Welcome", 6)
    c.append("Welcome to OpenLoop, a experimental ecosystem made for large scale automation. No matter your application, size and purpose, OpenLoop aims to deliver your needs. Any feedback and contribution is welcomed!\n\n- The Cyclone Team\n")
    c.append(Image("/static/img/CycloneWhite.png", 70))

    p.append(c)

    p.append(f"""<code>
Core Verion {openloop.comb_code}
OpenLoop {openloop.num}-{openloop.code}
{openloop.cache_gitver}

Making the world a better place.
</code>""")

    return p.export()

def login_nomongo():
    p = Page()
    p.append(Heading("MongoDB is offline", 3))
    p.append(Text("OpenLoop is disabled until a conection is reached", traditional=True))
    return p.export()