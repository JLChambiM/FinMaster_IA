from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import FinancialProfile

bp = Blueprint('profile_blueprint', __name__, url_prefix='/profile')

@bp.route('/')
@login_required
def view_profile():
    # Obtener el perfil más reciente del usuario
    profile = FinancialProfile.query.filter_by(user_id=current_user.id)\
        .order_by(FinancialProfile.created_at.desc())\
        .first()
    
    if not profile:
        return render_template('profile/no_profile.html')
    
    return render_template('profile/view.html', profile=profile)