from flask import Blueprint, render_template, request
from openloop import lite_api
from flask_httpauth import HTTPBasicAuth
from openloop.crossweb import *

class Lite_API:
    def __init__(self, shared) -> None:
        self.web = Blueprint("lite", __name__)
        web = self.web
        self.orders = {}
        self.cameras = {}
        self.auth = HTTPBasicAuth()
        devices_db = shared.database.db["devices"]
        camera_db = shared.database.db["cameras"]

        @self.auth.verify_password
        def verify_password(username, password):
            if shared.database.working:
                account = devices_db.find_one({"name": username})
                if account != None and account["key"] == password and account["lite"] == True:
                    return account

        config = (shared.config)

        def devices_flow():
            if shared.database.working:
                devices = shared.database.db["devices"]
                table = Table()
                head = Table_Header()
                head_row = Table_Row()

                head_row.append(Table_Cell("IoT ID"))
                head_row.append(Table_Cell("Label"))

                head.append(head_row)
                table.append(head)

                body = Table_Body()

                for device in devices.find({"lite": True}):
                    row = Table_Row()
                    row.append(Table_Cell(device['name']))
                    row.append(Table_Cell(device['label']))
                    body.append(row)

                table.append(body)

                return table.export()
            else:
                p = Div()
                p.append(Heading("MongoDB 423", 2))
                p.append("MongoDB is not connected, reboot and try again?")
                return p.export()

        shared.flow["lite"] = {
            "devices": devices_flow
        }

        @web.route("/")
        @shared.vault.login_required
        def index():
            p = Page()
            p.append(Heading("OpenLite Device Control", 0))

            c = Card("About", 7)
            c.append("OpenLite devices use OpenLoop Core to make a more simple version of OpenLoop. OpenLite uses Sapphire to create proxies as well as hosting plugins.")
            p.append(c)

            c = Card("Registered Devices", 5)
            d = Div()
            d.add_flow("lite.devices", 10000)
            
            text = Text("For configurating, use the ")
            text.append(Link("/api/", "API Manager"))

            c.append(text)
            c.append(d)
            p.append(c)
            return render_template("blank.jinja", methods = shared.methods, html = p.export(), title="Lite")