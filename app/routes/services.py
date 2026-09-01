from flask import Blueprint, render_template, abort
from app.models.service import Service

services_bp = Blueprint('services', __name__, url_prefix='/services')

@services_bp.route('/')
def index():
    services = Service.query.filter_by(is_active=True).order_by(Service.order.asc()).all()
    return render_template('services/index.html', services=services, active_page='services')

@services_bp.route('/<slug>')
def detail(slug):
    service = Service.query.filter_by(slug=slug, is_active=True).first_or_404()
    related_services = Service.query.filter(Service.id != service.id, Service.is_active == True).limit(3).all()
    return render_template('services/detail.html', service=service, related_services=related_services, active_page='services')
