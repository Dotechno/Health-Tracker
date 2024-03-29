from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField, SelectField, IntegerField, ValidationError
from wtforms.validators import DataRequired, Length, EqualTo, InputRequired


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    roles = StringField('Roles', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')


class PhysicianRegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    roles = StringField('Roles', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])

    physician_name = StringField('Physician Name',
                                 validators=[DataRequired(), Length(min=2, max=20)])
    cell_phone_number = StringField('Cell Phone Number',
                                    validators=[DataRequired(), Length(min=2, max=20)])
    work_time_start = IntegerField('Work Time Start',)
    work_time_end = IntegerField('Work Time End',)
    work_days = StringField('Work Days',
                            validators=[DataRequired(), Length(min=2, max=20)])

    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class PatientForm(FlaskForm):
    name = StringField('Name', validators=[
                       InputRequired(message='Name is required')])
    telephone = StringField('Telephone', validators=[
                            InputRequired(message='Telephone is required')])
    address = StringField('Address', validators=[
                          InputRequired(message='Address is required')])
    date_of_birth = DateField('Date of Birth', format='%Y-%m-%d',
                              validators=[InputRequired(message='Date of Birth is required')])
    gender = SelectField('Gender', choices=[('male', 'Male'), ('female', 'Female')], validators=[
                         InputRequired(message='Gender is required')])
    submit = SubmitField('Create Patient')
    insurance = StringField('Insurance')
    insurance_address = StringField('Insurance Address')
    insurance_status = SelectField('Insurance Status', choices=[('pay on time', 'Pay on Time'), (
        'late in payment', 'Late in payment'), ('difficult to get payment', 'Diffcult to get payment')])
    physician_name = StringField('Physician Name')


class MedicalEncounterForm(FlaskForm):
    encounter_date = DateField(
        'Encounter Date', format='%Y-%m-%d', validators=[InputRequired()])
    practitioner_id = SelectField('Practitioner ID', coerce=int)
    practitioner_type = StringField(
        'Practitioner Type', validators=[InputRequired()])
    complaint = StringField('Complaint', validators=[InputRequired()])
    diagnosis = StringField('Diagnosis', validators=[InputRequired()])
    treatment = StringField('Treatment', validators=[InputRequired()])
    referral = StringField('Referral', validators=[InputRequired()])
    recommended_followup = DateField(
        'Recommended Follow-up', validators=[InputRequired()])
    notes = StringField('Notes', validators=[InputRequired()])
    submission_date = DateField(
        'Submission Date', format='%Y-%m-%d', validators=[InputRequired()])
    patient_name = StringField('Patient Name', validators=[DataRequired()])
    patient_id = SelectField('Patient ID', coerce=int)
    submit = SubmitField('Create Medical Encounter')
