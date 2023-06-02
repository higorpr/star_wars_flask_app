from flask import Blueprint, jsonify, request
from app.services.movieService import MovieService
from app.services.planetService import PlanetService
from app.models.schemas import createMovieValidator, updateMovieValidator
from app.services.errors import CustomException

movieBlueprint = Blueprint("film", __name__, url_prefix="/movies")


# insert new movie (C)
@movieBlueprint.route("/", methods=["GET", "POST"])
def insertNewMovie():
    # Retrieve MovieService class
    movieService = MovieService()

    if request.method == "POST":
        planetService = PlanetService()

        # Get request body
        data = request.get_json()

        # Validate request
        if not createMovieValidator(data):
            return (
                jsonify(
                    {
                        "Error": "Please send valid fields for movie creation and at least the movie name"
                    }
                ),
                400,
            )

        # Unpack values
        title, releaseDate, director, *rest = data.values()

        # Check if movie was created with planetIds and if these planets exist in database
        if "planetIds" in data:
            planetIds = data["planetIds"]
            inexistantIds = planetService.getInexistantPlanetIds(planetIds)
            if inexistantIds != None:
                return (
                    jsonify(
                        {
                            f"Error: The following planet ids are not registered in the database: {inexistantIds}"
                        }
                    ),
                    404,
                )
        else:
            planetIds = []

        try:
            movieService.createMovie(title, releaseDate, director, planetIds)

            # Add the recently registered movieId to each entry in the planetIds list
            if len(planetIds) != 0:
                newMovieId = movieService.getMovieByTitle(title)["_id"]
                for planetId in planetIds:
                    planetService.updateMovieList(planetId, newMovieId)

            return jsonify({"message": "Movie Created"}), 201
        except CustomException as e:
            return jsonify({"Error": e.message}), e.statusCode
        except Exception as e:
            return jsonify({"Error": str(e)}), 500

    elif request.method == "GET":
        try:
            movies = movieService.getAllMovies()

            for movieInfo in movies:
                movieInfo["_id"] = str(movieInfo["_id"])

            return jsonify(movies), 200
        except CustomException as e:
            return jsonify({"Error": e.message}), e.statusCode
        except Exception as e:
            return jsonify({"Error": str(e)}), 500


@movieBlueprint.route("/<movieId>", methods=["GET"])
def retrieveMovie(movieId):
    movieService = MovieService()
    try:
        movie = movieService.getMovieById(movieId)
        movie["_id"] = str(movie["_id"])
        return jsonify(movie), 200
    except CustomException as e:
        return jsonify({"Error": e.message}), e.statusCode
    except Exception as e:
        return jsonify({"Error": str(e)}), 500


@movieBlueprint.route("/<movieId>", methods=["PUT"])
def updateMovie(movieId):
    movieService = MovieService()

    movieUpdates = request.get_json()

    if not updateMovieValidator(movieUpdates):
        return jsonify({"Error": "Please send valid fields for movie update"}), 400

    try:
        # Check if planet id exists
        movieService.getMovieById(movieId)

        # update planet
        movieService.updateMovieById(movieId, movieUpdates)
        targetMovie = movieService.getMovieById(movieId)

        return jsonify({"message": f"Planet {targetMovie['title']} updated"}), 200
    except CustomException as e:
        return jsonify({"Error": e.message}), e.statusCode
    except Exception as e:
        return jsonify({"Error": str(e)}), 500


@movieBlueprint.route("/<movieId>", methods=["DELETE"])
def deleteMovie(movieId):
    movieService = MovieService()
    planetService = PlanetService()

    try:
        # Verify if planetId exists and removes planetId from movie entries
        movie = movieService.getMovieById(movieId)
        planetsInIds = movie["planetIds"]
        print(planetsInIds)
        for planetId in planetsInIds:
            planetService.removeMovieIdFromList(planetId, movieId)

        # Perform deletion
        movieService.deleteMovieById(movieId)

        return jsonify({"message": f"Planet {movie['title']} deleted"}), 200
    except CustomException as e:
        return jsonify({"Error": e.message}), e.statusCode
    except Exception as e:
        return jsonify({"Error": str(e)}), 500
