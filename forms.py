from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo, InputRequired


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    roles = StringField('Roles', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class PatientForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired(message='Name is required')])
    telephone = StringField('Telephone', validators=[InputRequired(message='Telephone is required')])
    address = StringField('Address', validators=[InputRequired(message='Address is required')])
    date_of_birth = DateField('Date of Birth', format='%Y-%m-%d',validators=[InputRequired(message='Date of Birth is required')])
    gender = SelectField('Gender', choices=[('male', 'Male'), ('female', 'Female')], validators=[InputRequired(message='Gender is required')])
    submit = SubmitField('Create Patient')


class MedicalEncounterForm(FlaskForm):
    encounter_date = DateField('Encounter Date', format='%Y-%m-%d', validators=[InputRequired()])
    practitioner_id = StringField('Practitioner ID', validators=[InputRequired()])
    practitioner_type = StringField('Practitioner Type', validators=[InputRequired()])
    complaint = StringField('Complaint', validators=[InputRequired()])
    diagnosis = StringField('Diagnosis', validators=[InputRequired()])
    treatment = StringField('Treatment', validators=[InputRequired()])
    referral = StringField('Referral', validators=[InputRequired()])
    recommended_followup = StringField('Recommended Follow-up', validators=[InputRequired()])
    notes = StringField('Notes', validators=[InputRequired()])
    submission_date = DateField('Submission Date', format='%Y-%m-%d', validators=[InputRequired()])
    patient_name = StringField('Patient Name', validators=[InputRequired()])
    submit = SubmitField('Create Medical Encounter')
# Copy one of these form into CHat GPT
