import sys

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

from forms import PatientForm, RegistrationForm, LoginForm, MedicalEncounterForm
from datetime import datetime

# Initialize app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'arbitrarySecretKey'

# db = SQLAlchemy(app)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

# Word around so autopep8 E402 doesn't formats import after app = Flask(__name__)
if not 'models' in sys.modules:
    from model import db, User, Patient, MedicalEncounter


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



@app.route('/patient', methods=['GET','POST'])
def create_patient():
    form = PatientForm()
    if request.method == 'POST':
        name=form.name.data
        telephone=form.telephone.data
        address=form.address.data
        date_of_birth=form.date_of_birth.data
        gender=form.gender.data
        # push to db without validation
        patient = Patient(name=name, telephone=telephone, address=address, date_of_birth=date_of_birth, gender=gender)
        db.session.add(patient)
        db.session.commit()
        
        return "Good job"

    return render_template('patient.html', form=form)
    

@app.route('/medical_encounter', methods=['GET','POST'])
def create_medical_encounter():
    form = MedicalEncounterForm()
    if request.method == 'POST':
        encounter_date=form.encounter_date.data
        practitioner_type=form.practitioner_type.data
        complaint=form.complaint.data
        diagnosis=form.diagnosis.data
        treatment=form.treatment.data
        referral=form.referral.data
        recommended_followup=form.recommended_followup.data
        notes=form.notes.data
        submission_date=form.submission_date.data
        patient_id=Patient.query.filter_by(name=form.patient_name.data).first().id
        
        # push to db without validation
        medical_encounter = MedicalEncounter(encounter_date=encounter_date, practitioner_type=practitioner_type, complaint=complaint, diagnosis=diagnosis, treatment=treatment, referral=referral, recommended_followup=recommended_followup, notes=notes, submission_date=submission_date, patient_id=patient_id)
        db.session.add(medical_encounter)
        db.session.commit()
        
        return "Good job"

    return render_template('medical_encounter.html', form=form)


#Create a form similar to login and fill that in

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


if __name__ == '__main__':
    app.run(debug=True, port=5002)
