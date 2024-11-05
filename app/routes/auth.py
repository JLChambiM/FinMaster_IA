from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from app.models import User
from app import db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User(email=email)
        user.set_password(password)

        try:
            db.session.add(user)
            db.session.commit()
            flash('¡Registro exitoso! Por favor, inicia sesión.', 'success')
            return redirect(url_for('auth.login'))
        except:
            db.session.rollback()
            flash('Ocurrió un error al registrar tu cuenta. Por favor, inténtalo de nuevo.', 'danger')

    return render_template('auth/register.html')