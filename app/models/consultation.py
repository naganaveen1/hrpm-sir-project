from datetime import datetime
from app.models import db

class Consultation(db.Model):
    __tablename__ = 'consultations'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    business_name = db.Column(db.String(150), nullable=True)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=True)
    preferred_date = db.Column(db.String(30), nullable=False)
    preferred_time = db.Column(db.String(30), nullable=False)
    message = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='New')  # New, Confirmed, Completed, Cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Consultation {self.name} on {self.preferred_date}>'
