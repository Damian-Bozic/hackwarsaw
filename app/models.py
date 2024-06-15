from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    street_address = db.Column(db.String(100), nullable=False)
    postal_code = db.Column(db.String(20), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    youtube_link = db.Column(db.String(120))
    instagram_link = db.Column(db.String(120))
    bank_account_id = db.Column(db.Integer, db.ForeignKey('bank_account.id'))
    art_type_id = db.Column(db.Integer, db.ForeignKey('art_type.id'))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class BankAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_holder_name = db.Column(db.String(100), nullable=False)
    account_number = db.Column(db.String(20), nullable=False)
    routing_number = db.Column(db.String(9), nullable=False)
    user = db.relationship('User', backref='bank_account', lazy=True)

class ArtType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type_name = db.Column(db.String(50), nullable=False)
    subtypes = db.relationship('ArtSubtype', backref='art_type', lazy=True)

class ArtSubtype(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subtype_name = db.Column(db.String(50), nullable=False)
    art_type_id = db.Column(db.Integer, db.ForeignKey('art_type.id'))
