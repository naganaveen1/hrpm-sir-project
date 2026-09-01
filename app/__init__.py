import os
import urllib.parse
from flask import Flask, render_template
from config import config_by_name
from app.models import db
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')

    app = Flask(__name__)
    app.config.from_object(config_by_name.get(config_name, config_by_name['default']))

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'admin.login'
    login_manager.login_message_category = 'warning'

    # Global Context Processor for WhatsApp and Firm Metadata
    @app.context_processor
    def inject_global_vars():
        whatsapp_num = app.config.get('WHATSAPP_NUMBER', '+919876543210')
        clean_num = ''.join(c for c in whatsapp_num if c.isdigit())
        msg = urllib.parse.quote(app.config.get('WHATSAPP_DEFAULT_MESSAGE', 'Hello MVR Associates, I would like to inquire about your professional consultancy services.'))
        whatsapp_link = f"https://wa.me/{clean_num}?text={msg}"
        return dict(
            whatsapp_url=whatsapp_link,
            contact_phone=app.config.get('CONTACT_PHONE', '+91 98765 43210'),
            contact_email=app.config.get('CONTACT_EMAIL', 'info@mvrassociates.com'),
            contact_address=app.config.get('CONTACT_ADDRESS', 'Corporate Office, MVR Associates')
        )

    # User loader for Flask-Login
    from app.models.user import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        # Import models so SQLAlchemy registers tables
        from app.models.service import Service
        from app.models.enquiry import Enquiry
        from app.models.consultation import Consultation
        from app.models.article import Article
        from app.models.testimonial import Testimonial
        
        db.create_all()

    # Register Custom Error Handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500

    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template('errors/403.html'), 403

    # Register Blueprints
    from app.routes.main import main_bp
    from app.routes.services import services_bp
    from app.routes.resources import resources_bp
    from app.routes.contact import contact_bp
    from app.routes.admin import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(services_bp)
    app.register_blueprint(resources_bp)
    app.register_blueprint(contact_bp)
    app.register_blueprint(admin_bp)

    return app
