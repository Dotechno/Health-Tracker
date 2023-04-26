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
app.config['SECRET_KEY'] = 'arbitrarySecretKey'

# db = SQLAlchemy(app)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

# Word around so autopep8 E402 doesn't formats import after app = Flask(__name__)
if not 'models' in sys.modules:
    from model import db, User, Equipment, Vendors, EquipmentMaintenance, EquipmentLeased, EquipmentOwned

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

@app.route('/search_equipment/', methods=['GET', 'POST'])
def search_equipment():
    if request.method == 'POST':
        search_item = request.form.get('search_item')
        if search_item:
            equipments = Equipment.query.filter(Equipment.type.like('%'+search_item+'%')).all()
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
        # type
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
        equipment = Equipment(id=equipment_id, type=equipment_type, description=description, department=department, is_leased=is_leased, is_owned=is_owned)
        db.session.add(equipment)
        db.session.commit()
        flash(f'Equipment added!', 'success')
        return redirect(url_for('equipment'))


    equipments = Equipment.query.all()
    return render_template('equipment.html', equipments=equipments)


@app.route('/maintenance_history/<int:equipment_id>',methods=['GET', 'POST'])
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
        description_of_problem = request.form.get('description_of_problem')
        if is_resolved == True:
            is_resolved = True
        else:
            is_resolved = False

        
        history = EquipmentMaintenance(type_of_problem=type_of_problem, description_of_problem=description_of_problem, is_resolved=is_resolved, description_of_resoltion=description_of_problem, equipment_id=equipment_id)
        db.session.add(history)
        db.session.commit()
        return redirect(url_for('maintenance_history', equipment_id=equipment_id))
    else:
        maintenance_history = EquipmentMaintenance.query.filter_by(equipment_id=equipment_id).all()
        equipment = Equipment.query.get(equipment_id)
        return render_template('maintenance_history.html', maintenance_histories=maintenance_history, equipment=equipment)



@app.route('/owned/<int:equipment_id>')
def equipment_owned(equipment_id):
    owned_information = EquipmentOwned.query.filter_by(equipment_id=equipment_id).all()
    equipment = Equipment.query.get(equipment_id)
    return render_template('owned.html', owned_information= owned_information, equipment=equipment)


@app.route('/leased/<int:equipment_id>')
def equipment_leased(equipment_id):
    leased_information = EquipmentLeased.query.all()
    equipment = Equipment.query.get(equipment_id)
    return render_template('leased.html', leased_information=leased_information, equipment=equipment)

@app.route('/vendors', methods=['POST', 'GET'])
def vendors():
    if "GET" == request.method:
        vendor_data = Vendors.query.all()
        return render_template('vendors.html', equipment_data=vendor_data)
    if "POST" == request.method:
        search_item = request.form.get('search_item')
        if search_item:
            vendor_data = Vendors.query.filter(Vendors.name.like('%'+search_item+'%')).all()
            return render_template('vendors.html', equipment_data=vendor_data)

        
        return redirect(url_for('vendors'))


@ login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


if __name__ == '__main__':
    app.run(debug=True, port=5002)
