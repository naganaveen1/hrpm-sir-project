import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'mvr-associates-default-secret-key-2026-change-in-production')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload
    
    # WhatsApp & Contact Configuration
    WHATSAPP_NUMBER = os.getenv('WHATSAPP_NUMBER', '+919876543210')
    WHATSAPP_DEFAULT_MESSAGE = os.getenv('WHATSAPP_DEFAULT_MESSAGE', 'Hello MVR Associates, I would like to inquire about your professional consultancy services.')
    CONTACT_PHONE = os.getenv('CONTACT_PHONE', '+91 98765 43210')
    CONTACT_EMAIL = os.getenv('CONTACT_EMAIL', 'info@mvrassociates.com')
    CONTACT_ADDRESS = os.getenv('CONTACT_ADDRESS', 'Corporate Office, MVR Associates, Business District, India')

    # Mail & Notification Settings
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'true').lower() in ['true', '1', 't']
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', '')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', '')
    ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'admin@mvrassociates.com')

class DevelopmentConfig(Config):
    DEBUG = True
    ENV = 'development'
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URL', f"sqlite:///{os.path.join(BASE_DIR, 'mvr_associates.db')}")

class TestingConfig(Config):
    TESTING = True
    ENV = 'testing'
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL', 'sqlite:///:memory:')

class ProductionConfig(Config):
    DEBUG = False
    ENV = 'production'
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', f"postgresql://mvr_user:securepass@localhost:5432/mvr_associates_db")

config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
