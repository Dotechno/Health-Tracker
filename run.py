import sys

from flask import Flask, abort, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import random
import string
import appointment
import json

from forms import PatientForm, RegistrationForm, LoginForm, MedicalEncounterForm, PhysicianRegistrationForm
from datetime import datetime, timedelta

# Initialize app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
app.config['SQLALCHEMY_BINDS'] = {'prescription': 'sqlite:///prescription.db',
                                  'medication': 'sqlite:///medication.db'}

app.config['SECRET_KEY'] = 'arbitrarySecretKey'


# db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

# Work around autopep8 E402
if True:
    from CONSTANT import *


# Work around so autopep8 E402 doesn't formats import after app = Flask(__name__)
if not 'models' in sys.modules:
    from model import (db, User, LabOrder, LabTest, Prescription, Medication, Patient,
                       MedicalEncounter, Physician, Insurance, Appointment, Equipment,
                       Vendors, EquipmentMaintenance, EquipmentLeased, EquipmentOwned,
                       ServiceProvidedByClinic, Invoice, InvoiceLineItem
                       )

# Routes


@app.route('/', methods=['POST', 'GET'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'GET':
        form = RegistrationForm()
        return render_template('register.html', title='Register', form=form)

    # if post request
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        roles = request.form.get('roles')
        hashed_password = bcrypt.generate_password_hash(
            password).decode('utf-8')
        user = User(username=username, password=hashed_password, roles=roles)

        # check for duplicate username
        if User.query.filter_by(username=username).first():
            flash('Username already exists!', 'danger')
            return redirect(url_for('register'))

        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {username}!', 'success')
        return redirect(url_for('login'))


@app.route('/register_physician', methods=['GET', 'POST'])
def register_physician():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'GET':
        form = PhysicianRegistrationForm()
        return render_template('register_physician.html', title='Register', form=form)

    # if post request
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        roles = request.form.get('roles')
        hashed_password = bcrypt.generate_password_hash(
            password).decode('utf-8')
        user = User(username=username, password=hashed_password, roles=roles)

        # check for duplicate username
        if User.query.filter_by(username=username).first():
            flash('Username already exists!', 'danger')
            return redirect(url_for('register_physician'))

        # physician_name = request.form.get('physician_name')
        # cell_phone_number = request.form.get('cell_phone_number')
        # work_time_start = request.form.get('work_time_start')
        # work_time_end = request.form.get('work_time_end')
        # work_days = request.form.get('work_days')
        # days_working = ' '.join([str(elem) for elem in work_days])

        # physician = Physician(physician_name=username,
        #                       cell_phone_number=cell_phone_number, work_time_start=work_time_start,
        #                       work_time_end=work_time_end, work_days=work_days)

        data = request.get_json()
        name = data['physicianName']
        phone_number = data['cellPhoneNumber']
        start_time = data['workTimeStart']
        end_time = data['workTimeEnd']
        start_time_obj = datetime.strptime(start_time, '%H:%M')
        start_time = start_time_obj.strftime('%H:%M:%S')
        end_time_obj = datetime.strptime(end_time, '%H:%M')
        end_time = end_time_obj.strftime('%H:%M:%S')

        days_working = ' '.join([str(elem) for elem in data['workDays']])
        new_physcian = Physician(physician_name=name, cell_phone_number=phone_number,
                                 work_time_start=start_time, work_time_end=end_time, work_days=days_working)

        db.session.add(user)
        db.session.add(physician)

        db.session.commit()
        flash(f'Account created for {username}!', 'success')
        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'GET':
        return render_template('login.html', form=form, title='Login')

    # If post request
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            # Valid credentials, log user in and redirect to homepage
            flash(f'Logged in as {username}!', 'success')
            login_user(user, remember=form.remember.data)
            return redirect(url_for('dashboard'))
        else:
            # Invalid credentials, show error message
            flash('Login Unsuccessful. Please check username and password', 'danger')
            return render_template('login.html', form=form, title='Login', login_error=True)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if request.method == 'GET':
        current_user_name = current_user.username
        # check for capitalizations for first letters
        current_user_name = current_user_name.title()
        print(current_user_name)
        return render_template('dashboard.html', loggedin_user=current_user_name)


@app.route('/demo_dashboard', methods=['GET', 'POST'])
def demo_dashboard():
    # check for capitalizations for first letters
    return render_template('demo_dashboard.html')


@app.route('/admin')
@login_required
def admin():
    if current_user.roles != 'admin':
        # loguser out if not admin
        logout_user()
        return redirect(url_for('index'))
    users = User.query.order_by(User.username).all()
    return render_template('admin.html', users=users)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


#################### Charzezard Start Here ####################


@app.route('/create_patient', methods=['GET', 'POST'])
def create_patient():
    form = PatientForm()
    if request.method == 'POST':
        name = form.name.data
        telephone = form.telephone.data
        address = form.address.data
        date_of_birth = form.date_of_birth.data
        gender = form.gender.data
        insurance = form.insurance.data
        insurance_address = form.insurance_address.data
        insurance_status = form.insurance_status.data
        physician_name = form.physician_name.data

        specific_p = Physician.query.filter_by(
            physician_name=physician_name).first()

        # push to db without validation
        patient = Patient(name=name, telephone=telephone,
                          address=address, date_of_birth=date_of_birth, gender=gender, physician_id=specific_p.id)
        db.session.add(patient)

        all_insurance = Insurance.query.all()

        if not all_insurance:
            print('a')
        else:
            if insurance not in all_insurance:
                insurance = Insurance(
                    name=insurance, address=insurance_address, status=insurance_status, patient_id=patient.id)
                db.session.add(insurance)
        db.session.commit()

        return redirect(url_for('patient'))
    else:

        return render_template('patient_create_patient.html', form=form)


@app.route('/patient', methods=['GET', 'POST'])
def patient():

    patients = Patient.query.order_by(Patient.id).all()

    return render_template('patient.html', patients=patients)


@app.route('/patient/<int:patient_id>/medication', methods=['GET', 'POST'])
def medication(patient_id):
    all_medication = Medication.query.filter_by(patient_id=patient_id).all()
    patient = Patient.query.get(patient_id)
    return render_template('medication.html', medications=all_medication, patient=patient)

@app.route('/patient/<int:patient_id>/appointment', methods=['GET', 'POST'])
def viewappointment(patient_id):
    all_appointment = Appointment.query.filter_by(patient_id=patient_id).all()
    patient = Patient.query.get(patient_id)
    return render_template('appointment.html', all_appointment=all_appointment, patient=patient)



@app.route('/create_medical_encounter', methods=['GET', 'POST'])
def create_medical_encounter():
    form = MedicalEncounterForm()
    form.patient_id.choices = [(patient.id, patient.name)
                               for patient in Patient.query.all()]
    form.practitioner_id.choices = [(user.id, user.roles)
                                    for user in User.query.all()]

    if request.method == 'POST':
        encounter_date = form.encounter_date.data

        practitioner_type = form.practitioner_type.data
        complaint = form.complaint.data
        diagnosis = form.diagnosis.data
        treatment = form.treatment.data
        referral = form.referral.data
        recommended_followup = form.recommended_followup.data
        notes = form.notes.data

        submission_date = form.submission_date.data
        patient_id = form.patient_id.data
        patient = Patient.query.get(patient_id)
        patient_name = patient.name

        employee_id = current_user.id

        medical_encounter = MedicalEncounter(encounter_date=encounter_date, practitioner_type=practitioner_type, complaint=complaint, diagnosis=diagnosis, employee_id = employee_id,
                                             treatment=treatment, referral=referral, recommended_followup=recommended_followup, notes=notes, submission_date=submission_date, patient_id=patient_id)
        db.session.add(medical_encounter)
        db.session.commit()

        return redirect(url_for('medical_encounter'))

    return render_template('patient_create_medical_encounter.html', form=form)


@app.route('/medical_encounter/<int:me_id>/doctor_notes')
def doctor_notes(me_id):
    # if request.method == 'GET':
    Note = MedicalEncounter.query.filter_by(id=me_id).first()
    return render_template('me_doctor_note.html', Note=Note)


@app.route('/medical_encounter', methods=['GET', 'POST'])
def medical_encounter():
    medical_encounters = MedicalEncounter.query.order_by(
        MedicalEncounter.encounter_date).all()

    return render_template('patient_medical_encounter.html', mes=medical_encounters)


@app.route('/create_invoice', methods=['GET', 'POST'])
def create_invoice():
    if request.method == 'POST':
        patient_name = request.form['patient_name']
        insurance_carrier_id = request.form['insurance_carrier_id']
        service_ids = request.form.getlist('service_ids')
        patient = Patient.query.filter_by(name=patient_name).first()

        invoice = Invoice(patient_name=patient_name,
                          insurance_carrier_id=insurance_carrier_id, total_cost=0.0)
        db.session.add(invoice)
        db.session.commit()

        for service_id in service_ids:
            service = ServiceProvidedByClinic.query.get(service_id)
            status = 'unpaid'
            days = (service.due_date - service.date).days
            if (service.due_date - service.date).days < 0:
                status = 'overdue'
                days = (service.date - service.due_date).days
            line_item = InvoiceLineItem(invoice_id=invoice.id, service_id=service_id, date=service.date,
                                        cost=service.cost_for_service, status=status, due_date=service.due_date, number_date=days, date_paid="  ")
            db.session.add(line_item)
            invoice.total_cost += service.cost_for_service
        db.session.commit()
        return redirect(url_for('invoice', invoice_id=invoice.id))
    else:
        insurance_carriers = Insurance.query.all()
        services = ServiceProvidedByClinic.query.all()

        return render_template('billing_create_invoice.html', insurance_carriers=insurance_carriers, services=services)


@app.route('/invoice/<int:invoice_id>', methods=['POST', 'GET'])
def invoice(invoice_id):

    if request.method == 'POST':
        items = InvoiceLineItem.query.filter_by(invoice_id=invoice_id).all()
        for item in items:
            item.status = 'paid'
            item.number_date = 0
            item.date_paid = f'{(datetime.now()).date()}'
        db.session.commit()
        return render_template('billing_success.html')

        # invoice = Invoice.query.get(
        # invoice_id)

        # all_patient = Patient.query.filter_by(name=invoice.patient_name).first()

        # all_me = MedicalEncounter.query.order_by(MedicalEncounter.date.asc()).all()
        # physician = Physician.query.filter_by(patient_id=all_patient.id).first()
        # insurance = Insurance.query.filter_by(patient_id=all_patient.id).first()

        # if not invoice:
        #     abort(404)
        # items = InvoiceLineItem.query.filter_by(invoice_id=invoice_id).all()
        # payment_due_date = datetime.now() + timedelta(days=30)
        # due_date = f"{(payment_due_date - datetime.today()).days}"
        # return render_template('invoice.html', invoice=invoice, items=items, physician=physician, issued_date=due_date,
        #                     payment_due_date=payment_due_date, delta30days=timedelta(days=30), total_cost=invoice.total_cost)
    else:
        invoice = Invoice.query.get(
            invoice_id)

        all_patient = Patient.query.filter_by(
            name=invoice.patient_name).first()

        all_me = MedicalEncounter.query.order_by(
            MedicalEncounter.encounter_date.asc()).all()
        insurance = Insurance.query.filter_by(
            patient_id=all_patient.id).first()

        if not invoice:
            abort(404)

        items = InvoiceLineItem.query.filter_by(invoice_id=invoice_id).all()
        # order it by date
        items.sort(key=lambda x: x.date, reverse=True)

        return render_template('billing_invoice.html', invoice=invoice, items=items,
                               total_cost=invoice.total_cost, patient=all_patient)


@app.route('/create_insurance', methods=['GET', 'POST'])
def create_insurance():
    if request.method == "POST":
        name = request.form['insurance_name']
        address = request.form['insurance_address']
        status = request.form['insurance_status']

        insurance = Insurance(name=name, address=address, status=status)
        db.session.add(insurance)
        db.session.commit()
        return redirect(url_for('patient'))
    else:
        return render_template('billing_create_insurance.html')

#################### Charlie End Here ####################


################ Shane Start Here #########################


@app.route('/lab_tracking/', methods=['POST', 'GET'])
def lab_tracking():

    start_date_obj = datetime.min
    end_date_obj = datetime.max
    lab_test = LabTest.query.order_by(LabTest.lab_test_name).all()
    print(lab_test)
    if request.method == 'POST':

        searcht = request.form.get('search_type')
        start_date = request.form.get('start-date', '')
        end_date = request.form.get('end-date', '')

        if start_date and end_date:  # filter by date search
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
            end_date_obj += timedelta(days=1)
        # orders = LabOrder.query.order_by
        orders = LabOrder.query.order_by(LabOrder.id).all()

        print(start_date_obj)
        print(end_date_obj)

        orders = [order for order in orders if start_date_obj <=
                  order.lab_test_date <= end_date_obj]
        sort = request.args.get('sort', 'id')
    else:
        orders = LabOrder.query.order_by(LabOrder.id).all()
    # lab_test = LabTest.query.filter_by(lab_test_name="Your Test Name").first()
    return render_template('lab_tracking.html', orders=orders, lab_test=lab_test)


@app.route('/lab_tracking/delete_lab_order/<int:id>')
def delete(id):
    order_deleting = LabOrder.query.get_or_404(id)

    db.session.delete(order_deleting)
    db.session.commit()
    return redirect('/lab_tracking/')


@app.route('/lab_tracking_add_order/', methods=['POST', 'GET'])
def lab_tracking_add_order():
    if request.method == 'POST':
        ordr_ptname = request.form['ptname']
        ordr_phname = request.form['phname']
        ordr_lbtech = request.form['lbtech']
        ordr_lbresult = request.form['lbresult']
        # ordr_lbtestname = request.form['testname']
        ordr_timetemp = (request.form.get('lbdate') +
                         ' ' + "00:00:00")
        ordr_lbdate = datetime.strptime(ordr_timetemp, '%Y-%m-%d %H:%M:%S')
        ordr_timetemp = (request.form.get('lbodate') +
                         ' ' + "00:00:00")
        ordr_lbodate = datetime.strptime(ordr_timetemp, '%Y-%m-%d %H:%M:%S')

        lab_test_id = int(request.form.get('lab_test'))
        test = LabTest.query.get(lab_test_id)
        ordr_lbtestname = test.lab_test_name
        # print(lab_test_id, ordr_lbtestname)
        patient_id = Patient.query.filter_by(name=ordr_ptname).first().id
        new_ordr = LabOrder(lab_order_date=ordr_lbodate, test_name=ordr_lbtestname, patient_name=ordr_ptname,
                            physician_name=ordr_phname, lab_test_result=ordr_lbresult, lab_test_technician=ordr_lbtech, lab_test_date=ordr_lbdate)
        service = ServiceProvidedByClinic(service_description=ordr_lbtestname, service_cost=300,
                                          patient_id=patient_id, due_date=datetime.now() + timedelta(days=30), date=datetime.now())
        db.session.add(service)
        db.session.add(new_ordr)

        db.session.commit()
        print('successfully committed')
        flash('Lab order added successfully')
        return redirect('/lab_tracking/')

    else:
        lab_test = LabTest.query.order_by(LabTest.lab_test_name).all()
        # print(lab_test)
        orders = LabOrder.query.order_by(LabOrder.id).all()
        return render_template('lab_tracking_add_order.html', orders=orders, lab_test=lab_test)


@app.route('/lab_tracking_add_test/', methods=['POST', 'GET'])
def lab_tracking_add_test():
    if request.method == 'POST':
        print(request.form.get('testname'))
        lab_testname = request.form['testname']
        lab_result_type = request.form['result_type']
        if lab_result_type == "pos_neg":
            lab_posinegi = request.form.get('posi_negi')
            new_test = LabTest(lab_test_name=lab_testname,
                               low_normal_results=lab_posinegi, high_normal_results='')

        # if(lab_lowrange == ""):
        #    healthyrange = lab_highrange
        #    new_test = LabTest(lab_test_name = lab_testname, low_normal_results = healthyrange)
        # elif( lab_highrange == ""):
        #    healthyrange = lab_lowrange
        #    new_test = LabTest(lab_test_name = lab_testname, low_normal_results = healthyrange)

        else:
            lab_lowrange = request.form.get('lowrange')
            lab_highrange = request.form.get('highrange')
            new_test = LabTest(lab_test_name=lab_testname,
                               low_normal_results=lab_lowrange, high_normal_results=lab_highrange)

        existing_test = LabTest.query.filter_by(
            lab_test_name=lab_testname).first()
        if existing_test:
            flash('A test with this name already exists')

        else:
            # Add the new test to the database
            # new_test = LabTest(name=test_name, low_range=low_range, high_range=high_range)
            db.session.add(new_test)
            db.session.commit()
            flash('Test added successfully')

        # db.session.add(new_test)

        # db.session.commit()
        print('successfully committed')
        return redirect('/lab_tracking/')

    else:
        lab_test = LabTest.query.order_by(LabTest.lab_test_name).all()
        orders = LabOrder.query.order_by(LabOrder.id).all()
        return render_template('lab_tracking_add_test.html', orders=orders, lab_test=lab_test)


############################# Shane End Here #####################################


############################# IAN Starts Here #####################################
@app.route('/search_equipment/', methods=['GET', 'POST'])
def search_equipment():
    if request.method == 'POST':
        search_item = request.form.get('search_item')
        if search_item:
            equipments = Equipment.query.filter(
                Equipment.equipment_type.like('%'+search_item+'%')).all()
            return render_template('equipment.html', equipments=equipments)
        else:
            equipments = Equipment.query.all()
            return render_template('equipment.html', equipments=equipments)
    equipments = Equipment.query.all()
    return redirect(url_for('equipment'))


@app.route("/equipment", methods=['GET', 'POST'])
def equipment():
    if request.method == 'POST':
        # id
        # equipment_type
        # description
        # department
        # is_leased
        # is_owned
        equipment_id = request.form.get('equipment_id')
        equipment_type = request.form.get('equipment_type')
        description = request.form.get('description')
        department = request.form.get('department')
        is_owned = request.form.get('is_owned')
        if is_owned == 'on':
            is_owned = True
            is_leased = False
        else:
            is_owned = False
            is_leased = True
        equipment = Equipment(id=equipment_id, equipment_type=equipment_type, description=description,
                              department=department, is_leased=is_leased, is_owned=is_owned)
        db.session.add(equipment)
        db.session.commit()
        flash(f'Equipment added!', 'success')
        return redirect(url_for('equipment'))

    equipments = Equipment.query.all()
    return render_template('equipment.html', equipments=equipments)


@app.route('/maintenance_history/<int:equipment_id>', methods=['GET', 'POST'])
def maintenance_history(equipment_id):
    if request.method == 'POST':
        # id
        # type_of_problem
        # description_of_problem
        # is_resolved
        # description_of_resoltion
        # equipment_id
        type_of_problem = request.form.get('type_of_problem')
        description_of_problem = request.form.get('description_of_problem')
        is_resolved = request.form.get('is_resolved')
        description_of_resolution = request.form.get(
            'description_of_resolution')
        if is_resolved == True:
            is_resolved = True
        else:
            is_resolved = False

        history = EquipmentMaintenance(type_of_problem=type_of_problem, description_of_problem=description_of_problem,
                                       is_resolved=is_resolved, description_of_resolution=description_of_resolution, equipment_id=equipment_id)
        db.session.add(history)
        db.session.commit()
        return redirect(url_for('maintenance_history', equipment_id=equipment_id))
    else:
        maintenance_history = EquipmentMaintenance.query.filter_by(
            equipment_id=equipment_id).all()
        equipment = Equipment.query.get(equipment_id)
        return render_template('equipment_maintenance_history.html', maintenance_histories=maintenance_history, equipment=equipment)


@app.route('/owned/<int:equipment_id>')
def equipment_owned(equipment_id):
    owned_information = EquipmentOwned.query.filter_by(
        equipment_id=equipment_id).all()
    equipment = Equipment.query.get(equipment_id)
    return render_template('equipment_owned.html', owned_information=owned_information, equipment=equipment)


@app.route('/leased/<int:equipment_id>')
def equipment_leased(equipment_id):
    leased_information = EquipmentLeased.query.all()
    equipment = Equipment.query.get(equipment_id)
    return render_template('equipment_leased.html', leased_information=leased_information, equipment=equipment)


@app.route('/vendors', methods=['POST', 'GET'])
def vendors():
    if "GET" == request.method:
        vendor_data = Vendors.query.all()
        return render_template('equipment_vendors.html', equipment_data=vendor_data)
    if "POST" == request.method:
        search_item = request.form.get('search_item')
        if search_item:
            vendor_data = Vendors.query.filter(
                Vendors.name.like('%'+search_item+'%')).all()
            return render_template('equipment_vendors.html', equipment_data=vendor_data)

        return redirect(url_for('vendors'))
############################# IAN Ends Here #####################################


############################# Shweta Starts Here #####################################

# Route for Create Prescription


@app.route('/pharmacy_create_prescription', methods=['POST', 'GET'])
def pharmacy_create_prescription():
    # return render_template('pharmacy_create_prescription.html')
    if request.method == 'POST':
        patient_name = request.form['patient_name']
        physician_name = request.form.get("PhysicianName")
        medication = request.form.get('Medication')
        dosage = request.form.get('dosage')
        frequency = request.form.get('frequency')
        filled_by = request.form.get('filled_by')
        pharmacist_name = request.form.get('pharmacist_name')
        med_enc = request.form.get('med_enc')
        patient_id = Patient.query.filter_by(name=patient_name).first().id
        details = Prescription(patient_name=patient_name, physician_name=physician_name, medication=medication,
                               dosage=dosage, frequency=frequency, filled_by=filled_by, pharmacist_name=pharmacist_name, medical_encounter_id=med_enc)

        db.session.add(details)
        service = ServiceProvidedByClinic(service_description=medication, cost_for_service=100, patient_id = patient_id, due_date = datetime.now() + timedelta(days=30), date = datetime.now())
        db.session.add(service)
        db.session.commit()
        flash(f'Prescription added!', 'success')

        return redirect(url_for('pharmacy_create_prescription'))

    else:
        mes = MedicalEncounter.query.all()
        return render_template('pharmacy_create_prescription.html', mes=mes)

    # Route for retrieve Prescription # this is an extra route which is currently unused


@app.route('/pharmacy_generate_report', methods=['POST', 'GET'])
def retrieve_prescription():
    # return render_template('create_prescription.html')
    tasks = Prescription.query.order_by(Prescription.id).all()
    return render_template('pharmacy_generate_report.html', tasks=tasks)

# this is the current route used for retrieving based on the id or name and prescription name


@app.route('/pharmacy_retrieve_prescription_based', methods=['POST', 'GET'])
def pharmacy_retrieve_prescription_based():
    if request.method == 'POST':
        id = request.form['prescription_id']
        name = request.form['patient_name']
        medicine = request.form['prescribed_medication']
        tasks = Prescription.query.filter((Prescription.id == id) | (
            (Prescription.patient_name == name) & (Prescription.medication == medicine)))
        return render_template('pharmacy_retrieve_prescription_based.html', tasks=tasks)

    else:
        return render_template('pharmacy_retrieve_prescription_based.html')


# Route for adding medication
@app.route('/pharmacy_add_medication', methods=['POST', 'GET'])
def pharmacy_add_medication():
    if request.method == 'POST':

        medication = request.form.get('Medication')
        description = request.form.get('desc')
        dosage = request.form.get('dosage')
        frequency = request.form.get('frequency')
        side_effects = request.form.get('side_effects')
        interactions = request.form.get('interactions')
        patient_id = request.form.get('patient_id')
        details = Medication(medication=medication, description=description, dosage=dosage,
                             frequency=frequency, side_effects=side_effects, interactions=interactions, patient_id=patient_id)
        db.session.add(details)
        db.session.commit()
        flash(f'Prescription added!', 'success')
        return redirect(url_for('pharmacy_add_medication'))

    else:
        patients = Patient.query.all()
        return render_template('pharmacy_add_medication.html', patients=patients)

     # Route for retrieve Medications


@app.route('/pharmacy_retrieve_medication', methods=['POST', 'GET'])
def pharmacy_retrieve_medication():
    if 'get' == request.method:
        physicians = Physician.query.all()
        return render_template('pharmacy_retrieve_medication.html', physicians=physicians)
    # return render_template('create_prescription.html')
    # tasks = Medication.query.order_by(Medication.id).all()
    # eturn render_template('retrieve_medication.html', tasks=tasks)
    if request.method == 'POST':
        medication_name = request.form.get('medication_id')
        month = request.form.get('mon')
        physician_name = request.form.get('physician_name')
        physician_prescriptions = db.session.query(
            Prescription.physician_name,

            db.func.count(Prescription.medication).label('count')
        ).filter(func.strftime('%m', Prescription.date_filled) == month,
                Prescription.physician_name == physician_name).all()
        physicians = Physician.query.all()
        return render_template('pharmacy_retrieve_medication.html', outputs =physician_prescriptions, physicians = physicians)
    else:
        physicians = Physician.query.all()
        return render_template('pharmacy_retrieve_medication.html', physicians=physicians)


############################# Shweta End Here #####################################

############################# Amar Starts Here #####################################

@app.route("/physician-scheduler", methods=["GET", "POST"])
def physician_scheduler():
    global two_month_appointments, current_physician_id
    if current_user.roles == "admin":
        return physician_home()
    else:
        # get physican id from current_user.username
        current_physician_id = Physician.query.filter_by(
            physician_name=current_user.username).first().id
        physician_selected = find_physician_by_id(current_physician_id)
        physician_appointments = find_appointments_by_physician_id(
            current_physician_id)
        two_month_appointments = appointment.set_up(physician_selected.work_time_start,
                                                    physician_selected.work_time_end,
                                                    physician_selected.work_days,
                                                    physician_appointments)
        this_week = appointment.helper.get_subarray(
            two_month_appointments, current_week_index, 7)
        return render_template("appointments_scheduler.html", data=this_week)


@app.route("/physician-appointments", methods=["GET", "POST"])
def physician_appointments():
    global two_month_appointments, current_physician_id
    # get physican id from current_user.username
    physician_id = request.form.get('physician_id')
    physician_selected = find_physician_by_id(physician_id)
    physician_appointments = find_appointments_by_physician_id(physician_id)
    current_physician_id = physician_id
    two_month_appointments = appointment.set_up(physician_selected.work_time_start,
                                                physician_selected.work_time_end, physician_selected.work_days, physician_appointments)
    this_week = appointment.helper.get_subarray(
        two_month_appointments, current_week_index, 7)
    return render_template("appointments_scheduler.html", data=this_week)


@app.route("/slot_clicked", methods=["POST"])
def slot_clicked():
    global current_week_index
    slot_id = request.form.get('slot_id')
    appointment.helper.update_slot(two_month_appointments, slot_id)
    return ('', 204)


@app.route("/week_selected", methods=["POST"])
def week_selected():
    global current_week_index
    direction = request.form.get('direction')

    if direction == 'left' and current_week_index > MIN_WEEK:
        current_week_index -= 1
    elif direction == 'right' and current_week_index < MAX_WEEK:
        current_week_index += 1
    else:
        return ('', 204)

    return refresh_scheduler_page(current_week_index)


@app.route("/select_all", methods=["POST"])
def select_all():
    global current_week_index
    switch_status = True if request.form.get(
        'switchStatus') == 'true' else False
    day_date = request.form.get('dayDate')
    appointment.helper.select_all_day(
        data=two_month_appointments, date=day_date, status=switch_status)
    return refresh_scheduler_page(current_week_index)


@app.route("/select_week", methods=["POST"])
def select_week():
    global current_week_index
    print(f"current_week_index: {current_week_index}")
    this_week = appointment.helper.get_subarray(
        two_month_appointments, current_week_index, 7)
    appointment.helper.select_all_week(this_week)
    return refresh_scheduler_page(current_week_index)


def refresh_scheduler_page(current_week_index):
    global appointment_type_selected
    this_week = appointment.helper.get_subarray(
        two_month_appointments, current_week_index, 7)
    return render_template("appointments_scheduler.html", data=this_week, appointment_type=appointment_type_selected)


@app.route('/confirm_appointment', methods=['POST'])
def confirm_appointment():
    print("confirm_appointment")
    global get_user_selected_appointments
    get_user_selected_appointments = appointment.helper.get_selected_appointments(
        two_month_appointments)
    print(f"get_user_selected_appointments: {get_user_selected_appointments}")
    return json.dumps({'appointments': get_user_selected_appointments})


@app.route('/physician_redirect', methods=["POST"])
def physician_redirect():
    global appointment_type
    appointment_type = request.form['appointment_type']
    return {'redirect': url_for("physician_home_redirect")}


@app.route('/physician_home_redirect')
def physician_home_redirect():
    global current_physician_id, get_user_selected_appointments, appointment_type
    current_physician = find_physician_by_id(current_physician_id)
    for appointment in get_user_selected_appointments:
        date, hour = appointment.split(" ")
        add_appointment(physician_name=current_physician.physician_name, date_time=appointment, date=date, type=appointment_type,
                        time=hour, physician_id=current_physician.id)
    return render_template('physician.html', data=get_all_physicians(), datetime=datetime, appointments=get_all_appointments())


@app.route('/physician')
def physician_home():
    return render_template('physician.html', data=get_all_physicians(), datetime=datetime, appointments=get_all_appointments())


def find_physician_by_id(physician_id):
    return Physician.query.filter_by(id=physician_id).first()


def get_all_physicians():
    physicians = Physician.query.all()
    return physicians


def find_appointments_by_physician_id(physician_id):
    return Appointment.query.filter_by(physician_id=physician_id).all()


def get_all_appointments():
    appointments = Appointment.query.all()
    return appointments


def add_appointment(physician_name, date_time, date, type, time, physician_id):
    physcian = find_physician_by_id(physician_id)
    new_appointment = Appointment(physician_name=physcian.physician_name, appointment_date_time=date_time,
                                  appointment_date=date, appointment_type=type, appointment_time=time, physician_id=physician_id, patient_id = 1)

    db.session.add(new_appointment)
    date = datetime.strptime(date, '%m/%d/%y')
    service = ServiceProvidedByClinic(service_description=appointment_type, cost_for_service=75, date= date, due_date= date + timedelta(days=30), patient_id=1)
    db.session.add(service)
    db.session.commit()


@app.route('/add_physcian', methods=['POST'])
def add_physcian():
    # if data request is not json, try form
    if request:
        data = request.form
        name = data['physician_name']
        phone_number = data['cell_phone_number']
        start_time = data['work_time_start']
        end_time = data['work_time_end']
        work_days = data['work_days']
        new_physcian = Physician(physician_name=name, cell_phone_number=phone_number,
                                 work_time_start=start_time, work_time_end=end_time, work_days=work_days)
    else:
        data = request.get_json()
        name = data['physicianName']
        phone_number = data['cellPhoneNumber']
        start_time = data['workTimeStart']
        end_time = data['workTimeEnd']
        start_time_obj = datetime.strptime(start_time, '%H:%M')
        start_time = start_time_obj.strftime('%H:%M:%S')
        end_time_obj = datetime.strptime(end_time, '%H:%M')
        end_time = end_time_obj.strftime('%H:%M:%S')

        days_working = ' '.join([str(elem) for elem in data['workDays']])
        new_physcian = Physician(physician_name=name, cell_phone_number=phone_number,
                                 work_time_start=start_time, work_time_end=end_time, work_days=days_working)
    db.session.add(new_physcian)
    db.session.commit()

    return render_template('physician.html', data=get_all_physicians(), datetime=datetime, appointments=get_all_appointments())

############################# Amar End Here #####################################


@ app.route('/pricing')
def pricing():
    return render_template('pricing.html')


# @app.route('/members/<string:username>')
@app.route('/members/')
def members(username=None):
    if username == None:
        return render_template(template_name_or_list='members.html')

    user = User.query.filter_by(username=username).first()
    return render_template('members.html', user=user)


@app.route('/about_us')
def about_us():
    return render_template('about_us.html')


# handles 401
@app.errorhandler(401)
def to401(e):
    # redirect to login page
    return redirect(url_for('login'))

# handles 404


@app.errorhandler(404)
def to404(e):
    return render_template('404.html')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


if __name__ == '__main__':
    app.run(debug=True, port=550, host='0.0.0.0')
