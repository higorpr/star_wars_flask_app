from datetime import datetime
from app.database.db import mongo


class Planet:
    def __init__(
        self, name: str, climate: str, diameter: float, population: int, movieIds: list
    ):
        self.name = name
        self.climate = climate
        self.diameter = diameter
        self.population = population
        self.movieIds = movieIds
        self.planetCollection = mongo.db.planets

    def save(self):
        self.createdAt = datetime.utcnow()
        self.updatedAt = self.createdAt
        self.planetCollection.insert_one(self.__dict__)
