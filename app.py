from flask import Flask, render_template
from dotenv import load_dotenv
import logging

logging.info("Starting OpenLoop")
load_dotenv() # This is temportary, will change in openloop.config.check

app = Flask(__name__)

from openloop.loader import load_data

load_data(app)

if __name__=="__main__":
    logging.warning("This is not running on a production WSGI server, for non development use gunicorn or another WSGI server.")
    app.run("0.0.0.0")