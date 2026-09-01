from datetime import datetime
from app.models import db

class Enquiry(db.Model):
    __tablename__ = 'enquiries'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    business_name = db.Column(db.String(150), nullable=True)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=True)
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='New')  # New, Contacted, In Progress, Converted, Closed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Enquiry {self.name} - {self.status}>'
