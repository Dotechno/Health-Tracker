import sys

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

from forms import RegistrationForm, LoginForm, SearchForm
from datetime import datetime








# Initialize app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'arbitrarySecretKey'


List = [{
    "name": "Charlie"
}]


# db = SQLAlchemy(app)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

# Word around so autopep8 E402 doesn't formats import after app = Flask(__name__)
if not 'models' in sys.modules:
    from model import db, User, patient, medicalEncounter, prescription, appointment, labOrder, physican

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


@ login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))





@app.route('/InsuranceBilling', methods=['GET','POST'])
def InsuranceBilling():
     if request.method == 'POST':
         Find = request.form["PatientName"]
         name = patient.query.filter_by(name = Find).first()
         ME = medicalEncounter.query.filter_by(id = name.MedicalEncounter_id).first()
         Prescription = prescription.query.filter_by(id = ME.prescription_id).first()
         phyiscian = physican.query.filter_by(id = name.physican_id).first()
         personInfo = {
                'name': name.name,
                'ME': ME.Encounter,
                'Prescription': Prescription.name,
                'Physican': phyiscian.name
            }
         return render_template('InsuranceBilling.html',person = personInfo,Find = Find)
     else:
         return render_template('InsuranceBilling.html')


@app.route('/Founded/<Find>', methods=['GET','POST'])
def Search(Find):
    name = patient.query.filter_by(name = Find).first()
    ME = medicalEncounter.query.filter_by(id = name.MedicalEncounter_id).first()
    return render_template('Search.html', name = name,ME = ME)




    # if request.method == 'POST':
    #     Find = request.form.get('Searches')
    #     name = patient.query.all()
    #     list = patient.query.filter_by(name = Find)
    #     ME = medicalEncounter.query.filter_by(id =patient.MedicalEncounter_id)
    #     if Find != None:
    #         PersonInfo = { 
    #         'Name': list,
    #         'ME': ME
    #         }
    #         return render_template('InsuranceBilling.html', PersonInfo=PersonInfo, name=name)
    #     else:
    #         return render_template('InsuranceBilling.html', error = "No Patient Found", patients=name)

    # return render_template('InsuranceBilling.html', form=form)
    




if __name__ == '__main__':
    app.run(debug=True, port=5002)
