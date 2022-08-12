from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, redirect, render_template, request, url_for
from openloop.crossweb import *
from time import sleep
from flask_login import LoginManager, login_required, login_user, login_url, current_user
import os

from openloop.plugins import CoreThread

INCASE_HASH = os.environ.get("OPENLOOP_EMERGENCY", "")

class User:
    def __init__(self, username) -> None:
        self.is_authenticated = True
        self.is_active = True
        self.is_anonymous = False
        self.user_id = username
    
    def get_id(self):
        return self.user_id

class Auth_Handler:
    def __init__(self, shared) -> None:
        self.web = Blueprint("auth", __name__)
        web = self.web
        methods = shared.methods
        database = shared.database.db["users"]

        self._cache = {}

        """
        Auth Handler does not use Flow or any other functionality for security
        """
        
        class Authenticator(LoginManager):
            def __init__(self, app=None, add_context_processor=True):
                super().__init__(app, add_context_processor)

            def login_required(self, *args, **kwargs):
                return login_required(*args, **kwargs)

            def current_user(self):
                user = current_user
                return database.find_one({"username": user.user_id})

        self.auth = Authenticator(shared.app)
        auth = self.auth
        login_url("/login")

        @auth.user_loader
        def load_user(user_id):
            if database.find_one({"username": user_id}):
                return User(user_id)

        @web.route("/handle", methods=["POST"])
        def handle_login():
            username = request.form.get("username")
            password = request.form.get("password")
            if database.find_one({"admin": True}) == None:
                package = {
                    "username": username,
                    "fullname": "Administrator",
                    "admin": True,
                    "password": generate_password_hash(password)
                }
                database.insert_one(package)
            uid = database.find_one({"username": username})
            if uid != None:
                check = check_password_hash(uid["password"], password)
                if check == True:
                    login_user(User(uid["username"]))
                    return redirect("/")
            return redirect(url_for("web.login"))

        @auth.unauthorized_handler
        def redirect_login():
            return redirect(url_for("web.login"))

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
            
            if shared.database.working:
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
            if shared.database.working:
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
            if shared.database.working:
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