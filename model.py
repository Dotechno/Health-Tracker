from __main__ import app

from datetime import date
from sqlalchemy import Column, Date

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from enum import Enum

# import enum
from enum import Enum

# import datetime
from datetime import datetime

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


#### Health Tracker Module ####

class Patient(db.Model):  # 01
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    telephone = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(200), nullable=False)
    primary_physician = db.Column(db.Integer, db.ForeignKey(
        'physician.id'), nullable=False)
    medical_encounter = db.relationship(
        'MedicalEncounter', backref='patient')
    insurance = db.relationship('Insurance', backref='patient')
    appointment = db.relationship('Appointment', backref='patient')
    medication = db.relationship('Medication', backref='patient')


class MedicalEncounter(db.Model):  # 02
    id = db.Column(db.Integer, primary_key=True)
    encounter_date = db.Column(db.Date, nullable=False)
    # practitioner_id = db.Column(db.Integer, db.ForeignKey('physician.id'), nullable=False)
    practitioner_type = db.Column(db.String(200), nullable=False)
    complaint = db.Column(db.String(200), nullable=False)
    diagnosis = db.Column(db.String(200), nullable=False)
    treatment = db.Column(db.String(200), nullable=False)
    referral = db.Column(db.String(200), nullable=False)
    recommended_followup = db.Column(db.String(200), nullable=False)
    notes = db.Column(db.String(200), nullable=False)
    submission_date = db.Column(db.Date, nullable=False)
    lab_order = db.relationship('LabOrder', backref='medical_encounter')
    vital_signs_id = db.relationship('VitalSign', backref='medical_encounter')
    prescription = db.relationship('Prescription', backref='medical_encounter')
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))


# Model for creating prescription of Pharmacy Order Tracking Module


class Prescription(db.Model):  # 03 Shweta
    id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(200), db.ForeignKey(Patient.name))
    physician_name = db.Column(db.String(200), nullable=False)
    medication = db.Column(db.String(200), nullable=False)
    dosage = db.Column(db.Text, nullable=True)
    frequency = db.Column(db.String(200), nullable=False)
    filled_by = db.Column(db.String(200), nullable=False)
    date_filled = db.Column(Date, default=date.today)
    pharmacist_name = db.Column(db.String(200), nullable=False)
    medical_encounter_id = db.Column(db.Integer, db.ForeignKey(
        'medical_encounter.id'), nullable=False)


class LabTest(db.Model):  # 04
    id = db.Column(db.Integer, primary_key=True)
    lab_test_name = db.Column(db.String(200), nullable=False)
    low_normal_results = db.Column(db.String(200))
    high_normal_results = db.Column(db.String(200))
    # lab_order = db.relationship('LabOrder', backref='lab_test')

    def __repr__(self):
        return '<LabTest %r>' % self.id


class LabOrder(db.Model):  # 05
    id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(200), nullable=False)
    physician_name = db.Column(db.String(200), nullable=False)
    lab_test_date = db.Column(db.DateTime, nullable=False)
    lab_test_technician = db.Column(db.String(200), nullable=False)
    lab_test_result = db.Column(db.String(200), nullable=False)
    test_name = db.Column(db.String(200), nullable=False)
    lab_order_date = db.Column(db.DateTime, nullable=False)
    medical_encounter_id = db.Column(db.Integer, db.ForeignKey(
        'medical_encounter.id'), nullable=False)

    def __repr__(self):
        return '<LabOrder %r>' % self.id


class Physician(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    appointment = db.relationship('Appointment', backref='appointment')
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))


class Insurance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(200), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    invoice = db.relationship('Invoice', backref='insurance')

    def __repr__(self):
        return f"Insurance('{self.name}', '{self.address}', '{self.status}')"


class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(120), nullable=False)
    insurance_carrier_id = db.Column(
        db.Integer, db.ForeignKey('insurance.id'), nullable=False)
    total_cost = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow())
    status = db.Column(db.String(20), nullable=False, default='unpaid')


class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    physician_id = db.Column(db.Integer, db.ForeignKey('physician.id'))
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))


class VitalSign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body_temperature = db.Column(db.String(200), nullable=False)
    pulse_rate = db.Column(db.String(200), nullable=False)
    respiratory_rate = db.Column(db.String(200), nullable=False)
    blood_pressure = db.Column(db.String(200), nullable=False)
    encounter_id = db.Column(db.Integer, db.ForeignKey(
        'medical_encounter.id'), nullable=False)


class Medication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    dosage = db.Column(db.String(200), nullable=False)
    frequency = db.Column(db.String(200), nullable=False)
    duration = db.Column(db.String(200), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
