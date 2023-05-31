from flask import Flask
from .database import db


def create_app(config_object="app.settings"):
    app = Flask(__name__)
    app.config.from_object(config_object)
    db.init_app(app)

    return app
