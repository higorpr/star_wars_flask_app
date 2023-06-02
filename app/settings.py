import os
from flask import Config

MONGO_URI = os.getenv("MONGO_URI")

class TestingConfig(Config):
    DEBUG=False
    TESTING = True
    MONGO_URI = os.getenv("MONGO_URI")