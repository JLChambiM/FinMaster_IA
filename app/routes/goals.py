from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.models import LearningGoal, FinancialProfile

bp = Blueprint('goals_blueprint', __name__, url_prefix='/goals')

@bp.route('/')
@login_required
def view_goals():
    # Obtener el perfil más reciente del usuario
    profile = FinancialProfile.query.filter_by(user_id=current_user.id)\
        .order_by(FinancialProfile.created_at.desc())\
        .first()
    
    if not profile:
        return redirect(url_for('survey_blueprint.purpose'))
    
    return render_template('goals/view.html', profile=profile)