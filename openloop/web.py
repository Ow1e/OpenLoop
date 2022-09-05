from flask import Blueprint, render_template, url_for, send_from_directory, redirect, request
from openloop.page import index as serv_index, login_nomongo
from openloop.page import about as serv_about
from openloop.page import plugins as serv_flow_plugins
from openloop.page import plugins_view as serv_plugins
from openloop.page import login_page as serv_login
from openloop.page import welcome_page as serv_welcome

from flask_login import logout_user

MANIFEST = {
    "name": "OpenLoop",
    "short_name": "OpenLoop",
    "description": "Open Source IoT software.",
    "id": "/",
    "theme_color": "#4e73df",
    "background_color": "#4e73df",
    "start_url": "/",
    "display": "standalone",
    "icons": [
        {
            "src": "/static/img/OpenLoop512.png",
            "sizes": "512x512",
            "type": "image/png"
        }
    ]
}

def get_template():
    if "fullscreen" in request.args:
        return "fullscreen.jinja"
    else:
        return "blank.jinja"

class Web_Handler:
    def __init__(self, shared) -> None:
        web = Blueprint("web", __name__)
        self.web = web
        methods = shared.methods
        self.shared = shared
        
        # WEB MANIFEST PWA
        @web.route("/manifest.webmanifest")
        @shared.vault.login_required # So PWA does not fail on Login Screen, as it caches some pages
        def manifest():
            return MANIFEST

        @web.route("/sw.js")
        @shared.vault.login_required
        def service_worker():
            return send_from_directory(shared.app.static_folder, 'sw.js')

        def navbar(): # Navbars are requested seperately so they are not cached
            return render_template("nav_plugins.jinja", methods=methods)
        shared.flow["defaults"]["navbar"] = navbar

        @web.route("/")
        @shared.vault.login_required
        def index():
            return render_template(get_template(), methods=methods, html = serv_index(), title= "Dashboard", active=True)
        
        @web.route("/about")
        @shared.vault.login_required
        def about():
            return render_template(get_template(), methods=methods, html = serv_about(), title= "About" )

        @web.route("/client")
        @shared.vault.login_required
        def offline():
            return render_template("debug.jinja", methods=methods, title = "Client Debug")

        @web.route("/plugin/<name>")
        @shared.vault.login_required
        def view_plugin_index(name):
            plugin = self.get_plugin(name)
            if plugin:
                if "index" in plugin.pages:
                    return render_template(get_template(), methods=methods, html = plugin.pages["index"](), title=plugin.name)    
                else:
                    return render_template("404.jinja", methods=methods, code=404, text=f"{name} has no index page")
            else:
                return render_template("404.jinja", methods=methods, code=404, text=f"{name} is not a plugin")

        @web.route("/plugin/<name>/<page>")
        @shared.vault.login_required
        def view_plugin_age(name, page):
            plugin = self.get_plugin(name)
            if plugin:
                if page == "index":
                    return redirect(url_for(".view_plugin_index", name=name))
                elif page in plugin.pages:
                    return render_template(get_template(), methods=methods, html = plugin.pages[page](), title=f"{page} | {plugin.name}")    
                else:
                    return render_template("404.jinja", methods=methods, code=404, text=f"{name} has no {page} page")
            else:
                return render_template("404.jinja", methods=methods, code=404, text=f"{name} is not a plugin")

        @web.route("/login")
        def login():
            if shared.database.working:
                if shared.database.db["users"].find_one({"admin": True})==None:
                    return render_template("blank.jinja", methods=methods, html = serv_welcome(), title="Wizzard")
                return render_template("login.jinja", methods=methods)
            return render_template("login.jinja", methods=methods, html = login_nomongo(), title="Offline")

        @web.route("/reload")
        @shared.vault.login_required
        def reload():
            # This is for reauth (when someone forgets to have a secret or a password is changed)
            # DO NOT CACHE THIS (IT BREAKS EVERYTHING)
            return render_template("reload.html")

        @web.route("/logout")
        @shared.vault.login_required
        def logout():
            logout_user()
            return redirect(url_for(".login"))

    def get_plugin(self, name : str):
        chosen = None
        for i in self.shared.plugins.enviroments:
            if str(i.name).lower() == name.lower():
                chosen = i
                break
        return chosen

    def apply_errors(self, app):
        @app.errorhandler(500)
        @self._shared.vault.login_required
        def error_handl():
            return redirect("404.jinja", methods = self.shared.methods, code = 500, text="There was a unknown error, check the docs for debugging.")

        @app.errorhandler(404)
        @self._shared.vault.login_required
        def error_handl():
            return redirect("404.jinja", methods = self.shared.methods, code = 404, text="This path is not part of OpenLoop Web")