from app.database.db import mongo
from app.models.planetModel import Planet
from datetime import datetime
from bson.objectid import ObjectId


class PlanetRepository:
    def __init__(self):
        self.planetsCollection = mongo.db.planets

    # class method to retrieve movies (R)
    def getAllPlanets(self):
        return list(self.planetsCollection.find())

    # class retrieve to create new movie (R)
    def getPlanetById(self, planetId):
        return self.planetsCollection.find_one({"_id": ObjectId(planetId)})

    def getPlanetByName(self, planetName: str):
        planetInfo = self.planetsCollection.find({"name": planetName})
        return list(planetInfo)

    # class method to create new movie (C)
    def createPlanet(self, planet: Planet):
        return self.planetsCollection.insert_one(planet.__dict__)

    # class method to update movie on database (U)
    def updatePlanetById(self, planetId, planetUpdates):
        planetUpdates["updatedAt"] = datetime.utcnow()
        return self.planetsCollection.update_one(
            {"_id": ObjectId(planetId)}, {"$set": planetUpdates}
        )

    def updatePlanetMovieIdList(self, planetId, movieId):
        self.planetsCollection.update_one(
            {"_id": ObjectId(planetId)},
            {
                "$set": {"updatedAt": datetime.utcnow()},
                "$addToSet": {"movieIds": str(movieId)},
            },
        )

    # class method to delete movie from database (D)
    def deletePlanetById(self, planetId):
        return self.planetsCollection.delete_one({"_id": ObjectId(planetId)})

    def removeMoviefromList(self, planetId, movieId):
        self.planetsCollection.update_one(
            {"_id": ObjectId(planetId)},
            {
                "$set": {"updatedAt": datetime.utcnow()},
                "$pull": {"movieIds": str(movieId)},
            },
        )
