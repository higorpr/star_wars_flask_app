from datetime import datetime, date
from app.database.db import mongo


class Movie:
    def __init__(self, title: str, releaseDate: date, director: str, planetIds: list):
        self.title = title
        self.releaseDate = releaseDate
        self.director = director
        self.planetIds = planetIds
        self.createdAt = datetime.utcnow()
        self.updatedAt = self.createdAt
