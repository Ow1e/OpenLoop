from flask import Blueprint, render_template, url_for, send_from_directory
from openloop.page import routes
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
            return render_template("blank.jinja", html = routes["index"](), title= "Dashboard", active=True)
        
        @web.route("/about")
        def about():
            return render_template("blank.jinja", html = routes["about"](), title= "About" )

        @web.route("/client")
        def offline():
            return render_template("debug.jinja")
