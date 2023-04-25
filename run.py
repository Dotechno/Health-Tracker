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

    start_date_obj = datetime.min
    end_date_obj = datetime.max
    lab_test = LabTest.query.order_by(LabTest.lab_test_name).all()
    print(lab_test)
    if request.method == 'POST':

        searcht = request.form.get('search_type')
        start_date = request.form.get('start-date', '')
        end_date = request.form.get('end-date', '')


        if start_date and end_date: #filter by date search
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
            end_date_obj += timedelta(days=1)

        if searcht == 'patient':
            # get the search query from the form
            search_query = request.form['search_query']

            # search for lab orders by patient name
            orders = LabOrder.query.filter(LabOrder.patient_name.ilike(f'%{search_query}%')).all()
            # render the template with the search results
            orders = [order for order in orders if start_date_obj <= order.lab_test_date <= end_date_obj]

        elif searcht == 'physician':

            search_query = request.form['search_query']
            orders = LabOrder.query.filter(LabOrder.physician_name.ilike(f'%{search_query}%')).all()
            orders = [order for order in orders if start_date_obj <= order.lab_order_date <= end_date_obj]

        elif searcht == 'test':
            labtest_id = int(request.form.get('lab_tester'))
            test = LabTest.query.get(labtest_id)
            search_query = test.lab_test_name
            orders = LabOrder.query.filter(LabOrder.test_name.ilike(f'%{search_query}%')).all()
            orders = [order for order in orders if start_date_obj <= order.lab_order_date <= end_date_obj]

        elif searcht == 'labphy':
            labtest_id = int(request.form.get('lab_tester'))
            labrid = LabTest.query.get(labtest_id)
            labtest_name = labrid.lab_test_name

            physician_name = request.form.get('search_query')
            orders = LabOrder.query.filter(LabOrder.physician_name.ilike(f'%{physician_name}%'), LabOrder.test_name == labtest_name).all()
            orders = [order for order in orders if start_date_obj <= order.lab_order_date <= end_date_obj]

        return render_template('lab_tracking.html', orders=orders, lab_test=lab_test)


    else:
        sort = request.args.get('sort', 'id')
        if sort == 'patient_name':
            orders = LabOrder.query.order_by(func.lower(LabOrder.patient_name)).all()
        #elif sort == 'test_name':
        #    orders = LabOrder.query.order_by(func.lower(LabOrder.test_name)).all()
        #elif sort == 'lab_test_result':
        #    orders = LabOrder.query.order_by(LabOrder.lab_test_result).all()
        elif sort == 'lab_order_date':
            orders = LabOrder.query.order_by(LabOrder.lab_order_date).all()
        elif sort == 'lab_test_date':
            orders = LabOrder.query.order_by(LabOrder.lab_test_date).all()
        elif sort == 'physician_name':
            orders = LabOrder.query.order_by(func.lower(LabOrder.physician_name)).all()
        else: orders = LabOrder.query.order_by(LabOrder.id).all()
        return render_template('lab_tracking.html', orders=orders, lab_test=lab_test)


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
        #ordr_lbtestname = request.form['testname']
        ordr_timetemp = (request.form.get('lbdate') + ' ' + request.form.get('lbtime'))
        ordr_lbdate = datetime.strptime(ordr_timetemp,'%Y-%m-%d %H:%M:%S')
        ordr_timetemp = (request.form.get('lbodate') + ' ' + request.form.get('lbotime'))
        ordr_lbodate = datetime.strptime(ordr_timetemp,'%Y-%m-%d %H:%M:%S')

        lab_test_id = int(request.form.get('lab_test'))
        test = LabTest.query.get(lab_test_id)
        ordr_lbtestname = test.lab_test_name
        #print(lab_test_id, ordr_lbtestname)


        new_ordr = LabOrder(lab_order_date = ordr_lbodate, test_name = ordr_lbtestname, patient_name = ordr_ptname, physician_name = ordr_phname, lab_test_result = ordr_lbresult, lab_test_technician = ordr_lbtech, lab_test_date = ordr_lbdate)


        db.session.add(new_ordr)

        db.session.commit()
        print('successfully committed')
        flash('Lab order added successfully')
        return redirect('/lab_tracking_add_order/')


    else:
        lab_test = LabTest.query.order_by(LabTest.lab_test_name).all()
        #print(lab_test)
        orders = LabOrder.query.order_by(LabOrder.id).all()
        return render_template('lab_tracking_add_order.html', orders=orders, lab_test=lab_test)
    

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

        existing_test = LabTest.query.filter_by(lab_test_name=lab_testname).first()
        if existing_test:
            flash('A test with this name already exists')
            
        else:
            # Add the new test to the database
            #new_test = LabTest(name=test_name, low_range=low_range, high_range=high_range)
            db.session.add(new_test)
            db.session.commit()
            flash('Test added successfully')

        #db.session.add(new_test)

        #db.session.commit()
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
    return redirect(url_for('index'))




@ login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))




if __name__ == '__main__':
    app.run(debug=True, port=5002)




