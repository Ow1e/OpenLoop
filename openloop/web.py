from flask import Blueprint, render_template, url_for, send_from_directory, redirect
from openloop.page import index as serv_index
from openloop.page import about as serv_about
from openloop.page import plugins as serv_plugins
from openloop.page import set_pl_redirects
import os

MANIFEST = {
    "name": "OpenLoop",
    "short_name": "OpenLoop",
    "description": "Open Source IoT software.",
    "id": "/",
    "theme_color": "#4e73df",
    "background_color": "#4e73df",
    "start_url": ".",
    "display": "standalone",
    "icons": [
        {
            "src": "/static/img/OpenLoop512.png",
            "sizes": "512x512",
            "type": "image/png"
        }
    ]
}

class Web_Handler:
    def __init__(self, shared) -> None:
        web = Blueprint("web", __name__)
        self.web = web
        methods = shared.methods
        self.shared = shared
        set_pl_redirects(shared.plugins.enviroments, shared.flow)
        
        # WEB MANIFEST PWA
        @web.route("/manifest.webmanifest")
        def manifest():
            return MANIFEST

        @web.route("/sw.js")
        def service_worker():
            return send_from_directory(shared.app.static_folder, 'sw.js')

        def navbar(): # Navbars are requested seperately so they are not cached
            return render_template("nav_plugins.jinja", methods=methods)
        shared.flow["defaults"]["navbar"] = navbar

        @web.route("/")
        def index():
            return render_template("blank.jinja", methods=methods, html = serv_index(), title= "Dashboard", active=True)
        
        @web.route("/about")
        def about():
            return render_template("blank.jinja", methods=methods, html = serv_about(), title= "About" )

        @web.route("/client")
        def offline():
            return render_template("debug.jinja")

        @web.route("/plugins")
        def list_plugins():
            return render_template("blank.jinja", methods=methods, html = serv_plugins(shared.plugins.enviroments), title="Plugins")

        @web.route("/plugin/<name>")
        def view_plugin_index(name):
            plugin = self.get_plugin(name)
            if plugin:
                if "index" in plugin.pages:
                    return render_template("blank.jinja", methods=methods, html = plugin.pages["index"](), title=plugin.name)    
                else:
                    return render_template("404.jinja", methods=methods, code=404, text=f"{name} has no index page")
            else:
                return render_template("404.jinja", methods=methods, code=404, text=f"{name} is not a plugin")

        @web.route("/plugin/<name>/<page>")
        def view_plugin_age(name, page):
            plugin = self.get_plugin(name)
            if plugin:
                if page == "index":
                    return redirect(url_for(".view_plugin_index", name=name))
                elif page in plugin.pages:
                    return render_template("blank.jinja", methods=methods, html = plugin.pages[page](), title=f"{page} | {plugin.name}")    
                else:
                    return render_template("404.jinja", methods=methods, code=404, text=f"{name} has no {page} page")
            else:
                return render_template("404.jinja", methods=methods, code=404, text=f"{name} is not a plugin")


    def get_plugin(self, name : str):
        chosen = None
        for i in self.shared.plugins.enviroments:
            if str(i.name).lower() == name.lower():
                chosen = i
                break
        return chosen