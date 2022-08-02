from flask import Blueprint, render_template
from openloop.sapphire.node import Sapphire
from openloop.sapphire.package import packet, finalize
import os, logging
from openloop.crossweb import *

class Interactor:
    def __init__(self, node : Sapphire) -> None:
        self._node = node

    def add_filter(self, type, caller):
        if type in self._node.filters:
            self._node.filters[type].append(caller)
        else:
            self._node.filters[type] = [caller]

    def publish(self, type, data):
        self._node.send_pointer(type, data)
        return True

class Sapphire_Manager:
    def __init__(self, shared) -> None:
        web = Blueprint("sapphire", __name__)
        self._shared = shared
        self.web = web
        self.run_node()

        @web.route("/")
        @shared.vault.login_required
        def index():
            p = Page()
            p.append(Heading("Sapphire Viewer", 0))
            
            if self.node == None:
                c = Card("Sapphire Prompt", 6)
                c.append(Heading("Woops"))
                c.append(Text("Sapphire is not configurated in enviroment variables", color="primary"))
            else:
                c = Card("Connections", 6)
                for i in self.node.nodes_outbound+self.node.nodes_inbound:
                    text = f"{i.host}:{i.port} <-> {self.node.host}:{self.node.port}"
                    if i == self.node.pointer:
                        c.append(Text("(Inbound) "+text, color="primary"))
                    else:
                        c.append(Text("(Outbound) "+text, color="success"))

            p.append(c)
            
            return render_template("blank.jinja", methods=shared.methods, html = p.export(), title = "Sapphire")

    def auth(self, cridentials : tuple):
        if self._shared.database.working:
            devices = self._shared.database.db["devices"]
            username = cridentials[0]
            password = cridentials[1]
            query = devices.find_one({"name": username, "key": password})
            if query == None:
                return False
            else:
                return True

    def run_node(self):
        if os.getenv("SAPPHIRE_ENABLED", False):
            self.node = Sapphire("0.0.0.0", int(os.getenv("SAPPHIRE_PORT", 1519)), (os.getenv("SAPPHIRE_USERNAME", ""), os.getenv("SAPPHIRE_PASSWORD", "")), check=self.auth)
            logging.warning("Sapphire is experimental!")
            self.node.start()
            if os.getenv("SAPPHIRE_POINT", False)!=False:
                self.node.connect_with_node(os.getenv("SAPPHIRE_POINT"), int(os.getenv("SAPPHIRE_POINTPORT", 1519)), reconnect=True)
        else:
            self.node = None

    def destroy_filters(self):
        if self.node!=None:
            self.node.filters = {}