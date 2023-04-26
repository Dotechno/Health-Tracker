import sys

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

from forms import RegistrationForm, LoginForm
from datetime import datetime, timedelta


# Initialize app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
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

# class Patient(db.Model):  # 01
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(200), nullable=False)
#     telephone = db.Column(db.String(200), nullable=False)
#     address = db.Column(db.String(200), nullable=False)
#     date_of_birth = db.Column(db.Date, nullable=False)
#     gender = db.Column(db.String(200), nullable=False)
#     primary_physician = db.Column(db.Integer, db.ForeignKey(
#         'physician.id'), nullable=False)
#     medical_encounter = db.relationship(
#         'MedicalEncounter', backref='patient')
#     insurance = db.relationship('Insurance', backref='patient')
#     appointment = db.relationship('Appointment', backref='patient')
#     medication = db.relationship('Medication', backref='patient')


# class MedicalEncounter(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     encounter = db.Column(db.String(200), nullable=False)
#     prescription = db.relationship('Prescription', backref='medical_encounter')
#     LabOrder = db.relationship('LabOrder', backref='lab_order')
#     patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))

# class LabOrder(db.Model):  # 05
#     id = db.Column(db.Integer, primary_key=True)
#     patient_name = db.Column(db.String(200), nullable=False)
#     physician_name = db.Column(db.String(200), nullable=False)
#     lab_test_date = db.Column(db.DateTime, nullable=False)
#     lab_test_technician = db.Column(db.String(200), nullable=False)
#     lab_test_result = db.Column(db.String(200), nullable=False)
#     test_name = db.Column(db.String(200), nullable=False)
#     lab_order_date = db.Column(db.DateTime, nullable=False)
#     medical_encounter_id = db.Column(db.Integer, db.ForeignKey(
#         'medical_encounter.id'), nullable=False)


#  class Prescription(db.Model):  # 03 Shweta
#     id = db.Column(db.Integer, primary_key=True)
#     patient_name = db.Column(db.String(200), db.ForeignKey(Patient.name))
#     physician_name = db.Column(db.String(200), nullable=False)
#     medication = db.Column(db.String(200), nullable=False)
#     dosage = db.Column(db.Text, nullable=True)
#     frequency = db.Column(db.String(200), nullable=False)
#     filled_by = db.Column(db.String(200), nullable=False)
#     date_filled = db.Column(Date, default=date.today)
#     pharmacist_name = db.Column(db.String(200), nullable=False)
#     medical_encounter_id = db.Column(db.Integer, db.ForeignKey(
#         'medical_encounter.id'), nullable=False)


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
    patient = Patient(name='John Doe', telephone='123-456-7890', address='123 Main St', date_of_birth=datetime.strptime('2012-12-12', '%Y-%m-%d'), gender = "male", primary_physician=1, insurance_id = 1)
    carrier = Insurance(name='Blue Cross Blue Shield',
                        address='123 Main St', status="on time")
    bob_me = MedicalEncounter(
        encounter_date=datetime.strptime('2020-12-12', '%Y-%m-%d'), practitioner_type='Physician', complaint='Headache',
        diagnosis='Migraine', treatment='Tylenol', referral='None', recommended_followup='None',
        notes='None', submission_date=datetime.strptime('2020-12-12', '%Y-%m-%d'), patient_id=1)
    lab_order = LabOrder(patient_name='John Doe', physician_name='Dr. Smith', lab_test_date=datetime.strptime('2020-12-12', '%Y-%m-%d'), lab_test_technician='Jane Doe', lab_test_result='Positive', test_name='Blood Test'
                         , lab_order_date=datetime.strptime('2020-12-12', '%Y-%m-%d'), medical_encounter_id=1)
    prescription = Prescription(patient_name='John Doe', physician_name='Dr. Smith', medication='Tylenol', dosage='500mg', frequency='Once a day', filled_by='Jane Doe', pharmacist_name='Jane Doe', medical_encounter_id=1)
    physician = Physician(name='Dr. Smith', patient_id=1)
    appointment = Appointment(name='Dr. Smith', physician_id=1)
    service = ServiceProvidedByClinic(service_description='Blood Test', cost_for_service=100.00, date= lab_order.lab_test_date, due_date=lab_order.lab_test_date - timedelta(days=30), patient_id=1)
    service1 = ServiceProvidedByClinic(service_description='X-Rays', cost_for_service=200.00, date=datetime.now(), due_date=datetime.now(
    ) + timedelta(days=30), patient_id=1)
    
    # add to database
    db.session.add(user)
    db.session.add(patient)
    db.session.add(bob_me)
    db.session.add(lab_order)
    db.session.add(prescription)
    db.session.add(physician)
    db.session.add(appointment)
    db.session.add(carrier)



    db.session.add(service)
    db.session.add(service1)


    db.session.commit()
