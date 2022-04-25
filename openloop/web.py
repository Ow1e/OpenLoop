from flask import Blueprint, render_template
from openloop.page import routes

class Web_Handler:
    def __init__(self, shared) -> None:
        web = Blueprint("web", __name__)
        self.web = web
        
        @web.route("/")
        def index():
            return render_template("blank.jinja")
        
        @web.route("/about")
        def about():
            return render_template("blank.jinja", html = routes["about"]())
