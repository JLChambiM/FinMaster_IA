from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import FinancialProfile

bp = Blueprint('main_blueprint', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/dashboard')
@login_required
def dashboard():
    profile = FinancialProfile.query.filter_by(user_id=current_user.id)\
        .order_by(FinancialProfile.created_at.desc())\
        .first()
    
    return render_template('dashboard.html', profile=profile)