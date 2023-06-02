from .conftest import app


def testGetAllMethods(client):
    moviesResponse = client.get("/movies", follow_redirects=True)
    planetsResponse = client.get("/planets", follow_redirects=True)
    assert type(moviesResponse.json) == list
    assert moviesResponse.status_code == 200
    assert type(planetsResponse.json) == list
    assert planetsResponse.status_code == 200


def testPostMethods(client):
    moviePayloadRepeated = {
        "title": "Nova Esperança 2",
        "releaseDate": "1979-06-15",
        "director": "George Lucas",
    }

    moviePayloadNew = {
        "title": "The Empire Strikes",
        "releaseDate": "1979-06-15",
        "director": "George Lucas The III",
    }

    movieUrl = "/movies"
    oldMovieResponse = client.post(
        movieUrl, json=dict(moviePayloadRepeated), follow_redirects=True
    )
    assert oldMovieResponse.status_code == 409

    newMovieResponse = client.post(
        movieUrl, json=dict(moviePayloadNew), follow_redirects=True
    )
    assert newMovieResponse.status_code == 201

    planetPayloadRepeated = {
        "name": "New Earth 3",
        "population":2000000,
        "diameter":6000,
        "climate":"tropical"
    }

    planetPayloadNew = {
        "name": "Marte",
        "population": 0,
        "diameter": "5000",
        "climate": "cold",
    }

    planetUrl = "/planets"
    oldPlanetResponse = client.post(
        planetUrl, json=dict(planetPayloadRepeated), follow_redirects=True
    )
    assert oldPlanetResponse.status_code == 409

    newPlanetResponse = client.post(
        planetUrl, json=dict(planetPayloadNew), follow_redirects=True
    )
    assert newPlanetResponse.status_code == 201
