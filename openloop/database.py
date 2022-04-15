from flask_sqlalchemy import SQLAlchemy

class Database:
    def __init__(self, shared) -> None:
        settings = dict(shared.config["Settings"])
        shared.app.config["SQLALCHEMY_DATABASE_URI"] = settings.get("sqlalchemy_uri", "sqlite:///database.db")
        shared.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
        self.db = SQLAlchemy(shared.app)