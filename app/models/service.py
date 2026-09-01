import json
from datetime import datetime
from app.models import db

class Service(db.Model):
    __tablename__ = 'services'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    slug = db.Column(db.String(150), unique=True, nullable=False, index=True)
    short_description = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    icon = db.Column(db.String(100), nullable=False, default='briefcase')
    is_active = db.Column(db.Boolean, default=True)
    order = db.Column(db.Integer, default=0)
    
    # JSON-encoded text fields for detailed content
    problems_addressed_raw = db.Column(db.Text, nullable=True)
    services_included_raw = db.Column(db.Text, nullable=True)
    benefits_raw = db.Column(db.Text, nullable=True)
    process_steps_raw = db.Column(db.Text, nullable=True)
    faqs_raw = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    enquiries = db.relationship('Enquiry', backref='service', lazy=True)
    consultations = db.relationship('Consultation', backref='service', lazy=True)

    @staticmethod
    def generate_slug(title):
        import re
        if not title:
            return ""
        slug = re.sub(r'[^a-zA-Z0-9\s-]', '', title.lower())
        slug = re.sub(r'[\s-]+', '-', slug).strip('-')
        
        original_slug = slug or 'service'
        candidate_slug = original_slug
        count = 1
        while Service.query.filter_by(slug=candidate_slug).first():
            candidate_slug = f"{original_slug}-{count}"
            count += 1
        return candidate_slug

    @property
    def problems_addressed(self):
        if self.problems_addressed_raw:
            try:
                return json.loads(self.problems_addressed_raw)
            except Exception:
                return []
        return []

    @problems_addressed.setter
    def problems_addressed(self, value):
        self.problems_addressed_raw = json.dumps(value)

    @property
    def services_included(self):
        if self.services_included_raw:
            try:
                return json.loads(self.services_included_raw)
            except Exception:
                return []
        return []

    @services_included.setter
    def services_included(self, value):
        self.services_included_raw = json.dumps(value)

    @property
    def benefits(self):
        if self.benefits_raw:
            try:
                return json.loads(self.benefits_raw)
            except Exception:
                return []
        return []

    @benefits.setter
    def benefits(self, value):
        self.benefits_raw = json.dumps(value)

    @property
    def process_steps(self):
        if self.process_steps_raw:
            try:
                return json.loads(self.process_steps_raw)
            except Exception:
                return []
        return []

    @process_steps.setter
    def process_steps(self, value):
        self.process_steps_raw = json.dumps(value)

    @property
    def faqs(self):
        if self.faqs_raw:
            try:
                return json.loads(self.faqs_raw)
            except Exception:
                return []
        return []

    @faqs.setter
    def faqs(self, value):
        self.faqs_raw = json.dumps(value)

    def __repr__(self):
        return f'<Service {self.title}>'
