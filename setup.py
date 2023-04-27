import sys
from flask import Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'

# app.config['SQLALCHEMY_BINDS'] = {'prescription': 'sqlite:///prescription.db',
#                                   'medication': 'sqlite:///medication.db',
#                                   'patient': 'sqlite:///patient.db',
#                                   'medical_encounter': 'sqlite:///medical_encounter.db',
#                                   'vital_sign': 'sqlite:///vital_sign.db',
#                                   'physician': 'sqlite:///physician.db',
#                                   'insurance_status': 'sqlite:///insurance_status.db',
#                                   'insurance': 'sqlite:///insurance.db',
#                                   'lab_test': 'sqlite:///lab_test.db',
#                                   'lab_order': 'sqlite:///lab_order.db',
#                                   'clinic_service': 'sqlite:///clinic_service.db',
#                                   'invoice': 'sqlite:///invoice.db',
#                                   'invoice_line_item': 'sqlite:///invoice_line_item.db'}

app.config['SECRET_KEY'] = 'arbitrarySecretKey'


if not 'models' in sys.modules:
    from model import db

with app.app_context():
    db.create_all()
