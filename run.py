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
    from model import db, User, LabOrder, LabTest




# Routes


@app.route('/', methods=['POST', 'GET'])
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    else:
        return redirect(url_for('admin'))




#@app.route('/delete/<int:id>', methods=['GET', 'POST'])
#def delete(id):
#    task_to_delete = Todo.query.get_or_404(id)
#

#    try:
#        db.session.delete(task_to_delete)
#        db.session.commit()
#        return redirect('/')
#    except:
#        return 'There was a problem deleting that task'




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



################ Shane Start Here #########################


@app.route('/lab_tracking/', methods=['POST', 'GET'])
def lab_tracking():
    #if request.method == 'POST':
        #ordr_ptname = request.form['ptname']
        #ordr_phname = request.form['phname']
        #ordr_lbtech = request.form['lbtech']
        #ordr_lbresult = request.form['lbresult']


        #new_ordr = LabOrder(patient_name = ordr_ptname, physician_name = ordr_phname, lab_test_result = ordr_lbresult, lab_test_technician = ordr_lbtech)


        #db.session.add(new_ordr)
        #print('adding lab data ' )#all this print data is to check the values are correct
        #print('Patient name - ' + new_ordr.patient_name)
        #print('Physician name - ' + new_ordr.physician_name)
        #print('Lab name - ' + new_ordr.lab_test_result)
        #print('Lab Tech - ' + new_ordr.lab_test_technician)
        #db.session.commit()
        #print('successfully committed')
        #return redirect('/lab_tracking/')


    #else:
        orders = LabOrder.query.order_by(LabOrder.id).all()
        return render_template('lab_tracking.html', orders=orders)


@app.route('/lab_tracking/delete_lab_order/<int:id>')
def delete(id):
    order_deleting = LabOrder.query.get_or_404(id)


    db.session.delete(order_deleting)
    db.session.commit()
    return redirect('/lab_tracking/')
    

    
@app.route('/lab_tracking_add_order/', methods =['POST', 'GET'])
def lab_tracking_add_order():
    if request.method == 'POST':
        ordr_ptname = request.form['ptname']
        ordr_phname = request.form['phname']
        ordr_lbtech = request.form['lbtech']
        ordr_lbresult = request.form['lbresult']
        ordr_timetemp = (request.form.get('lbdate') + ' ' + request.form.get('lbtime'))
        ordr_lbdate = datetime.strptime(ordr_timetemp,'%Y-%m-%d %H:%M:%S')


        new_ordr = LabOrder(patient_name = ordr_ptname, physician_name = ordr_phname, lab_test_result = ordr_lbresult, lab_test_technician = ordr_lbtech, lab_test_date = ordr_lbdate)


        db.session.add(new_ordr)

        db.session.commit()
        print('successfully committed')
        return redirect('/lab_tracking_add_order/')


    else:
        orders = LabOrder.query.order_by(LabOrder.id).all()
        return render_template('lab_tracking_add_order.html', orders=orders)
    

@app.route('/lab_tracking_add_test/', methods =['POST', 'GET'])
def lab_tracking_add_test():
    if request.method == 'POST':
        print(request.form.get('testname'))
        lab_testname = request.form['testname']
        lab_lowrange = request.form['lowrange']
        lab_highrange = request.form['highrange']
        if(lab_lowrange == ""):
            healthyrange = lab_highrange
        elif( lab_highrange == ""):
            healthyrange = lab_lowrange
        else:
            healthyrange =  lab_lowrange + ' - ' + lab_highrange


        new_test = LabTest(lab_test_name = lab_testname, range_of_normal_results = healthyrange)


        db.session.add(new_test)

        db.session.commit()
        print('successfully committed')
        return redirect('/lab_tracking_add_test/')


    else:
        orders = LabOrder.query.order_by(LabOrder.id).all()
        return render_template('lab_tracking_add_test.html', orders=orders)
    
    
############################# Shane End Here #####################################

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))




@ login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))




if __name__ == '__main__':
    app.run(debug=True, port=5002)




