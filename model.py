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


class Equipment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    department = db.Column(db.String(200), nullable=False)
    is_leased = db.Column(db.Boolean, nullable=False)
    is_owned = db.Column(db.Boolean, nullable=False)
    maintenance = db.relationship(
        'EquipmentMaintenance', backref='equipment', lazy=True)
    equipment_owned = db.relationship(
        'EquipmentOwned', backref='equipment', lazy=True)
    vendor = db.relationship('Vendors', backref='equipment', lazy=True)
    equipment_leased = db.relationship(
        'EquipmentLeased', backref='equipment', lazy=True)


class Vendors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    type_of_equipment_provided = db.Column(db.String(200), nullable=False)
    is_preferred_vendor = db.Column(db.Boolean, nullable=False)
    equipment_id = db.Column(db.Integer, db.ForeignKey(
        'equipment.id'), nullable=False)


class EquipmentMaintenance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type_of_problem = db.Column(db.String(200), nullable=False)
    description_of_problem = db.Column(db.String(200), nullable=False)
    is_resolved = db.Column(db.Boolean, nullable=False)
    description_of_resoltion = db.Column(db.String(200), nullable=False)
    equipment_id = db.Column(db.Integer, db.ForeignKey(
        'equipment.id'), nullable=False)


class EquipmentLeased(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    leasing_company = db.Column(db.String(200), nullable=False)
    equipment_id = db.Column(db.Integer, db.ForeignKey(
        'equipment.id'), nullable=False)


class EquipmentOwned(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_purchased = db.Column(db.DateTime, nullable=False)
    warranty_information = db.Column(db.String(200), nullable=False)
    equipment_id = db.Column(db.Integer, db.ForeignKey(
        'equipment.id'), nullable=False)

