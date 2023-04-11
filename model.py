from __main__ import app
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from sqlalchemy import Enum


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


class ServiceProvidedByClinic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service_description = db.Column(db.String(200), nullable=False)
    cost_for_service = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    medical_encounter = db.relationship('MedicalEncounter', backref='patient')
    physician = db.relationship('Physician', backref='patient')
    insurance = db.relationship('Insurance', backref='patient')
    serviceprovidedbyclinic = db.relationship('ServiceProvidedByClinic', backref='patient')

class MedicalEncounter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    encounter = db.Column(db.String(200), nullable=False)
    prescription = db.relationship('Prescription', backref='medical_encounter')
    LabOrder = db.relationship('LabOrder', backref='lab_order')
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    date= db.Column(db.Date, nullable=False)
    
class LabOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    date = db.Column(db.Date, nullable=False)
    medical_encounter_id = db.Column(db.Integer, db.ForeignKey('medical_encounter.id'))

class Prescription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    medical_encounter_id = db.Column(db.Integer, db.ForeignKey('medical_encounter.id'))
    date = db.Column(db.Date, nullable=False)


class Physician(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    appointment = db.relationship('Appointment', backref='appointment')
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    physician_id = db.Column(db.Integer, db.ForeignKey('physician.id'))


class InsuranceStatus(Enum):
    on_time = 'Pays on time'
    late = 'Late in payments'
    diffcult = 'Difficult to get payments'

class Insurance (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(200), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))