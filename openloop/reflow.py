from types import BuiltinFunctionType, FunctionType, MethodType
from flask import Blueprint, jsonify
from datetime import datetime

def comp_time():
    time = datetime.now().time()
    return f"{time.hour}:{time.minute}:{time.second}"

class ReFlow(dict):
    def __init__(self):
        super().__init__()
        self["defaults"] = {
            "time": datetime.now,
            "timec": comp_time
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
            elif type(current) == MethodType:
                current = str(current())
            elif type(current) == FunctionType:
                current = str(current())

            return {
                "item": element,
                "value": current
            }