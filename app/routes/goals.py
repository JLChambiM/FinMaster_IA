from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import FinancialGoal, FinancialProfile
from app import db

bp = Blueprint('goals_blueprint', __name__, url_prefix='/goals')

@bp.route('/')
@login_required
def view_goals():
    # Obtener el perfil más reciente
    profile = FinancialProfile.query.filter_by(user_id=current_user.id)\
        .order_by(FinancialProfile.created_at.desc())\
        .first()
    
    if not profile:
        return redirect(url_for('survey_blueprint.purpose'))
    
    # Obtener objetivos organizados por categoría
    goals_by_category = {}
    for goal in profile.goals:
        category = goal.category
        if category not in goals_by_category:
            goals_by_category[category] = []
        goals_by_category[category].append(goal)
    
    return render_template('goals/view.html', 
                         profile=profile, 
                         goals_by_category=goals_by_category)