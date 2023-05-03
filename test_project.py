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


# def test_lab_tracking_add_order(client):
#     # logout
#     response = client.get('/logout', follow_redirects=True)
#     assert b"Login" in response.data

#     # login to test
#     response = client.post('/login', data=dict(
#         username='test',
#         password='test',
#     ), follow_redirects=True)
#     assert b"Home" in response.data

#     # create patient Bob
#     with app.app_context():
#         # class Patient(db.Model):  # 01
#         #     id = db.Column(db.Integer, primary_key=True)
#         #     name = db.Column(db.String(200), nullable=False)
#         #     telephone = db.Column(db.String(200), nullable=False)
#         #     address = db.Column(db.String(200), nullable=False)
#         #     date_of_birth = db.Column(db.Date, nullable=False)
#         #     gender = db.Column(db.String(200), nullable=False)
#         #     insurance = db.relationship('Insurance', backref='patient')
#         #     physician_id = db.Column(db.Integer, db.ForeignKey(
#         #         'physician.id'), nullable=False)
#         #     medical_encounter = db.relationship(
#         #         'MedicalEncounter', backref='patient')

#         #     appointment = db.relationship('Appointment', backref='patient')
#         #     medication = db.relationship('Medication', backref='patient')

#         bob = Patient(name='Bob', telephone='1234567890', address='1234 Bob St', gender="Male",
#                       date_of_birth=datetime.strptime('1990-01-01', '%Y-%m-%d'), physician_id=1)
#         db.session.add(bob)
#         db.session.commit()

#     response = client.post('/lab_tracking_add_order/', data=dict(
#         ptname='Bob',
#         phname='Dr. Bob',
#         lbtech='Bob',
#         lbresult='Positive',
#         lbdate='2020-01-01',
#         lbodate='2020-01-01',
#         lab_test='1'
#     ), follow_redirects=True)

#     with app.app_context():
#         order = LabOrder.query.filter_by(
#             lab_test_result='Positive').first()
#         assert order.lab_test_result == 'Positive'


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


def test_patient_200(client):
    response = client.get('/patient')
    assert response.status_code == 200

##### Test form #####


# def test_create_physican(client):
    # send a POST request to create a physician
    # client.post('/physician', data=dict(
    #     physician_name='Dr. Bob',
    #     cell_phone_number='619-123-4567',
    #     work_time_start=9,
    #     work_time_end=17,
    #     work_days='MWF',
    # ))

    # with app.app_context():
    #     physician = db.session.query(Physician).filter_by(
    #         physician_name='Dr. Bob').first()

    # assert physician.physician_name == 'Dr. Bob'


# def test_create_patient(client):
#     # send a POST request to create a patient
#     client.post('patient', data=dict(
#         name='John Doe',
#         telephone='555-1234',
#         address='123 Main St',
#         date_of_birth=datetime.now(),
#         gender='male',
#         physician_id=1
#     ))

#     # check if the patient was added to the database
#     with app.app_context():
#         patient = db.session.query(Patient).filter_by(name='John Doe').first()

#     assert patient.name == 'John Doe'
#     assert patient.telephone == '555-1234'
#     assert patient.address == '123 Main St'
#     assert patient.gender == 'male'

#     # check datetime type for date of birth
#     assert isinstance(patient.date_of_birth, datetime)

def test_medical_encounter_200(client):
    response = client.get('/medical_encounter')
    assert response.status_code == 200


# def test_create_me(client):
#     # send a POST request to create a patient
#     response = client.post('/create_medical_encounter', data=dict(
#         employee_id=1,
#         encounter_date=datetime.now(),
#         practitioner_type='physician',
#         complaint='headache',
#         diagnosis='migraine',
#         treatment='ibuprofen',
#         recommended_followup=datetime.now(),
#         referral='none',
#         notes='none',
#         submission_date=datetime.now(),
#         patient_id=1
#     ))

#     # check if the patient was added to the database
#     with app.app_context():
#         me = db.session.query(MedicalEncounter).filter_by(
#             patient_id=1).first()

#     assert me.practitioner_type == 'physician'
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

# def test_create_prescription(client):
#     response = client.post('/pharmacy_create_prescription', data=dict(
#         patient_name='John Doe',
#         physician_name='Dr. Doe',
#         medication='ibuprofen',
#         dosage='200mg',
#         frequency='once a day',
#         filled_by='Dr. Doe',
#         date_filled=datetime.now(),
#         pharmacist_name='Dr. Doe',
#         medical_encounter_id=1
#     ))
#     with app.app_context():
#         prescription = db.session.query(Prescription).filter_by(
#             patient_name="John Doe").first()

#     assert prescription.physician_name == 'Dr. Doe'

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


# def test_confirm_appointment(appointment, client):
#     two_month_appointments = appointment.set_up(
#         "09:00:00", "12:00:00", "Block Out", [])

#     import json

#     # send a POST request to the endpoint
#     response = client.post('/confirm_appointment')

#     # check that the response contains the expected appointments
#     expected_appointments = appointment.helper.get_selected_appointments(
#         two_month_appointments)
#     expected_response = json.dumps({'appointments': expected_appointments})
#     assert response.data == expected_response.encode()


##### TESTS FOR EXCEPIONS #####

def test_404(client):
    response = client.get('/random/', follow_redirects=True)
    assert b'404' in response.data

##### TESTING EQUIPMENT SYSTEM #####


def test_equipment_200(client):
    response = client.get('/equipment')
    assert response.status_code == 200


def test_equipment(client):
    response = client.post('/equipment', data=dict(
        equipment_type='X-Ray',
        description='X-Ray Machine',
        department='Radiology',
        is_owned='on'
    ), follow_redirects=True)

    with app.app_context():
        equipment = db.session.query(Equipment).filter_by(
            equipment_type="X-Ray").first()

    assert equipment.description == 'X-Ray Machine'


def test_equipment_maintenance_history_200(client):
    response = client.get('/maintenance_history')
    assert response.status_code == 200


def test_equipment_maintenance_history(client):
    response = client.post('/maintenance_history/1', data=dict(
        type_of_problem='Broken',
        description_of_problem='Broken',
        is_resolved=True,
        description_of_resolution='Smashed it on the ground',
    ), follow_redirects=True)

    with app.app_context():
        maintenance_history = db.session.query(EquipmentMaintenance).filter_by(
            type_of_problem="Broken").first()

    assert maintenance_history.description_of_problem == 'Broken'

# @app.route('/owned/<int:equipment_id>')
# def equipment_owned(equipment_id):
#     owned_information = EquipmentOwned.query.filter_by(
#         equipment_id=equipment_id).all()
#     equipment = Equipment.query.get(equipment_id)
#     return render_template('equipment_owned.html', owned_information=owned_information, equipment=equipment)


def test_equipment_owned_200(client):
    response = client.get('/owned/1')
    assert response.status_code == 200

# @app.route('/leased/<int:equipment_id>')
# def equipment_leased(equipment_id):
#     leased_information = EquipmentLeased.query.all()
#     equipment = Equipment.query.get(equipment_id)
#     return render_template('equipment_leased.html', leased_information=leased_information, equipment=equipment)


def test_equipment_leased_200(client):
    response = client.get('/leased/1')
    assert response.status_code == 200

# @app.route('/vendors', methods=['POST', 'GET'])
# def vendors():
#     if "GET" == request.method:
#         vendor_data = Vendors.query.all()
#         return render_template('equipment_vendors.html', equipment_data=vendor_data)
#     if "POST" == request.method:
#         search_item = request.form.get('search_item')
#         if search_item:
#             vendor_data = Vendors.query.filter(
#                 Vendors.name.like('%'+search_item+'%')).all()
#             return render_template('equipment_vendors.html', equipment_data=vendor_data)

#         return redirect(url_for('vendors'))


def test_equipment_vendors_200(client):
    response = client.get('/vendors')
    assert response.status_code == 200


##### TESTING APPOINTMENT SYSTEM #####
