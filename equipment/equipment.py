from flask import Flask, redirect, url_for, render_template
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

# app = Flask(__name__)

# db = SQLAlchemy(app)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

# with app.app_context():
#     db = SQLAlchemy(app)
#     db.init_app(app)

db = SQLAlchemy() # db intitialized here
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db.init_app(app)

class Equipment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    department = db.Column(db.String(200), nullable=False)
    is_leased = db.Column(db.Boolean, nullable=False)
    is_owned = db.Column(db.Boolean, nullable=False)
    vendor = db.relationship('Vendor', backref='equipment', lazy=True)
    maintenance = db.relationship('EquipmentMaintenance', backref='equipment', lazy=True)
    equipment_leased = db.relationship('EquipmentLeased', backref='equipment', lazy=True)
    equipment_owned = db.relationship('EquipmentOwned', backref='equipment', lazy=True)
class Vendors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_purchased = db.Column(db.DateTime, nullable=False)
    warranty_information = db.Column(db.String(200), nullable=False)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=False)
class EquipmentMaintenance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type_of_problem = db.Column(db.String(200), nullable=False)
    description_of_problem = db.Column(db.String(200), nullable=False)
    is_resolved = db.Column(db.Boolean, nullable=False)
    description_of_resoltion = db.Column(db.String(200), nullable=False)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=False)
class EquipmenLeased(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    leasing_company = db.Column(db.String(200), nullable=False)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=False)
class EquipmentOwned(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_purchased = db.Column(db.DateTime, nullable=False)
    warranty_information = db.Column(db.String(200), nullable=False)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=False)





#root page => home page
@app.route("/")
@app.route("/equipment")
def equipment():

    

    return render_template('equipment.html')

if __name__ == "__main__":
    app.run(debug=True)
    