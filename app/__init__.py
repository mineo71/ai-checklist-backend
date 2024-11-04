from flask import Flask
from app.config import DevelopmentConfig
from app.extensions import init_extensions, mongo
from app.auth.routes import auth_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    init_extensions(app)

    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app
