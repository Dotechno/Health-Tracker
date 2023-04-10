from __main__ import app
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

db = SQLAlchemy(app)



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    roles = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.id

    def is_active(self):
        return True

 # Model for  creating prescription of Pharmacy Order Tracking Module   
class Prescription(db.Model):
    __bind_key__ ='prescription'
    id = db.Column(db.Integer, primary_key=True)
    physician_name = db.Column(db.String(200), nullable=False)
    medication = db.Column(db.String(200), nullable=False)
    dosage=db.Column(db.Text, nullable=True)
    frequency=db.Column(db.String(200), nullable=True)
    filled_by=db.Column(db.String(200),nullable=True)
    date_filled=db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<User %r>' % self.id

    def is_active(self):
        return True
# Model for Adding Medication  Details
class Medication(db.Model):
    __bind_key__ ='medication'
    id = db.Column(db.Integer, primary_key=True)
    medication = db.Column(db.String(200), nullable=False)
    description=db.Column(db.String(500),nullable=False)
    dosage=db.Column(db.Text, nullable=True)
    frequency=db.Column(db.String(200), nullable=True)
    side_effects=db.Column(db.String(200),nullable=True)
    interactions=db.Column(db.String(200),nullable=True)
    
    def __repr__(self):
        return '<User %r>' % self.id

    def is_active(self):
        return True

