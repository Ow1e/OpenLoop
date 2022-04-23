from pydoc import render_doc
from flask import Blueprint, render_template
from openloop.page import routes

class Web_Handler:
    def __init__(self, shared) -> None:
        web = Blueprint("web", __name__)
        self.web = web
        
        shared.flow["pages"]["builtin"] = routes

        @web.route("/")
        def index():
            return render_template("index.jinja")
        
        @web.route("/<page>/")
        def render_page(page):
            if page in routes:
                page = str(page)
                return render_template("flow.jinja", flow=f"pages.builtin.{page}", title = page.title(), flow_enabled = True)
            else:
                return render_template("404.jinja", code=404, text="That page does not exist!")