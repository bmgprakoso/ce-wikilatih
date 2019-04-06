from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import re
from sqlalchemy.orm import validates

db = SQLAlchemy()


class Training(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    instructor = db.Column(db.String(30), nullable=False)
    location = db.Column(db.String(30), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)

    def json(self):
        return {'id': self.id, 'title': self.title, 'instructor': self.instructor, 'location': self.location,
                'start_date': str(self.start_date), 'end_date': str(self.end_date)}

    def save_to(self):
        db.session.add(self)
        db.session.commit()

    def delete_(self):
        db.session.delete(self)
        db.session.commit()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.Enum('basic', 'admin', name='user_roles'), default='basic')
    name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.Enum('male', 'female', name='gender'), nullable=False)
    phone = db.Column(db.String(30), nullable=False)
    institution = db.Column(db.String(100), nullable=False)

    def json(self):
        return {'id': self.id, 'email': self.email, 'role': self.role, 'name': self.name, 'gender': self.gender,
                'phone': self.phone,
                'institution': self.institution}

    def save_to(self):
        db.session.add(self)
        db.session.commit()

    def delete_(self):
        db.session.delete(self)
        db.session.commit()

    def set_password(self, password):
        if not password:
            raise AssertionError('password not provided')

        if not re.match('\d.*[A-Z]|[A-Z].*\d', password):
            raise AssertionError('password must contain 1 capital letter and 1 number')

        if len(password) < 8 or len(password) > 50:
            raise AssertionError('password must be between 8 and 50 characters')

        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @validates('email')
    def validate_email(self, key, email):
        if not email:
            raise AssertionError('no email provided')

        if User.query.filter(User.email == email).first():
            raise AssertionError('email is already in use')

        if not re.match("[^@]+@[^@]+\.[^@]+", email):
            raise AssertionError('provided email is not an email address')

        return email
