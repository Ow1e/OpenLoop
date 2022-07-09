from types import BuiltinFunctionType, FunctionType, MethodType
from flask import Blueprint, jsonify, escape, redirect, request, url_for, render_template
from openloop.defaults import package
import openloop
import openloop.crossweb

class Flow(dict):
    def __init__(self):
        super().__init__()
        self["defaults"] = package
        self["redirects"] = {}
        self["pages"] = {
            "builtin": {}
        }
        self["plugins"] = {} # This is for plugins
        self["void"] = None
        self["version"] = openloop.git_ver

class Flow_Serve:
    def __init__(self, shared) -> None:
        api = Blueprint("flow", __name__)
        self.web = api
        flow = shared.flow

        @api.errorhandler(500)
        def error(err):
            area = openloop.crossweb.Text(traditional=True)
            area.append(openloop.crossweb.Heading("500"))
            area.append("Restart OpenLoop and check Mongo :)")
            return render_template("fullscreen.jinja", html=area.export(), methods=shared.methods, title="Flow Error"), 500

        @api.route("/")
        @shared.vault.login_required
        def information():
            return {
                "version": "Flow Protocol Version 2.1"
            }

        @api.route("/refresh/<element>", methods=["GET", "POST"])
        @shared.vault.login_required
        def update_item(element : str):
            path = element.split(".")

            current = flow
            for i in path:
                if i in current:
                    current = current[i]
                else:
                    current = {}

            func = [BuiltinFunctionType, MethodType, FunctionType]

            if current == {}:
                current = None
            elif type(current) in func:
                if request.method == "POST":
                    current = current(request.form)
                    if request.form.get("formLocation")!=None:
                        return redirect(request.form.get("formLocation"))
                    else:
                        return redirect(url_for("web.index"))
                else:
                    current = current()

            if current == None:
                current = "null"

            return {
                "item": escape(element),
                "value": current
            }