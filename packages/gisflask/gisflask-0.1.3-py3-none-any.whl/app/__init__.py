import os
import logging
from flask import Flask
from flask_cors import CORS
from flasgger import Swagger
from app.extensions import db, migrate, jwt, bcrypt
from app.config import config_by_name

logging.basicConfig(level=logging.DEBUG)

def create_app(config_name='development'):
    app = Flask(__name__)
    app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")
    app.config.from_object(config_by_name[config_name])
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)
    CORS(app)
    
    # Initialize Swagger
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": "apispec",
                "route": "/apispec.json",
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/docs/"
    }
    Swagger(app, config=swagger_config)

    # Register blueprints
    from app.auth import auth_bp
    from app.main import main_bp
    from app.users import users_bp
    from app.products import products_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(products_bp)
    
    # Create a health check route
    @app.route('/health')
    def health_check():
        """
        Health Check Endpoint
        ---
        responses:
          200:
            description: Service is healthy
        """
        return {"status": "healthy"}, 200
    
    return app
