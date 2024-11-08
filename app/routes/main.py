from flask import Blueprint, render_template
from flask_login import login_required

# Definimos el blueprint con el nombre completo desde el inicio
bp = Blueprint('main_blueprint', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')