from openloop.config import check as configCheck
from openloop.database import Database
from openloop.web import Web_Handler

def load_data(app):
    """
    Applys blueprints and loads everything in one central class
    """
    class SharePoint:
        def __init__(self) -> None:
            self.app = app
            self.config = configCheck()
            self.database = Database(self).db            
            app.register_blueprint(Web_Handler().web)

    SharePoint()