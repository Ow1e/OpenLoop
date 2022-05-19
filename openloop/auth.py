from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, render_template
from openloop.crossweb import *
import os

INCASE_HASH = os.environ.get("OPENLOOP_EMERGENCY")

class Auth_Handler:
    def __init__(self, shared) -> None:
        self.web = Blueprint("auth", __name__)
        web = self.web
        self.auth = HTTPBasicAuth()
        auth = self.auth
        methods = shared.methods
        database_on = shared.database.working
        database = shared.database.db["users"]

        """
        Auth Handler does not use Flow or any other functionality for security
        """
        
        @self.auth.verify_password
        def verify_password(username, password):
            if database_on:
                account = database.find_one({"username": username})
                if account != None and check_password_hash(account["password"], password):
                    return account
            else:
                if username == "OpenLoop" and check_password_hash(INCASE_HASH, password):
                    return {
                        "username": "OpenLoop",
                        "fullname": "OpenLoop Emergency",
                        "admin": True,
                        "password": INCASE_HASH
                    }

        @web.route("/")
        @auth.login_required
        def index_users():
            p = Page()
            p.append(Heading("Users", 0))
            c = Card("Users", 12)

            table = Table()
            header = Table_Header()
            body = Table_Body()

            row = Table_Row()
            row.append(Table_Cell("Name"))
            row.append(Table_Cell("Username"))
            row.append(Table_Cell("Admin Access"))
            row.append(Table_Cell("Methods"))
            header.append(row)
            
            if database_on:
                for i in database.find():
                    row = Table_Row()
                    row.append(Table_Cell(i['fullname']))
                    row.append(Table_Cell(i['username']))
                    if i['admin']:
                        row.append(Table_Cell("Enabled"))
                    else:
                        row.append(Table_Cell("Disabled"))
                    row.append(Table_Cell("No Methods"))
                    body.append(row)
            else:
                body.append(Heading("MongoDB not conencted!"))
                body.append("We are geussing you are using a emergency password")

            table.append(header)
            table.append(body)

            my_user = auth.current_user()
            c.append(f"You are logged in as {my_user['fullname']} ({my_user['username']}).")
            c.append("<br><b>This page cannot be used offline, and does not autoupdate for security reasons.</b>")
            c.append(table)
            p.append(c)
            return render_template("blank.jinja", methods = methods, html = p.export(), title = "Users")