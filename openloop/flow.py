from types import BuiltinFunctionType, FunctionType, MethodType
from flask import Blueprint, jsonify, escape, redirect, request, url_for
from openloop.defaults import package

class Flow(dict):
    def __init__(self):
        super().__init__()
        self["defaults"] = package
        self["redirects"] = {}
        self["pages"] = {
            "builtin": {}
        }
        self["plugins"] = {} # This is for plugins

class Flow_Serve:
    def __init__(self, flow : dict) -> None:
        api = Blueprint("flow", __name__)
        self.web = api

        @api.route("/")
        def information():
            return {
                "version": "Flow Protocol Version 2.0"
            }

        @api.route("/refresh/<element>", methods=["GET", "POST"])
        def update_item(element : str):
            path = element.split(".")

            current = flow
            for i in path:
                if i in current:
                    current = current[i]
                else:
                    current = {}

            if current == {}:
                current = None
            elif type(current) == BuiltinFunctionType:
                current = str(current())
            elif type(current) == MethodType:
                current = str(current())
            elif type(current) == FunctionType:
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