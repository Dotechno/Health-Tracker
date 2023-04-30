import sys

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

from forms import RegistrationForm, LoginForm
from datetime import datetime, timedelta


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
app.config['SECRET_KEY'] = 'arbitrarySecretKey'


if not 'models' in sys.modules:
    from model import (db, User, LabOrder, LabTest, Prescription, Medication, Patient,
                       MedicalEncounter, Physician, Insurance, Appointment, Equipment,
                       Vendors, EquipmentMaintenance, EquipmentLeased, EquipmentOwned,
                       ServiceProvidedByClinic, Invoice, InvoiceLineItem, VitalSign
                       )

with app.app_context():
    user = User(username='admin', password='password', roles='admin')

    physician = Physician(physician_name='Dr. Smith', cell_phone_number='619-247-4212',
                          work_time_start="08:00:00", work_time_end="18:00:00",
                          work_days='Monday, Tuesday, Wednesday, Thursday, Friday')

    db.session.add(physician)

    john_doe = Patient(name='John Doe', telephone='619-583-0249', address='439 Main St',
                       date_of_birth=datetime.strptime('2012-12-12', '%Y-%m-%d'), gender="male",
                       physician_id=1)

    db.session.add(john_doe)

    jdfirstvisit = MedicalEncounter(encounter_date=datetime.strptime('2012-12-12', '%Y-%m-%d'),
                                    practitioner_type='Physician', complaint='fever',
                                    diagnosis='flu', treatment='Tylenol', referral='none',
                                    recommended_followup='none', notes='none',
                                    submission_date=datetime.strptime(
                                        '2012-12-12', '%Y-%m-%d'),
                                    patient_id=1)

    db.session.add(jdfirstvisit)

    bluecross = Insurance(name='Blue Cross Blue Shield',
                          address='123 Main St', status='Active', patient_id=1)

    db.session.add(bluecross)

    medication = Medication(medication='Tylenol', description='fever', dosage='2 tab',
                            frequency='1 day', side_effects='headache', interactions='paracetamol')
    prescription = Prescription(patient_name="John", physician_name='jake',
                                medication='tylenol', dosage='2 tab', frequency='1 day', filled_by='bob', pharmacist_name='bob')

    db.session.add(medication)
    db.session.add(prescription)

    john_vital_sign = VitalSign(
        body_temperature='98.6', pulse_rate='60', respiratory_rate='20', blood_pressure='120/80', encounter_id=1)

    db.session.add(john_vital_sign)

    bob_date = datetime.strptime('2007-01-15', '%Y-%m-%d')
    bob_ordr = LabOrder(lab_order_date=datetime.strptime('2007-01-15', '%Y-%m-%d'), test_name="Blood Pressure", patient_name="Bob Builder",
                        physician_name="John Doe", lab_test_result="130", lab_test_technician="John Mann", lab_test_date=datetime.strptime('2019-11-29', '%Y-%m-%d'))
    db.session.add(bob_ordr)

    TestBp = LabTest(lab_test_name="Blood Pressure",
                     low_normal_results="80", high_normal_results="100")
    db.session.add(TestBp)

    TestCscree = LabTest(lab_test_name="Cancer Screening",
                         low_normal_results="Negative", high_normal_results="")
    db.session.add(TestCscree)

    bobbb = LabOrder(lab_order_date=datetime.strptime('2010-11-15', '%Y-%m-%d'), test_name="Cancer Screening", patient_name="Bob Builder",
                     physician_name="Jacob Deer", lab_test_result="Positive", lab_test_technician="John Mann", lab_test_date=datetime.strptime('2023-11-29', '%Y-%m-%d'))
    db.session.add(bobbb)

    GoodOrdrr = LabOrder(lab_order_date=datetime.strptime('2017-05-25', '%Y-%m-%d'), test_name="Blood Pressure", patient_name="Guy Health",
                         physician_name="John Doe", lab_test_result="82", lab_test_technician="John Mann", lab_test_date=datetime.strptime('2020-06-18', '%Y-%m-%d'))
    db.session.add(GoodOrdrr)

    nocancer = LabOrder(lab_order_date=datetime.strptime('2019-04-12', '%Y-%m-%d'), test_name="Cancer Screening", patient_name="Guy Health",
                        physician_name="Jacob Deer", lab_test_result="Negative", lab_test_technician="John Mann", lab_test_date=datetime.strptime('2020-06-18', '%Y-%m-%d'))
    db.session.add(nocancer)

    equipment_1 = Equipment(type='Computer', description='Dell Laptop',
                            department='IT', is_leased=False, is_owned=True)
    equipment_2 = Equipment(type='Printer', description='HP LaserJet Printer',
                            department='Admin', is_leased=False, is_owned=False)
    equipment_3 = Equipment(type='Projector', description='Epson Multimedia',
                            department='Sales', is_leased=True, is_owned=False)
    equipment_4 = Equipment(type='Scanner', description='Canon Document',
                            department='HR', is_leased=False, is_owned=True)

    db.session.add_all([equipment_1, equipment_2, equipment_3, equipment_4])
    db.session.commit()

    owned_1 = EquipmentOwned(date_purchased=datetime.now(),
                             warranty_information='2 years', equipment_id=1)
    owned_2 = EquipmentOwned(date_purchased=datetime.now(),
                             warranty_information='3 years', equipment_id=4)

    db.session.add_all([owned_1, owned_2])

    leased_1 = EquipmentLeased(start_date=datetime.now(
    ), end_date=datetime.now(), leasing_company='ABC Inc', equipment_id=3)

    db.session.add(leased_1)

    maintenance_1 = EquipmentMaintenance(type_of_problem='Hardware issue', description_of_problem='Laptop not turning on',
                                         is_resolved=False, description_of_resoltion='', equipment_id=1)

    db.session.add(maintenance_1)

    vendor_1 = Vendors(name='Dell', address='123 Main St',
                       type_of_equipment_provided='Computers', is_preferred_vendor=True, equipment_id=1)

    db.session.add(vendor_1)

    vendors = Vendors(name='builder', address='mira roam road',
                      type_of_equipment_provided='Blood Pressure Monitor', is_preferred_vendor=True, equipment_id=1)
    mri_equipment = Equipment(type='MRI', description='Magnetic Resonance Imaging',
                              department='Radiology', is_leased=False, is_owned=True)
    blood_pressure_equipment = Equipment(
        type='Blood Pressure Monitor', description='Blood Pressure Monitor', department='Cardiology', is_leased=False, is_owned=True)

    logitics_llc_vendor = Vendors(name='Logistics LLC', address='1234 Main Street, Anytown, USA',
                                  type_of_equipment_provided='MRI', is_preferred_vendor=True, equipment_id=1)
    plug_issue_1 = EquipmentMaintenance(type_of_problem='plug issue', description_of_problem='plug is not working',
                                        is_resolved=False, description_of_resoltion='plug is replaced', equipment_id=1)

    db.session.add(user)
    db.session.add(plug_issue_1)
    db.session.add(john_vital_sign)
    db.session.add(mri_equipment)
    db.session.add(blood_pressure_equipment)
    db.session.add(logitics_llc_vendor)
    db.session.commit()
