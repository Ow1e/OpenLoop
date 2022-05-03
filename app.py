from flask import Flask, render_template
import logging

logging.info("Starting OpenLoop")

app = Flask(__name__)

from openloop.loader import load_data

load_data(app)

if __name__=="__main__":
    logging.warning("This is not running on a production WSGI server, for non development use gunicorn or another WSGI server.")
    app.run()