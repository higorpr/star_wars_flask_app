from app.database.db import mongo
from app.models.movieModel import Movie
from datetime import datetime
from bson.objectid import ObjectId


class MovieRepository:
    def __init__(self):
        self.movieCollection = mongo.db.movies

    # class method to retrieve movies (R)
    def getAllMovies(self):
        return self.movieCollection.find()

    # class method to retrieve new movie (R)
    def getMovieById(self, movieId):
        return self.movieCollection.find_one({"_id": ObjectId(movieId)})

    # class method to retrieve movie by name (R)
    def getMovieByTitle(self, movieTitle: str):
        movieInfo = list(self.movieCollection.find({"title": movieTitle}))
        return movieInfo

    # class method to create new movie (C)
    def createMovie(self, movie: Movie):
        return self.movieCollection.insert_one(movie.__dict__)

    # class method to update movie on database (U)
    def updateMovieById(self, movieId, movieUpdates):
        movieUpdates["updatedAt"] = datetime.utcnow()
        return self.movieCollection.update_one(
            {"_id": ObjectId(movieId)}, {"$set": movieUpdates}
        )

    def updateMoviePlanetIdList(self, movieId, planetId):
        self.movieCollection.update_one(
            {"_id": ObjectId(movieId)},
            {
                "$set": {"updatedAt": datetime.utcnow()},
                "$addToSet": {"planetIds": str(planetId)},
            },
        )

    # class method to delete movie from database (D)
    def deleteMovieById(self, movieId):
        return self.movieCollection.delete_one({"_id": ObjectId(movieId)})

    def removePlanetfromList(self, movieId, planetId):
        self.movieCollection.update_one(
            {"_id": ObjectId(movieId)},
            {
                "$set": {"updatedAt": datetime.utcnow()},
                "$pull": {"planetIds": str(planetId)},
            },
        )
