import sys

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

from datetime import datetime, timedelta


# Initialize app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
app.config['SECRET_KEY'] = 'arbitrarySecretKey'

# Word around so autopep8 E402 doesn't formats import after app = Flask(__name__)
if not 'models' in sys.modules:
    from model import db, User, Patient, MedicalEncounter, Prescription, Physician, Appointment, LabOrder, Insurance


with app.app_context():

# class Patient(db.Model):  # 01
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(200), nullable=False)
#     telephone = db.Column(db.String(200), nullable=False)
#     address = db.Column(db.String(200), nullable=False)
#     date_of_birth = db.Column(db.Date, nullable=False)
#     gender = db.Column(db.String(200), nullable=False)
#     primary_physician = db.relationship('Physician', backref='patient')
#     medical_encounter = db.relationship(
#         'MedicalEncounter', backref='patient')
#     insurance = db.relationship('Insurance', backref='patient')
#     appointment = db.relationship('Appointment', backref='patient')
#     medication = db.relationship('Medication', backref='patient')

# class MedicalEncounter(db.Model):  # 02
#     id = db.Column(db.Integer, primary_key=True)
#     encounter_date = db.Column(db.Date, nullable=False)
#     # practitioner_id = db.Column(db.Integer, db.ForeignKey('physician.id'), nullable=False)
#     practitioner_type = db.Column(db.String(200), nullable=False)
#     complaint = db.Column(db.String(200), nullable=False)
#     diagnosis = db.Column(db.String(200), nullable=False)
#     treatment = db.Column(db.String(200), nullable=False)
#     referral = db.Column(db.String(200), nullable=False)
#     recommended_followup = db.Column(db.String(200), nullable=False)
#     notes = db.Column(db.String(200), nullable=False)
#     submission_date = db.Column(db.Date, nullable=False)
#     lab_order = db.relationship('LabOrder', backref='medical_encounter')
#     vital_signs_id = db.relationship('VitalSign', backref='medical_encounter')
#     prescription = db.relationship('Prescription', backref='medical_encounter')
#     patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))


# class Physician(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     physician_name = db.Column(db.String(200), nullable=False)
#     appointment = db.relationship('Appointment', backref='appointment')
#     patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))


# class Physician(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     physician_name = db.Column(db.String(200), nullable=False)
#     appointment = db.relationship('Appointment', backref='appointment')
#     patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    
    
    patient = Patient(name='John Doe', telephone='1234567890', address='123 Main St', date_of_birth=datetime.now(), gender = 'Male')
    db.session.add(patient)
    physician = Physician(physician_name='Dr. Smith', patient_id=1)
    db.session.add(physician)
    me = MedicalEncounter(encounter_date=datetime.now(), practitioner_type='Physician', complaint='Headache', diagnosis='Migraine', treatment='Tylenol', referral='None', recommended_followup='None', notes='None', submission_date=datetime.now(), patient_id=1)
    db.session.add(me)
    db.session.commit()
