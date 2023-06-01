from app.database.db import mongo
from app.models.planetModel import Planet


class PlanetRepository:
    def __init__(self):
        self.planetsCollection = mongo.db.planets

    # class method to retrieve movies (R)
    def getAllPlanets(self):
        return self.planetsCollection.find()

    # class retrieve to create new movie (R)
    def getPlanetById(self, planetId: int):
        return self.planetsCollection.find_one({"_id": planetId})

    def getPlanetByName(self, planetName: str):
        return self.planetsCollection.find_one({"name": planetName})

    # class method to create new movie (C)
    def createPlanet(self, planet: Planet):
        return self.planetsCollection.insert_one(planet.__dict__)

    # class method to update movie on database (U)
    def updatePlanetById(self, planetId: int, planetUpdates):
        return self.planetsCollection.update_one(
            {"_id:": planetId}, {"$set": planetUpdates}
        )

    # class method to delete movie from database (D)
    def deletePlanetById(self, planetId: int):
        return self.planetsCollection.delete_one({"_id": planetId})
