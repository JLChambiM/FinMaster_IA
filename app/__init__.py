from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from .config import Config
import os

# Permitir OAuth sin HTTPS en desarrollo
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Configuración adicional para debugging
    app.config['DEBUG'] = True
    
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    login_manager.login_view = 'auth.login'
    
    from app import models
    from app.routes import main, auth
    from app.oauth import blueprint as google_blueprint
    
    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(google_blueprint, url_prefix="/login")

    return app