from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

class Database:
    def __init__(self, shared) -> None:
        settings = dict(shared.config["Settings"])
        shared.app.config["SQLALCHEMY_DATABASE_URI"] = settings.get("sqlalchemy_uri", "sqlite:///database.db")
        shared.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
        self.db = SQLAlchemy(shared.app)
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

        self.Users = Users