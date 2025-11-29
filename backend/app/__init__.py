from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import DevelopmentConfig

# initialize the SQLAlchemy object at module level
dbq = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    # Enable CORS for API routes from the frontend origin used in development.
    CORS(app)
    dbq.init_app(app)

    # import blueprints here to avoid circular imports
    from app.routes.user_routes import user_bp
    from app.routes.user_roles_routes import user_roles_bp

    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(user_roles_bp, url_prefix='/api/user_roles')

    with app.app_context():
        dbq.create_all()

    return app