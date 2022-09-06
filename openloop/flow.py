from types import BuiltinFunctionType, FunctionType, MethodType
from flask import Blueprint, jsonify, escape, redirect, request, url_for, render_template
from openloop.defaults import package
from datetime import datetime
import openloop
import openloop.crossweb

def flow_transit(current, forms = False):
    func = [BuiltinFunctionType, MethodType, FunctionType]
    if current == {}:
        current = None
    elif type(current) == dict:
        current = None
    elif type(current) in func:
        if forms and request.method == "POST":
            current = current(request.form)
            return render_template("reload.html")
        else:
            current = current()

    if current == None:
        current = "null"

    return {"value": current}

class Flow(dict):
    def __init__(self):
        super().__init__()
        self["defaults"] = package
        self["redirects"] = {}
        self["pages"] = {
            "builtin": {},
            "devices": {},
            "plugins": {}
        }
        self["plugins"] = {} # This is for plugins
        self["void"] = None
        self["version"] = openloop.git_ver()
        self.admin_only = [] # List of functions to blacklist, not paths to increase security. Introducing strings could lead to a vulneralbility.
        self.flow_transit = flow_transit

class Flow_Serve:
    def __init__(self, shared) -> None:
        api = Blueprint("flow", __name__)
        self.web = api
        flow = shared.flow
        self.auth = shared.auth
        self.flow = flow
        self.flow_transit = flow_transit

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

        if not element in self.flow.admin_only:
            return self.flow_transit(current, form_enabled)
        else:
            user = self.auth.auth.current_user()
            if user['admin']:
                pack = self.flow_transit(current, form_enabled)
                pack['authed'] = True
                return pack
            return {"value": None, "error": "Admin Only Object!", "user": user["username"]}