try:
    from run import app
except ImportError:
    from __main__ import app

from datetime import date
from sqlalchemy import Column, Date

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


#### Health Tracker Module ####

class Patient(db.Model):  # 01
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    telephone = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(200), nullable=False)
    insurance = db.relationship('Insurance', backref='patient')
    physician_id = db.Column(db.Integer, db.ForeignKey(
        'physician.id'), nullable=False)
    medical_encounter = db.relationship(
        'MedicalEncounter', backref='patient')

    appointment = db.relationship('Appointment', backref='patient')
    medication = db.relationship('Medication', backref='patient')


class MedicalEncounter(db.Model):  # 02
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, nullable=False)
    encounter_date = db.Column(db.Date, nullable=False)
    practitioner_type = db.Column(db.String(200), nullable=False)
    complaint = db.Column(db.String(200), nullable=False)
    diagnosis = db.Column(db.String(200), nullable=False)
    treatment = db.Column(db.String(200), nullable=False)
    referral = db.Column(db.String(200), nullable=False)
    recommended_followup = db.Column(db.Date, nullable=False)
    notes = db.Column(db.String(200), nullable=False)
    submission_date = db.Column(db.Date, nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    lab_order = db.relationship('LabOrder', backref='medical_encounter')
    vital_signs_id = db.relationship('VitalSign', backref='medical_encounter')
    prescription = db.relationship('Prescription', backref='medical_encounter')


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
        'medical_encounter.id'), nullable=True)


class LabTest(db.Model):  # 04
    id = db.Column(db.Integer, primary_key=True)
    lab_test_name = db.Column(db.String(200), nullable=False)
    low_normal_results = db.Column(db.String(200))
    high_normal_results = db.Column(db.String(200))
    lab_order = db.relationship('LabOrder', backref='lab_test')

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
    lab_test_id = db.Column(db.Integer, db.ForeignKey(
        'lab_test.id'), nullable=False)

    def __repr__(self):
        return '<LabOrder %r>' % self.id


class Physician(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    physician_name = db.Column(db.String(200), nullable=False)
    cell_phone_number = db.Column(db.String(200), nullable=False)
    work_time_start = db.Column(db.Integer, nullable=False)
    work_time_end = db.Column(db.Integer, nullable=False)
    work_days = db.Column(db.String(200), nullable=False)
    patients = db.relationship('Patient', backref='physician')
    # appointments = db.relationship('Appointment', backref='physician')

    def __str__(self):
        return f"Physician(id={self.id}, name='{self.physician_name}', phone='{self.cell_phone_number}',\
            work start={self.work_time_start}, work end={self.work_time_end}, work days='{self.work_days}')"


class Appointment(db.Model):
    # __bind_key__ = 'Appointment'
    id = db.Column(db.Integer, primary_key=True)
    physician_name = db.Column(db.String(200), nullable=False)
    appointment_date_time = db.Column(db.String(200), nullable=False)
    appointment_date = db.Column(db.String(200), nullable=False)
    appointment_type = db.Column(db.String(200), nullable=False)
    appointment_time = db.Column(db.String(200), nullable=False)
    physician_id = db.Column(db.Integer, nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    # service_type = db.relationship("ServiceProvidedByClinic")

    def __str__(self):
        return f"Appointment(id={self.id}, appointment_date_time={self.appointment_date_time},\
            appointment_date={self.appointment_date}, appointment_type={self.appointment_type},\
            appointment_time={self.appointment_time}, physician_id={self.physician_id})"


class ServiceProvidedByClinic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service_description = db.Column(db.String(200), nullable=False)
    cost_for_service = db.Column(db.Float, nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    due_date = db.Column(db.Date, nullable=False)
    date = db.Column(db.Date, nullable=False)
    invoice_line_item = db.relationship(
        'InvoiceLineItem', backref='service_provided_by_clinic')
    # service_type_id = db.Column(db.Integer, db.ForeignKey('ServiceProvidedByClinic.id'))


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
    due_date = db.Column(db.Date, nullable=False)
    number_date = db.Column(db.Integer, nullable=False)
    date_paid = db.Column(db.String(30), nullable=False)


class Insurance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, default='Add Insurance')
    address = db.Column(db.String(200), nullable=False, default='Add Address')
    status = db.Column(db.String(200), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    invoice = db.relationship('Invoice', backref='insurance')

    def __repr__(self):
        return f"Insurance('{self.name}', '{self.address}', '{self.status}')"


class VitalSign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body_temperature = db.Column(db.String(200), nullable=False)
    pulse_rate = db.Column(db.String(200), nullable=False)
    respiratory_rate = db.Column(db.String(200), nullable=False)
    blood_pressure = db.Column(db.String(200), nullable=False)
    encounter_id = db.Column(db.Integer, db.ForeignKey(
        'medical_encounter.id'), nullable=False)


class Medication(db.Model):  # Shweta
    id = db.Column(db.Integer, primary_key=True)
    medication = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    dosage = db.Column(db.Text, nullable=True)
    frequency = db.Column(db.String(200), nullable=True)
    side_effects = db.Column(db.String(200), nullable=True)
    interactions = db.Column(db.String(200), nullable=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))

##### Equipment Start #####


class Equipment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    equipment_type = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    department = db.Column(db.String(200), nullable=False)
    is_leased = db.Column(db.Boolean, nullable=False)
    is_owned = db.Column(db.Boolean, nullable=False)
    maintenance = db.relationship(
        'EquipmentMaintenance', backref='equipment', lazy=True)
    equipment_owned = db.relationship(
        'EquipmentOwned', backref='equipment', lazy=True)
    vendor = db.relationship('Vendors', backref='equipment', lazy=True)
    equipment_leased = db.relationship(
        'EquipmentLeased', backref='equipment', lazy=True)


class Vendors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    type_of_equipment_provided = db.Column(db.String(200), nullable=False)
    is_preferred_vendor = db.Column(db.Boolean, nullable=False)
    equipment_id = db.Column(db.Integer, db.ForeignKey(
        'equipment.id'), nullable=False)


class EquipmentMaintenance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type_of_problem = db.Column(db.String(200), nullable=False)
    description_of_problem = db.Column(db.String(200), nullable=False)
    is_resolved = db.Column(db.Boolean, nullable=False)
    description_of_resolution = db.Column(db.String(200), nullable=False)
    equipment_id = db.Column(db.Integer, db.ForeignKey(
        'equipment.id'), nullable=False)


class EquipmentLeased(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    leasing_company = db.Column(db.String(200), nullable=False)
    equipment_id = db.Column(db.Integer, db.ForeignKey(
        'equipment.id'), nullable=False)


class EquipmentOwned(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_purchased = db.Column(db.DateTime, nullable=False)
    warranty_information = db.Column(db.String(200), nullable=False)
    equipment_id = db.Column(db.Integer, db.ForeignKey(
        'equipment.id'), nullable=False)


##### Equipment End #####
