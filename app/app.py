from flask import Flask
from app.database import db
from app.controllers.movieController import movieBlueprint
from app.controllers.planetController import planetBlueprint
from dotenv import load_dotenv

load_dotenv()

def create_app(config_object="app.settings"):
    app = Flask(__name__)
    app.config.from_object(config_object)
    db.init_app(app)
    app.register_blueprint(movieBlueprint)
    app.register_blueprint(planetBlueprint)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
