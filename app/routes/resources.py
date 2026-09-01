from flask import Blueprint, render_template, request, abort, url_for
from app.models.article import Article

resources_bp = Blueprint('resources', __name__, url_prefix='/resources')

CATEGORIES = ['Business', 'Tax', 'Finance', 'Legal', 'HR']

@resources_bp.route('/')
def index():
    search_query = request.args.get('q', '').strip()
    category_filter = request.args.get('category', '').strip()

    query = Article.query.filter_by(is_published=True)

    if search_query:
        query = query.filter(
            (Article.title.ilike(f"%{search_query}%")) |
            (Article.excerpt.ilike(f"%{search_query}%")) |
            (Article.content.ilike(f"%{search_query}%"))
        )

    if category_filter and category_filter in CATEGORIES:
        query = query.filter_by(category=category_filter)

    articles = query.order_by(Article.created_at.desc()).all()

    return render_template(
        'resources/index.html',
        active_page='resources',
        articles=articles,
        categories=CATEGORIES,
        selected_category=category_filter,
        search_query=search_query
    )

@resources_bp.route('/<slug>')
def detail(slug):
    article = Article.query.filter_by(slug=slug, is_published=True).first_or_404()

    # Related articles in same category
    related_articles = Article.query.filter(
        Article.is_published == True,
        Article.category == article.category,
        Article.id != article.id
    ).order_by(Article.created_at.desc()).limit(3).all()

    # Fallback to latest articles if not enough in same category
    if len(related_articles) < 3:
        needed = 3 - len(related_articles)
        existing_ids = [a.id for a in related_articles] + [article.id]
        more_articles = Article.query.filter(
            Article.is_published == True,
            Article.id.notin_(existing_ids)
        ).order_by(Article.created_at.desc()).limit(needed).all()
        related_articles.extend(more_articles)

    return render_template(
        'resources/detail.html',
        active_page='resources',
        article=article,
        related_articles=related_articles
    )
