from flask import Blueprint, render_template

class Web_Handler:
    def __init__(self) -> None:
        web = Blueprint("web", __name__)
        self.web = web

        @web.route("/")
        def index():
            return render_template("index.jinja")