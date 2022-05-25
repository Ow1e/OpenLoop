from flask import Blueprint, request
from openloop import lite_api
from flask_httpauth import HTTPBasicAuth

class Lite_API:
    def __init__(self, shared) -> None:
        self.web = Blueprint("lite", __name__)
        web = self.web
        self.orders = {}
        self.auth = HTTPBasicAuth()
        database_on = shared.database.working
        devices_db = shared.database.db["devices"]

        @self.auth.verify_password
        def verify_password(username, password):
            if database_on:
                account = devices_db.find_one({"name": username})
                if account != None and account["key"] == password and account["lite"] == True:
                    return account

        config = (shared.config)

        @web.route("/login")
        @self.auth.login_required
        def register():
            return {
                "version": lite_api,
                "login": True,
                "config": {
                    "mongo": dict(config["MongoDB"])
                }
            }