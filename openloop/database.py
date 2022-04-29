from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from dateutil import tz
from werkzeug.security import generate_password_hash, check_password_hash

def div_exponent(inter, div):
    running = True
    current = 0
    while running:
        current += div
        if current >= inter:
            running = False
            return (int((current-div)/div), inter-(current-div))
    
def convert_zones(datetype : datetime):
    rel = datetype
    now = datetime.utcnow()
    change = now-rel
    ans = ""
    
    minutes, seconds = div_exponent(change.seconds, 60)
    hours, none = div_exponent(minutes, 60)
    if minutes > 1 and hours == 0:
        return f"{minutes} minutes ago."
    elif minutes < 1 and hours == 0:
        return f"{seconds} seconds ago."
    elif hours >= 1:
        return f"{hours} hour ago."
    else:
        return f"{hours} hour ago."

class Database:
    def __init__(self, shared) -> None:
        settings = dict(shared.config["Settings"])
        shared.app.config["SQLALCHEMY_DATABASE_URI"] = settings.get("sqlalchemy_uri", "sqlite:///database.db")
        shared.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
        self.db = SQLAlchemy(shared.app)
        self.models = self
        db = self.db

        class Users(db.Model):
            id = db.Column(db.Integer, primary_key=True)
            email = db.Column(db.String(120), index=True, unique=True)
            name = db.Column(db.String(128), nullable = False)
            password_hash = db.Column(db.String(128), nullable = False)

            # Thx https://dev.to/kaelscion/authentication-hashing-in-sqlalchemy-1bem

            def set_password(self, password):
                self.password_hash = generate_password_hash(password)

            def check_password(self, password):
                return check_password_hash(self.password_hash, password)

        class Alert(db.Model):
            id = db.Column(db.Integer, primary_key=True)
            link = db.Column(db.String(128), nullable = False, default="#")
            color = db.Column(db.String(32), nullable = False, default="primary")
            icon = db.Column(db.String(32), nullable = False, default="fas fa-box-open")
            date = db.Column(db.DateTime, nullable = False, default=datetime.utcnow)
            contents = db.Column(db.Text, nullable = False, default="Text here")

            def __repr__(self) -> str:
                return f"{self.id}: {self.color}, {self.icon}, {self.date} --> {self.link}"

            def export(self, html : str):
                return html.format(self.link, self.color, self.icon, convert_zones(self.date), self.contents)

        self.Alert = Alert
        self.Users = Users
