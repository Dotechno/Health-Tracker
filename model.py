from __main__ import app


from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user



db = SQLAlchemy(app)



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    roles = db.Column(db.String(200), nullable=False)


    def __repr__(self):
        return '<User %r>' % self.id


    def is_active(self):
        return True




class LabTest(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    lab_test_name = db.Column(db.String(200), nullable=False)
    low_normal_results = db.Column(db.String(200))
    high_normal_results=db.Column(db.String(200))
    #lab_order = db.relationship('LabOrder', backref='lab_test')

    def __repr__(self):
        return '<LabTest %r>' % self.id
   
class LabOrder(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    patient_name = db.Column(db.String(200), nullable=False)
    physician_name = db.Column(db.String(200), nullable=False)
    lab_test_date = db.Column(db.DateTime, nullable=False)
    lab_test_technician = db.Column(db.String(200), nullable=False)
    lab_test_result = db.Column(db.String(200), nullable=False)
    test_name = db.Column(db.String(200), nullable=False)
    lab_order_date = db.Column(db.DateTime, nullable=False)
    #test = db.Column(db.Integer, db.ForeignKey('lab_test.id'))

    def __repr__(self):
        return '<LabOrder %r>' % self.id




