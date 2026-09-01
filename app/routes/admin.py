import json
from datetime import datetime
from urllib.parse import urlparse, urljoin
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from app.models import db
from app.models.user import User
from app.models.service import Service
from app.models.enquiry import Enquiry
from app.models.consultation import Consultation
from app.models.article import Article
from app.models.testimonial import Testimonial
from app.forms import AdminLoginForm

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def is_safe_url(target):
    if not target:
        return False
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

@admin_bp.before_request
def restrict_admin_access():
    # Allow login route and static files without auth
    if request.endpoint in ('admin.login', 'static'):
        return None
    if not current_user.is_authenticated:
        return redirect(url_for('admin.login', next=request.full_path if request.query_string else request.path))
    if hasattr(current_user, 'role') and current_user.role != 'admin':
        logout_user()
        flash("Unauthorized access. Admin privileges required.", "danger")
        return redirect(url_for('admin.login'))

# --------------------------------------------------------------------------
# AUTHENTICATION ROUTES
# --------------------------------------------------------------------------
@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))

    form = AdminLoginForm()
    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        password = form.password.data
        remember = form.remember_me.data

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            if hasattr(user, 'is_active') and not user.is_active:
                flash("Your account has been deactivated. Please contact support.", "danger")
                return redirect(url_for('admin.login'))
            
            login_user(user, remember=remember)
            flash(f"Welcome back, {user.name}!", "success")
            next_page = request.args.get('next')
            if next_page and is_safe_url(next_page):
                return redirect(next_page)
            return redirect(url_for('admin.dashboard'))
        else:
            flash("Invalid email or password. Please try again.", "danger")

    return render_template('admin/login.html', form=form)

@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been successfully logged out.", "info")
    return redirect(url_for('admin.login'))



# --------------------------------------------------------------------------
# DASHBOARD OVERVIEW
# --------------------------------------------------------------------------
@admin_bp.route('/dashboard')
@login_required
def dashboard():
    total_enquiries = Enquiry.query.count()
    new_enquiries = Enquiry.query.filter_by(status='New').count()
    total_consultations = Consultation.query.count()
    total_services = Service.query.filter_by(is_active=True).count()

    recent_enquiries = Enquiry.query.order_by(Enquiry.created_at.desc()).limit(5).all()
    recent_consultations = Consultation.query.order_by(Consultation.created_at.desc()).limit(5).all()

    return render_template(
        'admin/dashboard.html',
        active_page='admin_dashboard',
        total_enquiries=total_enquiries,
        new_enquiries=new_enquiries,
        total_consultations=total_consultations,
        total_services=total_services,
        recent_enquiries=recent_enquiries,
        recent_consultations=recent_consultations
    )


# --------------------------------------------------------------------------
# ENQUIRIES MANAGEMENT
# --------------------------------------------------------------------------
@admin_bp.route('/enquiries')
@login_required
def enquiries():
    search_query = request.args.get('q', '').strip()
    status_filter = request.args.get('status', '').strip()

    query = Enquiry.query

    if search_query:
        query = query.filter(
            (Enquiry.name.ilike(f"%{search_query}%")) |
            (Enquiry.email.ilike(f"%{search_query}%")) |
            (Enquiry.phone.ilike(f"%{search_query}%")) |
            (Enquiry.business_name.ilike(f"%{search_query}%"))
        )

    if status_filter:
        query = query.filter_by(status=status_filter)

    enquiries_list = query.order_by(Enquiry.created_at.desc()).all()
    return render_template('admin/enquiries.html', active_page='admin_enquiries', enquiries=enquiries_list, search_query=search_query, status_filter=status_filter)

@admin_bp.route('/enquiries/<int:enquiry_id>/status', methods=['POST'])
@login_required
def update_enquiry_status(enquiry_id):
    enquiry = Enquiry.query.get_or_404(enquiry_id)
    new_status = request.form.get('status')
    if new_status in ['New', 'Contacted', 'In Progress', 'Converted', 'Closed']:
        enquiry.status = new_status
        db.session.commit()
        flash(f"Enquiry #{enquiry_id} status updated to '{new_status}'.", "success")
    return redirect(url_for('admin.enquiries'))

@admin_bp.route('/enquiries/<int:enquiry_id>/delete', methods=['POST'])
@login_required
def delete_enquiry(enquiry_id):
    enquiry = Enquiry.query.get_or_404(enquiry_id)
    db.session.delete(enquiry)
    db.session.commit()
    flash(f"Enquiry #{enquiry_id} deleted.", "success")
    return redirect(url_for('admin.enquiries'))


# --------------------------------------------------------------------------
# CONSULTATIONS MANAGEMENT
# --------------------------------------------------------------------------
@admin_bp.route('/consultations')
@login_required
def consultations():
    search_query = request.args.get('q', '').strip()
    status_filter = request.args.get('status', '').strip()

    query = Consultation.query

    if search_query:
        query = query.filter(
            (Consultation.name.ilike(f"%{search_query}%")) |
            (Consultation.email.ilike(f"%{search_query}%")) |
            (Consultation.phone.ilike(f"%{search_query}%"))
        )

    if status_filter:
        query = query.filter_by(status=status_filter)

    consultations_list = query.order_by(Consultation.created_at.desc()).all()
    return render_template('admin/consultations.html', active_page='admin_consultations', consultations=consultations_list, search_query=search_query, status_filter=status_filter)

@admin_bp.route('/consultations/<int:consultation_id>/status', methods=['POST'])
@login_required
def update_consultation_status(consultation_id):
    cons = Consultation.query.get_or_404(consultation_id)
    new_status = request.form.get('status')
    if new_status in ['New', 'Confirmed', 'Completed', 'Cancelled']:
        cons.status = new_status
        db.session.commit()
        flash(f"Consultation #{consultation_id} status updated to '{new_status}'.", "success")
    return redirect(url_for('admin.consultations'))

@admin_bp.route('/consultations/<int:consultation_id>/delete', methods=['POST'])
@login_required
def delete_consultation(consultation_id):
    cons = Consultation.query.get_or_404(consultation_id)
    db.session.delete(cons)
    db.session.commit()
    flash(f"Consultation #{consultation_id} deleted.", "success")
    return redirect(url_for('admin.consultations'))


# --------------------------------------------------------------------------
# SERVICES CMS
# --------------------------------------------------------------------------
@admin_bp.route('/services')
@login_required
def services():
    services_list = Service.query.order_by(Service.id.asc()).all()
    return render_template('admin/services.html', active_page='admin_services', services=services_list)

@admin_bp.route('/services/new', methods=['GET', 'POST'])
@login_required
def create_service():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        slug = request.form.get('slug', '').strip() or Service.generate_slug(title)
        icon = request.form.get('icon', 'briefcase').strip()
        short_description = request.form.get('short_description', '').strip()
        full_description = request.form.get('full_description', '').strip() or request.form.get('description', '').strip()

        # Complex fields stored as JSON arrays
        problems = [p.strip() for p in request.form.get('problems_addressed', '').split('\n') if p.strip()]
        included = [i.strip() for i in request.form.get('services_included', '').split('\n') if i.strip()]
        benefits = [b.strip() for b in request.form.get('benefits', '').split('\n') if b.strip()]

        service = Service(
            title=title,
            slug=slug,
            icon=icon,
            short_description=short_description,
            description=full_description,
            is_active=True
        )
        service.problems_addressed = problems
        service.services_included = included
        service.benefits = benefits

        db.session.add(service)
        db.session.commit()
        flash(f"Service '{title}' created successfully!", "success")
        return redirect(url_for('admin.services'))

    return render_template('admin/service_form.html', active_page='admin_services', service=None)

@admin_bp.route('/services/<int:service_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_service(service_id):
    service = Service.query.get_or_404(service_id)

    if request.method == 'POST':
        service.title = request.form.get('title', '').strip()
        service.slug = request.form.get('slug', '').strip() or Service.generate_slug(service.title)
        service.icon = request.form.get('icon', 'briefcase').strip()
        service.short_description = request.form.get('short_description', '').strip()
        service.description = request.form.get('full_description', '').strip() or request.form.get('description', '').strip()

        problems = [p.strip() for p in request.form.get('problems_addressed', '').split('\n') if p.strip()]
        included = [i.strip() for i in request.form.get('services_included', '').split('\n') if i.strip()]
        benefits = [b.strip() for b in request.form.get('benefits', '').split('\n') if b.strip()]

        service.problems_addressed = problems
        service.services_included = included
        service.benefits = benefits

        db.session.commit()
        flash(f"Service '{service.title}' updated successfully!", "success")
        return redirect(url_for('admin.services'))

    return render_template('admin/service_form.html', active_page='admin_services', service=service)

@admin_bp.route('/services/<int:service_id>/toggle-active', methods=['POST'])
@login_required
def toggle_service_active(service_id):
    service = Service.query.get_or_404(service_id)
    service.is_active = not service.is_active
    db.session.commit()
    flash(f"Service '{service.title}' is now {'Active' if service.is_active else 'Inactive'}.", "info")
    return redirect(url_for('admin.services'))

@admin_bp.route('/services/<int:service_id>/delete', methods=['POST'])
@login_required
def delete_service(service_id):
    service = Service.query.get_or_404(service_id)
    db.session.delete(service)
    db.session.commit()
    flash(f"Service deleted.", "success")
    return redirect(url_for('admin.services'))


# --------------------------------------------------------------------------
# ARTICLES CMS
# --------------------------------------------------------------------------
@admin_bp.route('/articles')
@login_required
def articles():
    articles_list = Article.query.order_by(Article.created_at.desc()).all()
    return render_template('admin/articles.html', active_page='admin_articles', articles=articles_list)

@admin_bp.route('/articles/new', methods=['GET', 'POST'])
@login_required
def create_article():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        slug = Article.generate_slug(title)
        category = request.form.get('category', 'Tax').strip()
        featured_image = request.form.get('featured_image', '').strip()
        excerpt = request.form.get('excerpt', '').strip() or request.form.get('summary', '').strip()
        content = request.form.get('content', '').strip()

        article = Article(
            title=title,
            slug=slug,
            category=category,
            excerpt=excerpt,
            content=content,
            featured_image=featured_image,
            is_published=True
        )
        db.session.add(article)
        db.session.commit()
        flash(f"Article '{title}' created and published!", "success")
        return redirect(url_for('admin.articles'))

    return render_template('admin/article_form.html', active_page='admin_articles', article=None)

@admin_bp.route('/articles/<int:article_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    article = Article.query.get_or_404(article_id)

    if request.method == 'POST':
        article.title = request.form.get('title', '').strip()
        article.category = request.form.get('category', '').strip()
        article.featured_image = request.form.get('featured_image', '').strip()
        article.excerpt = request.form.get('excerpt', '').strip() or request.form.get('summary', '').strip()
        article.content = request.form.get('content', '').strip()

        db.session.commit()
        flash(f"Article '{article.title}' updated successfully!", "success")
        return redirect(url_for('admin.articles'))

    return render_template('admin/article_form.html', active_page='admin_articles', article=article)


@admin_bp.route('/articles/<int:article_id>/toggle-published', methods=['POST'])
@login_required
def toggle_article_published(article_id):
    article = Article.query.get_or_404(article_id)
    article.is_published = not article.is_published
    db.session.commit()
    flash(f"Article status changed to {'Published' if article.is_published else 'Draft'}.", "info")
    return redirect(url_for('admin.articles'))


@admin_bp.route('/articles/<int:article_id>/delete', methods=['POST'])
@login_required
def delete_article(article_id):
    article = Article.query.get_or_404(article_id)
    db.session.delete(article)
    db.session.commit()
    flash("Article deleted.", "success")
    return redirect(url_for('admin.articles'))


# --------------------------------------------------------------------------
# TESTIMONIALS CMS
# --------------------------------------------------------------------------
@admin_bp.route('/testimonials')
@login_required
def testimonials():
    testimonials_list = Testimonial.query.order_by(Testimonial.created_at.desc()).all()
    return render_template('admin/testimonials.html', active_page='admin_testimonials', testimonials=testimonials_list)

@admin_bp.route('/testimonials/new', methods=['GET', 'POST'])
@login_required
def create_testimonial():
    if request.method == 'POST':
        client_name = request.form.get('client_name', '').strip()
        company_name = request.form.get('company_name', '').strip()
        designation = request.form.get('designation', '').strip()
        rating = int(request.form.get('rating', 5))
        content = request.form.get('content', '').strip()

        t = Testimonial(
            client_name=client_name,
            company_name=company_name,
            designation=designation,
            rating=rating,
            content=content,
            is_visible=True
        )
        db.session.add(t)
        db.session.commit()
        flash("Client testimonial added!", "success")
        return redirect(url_for('admin.testimonials'))

    return redirect(url_for('admin.testimonials'))


@admin_bp.route('/testimonials/<int:testimonial_id>/toggle-visible', methods=['POST'])
@login_required
def toggle_testimonial_visibility(testimonial_id):
    t = Testimonial.query.get_or_404(testimonial_id)
    t.is_visible = not t.is_visible
    db.session.commit()
    flash(f"Testimonial is now {'Visible' if t.is_visible else 'Hidden'}.", "info")
    return redirect(url_for('admin.testimonials'))

@admin_bp.route('/testimonials/<int:testimonial_id>/delete', methods=['POST'])
@login_required
def delete_testimonial(testimonial_id):
    t = Testimonial.query.get_or_404(testimonial_id)
    db.session.delete(t)
    db.session.commit()
    flash("Testimonial deleted.", "success")
    return redirect(url_for('admin.testimonials'))
