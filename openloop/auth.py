from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, redirect, render_template, request, url_for
from openloop.crossweb import *
import secrets
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

                if username == "OpenLoop" and check_password_hash(INCASE_HASH, password) and len(list(database.find({"admin": True})))>0:
                    return {
                        "username": "mongo_setup",
                        "fullname": "OpenLoop Mongo Setup",
                        "admin": True,
                        "password": INCASE_HASH
                    }
            else:
                if username == "OpenLoop" and check_password_hash(INCASE_HASH, password):
                    return {
                        "username": "OpenLoop",
                        "fullname": "OpenLoop Emergency",
                        "admin": True,
                        "password": INCASE_HASH
                    }

        def get_user():
            user = auth.current_user()
            user.pop("_id")
            user.pop("password")
            user.pop("admin")
            return user

        def username():
            user = get_user()
            return user["username"]

        def fullname():
            user = get_user()
            return user["fullname"]

        shared.flow["auth"] = {
            "username": username,
            "fullname": fullname
        }

        @web.route("/")
        @auth.login_required
        def index_users():
            p = Page()
            p.append(Heading("Users", 0))
            c = Card("Users", 12)
            my_user = auth.current_user()

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

                    if my_user['admin'] == True and my_user!=i:
                        cell = Table_Cell()
                        cell.append(Button(text="Delete User", flow="void", href="/auth/del/"+i['username']))
                        
                        if i['password']==None:
                            cell.append("Password not set!")

                        row.append(cell)
                    else:
                        row.append(Table_Cell("No Methods"))
                    body.append(row)
            else:
                body.append(Heading("MongoDB not conencted!"))
                body.append("We are geussing you are using a emergency password")

            table.append(header)
            table.append(body)

            c.append(f"You are logged in as {my_user['fullname']} ({my_user['username']}).")
            c.append("<br><b>This page cannot be used offline, and does not autoupdate for security reasons.</b>")
            c.append(table)
            if my_user['admin']:
                c.append(Button(text="Register User", href="add", flow="void", icon="fas fa-user-plus"))
            p.append(c)
            return render_template("blank.jinja", methods = methods, html = p.export(), title = "Users")

        @web.route("/del/<username>")
        @auth.login_required
        def delete_user(username):
            if database_on:
                user = database.find_one({"username": username})
                my_user = auth.current_user()
                if user == None:
                    return render_template("404.jinja", methods=methods, code=404, text="User does not exist"), 501
                elif my_user['admin']==False:
                    return render_template("404.jinja", methods=methods, code=403, text="You are not a admin!"), 403
                elif user == auth.current_user():
                    return render_template("404.jinja", methods=methods, code=403, text="You cannot delete yourself!<br>Ask a friend?")
                else:
                    database.delete_one(user)
                    return redirect(url_for(".index_users"))
            else:
                return render_template("404.jinja", code=501, text="MongoDB is not configured"), 501

        @web.route("/add", methods=["GET", "POST"])
        @auth.login_required
        def add_user():
            my_user = auth.current_user()
            if database_on:
                if my_user['admin']==True:
                    if request.method == "GET":
                        p = Page()
                        head = Heading("Add User<br>", 0)
                        head.append(Button(icon="fas fa-backward", text="View Users", href="/auth/", flow="void"))
                        p.append(head)
                        c = Card("Add User", 6)

                        form = HTML_Form("")
                        row = Row()

                        name = Form_Element()
                        name.append(Label("Full Name"))
                        name.append(Input("name", placeholder="John Doe", required=True))
                        row.append(name)

                        username = Form_Element()
                        username.append(Label("Username"))
                        username.append(Input("username", placeholder="joe", required=True))
                        row.append(username)

                        form.append(row)

                        passw = Form_Element()
                        passw.append(Label("Password"))
                        passw.append(Input("password", type="password", required=True))
                        form.append(passw)

                        form.append(Form_Check("Admin access", "admin", False))
                        form.append(Text("Only enable admin for someone who needs it, admins can delete other admins.<br>"))
                        form.append(Form_Button(text="Create User"))
                        c.append(form)

                        p.append(c)
                        return render_template("blank.jinja", methods = methods, html = p.export(), title = "Add User")
                    else:
                        name = request.form.get("name")
                        username = request.form.get("username")
                        password = request.form.get("password")
                        admin = request.form.get("admin", False)
                        if admin == "on":
                            admin = True

                        package = {
                            "username": username,
                            "fullname": name,
                            "admin": admin,
                            "password": generate_password_hash(password)
                        }

                        database.insert_one(package)
                        return redirect(url_for(".index_users"))
                else:
                    return render_template("404.jinja", methods = methods, code=403, text="You are not a admin!"), 403
            else:
                return render_template("404.jinja", methods = methods, code=501, text="MongoDB is not configured"), 501