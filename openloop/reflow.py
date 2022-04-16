from types import BuiltinFunctionType
from flask import Blueprint, jsonify
from datetime import datetime

class ReFlow(dict):
    def __init__(self):
        super().__init__()
        self["defaults"] = {
            "time": datetime.now
        }

class ReFlow_Serve:
    def __init__(self, reflow : dict) -> None:
        api = Blueprint("reflow", __name__)
        self.web = api

        @api.route("/")
        def information():
            return {
                "version": "ReFlow Protocol Version 1.0"
            }

        @api.route("/refresh/<element>")
        def update_item(element : str):
            path = element.split(".")

            current = reflow
            for i in path:
                if i in current:
                    current = current[i]
                else:
                    current = {}

            if current == {}:
                current = None
            elif type(current) == BuiltinFunctionType:
                current = str(current())

            return {
                "item": element,
                "value": current
            }