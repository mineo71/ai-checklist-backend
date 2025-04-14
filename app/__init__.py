from flask import Flask
from app.config import DevelopmentConfig
from app.data.routes import data_bp
from app.extensions import init_extensions, mongo
from app.auth.routes import auth_bp
from app.hives.routes import hive_bp
from app.invitations.routes import invite_bp
from app.settings.routes import settings_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    init_extensions(app)

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(hive_bp, url_prefix='/api')
    app.register_blueprint(settings_bp, url_prefix='/api')
    app.register_blueprint(data_bp, url_prefix='/api')
    app.register_blueprint(invite_bp, url_prefix='/api')

    return app
