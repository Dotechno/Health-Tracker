# Healthtrack

## Table of Contents
- [Setup](#setup)
- [Unit Testing](#unit-testing)
- [Naming Conventions](#naming-conventions)
    - [Structure](#structure)
    - [Python](#python)
    - [Branching Naming Convention](#branching-naming-convention)
- [Database Relationships Using SQLAlchemy](#database-relationships-using-sqlalchemy)
    - [One-to-One](#one-to-one)
    - [One-to-Many](#one-to-many)
    - [Many-to-Many](#many-to-many)


## Setup

``` bash
git clone https://github.com/Dotechno/Health-Tracker
cd Health-Tracker

# Create python venv
python -m venv venv

# Assuming ur using mac or linux
venv/Scripts/activate

# If windows
# venv\Scripts\activate.bat

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

## Unit Testing
```bash
pytest -s -v
```

## Setup DB 
python setup.py
```
## Naming Conventions

### Structure
- Models/Class: `CamelCase` i.e. `User`, `Patient`, `MedicalEncounter`
- Fields/var: `snake_case` i.e. `first_name`, `last_name`, `telephone_number`
- Router URL: `kebab-case` i.e. `admin-panel`, `nurse-panel`, `doctor-panel`
- Filenames: `snake_case` i.e. `user.py`, `patient.py`, `medical_encounter.py`

### Python
- Functions: `snake_case` i.e. `get_user`, `get_patient`, `get_medical_encounter`
- Reference: [pep8](https://www.python.org/dev/peps/pep-0008/#function-and-variable-names)

### Branching Naming Convention
Examples
- Features: `feature/add-admin-button-to-panel`
- Refactor: `refactor/admin-panel/nurse-to-admin`
- Fix: `fix/removed-annoying-alert-button`


## Database Relationships Using SQLAlchemy

### One-to-One
##### See [Video](https://www.youtube.com/watch?v=JI76IvF9Lwg&list=PLXmMXHVSvS-BlLA5beNJojJLlpE0PJgCW&index=25) for more information
```python
class Parent(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  child = db.relationship('Child', backref='parent', useList=False)

class Child(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  parent_id = db.Column(db.Integer, db.ForeignKey('parent.id'))
```

### One-to-Many
##### See [Video](https://www.youtube.com/watch?v=VVX7JIWx-ss&list=PLXmMXHVSvS-BlLA5beNJojJLlpE0PJgCW&index=5) for more information
```python
class Owner(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  pets = db.relationship('Pet', backref='owner')

class Pet(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  owner_id = db.Column(db.Integer, db.ForeignKey('owner.id'))
```

### Many-to-Many
##### See [Video](https://www.youtube.com/watch?v=47i-jzrrIGQ&list=PLXmMXHVSvS-BlLA5beNJojJLlpE0PJgCW&index=7) for more information
```python
# creates another table that holds the primary 
# keys of both tables being referenced
user_channel = db.Table('user_channel',
  db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
  db.Column('channel_id', db.Integer, db.ForeignKey('channel.id')),
)

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  following = db.relationship('Channel', secondary=user_channel,backref='followers')

class Channel(db.Model):
  id = db.Column(db.Integer, primary_key=True)
```

