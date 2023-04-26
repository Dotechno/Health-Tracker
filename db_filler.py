import sys

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

from datetime import datetime, timedelta


# Initialize app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'arbitrarySecretKey'

# Word around so autopep8 E402 doesn't formats import after app = Flask(__name__)
if not 'models' in sys.modules:
    from model import db, User, Patient, MedicalEncounter, Prescription, Physician, ServiceProvidedByClinic, Appointment, LabOrder, Insurance, InsuranceStatus



with app.app_context():


    bob = Physician(name='Bob')
    db.session.add(bob)
    med_mob= Insurance(name='MedMob', address='123 Red Rd', status='Active',patient_id=[24],invoice=200)
    db.session.add(med_mob)
    tylenol = Prescription(name='Tylenol',appointment='Check-up',date='2020-12-12')
    db.session.add(tylenol)
    surgery =Appointment(name='Surgery',physician_id=1,patient_id=24)
    db.session.add(surgery)



    db.session.commit()