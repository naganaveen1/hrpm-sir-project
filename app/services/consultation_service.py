from app.models import db
from app.models.consultation import Consultation

class ConsultationService:
    @staticmethod
    def create_consultation(name, email, phone, preferred_date, preferred_time, business_name=None, service_id=None, message=None):
        """Create and persist a new consultation appointment booking."""
        consultation = Consultation(
            name=name.strip(),
            email=email.strip().lower(),
            phone=phone.strip(),
            preferred_date=preferred_date.strip(),
            preferred_time=preferred_time.strip(),
            business_name=business_name.strip() if business_name else None,
            service_id=service_id if service_id and service_id != 0 else None,
            message=message.strip() if message else None,
            status='New'
        )
        db.session.add(consultation)
        db.session.commit()
        return consultation

    @staticmethod
    def get_all_consultations():
        """Retrieve all consultations ordered by creation date."""
        return Consultation.query.order_by(Consultation.created_at.desc()).all()

    @staticmethod
    def update_status(consultation_id, new_status):
        """Update consultation status (New, Confirmed, Completed, Cancelled)."""
        consultation = Consultation.query.get(consultation_id)
        if consultation:
            consultation.status = new_status
            db.session.commit()
            return consultation
        return None
