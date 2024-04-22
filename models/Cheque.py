from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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
