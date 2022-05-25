"""
Includes backend api and CrossWeb code
"""

from openloop.crossweb import *
from flask import Blueprint, render_template, request
from openloop.names import generate
from flask_httpauth import HTTPBasicAuth
import secrets
import datetime


def api_render():
    p = Page()
    p.append(Heading("Programming Interface", 0))
    keys = Card("API Keys", 7)
    keys.add_flow("api.api_keys", 10000)
    p.append(keys)

    form_card = Card("Active Feeds", 5)

    form = Form("api.keys_submit")
    form.append(Heading("Register Feed", 2))
    row = Row()
    form_elem = Form_Element()
    form_elem.append(Label("Label Name"))
    form_elem.append(Input("name", placeholder="My Sensor"))
    row.append(form_elem)
    form.append(row)
    form.append(Form_Check("Enable OpenLite on device", "lite", False))
    form.append(Form_Button("Register"))
    form_card.append(form)

    form = Form("api.keys_delete")
    form.append(Heading("Delete Feed", 2))
    row = Row()
    form_elem = Form_Element()
    form_elem.append(Label("IoT ID"))
    form_elem.append(Input("id", placeholder="Elements Flower"))
    form_elem.append(Form_Button("Delete", "danger"))
    row.append(form_elem)
    form.append(row)
    form_card.append(form)

    p.append(form_card)
    return p.export()


class API_Handler:
    def __init__(self, shared):
        api = Blueprint("api", __name__)
        self.shared = shared
        self.api = api
        devices_db = shared.database.db["devices"]
        stream_db = shared.database.db["streams"]
        database_on = shared.database.working
        api_auth = HTTPBasicAuth()
        self.api_auth = api_auth

        @api_auth.verify_password
        def verify_password(username, password):
            if database_on:
                account = devices_db.find_one({"name": username})
                if account != None and account["key"] == password:
                    return account

        @api.route("/stream", methods=["POST"])
        @api_auth.login_required
        def stream():
            device = api_auth.current_user()
            data = request.form
            package = {
                "device": device["_id"],
                "time": datetime.datetime.utcnow()
            }
            for i in data:
                package[i] = data[i]
            stream_db.insert_one(package)
            return {"status": "complete"}

        shared.flow["api"] = {
            "api_keys": self.api_keys,
            "keys_submit": self.keys_submit,
            "keys_delete": self.keys_delete
        }

        @api.route("/")
        @shared.vault.login_required
        def api():
            return render_template("blank.jinja", methods=shared.methods, html=api_render(), title="API")

    def api_keys(self):
        if self.shared.database.working:
            devices = self.shared.database.db["devices"]
            table = Table()
            head = Table_Header()
            head_row = Table_Row()

            head_row.append(Table_Cell("IoT ID"))
            head_row.append(Table_Cell("IoT Key"))
            head_row.append(Table_Cell("Label"))
            head_row.append(Table_Cell("OpenLite"))

            head.append(head_row)
            table.append(head)

            body = Table_Body()

            for device in devices.find():
                row = Table_Row()
                row.append(Table_Cell(device['name']))
                row.append(Table_Cell(device['key']))
                row.append(Table_Cell(device['label']))
                if device["lite"] == True:
                    row.append(Table_Cell("Enabled"))
                else:
                    row.append(Table_Cell("Disabled"))
                body.append(row)

            table.append(body)

            return table.export()
        else:
            p = Div()
            p.append(Heading("MongoDB 423", 2))
            p.append("MongoDB is not connected, reboot and try again?")
            return p.export()

    def keys_submit(self, args):
        if self.shared.database.working:
            devices = self.shared.database.db["devices"]

            checking = True
            while checking:
                uuid = generate()
                query = devices.find_one({"uuid": uuid})
                if query == None or len(query) == 0:

                    lite = args.get("lite", False)
                    if lite == "on":
                        lite = True

                    device = {
                        "label": args.get("name", ""),
                        "name": uuid,
                        "key": secrets.token_urlsafe(16),
                        "status": None,
                        "lite": lite
                    }
                    checking = False
                    devices.insert_one(device)

    def keys_delete(self, args):
        if self.shared.database.working:
            print("Delete")
            devices = self.shared.database.db["devices"]
            devices.delete_one({"name": args.get("id")})
