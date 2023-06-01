from app.models.planetModel import Planet
from app.repositories.planetRepository import PlanetRepository
from .errors import CustomException


class PlanetService:
    # Initiate class with an instance of PlanetRepository to get its methods
    def __init__(self):
        self.planetRepository = PlanetRepository()

    def getAllPlanets(self):
        return self.planetRepository.getAllPlanets()

    def getPlanetById(self, planetId: int):
        return self.planetRepository.getPlanetById(planetId)

    def createPlanet(self, name, climate, diameter, population, movieIds=[]):
        # Verify if planet is duplicated
        planetExists = self.planetRepository.getPlanetByName(name)
        if planetExists:
            raise CustomException("Duplicated Planet Error", 409)

        # Create planet entry on database
        planet = Planet(name, climate, diameter, population, movieIds)
        return self.planetRepository.createPlanet(planet)

    def updatePlanetById(self, planetId: int, planetUpdates):
        return self.planetRepository.updatePlanetById(planetId, planetUpdates)

    def deletePlanetById(self, planetId: int):
        return self.planetRepository.deletePlanetById(planetId)

    def deletePlanetByTitle(self, planetName: str):
        planet = self.planetRepository.getPlanetByName(planetName)
        planetId = int(planet["_id"])
        return self.planetRepository.deletePlanetById(planetId)
