from flask import Blueprint, render_template, url_for, send_from_directory
from openloop.page import index as serv_index
from openloop.page import about as serv_about
from openloop.page import plugins as serv_plugins
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
        
        # WEB MANIFEST PWA
        @web.route("/manifest.webmanifest")
        def manifest():
            return MANIFEST

        @web.route("/sw.js")
        def service_worker():
            return send_from_directory(shared.app.static_folder, 'sw.js')

        @web.route("/")
        def index():
            return render_template("blank.jinja", html = serv_index(), title= "Dashboard", active=True)
        
        @web.route("/about")
        def about():
            return render_template("blank.jinja", html = serv_about(), title= "About" )

        @web.route("/client")
        def offline():
            return render_template("debug.jinja")

        @web.route("/plugins")
        def list_plugins():
            return render_template("blank.jinja", html = serv_plugins(shared.plugins.enviroments))
