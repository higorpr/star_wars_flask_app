from flask import Blueprint, jsonify, request

movieBlueprint = Blueprint("film", __name__, url_prefix="/movies")


# insert new movie (C)
@movieBlueprint.route("/", methods=["POST"])
def create_movie():
    data = request.get_json()
