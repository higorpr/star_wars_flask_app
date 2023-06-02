from cerberus import Validator

createPlanetSchema = {
    "name": {"type": "string", "required": True},
    "climate": {"type": "string"},
    "diameter": {"type": "number"},
    "population": {"type": "number"},
    "movieIds": {"type": "list"},
}

createPlanetValidator = Validator(createPlanetSchema)

updatePlanetSchema = {
    "name": {"type": "string"},
    "climate": {"type": "string"},
    "diameter": {"type": "number"},
    "population": {"type": "number"},
    "movieIds": {"type": "list"},
}

updatePlanetValidator = Validator(updatePlanetSchema)

createMovieSchema = {
    "title": {"type": "string", "required": True},
    "releaseDate": {"type": "string"},
    "director": {"type": "string"},
    "planetIds": {"type": "list"},
}

createMovieValidator = Validator(createMovieSchema)

updateMovieSchema = {
    "title": {"type": "string"},
    "releaseDate": {"type": "string"},
    "director": {"type": "string"},
    "planetIds": {"type": "list"},
}

updateMovieValidator = Validator(updateMovieSchema)
