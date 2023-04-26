import sys


from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

from forms import RegistrationForm, LoginForm
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


# Word around so autopep8 E402 doesn't formats import after app = Flask(__name__)
if not 'models' in sys.modules:
    from model import db, User, LabOrder, LabTest, Prescription, Medication


# Routes


@app.route('/', methods=['POST', 'GET'])
def index():
    # if logged in
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')


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

        # if searcht == 'patient':
        #     # get the search query from the form
        #     search_query = request.form['search_query']

        #     # search for lab orders by patient name
        #     orders = LabOrder.query.filter(
        #         LabOrder.patient_name.ilike(f'%{search_query}%')).all()
        #     # render the template with the search results
        #     orders = [order for order in orders if start_date_obj <=
        #               order.lab_test_date <= end_date_obj]

        # elif searcht == 'physician':

        #     search_query = request.form['search_query']
        #     orders = LabOrder.query.filter(
        #         LabOrder.physician_name.ilike(f'%{search_query}%')).all()
        #     orders = [order for order in orders if start_date_obj <=
        #               order.lab_order_date <= end_date_obj]

        # elif searcht == 'test':
        #     labtest_id = int(request.form.get('lab_tester'))
        #     test = LabTest.query.get(labtest_id)
        #     search_query = test.lab_test_name
        #     orders = LabOrder.query.filter(
        #         LabOrder.test_name.ilike(f'%{search_query}%')).all()
        #     orders = [order for order in orders if start_date_obj <=
        #               order.lab_order_date <= end_date_obj]

        # elif searcht == 'labphy':
        #     labtest_id = int(request.form.get('lab_tester'))
        #     labrid = LabTest.query.get(labtest_id)
        #     labtest_name = labrid.lab_test_name

        #     physician_name = request.form.get('search_query')
        #     orders = LabOrder.query.filter(LabOrder.physician_name.ilike(
        #         f'%{physician_name}%'), LabOrder.test_name == labtest_name).all()
        #     orders = [order for order in orders if start_date_obj <=
        #               order.lab_order_date <= end_date_obj]

        orders = [order for order in orders if start_date_obj <=
                  order.lab_test_date <= end_date_obj]
        sort = request.args.get('sort', 'id')
        # if sort == 'patient_name':
        #     orders = LabOrder.query.order_by(LabOrder.id).all()

        # elif sort == 'test_name':
        #    orders = LabOrder.query.order_by(func.lower(LabOrder.test_name)).all()
        # elif sort == 'lab_test_result':
        #    orders = LabOrder.query.order_by(LabOrder.lab_test_result).all()
        # elif sort == 'lab_order_date':
        #     orders = LabOrder.query.order_by(LabOrder.lab_order_date).all()
        # elif sort == 'lab_test_date':
        #     orders = LabOrder.query.order_by(LabOrder.lab_test_date).all()
        # elif sort == 'physician_name':
        #     orders = LabOrder.query.order_by(
        #         func.lower(LabOrder.physician_name)).all()
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

        new_ordr = LabOrder(lab_order_date=ordr_lbodate, test_name=ordr_lbtestname, patient_name=ordr_ptname,
                            physician_name=ordr_phname, lab_test_result=ordr_lbresult, lab_test_technician=ordr_lbtech, lab_test_date=ordr_lbdate)

        db.session.add(new_ordr)

        db.session.commit()
        print('successfully committed')
        flash('Lab order added successfully')
        return redirect('/lab_tracking_add_order/')

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
        return redirect('/lab_tracking_add_test/')

    else:
        lab_test = LabTest.query.order_by(LabTest.lab_test_name).all()
        orders = LabOrder.query.order_by(LabOrder.id).all()
        return render_template('lab_tracking_add_test.html', orders=orders, lab_test=lab_test)


############################# Shane End Here #####################################

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

############################# Shweta Starts Here #####################################

# Route for Create Prescription


@app.route('/create_prescription', methods=['POST', 'GET'])
def create_prescription():
    # return render_template('pharmacy_create_prescription.html')
    if request.method == 'POST':
        patient_name = request.form['patient_name']
        physician_name = request.form.get("PhysicianName")
        medication = request.form.get('Medication')
        dosage = request.form.get('dosage')
        frequency = request.form.get('frequency')
        filled_by = request.form.get('filled_by')
        pharmacist_name = request.form.get('pharmacist_name')
       # med_enc=request.form.get('med_enc')
        Details = Prescription(patient_name=patient_name, physician_name=physician_name, medication=medication,
                               dosage=dosage, frequency=frequency, filled_by=filled_by, pharmacist_name=pharmacist_name)
        db.session.add(Details)
        db.session.commit()
        flash(f'Prescription added!', 'success')
        return redirect(url_for('create_prescription'))

    else:
        return render_template('pharmacy_create_prescription.html')

    # Route for retrieve Prescription # this is an extra route which is currently unused


@app.route('/generate_report', methods=['POST', 'GET'])
def retrieve_prescription():
    # return render_template('create_prescription.html')
    tasks = Prescription.query.order_by(Prescription.id).all()
    return render_template('pharmacy_generate_report.html', tasks=tasks)

# this is the current route used for retrieving based on the id or name and prescription name


@app.route('/retrieve_prescription_based', methods=['POST', 'GET'])
def retrieve_prescription_based():
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
@app.route('/add_medication', methods=['POST', 'GET'])
def add_medication():
    if request.method == 'POST':

        medication = request.form.get('Medication')
        description = request.form.get('desc')
        dosage = request.form.get('dosage')
        frequency = request.form.get('frequency')
        side_effects = request.form.get('side_effects')
        interactions = request.form.get('interactions')
        Details = Medication(medication=medication, description=description, dosage=dosage,
                             frequency=frequency, side_effects=side_effects, interactions=interactions)
        db.session.add(Details)
        db.session.commit()
        flash(f'Prescription added!', 'success')
        return redirect(url_for('add_medication'))

    else:
        return render_template('pharmacy_add_medication.html')

     # Route for retrieve Medications


@app.route('/retrieve_medication', methods=['POST', 'GET'])
def retrieve_medication():
    # return render_template('create_prescription.html')
    # tasks = Medication.query.order_by(Medication.id).all()
    # eturn render_template('retrieve_medication.html', tasks=tasks)
    month = request.form.get('mon')
    physician_name = request.form.get('physician_name')
    physician_prescriptions = db.session.query(
        Prescription.physician_name,

        db.func.count(Prescription.medication).label('count')
    ).filter(func.strftime('%m', Prescription.date_filled) == month,
             Prescription.physician_name == physician_name).all()
    return render_template('pharmacy_retrieve_medication.html', output=physician_prescriptions)


############################# Shweta End Here #####################################

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
    app.run(debug=True, port=5002)
