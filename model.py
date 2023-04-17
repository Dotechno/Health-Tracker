# from __main__ import app
# from datetime import datetime

# from flask_sqlalchemy import SQLAlchemy
# from flask_bcrypt import Bcrypt
# from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

# db = SQLAlchemy(app)



# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(200), nullable=False)
#     password = db.Column(db.String(200), nullable=False)
#     roles = db.Column(db.String(200), nullable=False)

#     def __repr__(self):
#         return '<User %r>' % self.id

#     def is_active(self):
#         return True

#  # Model for  creating prescription of Pharmacy Order Tracking Module   
# class Prescription(db.Model):
#     __bind_key__ ='prescription'
#     id = db.Column(db.Integer, primary_key=True)
#     physician_name = db.Column(db.String(200), nullable=False)
#     medication = db.Column(db.String(200), nullable=False)
#     dosage=db.Column(db.Text, nullable=True)
#     frequency=db.Column(db.String(200), nullable=True)
#     filled_by=db.Column(db.String(200),nullable=True)
#     date_filled=db.Column(db.DateTime, default=datetime.utcnow)

#     def __repr__(self):
#         return '<User %r>' % self.id

#     def is_active(self):
#         return True
# # Model for Adding Medication  Details
# class Medication(db.Model):
#     __bind_key__ ='medication'
#     id = db.Column(db.Integer, primary_key=True)
#     medication = db.Column(db.String(200), nullable=False)
#     description=db.Column(db.String(500),nullable=False)
#     dosage=db.Column(db.Text, nullable=True)
#     frequency=db.Column(db.String(200), nullable=True)
#     side_effects=db.Column(db.String(200),nullable=True)
#     interactions=db.Column(db.String(200),nullable=True)
    
#     def __repr__(self):
#         return '<User %r>' % self.id

#     def is_active(self):
#         return True

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

# class Physician(db.Model):  # Jordan
#     __bind_key__ = 'physician'

#     id = db.Column(db.Integer, primary_key=True)
#     employee_id = db.Column(db.Integer, nullable=False)
#     physician_name = db.Column(db.String(200), nullable=False)
#     cell_phone_number = db.Column(db.String(200), nullable=False)
#     work_time_start = db.Column(db.Integer, nullable=False)
#     work_time_end = db.Column(db.Integer, nullable=False)
#     work_days = db.Column(db.String(200), nullable=False)
#     patients = db.relationship('Patient', backref='physician')
#     appointments = db.relationship('Appointment', backref='physician')
    
class Patient(db.Model):
    __bind_key__='patient'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    telephone_num = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    date_of_birth = db.Column(db.String(200), nullable=False)
    gender = db.Column(db.String(200), nullable=False)
    # medical_encounters = db.relationship('MedicalEncounter', backref='patient')
    # appointments = db.relationship('Appointment', backref='patient')
    # medication = db.relationship('Medication', backref='patient')
#     primary_physician = db.Column(
#         db.Integer, db.ForeignKey(Physician.id), nullable=False)
#     insurance = db.relationship('Insurance', backref='patient')
#     service_provided_by_clinic = db.relationship(
#         'ServiceProvidedByClinic', backref='patient')


# class MedicalEncounter(db.Model):  # Jordan
#     __bind_key__ = 'medical_encounter'
#     id = db.Column(db.Integer, primary_key=True)
#     encounter_date_time = db.Column(db.String(200), nullable=False)
#     practitioner_type_seen = db.Column(db.String(200), nullable=False)
#     patient_complaints = db.Column(db.String(200), nullable=False)
#     practitioners_notes = db.Column(db.String(200), nullable=False)
#     diagnosis = db.Column(db.String(200), nullable=False)
#     treatment_plan = db.Column(db.String(200), nullable=False)
#     referral_to_specialists = db.Column(db.String(200), nullable=False)
#     recommended_follow_up = db.Column(db.String(200), nullable=False)
#     date_time_encounter_submitted = db.Column(db.String(200), nullable=False)
#     employee_id_who_submitted = db.Column(db.String(200), nullable=False)
#     lab_orders = db.relationship('LabOrder', backref='medical_encounter')
#     vital_signs = db.relationship('VitalSign', backref='medical_encounter')
#     prescriptions = db.relationship(
#         'Prescription', backref='medical_encounter')
#     patient_id = db.Column(db.Integer, db.ForeignKey(
#         Patient.id), nullable=False)



# class VitalSign(db.Model):
#     __bind_key__ = 'vital_sign'

#     id = db.Column(db.Integer, primary_key=True)
#     body_temperature = db.Column(db.Double, nullable=False)
#     pulse_rate = db.Column(db.Double, nullable=False)
#     respiration_rate = db.Column(db.Double, nullable=False)
#     blood_pressure = db.Column(db.Double, nullable=False)
#     encounter_key = db.Column(db.Integer, db.ForeignKey(
#         MedicalEncounter.id), nullable=False)





# Model for  creating prescription of Pharmacy Order Tracking Module
class Prescription(db.Model):  # Shweta
    __bind_key__ = 'prescription'
    id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(200), db.ForeignKey(Patient.name))
    physician_name = db.Column(db.String(200), nullable=False)
    medication = db.Column(db.String(200), nullable=False)
    dosage = db.Column(db.Text, nullable=True)
    frequency = db.Column(db.String(200), nullable=True)
    filled_by = db.Column(db.String(200), nullable=True)
    date_filled = db.Column(db.DateTime, default=datetime.utcnow)
    #medical_encounter_id = db.Column(
     #   db.Integer, db.ForeignKey(MedicalEncounter.id))

    def __repr__(self):
        return '<User %r>' % self.id

    def is_active(self):
        return True


class Medication(db.Model):  # Shweta
    __bind_key__ = 'medication'
    id = db.Column(db.Integer, primary_key=True)
    medication = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    dosage = db.Column(db.Text, nullable=True)
    frequency = db.Column(db.String(200), nullable=True)
    side_effects = db.Column(db.String(200), nullable=True)
    interactions = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return '<User %r>' % self.id

    def is_active(self):
        return True


# class InsuranceStatus(Enum):  # Charlie
#     __bind_key__ = 'insurance_status'

#     on_time = 'Pays on time'
#     late = 'Late in payments'
#     diffcult = 'Difficult to get payments'


# class Insurance(db.Model):  # Charlie
#     __bind_key__ = 'insurance'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(200), nullable=False)
#     address = db.Column(db.String(200), nullable=False)
#     status = db.Column(db.String(200), nullable=False)
#     patient_id = db.Column(db.Integer, db.ForeignKey(Patient.id))
#     invoice = db.relationship('Invoice', backref='insurance')
#     insurance_carrier_id = db.Column(
#         db.Integer, db.ForeignKey('insurance.id'), nullable=False)

#     def __repr__(self):
#         return f"Insurance('{self.name}', '{self.address}', '{self.status}')"


# class LabTest(db.Model):  # Shane
#     __bind_key__ = 'lab_test'

#     id = db.Column(db.Integer, primary_key=True)
#     lab_test_name = db.Column(db.String(200), nullable=False)
#     range_of_normal_results = db.Column(db.String(200))

#     def repr(self):
#         return '<LabTest %r>' % self.id


# class LabOrder(db.Model):  # Shane
#     __bind_key__ = 'lab_order'

#     id = db.Column(db.Integer, primary_key=True)
#     patient_name = db.Column(db.String(200), nullable=False)
#     physician_name = db.Column(db.String(200), nullable=False)
#     lab_test_date = db.Column(db.DateTime, nullable=False)
#     lab_test_technician = db.Column(db.String(200), nullable=False)
#     lab_test_result = db.Column(db.String(200), nullable=False)
#     medical_encounter_id = db.Column(
#         db.Integer, db.ForeignKey(MedicalEncounter.id))

#     def repr(self):
#         return '<LabOrder %r>' % self.id


# class ServiceProvidedByClinic(db.Model):  # Charlie
#     __bind_key__ = 'clinic_service'

#     id = db.Column(db.Integer, primary_key=True)
#     service_description = db.Column(db.String(200), nullable=False)
#     cost_for_service = db.Column(db.Float, nullable=False)
#     patient_id = db.Column(db.Integer, db.ForeignKey(Patient.id))
#     due_date = db.Column(db.Date, nullable=False)
#     date = db.Column(db.Date, nullable=False)
#     invoice_line_item = db.relationship(
#         'InvoiceLineItem', backref='service_provided_by_clinic')


# class Invoice(db.Model):  # Charlie
#     __bind_key__ = 'invoice'

#     id = db.Column(db.Integer, primary_key=True)
#     patient_name = db.Column(db.String(120), nullable=False)
#     insurance_carrier_id = db.Column(
#         db.Integer, db.ForeignKey(Insurance.id), nullable=False)
#     total_cost = db.Column(db.Float, nullable=False)
#     date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
#     status = db.Column(db.String(20), nullable=False, default='unpaid')
#     insurance_obj = db.relationship('Insurance', backref='invoices')


# class InvoiceLineItem(db.Model):  # Charlie
#     __bind_key__ = 'invoice_line_item'
#     id = db.Column(db.Integer, primary_key=True)
#     invoice_id = db.Column(db.Integer, db.ForeignKey(
#         Invoice.id), nullable=False)
#     service_id = db.Column(db.Integer, db.ForeignKey(
#         ServiceProvidedByClinic.id), nullable=False)  # Fix the table name here
#     date = db.Column(db.DateTime, nullable=False)
#     cost = db.Column(db.Float, nullable=False)
#     status = db.Column(db.String(30), nullable=False)