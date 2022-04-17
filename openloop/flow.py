from types import BuiltinFunctionType, FunctionType, MethodType
from flask import Blueprint, jsonify
from datetime import datetime
import psutil

def comp_time():
    time = datetime.now().time()
    return f"{time.hour}:{time.minute}:{time.second}"

global cpu_hist
cpu_hist = []
def cpu_str():
    val = psutil.cpu_percent()
    if val == 0 or val == 100:
        val = cpu_hist[len(cpu_hist)-1]
    else:
        cpu_hist.append(val)
    return str(val)+"%"

class Flow(dict):
    def __init__(self):
        super().__init__()
        self["defaults"] = {
            "time": datetime.now,
            "timec": comp_time,
            "cpu": cpu_str
        }

class Flow_Serve:
    def __init__(self, reflow : dict) -> None:
        api = Blueprint("flow", __name__)
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
                current = current()

            return {
                "item": element,
                "value": current
            }