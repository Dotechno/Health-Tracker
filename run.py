import sys

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

from forms import RegistrationForm, LoginForm
from datetime import datetime

# Initialize app
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_BINDS']={'prescription':'sqlite:///prescription.db',
                                'medication':'sqlite:///medication.db'}



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
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    else:
        return redirect(url_for('admin'))


@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.title = request.form['title']
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'
    else:
        return render_template('upda\watchte.html', task=task)


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

# Route for Create Prescription

@app.route('/create_prescription', methods=['POST', 'GET'])
def create_prescription():
    #return render_template('create_prescription.html')
    if request.method == 'POST':
        
        id=request.form['id']
        physician_name=request.form.get("PhysicianName")
        medication=request.form.get('Medication')
        dosage=request.form.get('dosage')
        frequency=request.form.get('frequency')
        filled_by=request.form.get('filled_by')
        Details=Prescription(id=id,physician_name=physician_name,medication=medication,dosage=dosage,frequency=frequency,filled_by=filled_by)
        db.session.add(Details)
        db.session.commit()
        flash(f'Prescription added!', 'success')
        return redirect(url_for('create_prescription'))



    else:
        return render_template('create_prescription.html')
    
    # Route for retrieve Prescription

@app.route('/retrieve_prescription', methods=['POST', 'GET'])
def retrieve_prescription():
    #return render_template('create_prescription.html')
    tasks = Prescription.query.order_by(Prescription.id).all()
    return render_template('retrieve_prescription.html', tasks=tasks)


# Route for adding medication
@app.route('/add_medication', methods=['POST', 'GET'])
def add_medication():
    if request.method == 'POST':
        
        id=request.form['id']
        medication=request.form.get('Medication')
        description=request.form.get('desc')
        dosage=request.form.get('dosage')
        frequency=request.form.get('frequency')
        side_effects=request.form.get('side_effects')
        interactions=request.form.get('interactions')
        Details=Medication(id=id,medication=medication,description=description,dosage=dosage,frequency=frequency,side_effects=side_effects,interactions=interactions)
        db.session.add(Details)
        db.session.commit()
        flash(f'Prescription added!', 'success')
        return redirect(url_for('add_medication'))



    else:
        return render_template('add_medication.html')
     # Route for retrieve Medications

@app.route('/retrieve_medication', methods=['POST', 'GET'])
def retrieve_medication():
    #return render_template('create_prescription.html')
    tasks = Medication.query.order_by(Medication.id).all()
    return render_template('retrieve_medication.html', tasks=tasks)


@ login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


if __name__ == '__main__':
    app.run(debug=True, port=5002)
