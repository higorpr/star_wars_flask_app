import sys
import os

# Adicione o diretório raiz do projeto ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app.app import create_app

# Resto do seu código de configuração do conftest.py



@pytest.fixture
def app():
    app = create_app(config_object="app.settings.TestingConfig")
    yield app


@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client