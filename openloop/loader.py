from openloop.alerts import AlertManager
from openloop.config import check as configCheck
from openloop.database import Database
from openloop.web import Web_Handler
from openloop.reflow import ReFlow, ReFlow_Serve
from openloop.plugins import Deployer

def load_data(app):
    """
    Applys blueprints and loads everything in one central class
    """
    class SharePoint:
        def __init__(self) -> None:
            self.app = app
            self.config = configCheck()
            self.database = Database(self).db  

            self.reflow = ReFlow()
            app.register_blueprint(ReFlow_Serve(self.reflow).web, url_prefix="/reflow")

            self.alerts = AlertManager(self)

            self.plugins = Deployer()

            app.register_blueprint(Web_Handler().web)

    SharePoint()