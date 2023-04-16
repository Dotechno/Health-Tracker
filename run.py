import sys



from flask import Flask, abort, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

from forms import RegistrationForm, LoginForm, SearchForm
from datetime import datetime
from Billing import cost


# Initialize app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'arbitrarySecretKey'


# db = SQLAlchemy(app)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

# Word around so autopep8 E402 doesn't formats import after app = Flask(__name__)
if not 'models' in sys.modules:
    from model import db, User, Patient, MedicalEncounter, Prescription, Physician, ServiceProvidedByClinic, Appointment, LabOrder,Insurance, Invoice, InvoiceLineItem
# Routes


@app.route('/', methods=['POST', 'GET'])
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    else:
        return redirect(url_for('admin'))



@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('admin'))

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
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {username}!', 'success')
        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('admin'))

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
            return redirect(url_for('admin'))
        else:
            # Invalid credentials, show error message
            flash('Login Unsuccessful. Please check username and password', 'danger')
            return render_template('login.html', form=form, title='Login', login_error=True)


@app.route('/admin')
def admin():
    users = User.query.order_by(User.username).all()
    return render_template('admin.html', users=users)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@ login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/insurance_billing', methods=['GET', 'POST'])
def InsuranceBilling():
    if request.method == 'POST':
        find = request.form["PatientName"]
        find = "John Doe"
        # find the patient names
        
        patient = Patient.query.filter_by(name=find).first()
        if patient is None:
            return render_template('insurance_billing.html', is_get=True)
        
        all_me = MedicalEncounter.query.order_by(MedicalEncounter.date.asc()).all()
        print(all_me)
        physician = Physician.query.filter_by(patient_id=patient.id).first()
        insurance = Insurance.query.filter_by(patient_id=patient.id).first()
        # query all the prescriptions from db not only from the patient
        # prescriptions = Prescription.query.filter_by(medical_encounter_id=me.id).all()
        all_prescriptions = Prescription.query.all()
        me_list = []
        for me in all_me:
            if me.patient_id == patient.id:
                me.list = me_list.append(me)

        
        # filters the prescriptions that belong to the patient
        prescriptions = []
        refill = []
        for prescription in all_prescriptions:
            if prescription.medical_encounter_id == me.id:
                prescriptions.append(prescription)
                refill.append(prescription.date)
        
        all_lab_order = LabOrder.query.all()

        lab_order_list = []
        lab_order_list_dates = []
        for labOrder in all_lab_order:
            if labOrder.medical_encounter_id == me.id:
                lab_order_list.append(labOrder)
                lab_order_list_dates.append(labOrder.date)

        # add a new service to the patient medical encounter and use a unique id
        
        costs = (cost['Physician'] * len(me_list)) + (cost['Prescription'] * len(prescriptions)) + (cost['Laborder'] * len(lab_order_list))

        # TODO: Add the following snippet to lab order med. encounter prescription form submission
        # for prescription in prescriptions:
        #     service = ServiceProvidedByClinic(date = prescription.date ,service_description= prescription.name, cost_for_service= cost['Prescription'], patient_id = patient.id )
        #     db.session.add(service)
        #     db.session.commit()

        # for labOrder in lab_order_list:
        #     service = ServiceProvidedByClinic(date = labOrder.date ,service_description= labOrder.name, cost_for_service= cost['Laborder'] , patient_id = patient.id )
        #     db.session.add(service)
        #     db.session.commit()

        # for me in me_list:
        #     service = ServiceProvidedByClinic(date = me.date ,service_description= me.encounter, cost_for_service= cost['Physician'] , patient_id = patient.id)
        #     db.session.add(service)
        #     db.session.commit()
        
        all_service  = ServiceProvidedByClinic.query.order_by(ServiceProvidedByClinic.date.asc()).all()
        services = []
        
        for service in all_service:
            if service.patient_id == patient.id:
                services.append(service)
                
        personInfo = {
            'name': patient.name,
            'ME': me.encounter,
            'service': service.cost_for_service,
            "Carrier_Name": insurance.name,
            "Insurance_address": insurance.address,
        }
        return render_template('insurance_billing.html', PatientInfo=personInfo,services = services, is_get=False)
    else:
        return render_template('insurance_billing.html', is_get=True)


@app.route('/invoices', methods=['GET', 'POST'])
def generate_invoice():
    if request.method == 'POST':
        patient_name = request.form['patient_name']
        insurance_carrier_id = request.form['insurance_carrier_id']
        service_ids = request.form.getlist('service_ids')
        invoice = Invoice(patient_name=patient_name, insurance_carrier_id=insurance_carrier_id, total_cost=0.0)
        db.session.add(invoice)
        db.session.commit()
        for service_id in service_ids:
            service = ServiceProvidedByClinic.query.get(service_id)
            line_item = InvoiceLineItem(invoice_id=invoice.id, service_id=service_id, date=datetime.now(),
                                        cost=service.cost, status='unpaid')
            db.session.add(line_item)
            invoice.total_cost += service.cost
        db.session.commit()
        return redirect(url_for('get_invoice', invoice_id=invoice.id))
    else:
        insurance_carriers = Insurance.query.all()
        services = ServiceProvidedByClinic.query.all()
        return render_template('invoices.html', insurance_carriers=insurance_carriers, services=services)

@app.route('/invoices/<int:invoice_id>')
def get_invoice(invoice_id):
    invoice = Invoice.query.get(invoice_id)
    if not invoice:
        abort(404)
    items = InvoiceLineItem.query.filter_by(invoice_id=invoice_id).all()
    return render_template('invoice.html', invoice=invoice, items=items)


# @app.route('/search_insurance/<find>', methods=['GET', 'POST'])
# def SearchInsurance(find):
#     if request.method == 'POST':
#         find = request.form["PatientName"]
#         return redirect(url_for('InsuranceBilling', find=find))
#     else:
#         return render_template('search_insurance.html', is_get=True)



if __name__ == '__main__':
    app.run(debug=True, port=5002)
