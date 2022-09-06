"""
For uploading plugins and other stuff
"""

from flask import Blueprint, render_template

from openloop.page import plugins_view
from openloop.page import plugins as plugin_list

class Maintain_Handler:
    def __init__(self, shared) -> None:
        web = Blueprint("maintain", __name__)
        self.web = web
        methods = shared.methods

        shared.flow.admin_only.append("pages.plugins.restart")
        flow = shared.flow["pages"]["plugins"]

        @web.route("/")
        @shared.vault.login_required
        def list_plugins():
            return render_template("blank.jinja", methods=methods, html = plugins_view(), title="Plugins")

        def restart_plugins():
            shared.plugins.restart()
            shared.sapphire.destroy_filters()

        def myplugin_list():
            return plugin_list(shared.plugins.enviroments)

        flow["mylist"] = myplugin_list
        flow["restart"] = restart_plugins