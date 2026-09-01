from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.forms import EnquiryForm, ConsultationForm
from app.services.enquiry_service import EnquiryService
from app.services.consultation_service import ConsultationService
from app.services.service_catalog import ServiceCatalogService

contact_bp = Blueprint('contact', __name__)

@contact_bp.route('/contact', methods=['GET', 'POST'])
def index():
    form = EnquiryForm()
    active_services = ServiceCatalogService.get_all_active_services()
    
    # Populate service dropdown choices (0 for General / Not sure)
    form.service_id.choices = [(0, 'General Inquiry / Select Service')] + [(s.id, s.title) for s in active_services]
    
    # Pre-select service from URL query param if present
    preselect_service_id = request.args.get('service_id', type=int)
    if request.method == 'GET' and preselect_service_id:
        form.service_id.data = preselect_service_id

    if form.validate_on_submit():
        try:
            enquiry = EnquiryService.create_enquiry(
                name=form.name.data,
                email=form.email.data,
                phone=form.phone.data,
                message=form.message.data,
                business_name=business_name if (business_name := form.business_name.data) else None,
                service_id=form.service_id.data if form.service_id.data != 0 else None
            )
            flash("Thank you for contacting MVR Associates! Your inquiry has been received. Our consultancy team will reach out to you within 24 hours.", "success")
            return redirect(url_for('contact.index'))
        except Exception as e:
            flash("An unexpected error occurred while processing your request. Please try again or reach out to us directly.", "danger")

    return render_template('contact/index.html', form=form, active_page='contact')

@contact_bp.route('/consultation', methods=['GET', 'POST'])
def consultation():
    form = ConsultationForm()
    active_services = ServiceCatalogService.get_all_active_services()
    
    form.service_id.choices = [(0, 'General Business Advisory')] + [(s.id, s.title) for s in active_services]
    
    preselect_service_id = request.args.get('service_id', type=int)
    if request.method == 'GET' and preselect_service_id:
        form.service_id.data = preselect_service_id

    if form.validate_on_submit():
        try:
            consultation_req = ConsultationService.create_consultation(
                name=form.name.data,
                email=form.email.data,
                phone=form.phone.data,
                preferred_date=form.preferred_date.data,
                preferred_time=form.preferred_time.data,
                business_name=form.business_name.data,
                service_id=form.service_id.data if form.service_id.data != 0 else None,
                message=form.message.data
            )
            flash("Your consultation request has been successfully submitted! We will confirm your preferred date and time slot shortly.", "success")
            return redirect(url_for('contact.consultation'))
        except Exception as e:
            flash("An error occurred while booking your consultation. Please verify your inputs and try again.", "danger")

    return render_template('contact/consultation.html', form=form, active_page='contact')
