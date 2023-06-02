from app.models.planetModel import Planet
from app.repositories.planetRepository import PlanetRepository
from .errors import CustomException


class PlanetService:
    # Initiate class with an instance of PlanetRepository to get its methods
    def __init__(self):
        self.planetRepository = PlanetRepository()

    def getAllPlanets(self):
        return self.planetRepository.getAllPlanets()

    def getPlanetById(self, planetId):
        planet = self.planetRepository.getPlanetById(planetId)
        if planet == None:
            raise CustomException("Invalid Planet Id Error", 400)
        planet["_id"] = str(planet["_id"])
        return planet

    def getPlanetByName(self, planetName):
        planet = self.planetRepository.getPlanetByName(planetName)
        return planet

    def createPlanet(self, name, climate, diameter, population, movieIds=[]):
        # Verify if planet is duplicated
        planetExists = self.planetRepository.getPlanetByName(name)
        if planetExists == None:
            raise CustomException("Duplicated Planet Error", 409)

        # Create planet entry on database
        planet = Planet(name, climate, diameter, population, movieIds)
        return self.planetRepository.createPlanet(planet)

    def updatePlanetById(self, planetId, planetUpdates):
        return self.planetRepository.updatePlanetById(planetId, planetUpdates)

    def deletePlanetById(self, planetId):
        return self.planetRepository.deletePlanetById(planetId)

    def deletePlanetByTitle(self, planetName):
        planet = self.planetRepository.getPlanetByName(planetName)
        planetId = str(planet["_id"])
        return self.planetRepository.deletePlanetById(planetId)

    def getInexistantPlanetIds(self, planetIds: list):
        if planetIds == []:
            return None

        wrongIds = []
        for planetId in planetIds:
            if self.planetRepository.getPlanetById(planetId) == None:
                wrongIds.append(planetId)

        # Return "None" when there are no inexistante Ids
        if len(wrongIds) == 0:
            return None

        return wrongIds

    def updateMovieList(self, planetId, movieId):
        return self.planetRepository.updatePlanetMovieIdList(planetId, movieId)

    def removeMovieIdFromList(self, planetId, movieId):
        return self.planetRepository.removeMoviefromList(planetId, movieId)
