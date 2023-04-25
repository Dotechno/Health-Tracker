import sys

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

from forms import RegistrationForm, LoginForm
from datetime import date, datetime
from sqlalchemy import func


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
    from model import db, User, Prescription, Medication


# Routes

@app.route('/', methods=['POST', 'GET'])
def index():
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


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

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
