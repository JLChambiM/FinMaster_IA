from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
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


@bp.route('/login', methods=['GET', 'POST'])
def login():
    # Si el usuario ya está autenticado, redirigir al dashboard
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            # Login exitoso
            login_user(user)
            flash('Has iniciado sesión exitosamente.', 'success')
            
            # Redirigir a la página que el usuario intentaba acceder
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.dashboard'))
        else:
            # Login fallido
            flash('Email o contraseña incorrectos.', 'danger')
    
    return render_template('auth/login.html')

@bp.route('/logout')
@login_required  # Solo usuarios autenticados pueden cerrar sesión
def logout():
    logout_user()
    flash('Has cerrado sesión exitosamente.', 'success')
    return redirect(url_for('main.index'))
