"""
Includes backend api and CrossWeb code
"""

from openloop.crossweb import *
from flask import Blueprint, render_template

def api_render():
    p = Page()
    p.append(Heading("Programming Interface", 0))
    keys = Card("API Keys", 7)
    keys.add_flow("api.api_keys")
    form = Card("Register Key", 5)
    p.append(keys)
    p.append(form)
    return p.export()

class API_Handler:
    def __init__(self, shared):
        api = Blueprint("api", __name__)
        self.api = api

        shared.flow["api"] = {"api_keys": self.api_keys}

        @api.route("/")
        def api():
            return render_template("blank.jinja", html = api_render(), title= "API" )

    def api_keys(self):
        table = Table()
        head = Table_Header()
        head_row = Table_Row()

        head_row.append(Table_Cell("IoT ID"))
        head_row.append(Table_Cell("IoT Key"))
        head_row.append(Table_Cell("Label"))

        head.append(head_row)
        table.append(head)

        body = Table_Body()
        row = Table_Row()

        row.append(Table_Cell("Gallium Feverfew"))
        row.append(Table_Cell("5BCCD1F11A"))
        row.append(Table_Cell("Soil Sensor"))

        body.append(row)
        table.append(body)
        

        return table.export()