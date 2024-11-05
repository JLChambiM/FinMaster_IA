from flask_dance.contrib.google import make_google_blueprint, google
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
from flask_dance.consumer import oauth_authorized
from flask import flash, redirect, url_for, current_app
from flask_login import login_user, current_user
from app.models import User, OAuth
from app import db
import os

blueprint = make_google_blueprint(
    client_id=os.getenv('GOOGLE_CLIENT_ID'),
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
    scope=["profile", "email"],
    storage=SQLAlchemyStorage(OAuth, db.session, user=current_user)
)

@blueprint.route('/google')
def google_login():
    if not google.authorized:
        return redirect(url_for('google.login'))
    
    try:
        resp = google.get('/oauth2/v2/userinfo')
        assert resp.ok, resp.text
        
        email = resp.json()['email']
        user = User.query.filter_by(email=email).first()
        
        if not user:
            user = User(email=email, is_active=True)
            db.session.add(user)
            db.session.commit()
            flash('Cuenta creada exitosamente', 'success')
        
        login_user(user)
        flash('Inicio de sesión exitoso', 'success')
        return redirect(url_for('main.index'))
        
    except Exception as e:
        flash(f'Error durante el inicio de sesión: {str(e)}', 'error')
        return redirect(url_for('auth.login'))

@oauth_authorized.connect_via(blueprint)
def google_logged_in(blueprint, token):
    if not token:
        flash('No se pudo iniciar sesión con Google.', 'error')
        return False
    
    resp = blueprint.session.get('/oauth2/v2/userinfo')
    if not resp.ok:
        flash('No se pudo obtener la información del usuario.', 'error')
        return False

    info = resp.json()
    email = info['email']

    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(email=email, is_active=True)
        db.session.add(user)
        db.session.commit()

    login_user(user)
    flash('Inicio de sesión exitoso con Google', 'success')
    return redirect(url_for('main.index'))