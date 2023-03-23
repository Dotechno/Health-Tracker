from __main__ import app

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

class serviceProvidedByClinic(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    service_Type = db.Column(db.String(200),nullable = False)
    service_Description = db.Column(db.String(200), nullable = False)
    cost_For_Service = db.Column(db.Float, nullable = False)
    prescription= db.relationship('prescription', backref = 'prescription',uselist = False)
    appointment = db.relationship('appointment', backref = 'appointment',uselist = False)
    labOrder = db.relationship('labOrder', backref = 'labOrder',uselist = False)

class patient (db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200),nullable=False)
    MedicalEncounter_id = db.Column(db.Integer, db.ForeignKey('medical_encounter.id'))
    
class labOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    service_provided_id = db.Column(db.Integer, db.ForeignKey('service_provided_by_clinic.id'))

class appointment(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    service_provided_id = db.Column(db.Integer, db.ForeignKey('service_provided_by_clinic.id'))

class prescription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service_provided_id = db.Column(db.Integer, db.ForeignKey('service_provided_by_clinic.id'))
    

class medicalEncounter(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    Encounter = db.Column(db.String(200), nullable = False)
    Patient = db.relationship('patient', backref = 'patient')
    
class physican(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200), nullable = False)