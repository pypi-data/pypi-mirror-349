from flask import Blueprint

products_bp = Blueprint('products', __name__, url_prefix='/products')

from app.products import routes