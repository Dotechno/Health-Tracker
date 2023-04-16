from __main__ import app
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from enum import Enum


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
    invoice_line_item = db.relationship('InvoiceLineItem', backref='service_provided_by_clinic')

class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(120), nullable=False)
    insurance_carrier_id = db.Column(db.Integer, db.ForeignKey('insurance.id'), nullable=False)
    total_cost = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    status = db.Column(db.String(20), nullable=False, default='unpaid')
    insurance_obj = db.relationship('Insurance', backref='invoices')



class InvoiceLineItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoice.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service_provided_by_clinic.id'), nullable=False)  # Fix the table name here
    date = db.Column(db.DateTime, nullable=False)
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
    insurance_carrier_id = db.Column(db.Integer, db.ForeignKey('insurance.id'), nullable=False)

    def __repr__(self):
        return f"Insurance('{self.name}', '{self.address}', '{self.status}')"
    
## not important
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
