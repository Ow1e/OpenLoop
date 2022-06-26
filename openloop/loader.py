from openloop.alerts import AlertManager
from openloop.auth import Auth_Handler
from openloop.config import check as configCheck
from openloop.database import Database
from openloop.web import Web_Handler
from openloop.flow import Flow, Flow_Serve
from openloop.plugins import Deployer
from openloop.api import API_Handler
from openloop.methods import Methods
from openloop.lite import Lite_API
from openloop.dash import Dash_Manager
import logging

def load_data(app, config = configCheck()):
    """
    Applys blueprints and loads everything in one central class
    """
    class SharePoint:
        def __init__(self) -> None:
            self.app = app

            self.config = config
            self.database = Database(self)

            self.flow = Flow() # Only used when in OpenLoop
            self.alerts = AlertManager(self)
            self.methods = Methods(self)
            self.dash = Dash_Manager(self)

            self.plugins = Deployer(self)

            if "lite" in config:
                self.auth = Auth_Handler(self)
                self.vault = self.auth.auth

                app.register_blueprint(self.auth.web, url_prefix="/auth")
                app.register_blueprint(Flow_Serve(self).web, url_prefix="/flow")
                app.register_blueprint(API_Handler(self).api, url_prefix="/api")
                app.register_blueprint(Lite_API(self).web, url_prefix="/lite")
                app.register_blueprint(Web_Handler(self).web)

            logging.info("Completed imports in Sharepoint")

    logging.info("Loading Sharepoint")
    share = SharePoint()
    logging.info("Completed Sharepoint")
    return share