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
from datetime import date
from sqlalchemy import Column, Date


from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

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


class Patient(db.Model):
    __bind_key__ = 'patient'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    telephone_num = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    date_of_birth = db.Column(db.String(200), nullable=False)
    gender = db.Column(db.String(200), nullable=False)


# Model for creating prescription of Pharmacy Order Tracking Module
class Prescription(db.Model):  # Shweta
    __bind_key__ = 'prescription'
    id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(200), db.ForeignKey(Patient.name))
    physician_name = db.Column(db.String(200), nullable=False)
    medication = db.Column(db.String(200), nullable=False)
    dosage = db.Column(db.Text, nullable=True)
    frequency = db.Column(db.String(200), nullable=False)
    filled_by = db.Column(db.String(200), nullable=False)
    date_filled = db.Column(Date, default=date.today)
    pharmacist_name = db.Column(db.String(200), nullable=False)

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


class LabTest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lab_test_name = db.Column(db.String(200), nullable=False)
    low_normal_results = db.Column(db.String(200))
    high_normal_results = db.Column(db.String(200))
    # lab_order = db.relationship('LabOrder', backref='lab_test')

    def __repr__(self):
        return '<LabTest %r>' % self.id


class LabOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(200), nullable=False)
    physician_name = db.Column(db.String(200), nullable=False)
    lab_test_date = db.Column(db.DateTime, nullable=False)
    lab_test_technician = db.Column(db.String(200), nullable=False)
    lab_test_result = db.Column(db.String(200), nullable=False)
    test_name = db.Column(db.String(200), nullable=False)
    lab_order_date = db.Column(db.DateTime, nullable=False)
    # test = db.Column(db.Integer, db.ForeignKey('lab_test.id'))

    def __repr__(self):
        return '<LabOrder %r>' % self.id
