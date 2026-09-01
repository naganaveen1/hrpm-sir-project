import re
from datetime import datetime
from app.models import db

class Article(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False, index=True)
    excerpt = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False, default='Tax & Legal')
    featured_image = db.Column(db.String(255), nullable=True)
    is_published = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @staticmethod
    def generate_slug(title):
        if not title:
            return ""
        slug = re.sub(r'[^a-zA-Z0-9\s-]', '', title.lower())
        slug = re.sub(r'[\s-]+', '-', slug).strip('-')
        
        original_slug = slug or 'article'
        candidate_slug = original_slug
        count = 1
        while Article.query.filter_by(slug=candidate_slug).first():
            candidate_slug = f"{original_slug}-{count}"
            count += 1
        return candidate_slug

    @property
    def author(self):
        return "MVR Associates Editorial"

    def __repr__(self):
        return f'<Article {self.title}>'

