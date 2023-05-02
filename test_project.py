from run import app

from model import (db, User, LabOrder, LabTest, Prescription, Medication, Patient,
                   MedicalEncounter, Physician, Insurance, Appointment, Equipment,
                   Vendors, EquipmentMaintenance, EquipmentLeased, EquipmentOwned,
                   ServiceProvidedByClinic, Invoice, InvoiceLineItem
                   )

from datetime import datetime

##### INDEX AND BASIC TESTS #####
# prints the current section


def test_index_200(client):
    response = client.get('/')
    assert response.status_code == 200


def test_index_response(client):
    response = client.get('/')
    assert b"Dotechno" in response.data


def test_register_200(client):
    response = client.get('/register')
    assert response.status_code == 200


def test_register_response(client):
    response = client.get('/register')
    assert b"Register" in response.data


def test_register_post_redirect(client):
    # post
    response = client.post('/register', data=dict(
        username='test',
        password='test',
        roles='admin'
    ), follow_redirects=True)
    assert response.status_code == 200


def test_register_post_response(client):
    # check if redirects to login
    response = client.post('/register', data=dict(
        username='test2',
        password='test2',
        roles='admin'
    ), follow_redirects=True)

    with app.app_context():
        user = db.session.query(User).filter_by(username='test2').first()

    assert user.username == 'test2'
    assert b"Login" in response.data


def test_register_physician_200(client):
    response = client.get('/register_physician')
    assert response.status_code == 200


def test_register_physician_response(client):
    response = client.get('/register_physician')
    assert b"Work" in response.data


def test_login_200(client):
    response = client.get('/login')
    assert response.status_code == 200


def test_login_response(client):
    response = client.get('/login')
    assert b"Login" in response.data


def test_logout_functionality(client):
    # login first
    response = client.post('/login', data=dict(
        username='test',
        password='test',
    ), follow_redirects=True)
    assert b"Home" in response.data
    # logout
    response = client.get('/logout', follow_redirects=True)
    assert b"Login" in response.data


def test_login_post_response(client):
    # check if redirects to login
    response = client.post('/login', data=dict(
        username='test',
        password='test',
    ), follow_redirects=True)
    assert b"Home" in response.data


def test_about_us_200(client):
    response = client.get('/about_us')
    assert response.status_code == 200


def test_about_us_response(client):
    response = client.get('/about_us')
    assert b"About Us" in response.data


##### TESTS FOR LABTRACKING PAGES #####
# test add


def test_lab_tracking_add_test(client):
    # post
    response = client.post('/lab_tracking_add_test', data=dict(
        testname='Cancer Screening',
        result_type='pos_neg',
        posi_negi='positive'
    ), follow_redirects=True)
    assert response.status_code == 200

    # check in db
    with app.app_context():
        cancer_screening = db.session.query(LabTest).filter_by(
            lab_test_name='Cancer Screening').first()
    assert cancer_screening.lab_test_name == 'Cancer Screening'
    # assert cancer_screening.posi_negi == 'positive'


def test_lab_tracking_200(client):
    response = client.get('/lab_tracking/')
    assert response.status_code == 200


def test_lab_tracking_response(client):
    # logout
    response = client.get('/logout', follow_redirects=True)
    assert b"Login" in response.data

    # login to test
    response = client.post('/login', data=dict(
        username='test',
        password='test',
    ), follow_redirects=True)
    assert b"Home" in response.data

    response = client.get('/lab_tracking/')
    assert b"Lab Tracker" in response.data


def test_lab_tracking_post_response(client):
    # logout
    response = client.get('/logout', follow_redirects=True)
    assert b"Login" in response.data

    # login to test
    response = client.post('/login', data=dict(
        username='test',
        password='test',
    ), follow_redirects=True)
    assert b"Home" in response.data

    response = client.post('/lab_tracking', data=dict(
        search_type='lab_test_name',
        start_date='2020-01-01',
        end_date='2020-01-01'
    ), follow_redirects=True)
    assert b"Lab Tracker" in response.data


def test_lab_tracking_post_response2(client):
    # logout
    response = client.get('/logout', follow_redirects=True)
    assert b"Login" in response.data

    # login to test
    response = client.post('/login', data=dict(
        username='test',
        password='test',
    ), follow_redirects=True)
    assert b"Home" in response.data

    response = client.post('/lab_tracking', data=dict(
        search_type='lab_test_name',
        start_date='2020-01-01',
        end_date='2020-01-01',
        test_name='Cancer Screening'
    ), follow_redirects=True)
    assert b"Lab Tracker" in response.data

# @app.route('/lab_tracking_add_order/', methods=['POST', 'GET'])
# def lab_tracking_add_order():
#     if request.method == 'POST':
#         ordr_ptname = request.form['ptname']
#         ordr_phname = request.form['phname']
#         ordr_lbtech = request.form['lbtech']
#         ordr_lbresult = request.form['lbresult']
#         # ordr_lbtestname = request.form['testname']
#         ordr_timetemp = (request.form.get('lbdate') +
#                          ' ' + "00:00:00")
#         ordr_lbdate = datetime.strptime(ordr_timetemp, '%Y-%m-%d %H:%M:%S')
#         ordr_timetemp = (request.form.get('lbodate') +
#                          ' ' + "00:00:00")
#         ordr_lbodate = datetime.strptime(ordr_timetemp, '%Y-%m-%d %H:%M:%S')

#         lab_test_id = int(request.form.get('lab_test'))
#         test = LabTest.query.get(lab_test_id)
#         ordr_lbtestname = test.lab_test_name
#         # print(lab_test_id, ordr_lbtestname)
#         patient_id = Patient.query.filter_by(name=ordr_ptname).first().id
#         new_ordr = LabOrder(lab_order_date=ordr_lbodate, test_name=ordr_lbtestname, patient_name=ordr_ptname,
#                             physician_name=ordr_phname, lab_test_result=ordr_lbresult, lab_test_technician=ordr_lbtech, lab_test_date=ordr_lbdate)
#         service = ServiceProvidedByClinic(service_description=ordr_lbtestname, service_cost=300,
#                                           patient_id=patient_id, due_date=datetime.now() + timedelta(days=30), date=datetime.now())
#         db.session.add(service)
#         db.session.add(new_ordr)

#         db.session.commit()
#         print('successfully committed')
#         flash('Lab order added successfully')
#         return redirect('/lab_tracking/')

#     else:
#         lab_test = LabTest.query.order_by(LabTest.lab_test_name).all()
#         # print(lab_test)
#         orders = LabOrder.query.order_by(LabOrder.id).all()
#         return render_template('lab_tracking_add_order.html', orders=orders, lab_test=lab_test)


def test_lab_tracking_add_order(client):
    # logout
    response = client.get('/logout', follow_redirects=True)
    assert b"Login" in response.data

    # login to test
    response = client.post('/login', data=dict(
        username='test',
        password='test',
    ), follow_redirects=True)
    assert b"Home" in response.data

    response = client.post('/lab_tracking_add_order/', data=dict(
        ptname='Bob',
        phname='Dr. Doe',
        lbtech='John',
        lbresult='Positive',
        lbdate=datetime.now(),
        lbodate=datetime.now(),
        lab_test=1
    ), follow_redirects=True)

    with app.app_context():
        order = LabOrder.query.filter_by(
            lbresult='Positive').first()
        assert order.lab_test_result == 'Positive'


##### TESTS FOR PAGES #####


def test_admin_200(client):
    # logout first
    response = client.get('/logout', follow_redirects=True)
    assert b"Login" in response.data

    # attempt to access admin page
    response = client.get('/admin', follow_redirects=True)
    assert b"Login" in response.data

    # login
    response = client.post('/login', data=dict(
        username='test',
        password='test',
    ), follow_redirects=True)
    # access admin page
    response = client.get('/admin', follow_redirects=True)
    assert b"Home" in response.data


# class Patient(db.Model):  # 01
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(200), nullable=False)
#     telephone = db.Column(db.String(200), nullable=False)
#     address = db.Column(db.String(200), nullable=False)
#     date_of_birth = db.Column(db.Date, nullable=False)
#     gender = db.Column(db.String(200), nullable=False)
#     insurance = db.relationship('Insurance', backref='patient')
#     physician_id = db.Column(db.Integer, db.ForeignKey(
#         'physician.id'), nullable=False)
#     medical_encounter = db.relationship(
#         'MedicalEncounter', backref='patient')

#     appointment = db.relationship('Appointment', backref='patient')
#     medication = db.relationship('Medication', backref='patient')

def test_patient_200(client):
    response = client.get('/patient')
    assert response.status_code == 200

##### Test form #####

# class Physician(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     # employee_id = db.Column(db.Integer, nullable=False)
#     physician_name = db.Column(db.String(200), nullable=False)
#     cell_phone_number = db.Column(db.String(200), nullable=False)
#     work_time_start = db.Column(db.Integer, nullable=False)
#     work_time_end = db.Column(db.Integer, nullable=False)
#     work_days = db.Column(db.String(200), nullable=False)
#     patients = db.relationship('Patient', backref='physician')
#     # appointments = db.relationship('Appointment', backref='physician')


def test_create_physican(client):
    client.post('/add_physician', data=dict(
        physician_name='Dr.Doe',
        phone_number='619-555-1234',
        start_time="09:00:00",
        end_time="17:00:00",
        days_working="Monday Wednesday Friday"
    ))

    with app.app_context():
        p = db.session.query(Physician).filter_by(
            physician_name='Dr.Doe').first()

        assert p.physician_name == 'Dr.Doe'
        assert p.cell_phone_number == '619-555-1234'
        assert p.work_time_start == '09:00:00'
        assert p.work_time_end == '17:00:00'
        assert p.work_days == 'Monday Wednesday Friday'


def test_create_patient(client):
    # send a POST request to create a patient
    client.post('patient', data=dict(
        name='John Doe',
        telephone='555-1234',
        address='123 Main St',
        date_of_birth=datetime.now(),
        gender='male',
        physician_id=1
    ))

    # check if the patient was added to the database
    with app.app_context():
        patient = db.session.query(Patient).filter_by(name='John Doe').first()

    assert patient.name == 'John Doe'
    assert patient.telephone == '555-1234'
    assert patient.address == '123 Main St'
    assert patient.gender == 'male'

    # check datetime type for date of birth
    assert isinstance(patient.date_of_birth, datetime)


# class MedicalEncounter(db.Model):  # 02
#     id = db.Column(db.Integer, primary_key=True)
#     employee_id = db.Column(db.Integer, nullable=False)
#     encounter_date = db.Column(db.Date, nullable=False)
#     practitioner_type = db.Column(db.String(200), nullable=False)
#     complaint = db.Column(db.String(200), nullable=False)
#     diagnosis = db.Column(db.String(200), nullable=False)
#     treatment = db.Column(db.String(200), nullable=False)
#     referral = db.Column(db.String(200), nullable=False)
#     recommended_followup = db.Column(db.Date, nullable=False)
#     notes = db.Column(db.String(200), nullable=False)
#     submission_date = db.Column(db.Date, nullable=False)
#     patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
#     lab_order = db.relationship('LabOrder', backref='medical_encounter')
#     vital_signs_id = db.relationship('VitalSign', backref='medical_encounter')
#     prescription = db.relationship('Prescription', backref='medical_encounter')


def test_create_me(client):
    # send a POST request to create a patient
    response = client.post('/create_medical_encounter', data=dict(
        employee_id=1,
        encounter_date=datetime.now(),
        practitioner_type='physician',
        complaint='headache',
        diagnosis='migraine',
        treatment='ibuprofen',
        recommended_followup=datetime.now(),
        referral='none',
        notes='none',
        submission_date=datetime.now(),
        patient_id=1
    ))

    # check if the patient was added to the database
    with app.app_context():
        me = db.session.query(MedicalEncounter).filter_by(
            patient_id=1).first()

    assert me.practitioner_type == 'physician'
    # assert me.complaint == 'headache'
    # assert me.diagnosis == 'migraine'
    # assert me.treatment == 'ibuprofen'
    # assert me.referral == 'none'
    # assert me.notes == 'none'
    # assert me.patient_id == 1


# class Prescription(db.Model):  # 03 Shweta
#     id = db.Column(db.Integer, primary_key=True)
#     patient_name = db.Column(db.String(200), db.ForeignKey(Patient.name))
#     physician_name = db.Column(db.String(200), nullable=False)
#     medication = db.Column(db.String(200), nullable=False)
#     dosage = db.Column(db.Text, nullable=True)
#     frequency = db.Column(db.String(200), nullable=False)
#     filled_by = db.Column(db.String(200), nullable=False)
#     date_filled = db.Column(Date, default=date.today)
#     pharmacist_name = db.Column(db.String(200), nullable=False)
#     medical_encounter_id = db.Column(db.Integer, db.ForeignKey(
#         'medical_encounter.id'), nullable=True)

def test_create_prescription(client):
    response = client.post('/pharmacy_create_prescription', data=dict(
        patient_name='John Doe',
        physician_name='Dr. Doe',
        medication='ibuprofen',
        dosage='200mg',
        frequency='once a day',
        filled_by='Dr. Doe',
        date_filled=datetime.now(),
        pharmacist_name='Dr. Doe',
        medical_encounter_id=1
    ))
    with app.app_context():
        prescription = db.session.query(Prescription).filter_by(
            patient_name="John Doe").first()

    assert prescription.physician_name == 'Dr. Doe'
    assert prescription.medication == 'ibuprofen'
    assert prescription.dosage == '200mg'
    assert prescription.frequency == 'once a day'
    assert prescription.filled_by == 'Dr. Doe'
    assert prescription.pharmacist_name == 'Dr. Doe'

# class Medication(db.Model):  # Shweta
#     id = db.Column(db.Integer, primary_key=True)
#     medication = db.Column(db.String(200), nullable=False)
#     description = db.Column(db.String(500), nullable=False)
#     dosage = db.Column(db.Text, nullable=True)
#     frequency = db.Column(db.String(200), nullable=True)
#     side_effects = db.Column(db.String(200), nullable=True)
#     interactions = db.Column(db.String(200), nullable=True)
#     patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))


def create_medication(client):
    response = client.post('/pharmacy_add_medication', data=dict(
        medication='ibuprofen',
        description='pain reliever',
        dosage='200mg',
        frequency='once a day',
        side_effects='none',
        interactions='none',
        patient_id=1

    ))
    with app.app_context():
        m = db.session.query(Medication).filter_by(
            medication="ibuprofen").first()

    assert m.description == 'pain reliever'
    assert m.dosage == '200mg'
    assert m.frequency == 'once a day'
    assert m.side_effects == 'none'
    assert m.interactions == 'none'
    assert m.patient_id == 1
    assert m.medication == 'ibuprofen'


# class LabOrder(db.Model):  # 05
#     id = db.Column(db.Integer, primary_key=True)
#     patient_name = db.Column(db.String(200), nullable=False)
#     physician_name = db.Column(db.String(200), nullable=False)
#     lab_test_date = db.Column(db.DateTime, nullable=False)
#     lab_test_technician = db.Column(db.String(200), nullable=False)
#     lab_test_result = db.Column(db.String(200), nullable=False)
#     test_name = db.Column(db.String(200), nullable=False)
#     lab_order_date = db.Column(db.DateTime, nullable=False)
#     medical_encounter_id = db.Column(db.Integer, db.ForeignKey(
#         'medical_encounter.id'), nullable=False)
#     lab_test_id = db.Column(db.Integer, db.ForeignKey(
#         'lab_test.id'), nullable=False)


##### END Test form #####


def test_pricing_200(client):
    response = client.get('/pricing')
    assert response.status_code == 200


def test_pricing_response(client):
    response = client.get('/pricing')
    assert b"$25" in response.data


def test_physician_200(client):
    response = client.get('/physician')
    assert response.status_code == 200


def test_physician_home_200(client):
    with app.app_context():
        new_physcian = Physician(physician_name="Mike Anderson", cell_phone_number="619-123-3456",
                                 work_time_start="09:00:00", work_time_end="12:00:00", work_days="Monday Tuesday")
        db.session.add(new_physcian)
        db.session.commit()

        physcian_id = Physician.query.filter_by(id=new_physcian.id).first()

    response = client.post('/physician_home_redirect', data=dict(
        current_physician=physcian_id,
    ), follow_redirects=True)
    assert response.status_code == 405


def test_physician_redirect(client):
    with app.app_context():
        data = {'appointment_type': 'new patient'}
        response = client.post('/physician_redirect', data=data)

        # check that the response status code is 200 (OK)
        assert response.status_code == 200

        # check that the response contains a redirect URL
        response_data = response.get_json()
        assert 'redirect' in response_data
        assert response_data['redirect'] == '/physician_home_redirect'


def test_physician_home_200(client):
    with app.app_context():
        new_physcian = Physician(physician_name="Mike Anderson", cell_phone_number="619-123-3456",
                                 work_time_start="09:00:00", work_time_end="12:00:00", work_days="Monday Tuesday")
        db.session.add(new_physcian)
        db.session.commit()

        physcian_id = Physician.query.filter_by(id=new_physcian.id).first()

    response = client.post('/physician_home_redirect', data=dict(
        current_physician=physcian_id,
    ), follow_redirects=True)
    assert response.status_code == 405


def test_confirm_appointment(appointment, client):
    two_month_appointments = appointment.set_up("09:00:00",
                                                "12:00:00", "Block Out", [])
    get_user_selected_appointments = appointment.helper.get_selected_appointments(
        two_month_appointments)
    data = {'get_user_selected_appointments': get_user_selected_appointments}

    response = client.post('/confirm_appointment', data=data)

    # check that the response status code is 200 (OK)
    assert response.status_code == 200


##### TESTS FOR EXCEPIONS #####

def test_404(client):
    response = client.get('/random')
    assert response.data == b'404'

##### TESTING APPOINTMENT SYSTEM #####
