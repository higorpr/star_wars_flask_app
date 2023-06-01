from flask import Blueprint, jsonify, request
from app.services.planetService import PlanetService
from app.services.errors import CustomException

planetBlueprint = Blueprint("planet", __name__, url_prefix="/planets")


@planetBlueprint.route("/", methods=["POST"])
def insertNewPlanet():
    data = request.get_json()
    print(data["test"])
    # name, climate, diameter, population, movies = request.get_json().values()
    planetService = PlanetService()

    try:
        # planetService.createPlanet()
        return jsonify({"message": "Debugging"}), 201
    except CustomException as e:
        return jsonify({"error": e.message}), e.statusCode
    except Exception as e:
        return jsonify({"error": str(e)}), 500
