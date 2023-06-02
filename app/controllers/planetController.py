from flask import Blueprint, jsonify, request
from app.services.planetService import PlanetService
from app.services.movieService import MovieService
from app.services.errors import CustomException
from app.models.schemas import updatePlanetValidator, createPlanetValidator

planetBlueprint = Blueprint("planet", __name__, url_prefix="/planets")


@planetBlueprint.route("/", methods=["GET", "POST"])
def insertNewPlanet():
    # Retrieve PlanetService class
    planetService = PlanetService()

    if request.method == "POST":
        movieService = MovieService()

        # Get request body
        data = request.get_json()

        # Validate request
        if not createPlanetValidator(data):
            return (
                jsonify(
                    {
                        "Error": "Please send valid fields for planet creation and at least the planet name"
                    }
                ),
                400,
            )

        # Unpack values
        name, climate, diameter, population, *rest = data.values()

        # Check if planet was created with movieIds and if these movies exist in database
        if "movieIds" in data:
            movieIds = data["movieIds"]
            inexistantIds = movieService.getInexistantMovieIds(movieIds)
            if inexistantIds != None:
                return (
                    jsonify(
                        f"Error: The following movie ids are not registered in the database: {inexistantIds}"
                    ),
                    404,
                )
        else:
            movieIds = []

        try:
            planetService.createPlanet(name, climate, diameter, population, movieIds)

            # Add the recently registered planetId to each entry in the movieIds list
            if len(movieIds) != 0:
                newPlanetId = planetService.getPlanetByName(name)["_id"]
                for movieId in movieIds:
                    movieService.updatePlanetList(movieId, newPlanetId)

            return jsonify({"message": "Planet Created"}), 201
        except CustomException as e:
            return jsonify({"Error": e.message}), e.statusCode
        except Exception as e:
            return jsonify({"Error": str(e)}), 500

    elif request.method == "GET":
        try:
            planets = planetService.getAllPlanets()

            for planetInfo in planets:
                planetInfo["_id"] = str(planetInfo["_id"])

            return jsonify(planets), 200
        except CustomException as e:
            return jsonify({"Error": e.message}), e.statusCode
        except Exception as e:
            return jsonify({"Error": str(e)}), 500


@planetBlueprint.route("/<planetId>", methods=["GET"])
def retrievePlanet(planetId):
    planetService = PlanetService()
    try:
        planet = planetService.getPlanetById(planetId)
        planet["_id"] = str(planet["_id"])
        return jsonify(planet), 200
    except CustomException as e:
        return jsonify({"Error": e.message}), e.statusCode
    except Exception as e:
        return jsonify({"Error": str(e)}), 500


@planetBlueprint.route("/<planetId>", methods=["PUT"])
def updatePlanet(planetId):
    planetService = PlanetService()
    movieService = MovieService()

    planetUpdates = request.get_json()

    try:
        # Check if planet was updated with movieIds and if these movies exist in database
        if "movieIds" in planetUpdates:
            movieIds = planetUpdates["movieIds"]
            inexistantIds = movieService.getInexistantMovieIds(movieIds)
            if inexistantIds != None:
                return (
                    jsonify(
                        f"Error: The following movie ids are not registered in the database: {inexistantIds}"
                    ),
                    404,
                )

        if not updatePlanetValidator(planetUpdates):
            return jsonify({"Error": "Please send valid fields for planet update"}), 400

        # Check if planet id exists
        planetService.getPlanetById(planetId)

        # update planet
        planetService.updatePlanetById(planetId, planetUpdates)
        targetPlanet = planetService.getPlanetById(planetId)

        return jsonify({"message": f"Planet {targetPlanet['name']} updated"}), 200
    except CustomException as e:
        return jsonify({"Error": e.message}), e.statusCode
    except Exception as e:
        return jsonify({"Error": str(e)}), 500


@planetBlueprint.route("/<planetId>", methods=["DELETE"])
def deletePlanet(planetId):
    planetService = PlanetService()
    movieService = MovieService()

    try:
        # Verify if planetId exists and removes planetId from movie entries
        planet = planetService.getPlanetById(planetId)

        moviesInIds = planet["movieIds"]
        print(moviesInIds)
        for movieId in moviesInIds:
            movieService.removePlanetIdFromList(movieId, planetId)

        # Perform deletion
        planetService.deletePlanetById(planetId)

        return jsonify({"message": f"Planet {planet['name']} deleted"}), 200
    except CustomException as e:
        return jsonify({"Error": e.message}), e.statusCode
    except Exception as e:
        return jsonify({"Error": str(e)}), 500
