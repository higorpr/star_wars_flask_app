from app.models.movieModel import Movie
from app.repositories.movieRepository import MovieRepository
from .errors import CustomException


class MovieService:
    # Initiate class with an instance of MovieRepository to get its methods
    def __init__(self):
        self.movieRepository = MovieRepository()

    def getAllMovies(self):
        return list(self.movieRepository.getAllMovies())

    def getMovieById(self, movieId):
        movie = self.movieRepository.getMovieById(movieId)
        if movie == None:
            raise CustomException("Invalid Movie Id Error", 400)
        movie["_id"] = str(movie["_id"])
        return movie

    def getMovieByTitle(self, movieTitle):
        movie = self.movieRepository.getMovieByTitle(movieTitle)
        return movie[0]

    def createMovie(self, title, releaseDate, director, planetIds=[]):
        # Verify if sent movie is duplicated
        movieExists = self.movieRepository.getMovieByTitle(title)
        if len(movieExists) > 0:
            raise CustomException("Duplicated Planet Error", 409)

        # Create movie entry on database
        movie = Movie(title, releaseDate, director, planetIds)
        return self.movieRepository.createMovie(movie)

    def updateMovieById(self, movieId, movieUpdates):
        return self.movieRepository.updateMovieById(movieId, movieUpdates)

    def deleteMovieById(self, movieId):
        return self.movieRepository.deleteMovieById(movieId)

    def deleteMovieByTitle(self, movieTitle: str):
        movie = self.movieRepository.getMovieByTitle(movieTitle)
        movieId = int(movie["_id"])
        return self.movieRepository.deleteMovieById(movieId)

    def getInexistantMovieIds(self, movieIds: list):
        if movieIds == []:
            return None

        wrongIds = []
        for movieId in movieIds:
            if self.movieRepository.getMovieById(movieId) == None:
                wrongIds.append(movieId)

        # Return "None" when there are no inexistante Ids
        if len(wrongIds) == 0:
            return None

        return wrongIds

    def updatePlanetList(self, movieId, planetId):
        return self.movieRepository.updateMoviePlanetIdList(movieId, planetId)

    def removePlanetIdFromList(self, movieId, planetId):
        return self.movieRepository.removePlanetfromList(movieId, planetId)
