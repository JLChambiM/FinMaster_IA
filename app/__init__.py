from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from .config import Config
import os

# Permitir OAuth sin HTTPS en desarrollo
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Inicializar extensiones
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    login_manager.login_view = 'auth_blueprint.login'
    
    # Importar modelos
    from app import models
    
    # Importar blueprints
    from app.routes import main, auth, survey, profile
    from app.oauth import blueprint as google_blueprint
    
    # Registrar blueprints
    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(survey.bp)
    app.register_blueprint(profile.bp)
    app.register_blueprint(google_blueprint, name='google_blueprint')

    return app