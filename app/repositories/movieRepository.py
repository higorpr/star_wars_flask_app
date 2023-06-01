from app.database.db import mongo
from app.models.movieModel import Movie


class MovieRepository:
    def __init__(self):
        self.movieCollection = mongo.db.movies

    # class method to retrieve movies (R)
    def getAllMovies(self):
        return self.movieCollection.find()

    # class method to retrieve to create new movie (R)
    def getMovieById(self, movieId: int):
        return self.movieCollection.find_one({"_id": movieId})

    # class method to retrieve movie by name (R)
    def getMovieByTitle(self, movieTitle: str):
        return self.movieCollection.find_one({"title": movieTitle})

    # class method to create new movie (C)
    def createMovie(self, movie: Movie):
        return self.movieCollection.insert_one(movie.__dict__)

    # class method to update movie on database (U)
    def updateMovieById(self, movieId: int, movieUpdates):
        return self.movieCollection.update_one(
            {"_id:": movieId}, {"$set": movieUpdates}
        )

    # class method to delete movie from database (D)
    def deleteMovieById(self, movieId: int):
        return self.movieCollection.delete_one({"_id": movieId})
