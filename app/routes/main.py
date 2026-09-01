from flask import Blueprint, render_template
from app.models.testimonial import Testimonial

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    testimonials = Testimonial.query.filter_by(is_visible=True).order_by(Testimonial.created_at.desc()).all()
    return render_template('main/index.html', active_page='home', testimonials=testimonials)

@main_bp.route('/about')
def about():
    return render_template('main/index.html', active_page='about')

@main_bp.route('/solutions')
def solutions():
    return render_template('main/index.html', active_page='solutions')

@main_bp.route('/privacy-policy')
def privacy():
    return render_template('main/index.html', active_page='privacy')

@main_bp.route('/terms-and-conditions')
def terms():
    return render_template('main/index.html', active_page='terms')

@main_bp.route('/disclaimer')
def disclaimer():
    return render_template('main/index.html', active_page='disclaimer')

@main_bp.route('/design-system')
def design_system():
    return render_template('design_system.html', active_page='design-system')
