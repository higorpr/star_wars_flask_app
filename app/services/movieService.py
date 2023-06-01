from app.models.movieModel import Movie
from app.repositories.movieRepository import MovieRepository
from .errors import CustomException


class MovieService:
    # Initiate class with an instance of MovieRepository to get its methods
    def __init__(self):
        self.movieRepository = MovieRepository()

    def getAllMovies(self):
        return self.movieRepository.getAllMovies()

    def getMovieById(self, movieId: int):
        return self.movieRepository.getMovieById(movieId)

    def createMovie(self, title, releaseDate, director, planetIds=[]):
        # Verify if sent movie is duplicated
        movieExists = self.movieRepository.getMovieByTitle(title)
        if movieExists:
            raise CustomException("Duplicated Movie Error", 409)

        # Create movie entry on database
        movie = Movie(title, releaseDate, director, planetIds)
        return self.movieRepository.createMovie(movie)

    def updateMovieById(self, movieId: int, movieUpdates):
        return self.movieRepository.updateMovieById(movieId, movieUpdates)

    def deleteMovieById(self, movieId: int):
        return self.movieRepository.deleteMovieById(movieId)

    def deleteMovieByTitle(self, movieTitle: str):
        movie = self.movieRepository.getMovieByTitle(movieTitle)
        movieId = int(movie["_id"])
        return self.movieRepository.deleteMovieById(movieId)
