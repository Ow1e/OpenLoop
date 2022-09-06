"""
Web API View for OpenLoop Web
"""

from flask import Blueprint, render_template, request, redirect, url_for
from openloop.time import convert_zones
import secrets
from openloop.crossweb import *
from openloop.devices.web import (
    create_api_prompt,
    create_group_prompt,
    prompt_name,
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
        working = shared.database.working
        self.working = working

        flow["groups"] = self.group_list

        def no_mongo():
            return render_template("404.jinja", code=403, text="MongoDB cannot connect")

        @web.route("/")
        @shared.vault.login_required
        def group_view():
            if working:
                return render_template("blank.jinja", methods=shared.methods, html = view_groups(), title="Device Groups")
            else:
                return no_mongo()

        @web.route("/group/<group>/delete", methods=["GET", "POST"])
        @shared.vault.login_required
        def delete_group(group):
            if request.method == "GET":
                return render_template("blank.jinja", methods=shared.methods, html = prompt(), title="Delete Group")
            else:
                if working:
                    myuser = shared.vault.current_user()
                    if myuser['admin']==True:
                        self.device_groups.delete_one({"name": group})
                return redirect(url_for(".group_view"))

        @web.route("/group/<group>/delete/<type>/<name>", methods=["GET", "POST"])
        @shared.vault.login_required
        def delete_group_in(group, type, name):
            if request.method == "GET":
                return render_template("blank.jinja", methods=shared.methods, html = prompt_name(name), title="Delete Items")
            else:
                if working:
                    myuser = shared.vault.current_user()
                    if myuser['admin']==True:
                        group = self.device_groups.find_one({"name": group})
                        if group!=None:
                            if type == "instance":
                                query = {"name": name, "group": group["_id"]}
                                obj = self.instances.find_one(query)
                                if obj!=None and obj["_id"]!=shared.database.identity["_id"]:
                                    self.instances.delete_one(query)
                            elif type == "device":
                                self.devices.delete_one({"name": name, "group": group["_id"]})
                    return redirect(url_for(".group_view"))

        @web.route("/create", methods=["GET", "POST"])
        @shared.vault.login_required
        def create_group():
            if request.method == "GET":
                return render_template("blank.jinja", methods=shared.methods, html = create_group_prompt(), title="Create Group")
            else:
                if working:
                    myuser = shared.vault.current_user()
                    name = request.form.get("name")

                    if myuser['admin']==True and name!=None and self.device_groups.find_one({"name": name})==None:
                        self.device_groups.insert_one({"name": name})
                return redirect(url_for(".group_view"))

        @web.route("/group/<group>/create", methods=["GET", "POST"])
        def create_device(group):
            if request.method == "GET":
                return render_template("blank.jinja", methods=shared.methods, html = create_api_prompt(), title="Create Device")
            else:
                if working:
                    myuser = shared.vault.current_user()

                    name = request.form.get("name")
                    store = request.form.get("store", "off") == "on"
                    endpoints = request.form.get("endpoints", "off") == "on"
                    plugins = request.form.get("plugins", "off") == "on"
                    apis = request.form.get("apis", "off") == "on"

                    group = self.device_groups.find_one({"name": group})

                    if group!=None and myuser["admin"]==True:
                            pkg = {
                                "name": name,
                                "store": store,
                                "endpoints": endpoints,
                                "plugins": plugins,
                                "apis": apis,
                                "group": group["_id"],
                                "secret": secrets.token_urlsafe(16)
                            }
                            self.devices.insert_one(pkg)

                return redirect(url_for(".group_view"))


        @web.route("/group/<group>")
        @shared.vault.login_required
        def device_view(group : str):
            if working:
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
                    row.append(Table_Cell("Options"))
                    head.append(row)
                    table.append(head)

                    body = Table_Body()
                    for i in self.devices.find({"group": query["_id"]}):
                        row = Table_Row()
                        row.append(Table_Cell(i["name"]))
                        row.append(Table_Cell(i["secret"]))
                        row.append(Table_Cell(Button("danger", icon="fas fa-trash-alt", text="Delete", href=f"/api/group/{query['name']}/delete/device/{i['name']}")))
                        body.append(row)
                    table.append(body)
                    c.append(table)
                    c.append(Button("success", "fas fa-plus", href=f"/api/group/{group}/create", text="Create"))

                    fullrow.append(c)

                    # Instances

                    c = Card("Instances", 6)
                    c.append("For everything OpenLoop & OpenLite and other OpenLoop Core nodes. Remember to label!")

                    table = Table()

                    head = Table_Header()
                    row = Table_Row()
                    row.append(Table_Cell("Name"))
                    row.append(Table_Cell("Last Ping"))
                    row.append(Table_Cell("Options"))
                    head.append(row)
                    table.append(head)

                    body = Table_Body()
                    for i in self.instances.find({"group": query["_id"]}):
                        row = Table_Row()
                        row.append(Table_Cell(i["name"]))
                        row.append(Table_Cell(convert_zones(i["ping"])))
                        if shared.database.identity["_id"] != i["_id"]:
                            row.append(Table_Cell(Button("danger", icon="fas fa-trash-alt", text="Delete", href=f"/api/group/{query['name']}/delete/instance/{i['name']}")))
                        else:
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
                return redirect("/api/")
            else:
                return no_mongo()


    def group_list(self):
        void = ""
        if self.working:
            for i in self.device_groups.find({}):
                row = Table_Row()

                devices = len(list(self.devices.find({"group": i["_id"]})))
                instances = len(list(self.instances.find({"group": i["_id"]})))

                row.append(Table_Cell(i["name"]))
                row.append(Table_Cell(devices))
                row.append(Table_Cell(instances))
                buttons = Void()
                buttons.append(Button(icon="fas fa-eye", text="View", href="/api/group/"+i['name']))
                if devices == 0 and instances == 0:
                    buttons.append(Button("danger", icon="fas fa-trash-alt", text="Delete", href=f"/api/group/{i['name']}/delete", push=10))
                row.append(Table_Cell(buttons))

                void += row.export()
        
        return void