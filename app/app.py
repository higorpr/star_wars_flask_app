from flask import Flask
from .database import db
from app.controllers.movieController import movieBlueprint
from app.controllers.planetController import planetBlueprint


def create_app(config_object="app.settings"):
    app = Flask(__name__)
    app.config.from_object(config_object)
    db.init_app(app)
    app.register_blueprint(movieBlueprint)
    app.register_blueprint(planetBlueprint)

    return app
