from __main__ import app
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from enum import Enum


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


class ServiceProvidedByClinic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service_description = db.Column(db.String(200), nullable=False)
    cost_for_service = db.Column(db.Float, nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    due_date = db.Column(db.Date, nullable=False)
    date = db.Column(db.Date, nullable=False)
    invoice_line_item = db.relationship(
        'InvoiceLineItem', backref='service_provided_by_clinic')


class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(120), nullable=False)
    insurance_carrier_id = db.Column(
        db.Integer, db.ForeignKey('insurance.id'), nullable=False)
    total_cost = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow())
    status = db.Column(db.String(20), nullable=False, default='unpaid')


class InvoiceLineItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey(
        'invoice.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey(
        'service_provided_by_clinic.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    cost = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(30), nullable=False)


class InsuranceStatus(Enum):
    on_time = 'Pays on time'
    late = 'Late in payments'
    diffcult = 'Difficult to get payments'


class Insurance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(200), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    invoice = db.relationship('Invoice', backref='insurance')

    def __repr__(self):
        return f"Insurance('{self.name}', '{self.address}', '{self.status}')"

# not important


class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    telephone = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(200), nullable=False)
    medical_encounter = db.relationship('MedicalEncounter', backref='patient')
    primary_physician = db.relationship('Physician', backref='patient')
    insurance = db.relationship('Insurance', backref='patient')
    current_medication = db.relationship('Medication', backref='patient')
    current_appointments = db.relationship('Appointment', backref='patient')
    

class MedicalEncounter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    encounter_date = db.Column(db.Date, nullable=False)
    practitioner_id = db.Column(db.Integer, db.ForeignKey('physician.id'), nullable=False)
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
    prescription= db.relationship('Prescription', backref='medical_encounter')
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))


    
class VitalSign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body_temperature = db.Column(db.Double, nullable=False)
    pulse_rate = db.Column(db.Double, nullable=False)
    respiration_rate = db.Column(db.Double, nullable=False)
    blood_pressure = db.Column(db.Double, nullable=False)
    encounter_key = db.Column(db.Integer, db.ForeignKey(
        'medical_encounter.id'), nullable=False)
    
class Medication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    dosage = db.Column(db.String(200), nullable=False)
    frequency = db.Column(db.String(200), nullable=False)
    duration = db.Column(db.String(200), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
#Copy into ChatGPT and ask to make a python flask form

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
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
