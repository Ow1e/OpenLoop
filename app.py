from flask import Flask, render_template

app = Flask(__name__)

from openloop.loader import load_data

load_data(app)

if __name__=="__main__":
    app.run()