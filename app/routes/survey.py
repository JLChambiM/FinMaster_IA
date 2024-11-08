from flask import Blueprint, render_template
from flask_login import login_required

bp = Blueprint('survey_blueprint', __name__, url_prefix='/survey')

@bp.route('/purpose')
@login_required
def purpose():
    try:
        return render_template('survey/purpose.html')
    except Exception as e:
        print(f"Error en purpose: {str(e)}")
        raise

@bp.route('/start')
@login_required
def start():
    try:
        return render_template('survey/survey.html')
    except Exception as e:
        print(f"Error en start: {str(e)}")
        raise