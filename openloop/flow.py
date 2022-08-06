from types import BuiltinFunctionType, FunctionType, MethodType
from flask import Blueprint, jsonify, escape, redirect, request, url_for, render_template
from openloop.defaults import package
from datetime import datetime
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
        self["version"] = openloop.git_ver()
        self.admin_only = [] # List of functions to blacklist, not paths to increase security. Introducing strings could lead toa vulneralbility.

class Flow_Serve:
    def __init__(self, shared) -> None:
        api = Blueprint("flow", __name__)
        self.web = api
        flow = shared.flow
        self.flow = flow

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
                "version": "Flow Protocol Version 2.2"
            }

        @api.route("/refresh/<element>", methods=["GET", "POST"])
        @shared.vault.login_required
        def update_item(element : str):
            start = datetime.now()

            return self.flow_find(element, True)

        @api.route("/package", methods=["GET"])
        @shared.vault.login_required
        def update_packages():
            start = datetime.now()
            package = {
                "data": {},
                "request": []
            }
            arguments = dict(request.args)

            for i in arguments:
                package["data"][i] = self.flow_find(i)
                package["request"].append(i)

            package["time"] = (datetime.now() - start).total_seconds()

            return jsonify(package)

        @api.route("/raw/<element>", methods=["GET"])
        @shared.vault.login_required
        def raw_request(element):
            d = self.flow_find(element)
            return d["value"]

    def flow_find(self, element, form_enabled = False):
        start = datetime.now()
        path = element.split(".")

        current = self.flow
        for i in path:
            if i in current:
                current = current[i]
            else:
                current = {}

        func = [BuiltinFunctionType, MethodType, FunctionType]
        if not current in self.flow.admin_only:
            if current == {}:
                current = None
            elif type(current) == dict:
                current = None
            elif type(current) in func:
                if request.method == "POST" and form_enabled:
                    current = current(request.form)
                    if request.form.get("formLocation")!=None:
                        return redirect(request.form.get("formLocation"))
                    else:
                        return redirect(url_for("web.index"))
                else:
                    current = current()

            if current == None:
                current = "null"

            return {"value": current}
        else:
            return {"value": None, "error": "Admin Only Object!"}