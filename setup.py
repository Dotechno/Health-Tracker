import sys
from flask import Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
#app.config['SQLALCHEMY_BINDS']={'prescription':'sqlite:///prescription.db'}

app.config['SECRET_KEY'] = 'arbitrarySecretKey'


if not 'models' in sys.modules:
    from model import db

with app.app_context():
    db.create_all()
