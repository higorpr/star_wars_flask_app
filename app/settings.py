import os
from flask import Config

MONGO_URI = os.getenv("MONGO_URI")

class TestingConfig(Config):
    DEBUG=False
    TESTING = True
    MONGO_URI = "mongodb+srv://higorpr:0u0e657A@starwarscluster.tf1zbiq.mongodb.net/StarWarsDatabase?retryWrites=true&w=majority"