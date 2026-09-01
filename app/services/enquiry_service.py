from app.models import db
from app.models.enquiry import Enquiry

class EnquiryService:
    @staticmethod
    def create_enquiry(name, email, phone, message, business_name=None, service_id=None):
        """Create and persist a new customer contact enquiry."""
        enquiry = Enquiry(
            name=name.strip(),
            email=email.strip().lower(),
            phone=phone.strip(),
            message=message.strip(),
            business_name=business_name.strip() if business_name else None,
            service_id=service_id if service_id and service_id != 0 else None,
            status='New'
        )
        db.session.add(enquiry)
        db.session.commit()
        return enquiry

    @staticmethod
    def get_all_enquiries():
        """Retrieve all customer enquiries ordered by creation timestamp."""
        return Enquiry.query.order_by(Enquiry.created_at.desc()).all()

    @staticmethod
    def update_status(enquiry_id, new_status):
        """Update enquiry status (New, Contacted, In Progress, Converted, Closed)."""
        enquiry = Enquiry.query.get(enquiry_id)
        if enquiry:
            enquiry.status = new_status
            db.session.commit()
            return enquiry
        return None
