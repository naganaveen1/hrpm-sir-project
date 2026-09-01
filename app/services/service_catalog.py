from app.models.service import Service
from app.models import db

class ServiceCatalogService:
    @staticmethod
    def get_all_active_services():
        """Retrieve all active services sorted by order priority."""
        return Service.query.filter_by(is_active=True).order_by(Service.order.asc()).all()

    @staticmethod
    def get_service_by_slug(slug):
        """Retrieve a specific active service by its unique URL slug."""
        return Service.query.filter_by(slug=slug, is_active=True).first()

    @staticmethod
    def get_related_services(current_service_id, limit=3):
        """Retrieve related active services excluding current service ID."""
        return Service.query.filter(
            Service.id != current_service_id,
            Service.is_active == True
        ).order_by(Service.order.asc()).limit(limit).all()
