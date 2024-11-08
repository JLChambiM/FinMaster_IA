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
    storage=SQLAlchemyStorage(OAuth, db.session, user=current_user),
    authorized_url="/login/google/authorized",  # Explícitamente definir la URL
    redirect_url="/login/google/authorized"     # URL de redirección
)

@oauth_authorized.connect_via(blueprint)
def google_logged_in(blueprint, token):
    if not token:
        print("No token received")  # Debug print
        flash('Error al iniciar sesión con Google.', 'error')
        return False

    try:
        resp = blueprint.session.get('/oauth2/v2/userinfo')
        if not resp.ok:
            print(f"Failed to get user info: {resp.text}")  # Debug print
            flash('Error al obtener información del usuario.', 'error')
            return False

        info = resp.json()
        email = info.get('email')
        if not email:
            print("No email in response")  # Debug print
            flash('No se pudo obtener el email.', 'error')
            return False

        user = User.query.filter_by(email=email).first()
        if not user:
            user = User(email=email, is_active=True)
            db.session.add(user)
            db.session.commit()

        login_user(user)
        flash('Inicio de sesión exitoso con Google', 'success')
        return False  # Let Flask-Dance handle the redirect

    except Exception as e:
        print(f"Error during login: {str(e)}")  # Debug print
        flash(f'Error inesperado: {str(e)}', 'error')
        return False