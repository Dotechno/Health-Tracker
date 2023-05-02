import pytest

from run import db
import os

import time

# # delete all files in instance folder
# os.system('del /f /q /s instance\*')

# # run db_filler_data.py
# os.system('python db_filler_data.py')


@pytest.fixture()
def app():
    from run import app

    app.config['TESTING'] = True

    with app.app_context():
        db.create_all()

    yield app


def app_appointment():
    import appointment
    yield appointment


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def appointment_client(app_appointment):
    return app_appointment.test_client()
