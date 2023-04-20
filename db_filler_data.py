import sys

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

from forms import RegistrationForm, LoginForm, SearchForm
from datetime import datetime, timedelta


# Initialize app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'arbitrarySecretKey'

# Word around so autopep8 E402 doesn't formats import after app = Flask(__name__)
if not 'models' in sys.modules:
    from model import db, User, Patient, MedicalEncounter, Prescription, Physician, ServiceProvidedByClinic, Appointment, LabOrder, Insurance, InsuranceStatus


# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(200), nullable=False)
#     password = db.Column(db.String(200), nullable=False)
#     roles = db.Column(db.String(200), nullable=False)

#     def __repr__(self):
#         return '<User %r>' % self.id

#     def is_active(self):
#         return True


# class ServiceProvidedByClinic(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     service_description = db.Column(db.String(200), nullable=False)
#     cost_for_service = db.Column(db.Float, nullable=False)
#     patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
#     due_date = db.Column(db.Date, nullable=False)
#     date = db.Column(db.Date, nullable=False)
#     date_paid = db.Column(db.Date, nullable=False)

# class Patient(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(200), nullable=False)
#     medical_encounter = db.relationship('MedicalEncounter', backref='patient')
#     physician = db.relationship('Physician', backref='patient')

# class MedicalEncounter(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     encounter = db.Column(db.String(200), nullable=False)
#     prescription = db.relationship('Prescription', backref='medical_encounter')
#     LabOrder = db.relationship('LabOrder', backref='lab_order')
#     patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))

# class LabOrder(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(200), nullable=False)
#     service_provided = db.relationship('ServiceProvidedByClinic', backref='laborder')
#     medical_encounter_id = db.Column(db.Integer, db.ForeignKey('medical_encounter.id'))

# class Prescription(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(200), nullable=False)
#     service_provided = db.relationship('ServiceProvidedByClinic', backref='prescription')
#     medical_encounter_id = db.Column(db.Integer, db.ForeignKey('medical_encounter.id'))


# class Physician(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(200), nullable=False)
#     appointment = db.relationship('Appointment', backref='appointment')
#     patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))

# class Appointment(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(200), nullable=False)
#     service_provided = db.relationship('ServiceProvidedByClinic', backref='serviceprovidedbyclinic', uselist=False)
#     physician_id = db.Column(db.Integer, db.ForeignKey('physician.id'))

# class Insurance (db.model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(200), nullable=False)
#     address = db.Column(db.String(200), nullable=False)
#     status = db.Column(db.String(200), nullable=False)
#     patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))

with app.app_context():
    # create user
    user = User(username='admin', password='password', roles='admin')
    patient = Patient(name='John Doe')
    carrier = Insurance(name='Blue Cross Blue Shield',
                        address='123 Main St', status="on time", patient_id=1)
    medical_encounter = MedicalEncounter(
        encounter='Fever', patient_id=1, date=datetime.now())
    lab_order = LabOrder(
        name='Blood Test', medical_encounter_id=1, date=datetime.now())
    prescription = Prescription(
        name='Tylenol', medical_encounter_id=1, date=datetime.now())
    physician = Physician(name='Dr. Smith', patient_id=1)
    appointment = Appointment(name='Dr. Smith', physician_id=1)
    service = ServiceProvidedByClinic(service_description='Blood Test', cost_for_service=100.00, date=datetime.now(
    ), due_date=datetime.now() + timedelta(days=30), patient_id=1)
    service1 = ServiceProvidedByClinic(service_description='X-Rays', cost_for_service=200.00, date=datetime.now(), due_date=datetime.now(
    ) + timedelta(days=30), patient_id=1)
    
    # add to database
    db.session.add(user)
    db.session.add(patient)
    db.session.add(medical_encounter)
    db.session.add(lab_order)
    db.session.add(prescription)
    db.session.add(physician)
    db.session.add(appointment)
    db.session.add(service)
    db.session.add(service1)
    db.session.add(carrier)

    db.session.commit()
