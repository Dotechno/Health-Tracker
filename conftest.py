import pytest

from run import db


@pytest.fixture()
def app():
    from run import app

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()
