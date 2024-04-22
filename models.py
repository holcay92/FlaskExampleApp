from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from extensions import db

class Customer(db.Model):
    __tablename__ = 'customer'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    phone_number = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(50))
    is_verified = db.Column(db.Boolean, default=False)
    def check_password(self, password):
        return self.password == password
        

class Cheque(db.Model):
    __tablename__ = 'cheque'
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    cash_out_date = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    bank = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    status = db.Column(db.String(50), default='Pending')
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    receiver_customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
