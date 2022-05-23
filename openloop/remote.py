from flask import Blueprint, render_template
from time import sleep
from openloop.crossweb import *
import subprocess

class Manager:
    def __init__(self, args) -> None:
        self.set(args)

    def set(self, args):
        self.cli = subprocess.Popen(args, shell=True, stdin=subprocess.PIPE, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text = True)

    def comm(self, args):
        if self.cli.returncode == None:
            self.cli.communicate(args)
        else:
            self.set(args)

    def get(self):
        out, error = self.cli.communicate()
        if not error:
            return out.replace("\n", "<br>")
        else:
            return error

    def wait(self):
        self.cli.wait()

class Remote_Manager:
    def __init__(self, shared) -> None:
        self.man = Manager('echo hello!')
        self.web = Blueprint("remote", __name__)
        web = self.web
        methods = shared.methods

        def form(args):
            self.man.comm(args.get("command", 'echo "Please provide a input"'))

        shared.flow["remote"] = {
            "get": self.man.get,
            "form": form
        }

        @web.route("/")
        def index():
            p = Page()
            p.append(Heading("Remote Management Page (BETA)"))
            c = Card("Remote Window", 12)
            terminal = Code()
            terminal.add_flow("remote.get")
            c.append(terminal)
            c.append("This is not like SSH, and does not capture/transmit anything other thsn the input in the form. So its reccomended to use SSH instead.")

            form = Form("remote.form")
            
            input = Form_Element()
            input.append(Input("command", placeholder='echo Hello World!', required=True))
            form.append(input)

            c.append(form)

            p.append(c)
            return render_template("blank.jinja", methods = methods, html = p.export(), title = "Remote")