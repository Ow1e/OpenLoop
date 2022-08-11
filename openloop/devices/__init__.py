"""
Web API View for OpenLoop Web
"""

from flask import Blueprint, render_template, request, redirect, url_for
from openloop.time import convert_zones
from openloop.crossweb import *
from openloop.devices.web import (
    view_groups,
    prompt
)

class API_Handler:
    def __init__(self, shared) -> None:
        self._shared = shared
        self.web = Blueprint("api", __name__)
        flow = shared.flow["pages"]["devices"]

        web = self.web

        self.device_groups = shared.database.db["groups"]
        self.devices = shared.database.db["devices"]
        self.instances = shared.database.db["instances"]

        flow["groups"] = self.group_list

        @web.route("/")
        @shared.vault.login_required
        def group_view():
            return render_template("blank.jinja", methods=shared.methods, html = view_groups(), title="Device Groups")

        @web.route("/group/<group>/delete", methods=["GET", "POST"])
        @shared.vault.login_required
        def delete_group(group):
            if request.method == "GET":
                return render_template("blank.jinja", methods=shared.methods, html = prompt(), title="Device Groups")
            else:
                myuser = shared.vault.current_user()
                if myuser['admin']==True:
                    self.device_groups.delete_one({"name": group})
                return redirect(url_for(".group_view"))

        @web.route("/group/<group>")
        @shared.vault.login_required
        def device_view(group : str):
            query = self.device_groups.find_one({"name": group})
            if query!=None:
                p = Page()
                p.append(Heading(query['name'], 0))
                fullrow = Row()
                # Devices

                c = Card("Devices", 6)
                c.append("For storing data in the database, serialized. Every sensor has its own key for easy data. Remember to label!")

                table = Table()

                head = Table_Header()
                row = Table_Row()
                row.append(Table_Cell("Name"))
                row.append(Table_Cell("Secret"))
                row.append(Table_Cell("Archive"))
                head.append(row)
                table.append(head)

                body = Table_Body()
                for i in self.devices.find({"group": query["_id"]}):
                    row = Table_Row()
                    row.append(Table_Cell(i["name"]))
                    row.append(Table_Cell(i["secret"]))
                    row.append(Table_Cell("None"))
                    body.append(row)
                table.append(body)
                c.append(table)

                fullrow.append(c)

                # Instances

                c = Card("Instances", 6)
                c.append("For everything OpenLoop & OpenLite and other OpenLoop Core nodes. Remember to label!")

                table = Table()

                head = Table_Header()
                row = Table_Row()
                row.append(Table_Cell("Name"))
                row.append(Table_Cell("Last Ping"))
                row.append(Table_Cell("Archive"))
                head.append(row)
                table.append(head)

                body = Table_Body()
                for i in self.instances.find({"group": query["_id"]}):
                    row = Table_Row()
                    row.append(Table_Cell(i["name"]))
                    row.append(Table_Cell(convert_zones(i["ping"])))
                    row.append(Table_Cell("None"))
                    body.append(row)
                table.append(body)
                c.append(table)

                fullrow.append(c)

                c = Card("About", 6)
                c.append("OpenLoop V5 uses a identity system, that can label nodes and create networks as well as group sensors / devices for advanced queries.")
                fullrow.append(c)

                c = Card("Integrate", 6)
                c.append("For setting up a OpenLite / OpenLoop node, use")
                c.append(Code(f"OPENLOOP_GROUP='{query['name']}'\nOPENLOOP='My Instance Name'"))
                fullrow.append(c)

                p.append(fullrow)

                return render_template("blank.jinja", methods=shared.methods, html = p.export(), title=query['name'])
            return "nerd"


    def group_list(self):
        void = ""
        for i in self.device_groups.find({}):
            row = Table_Row()

            devices = len(list(self.devices.find({"group": i["_id"]})))
            instances = len(list(self.instances.find({"group": i["_id"]})))

            row.append(Table_Cell(i["name"]))
            row.append(Table_Cell(devices))
            row.append(Table_Cell(instances))
            buttons = Void()
            buttons.append(Button("success", icon="fas fa-eye", text="View", href="/api/group/"+i['name']))
            if devices == 0 and instances == 0:
                buttons.append(Button("danger", icon="fas fa-trash-alt", text="Delete", href=f"/api/group/{i['name']}/delete", push=10))
            row.append(Table_Cell(buttons))

            void += row.export()
        
        return void