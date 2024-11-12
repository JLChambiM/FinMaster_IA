from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.forms.survey import SurveyForm
from app.models import Survey
from app.services.survey_processor import SurveyProcessor
from app import db
from datetime import datetime

bp = Blueprint('survey_blueprint', __name__, url_prefix='/survey')

@bp.route('/purpose')
@login_required
def purpose():
    return render_template('survey/purpose.html')

@bp.route('/start', methods=['GET', 'POST'])
@login_required
def start():
    form = SurveyForm()
    
    if form.validate_on_submit():
        try:
            # Crear encuesta
            survey = Survey(
                user_id=current_user.id,
                created_at=datetime.utcnow(),
                is_completed=True,
                completed_at=datetime.utcnow(),
                
                monthly_income=form.monthly_income.data,
                monthly_expenses=form.monthly_expenses.data,
                current_savings=form.current_savings.data,
                has_debts=form.has_debts.data,
                total_debt=form.total_debt.data if form.has_debts.data else 0,
                monthly_debt_payment=form.monthly_debt_payment.data if form.has_debts.data else 0,
                primary_goal=form.primary_goal.data,
                goal_timeframe=form.goal_timeframe.data,
                goal_amount=form.goal_amount.data,
                risk_tolerance=form.risk_tolerance.data,
                investment_experience=form.investment_experience.data,
                has_budget=form.has_budget.data,
                tracks_expenses=form.tracks_expenses.data,
                has_emergency_fund=form.has_emergency_fund.data
            )
            
            # Guardar encuesta
            db.session.add(survey)
            db.session.commit()

            # Procesar encuesta y crear perfil
            processor = SurveyProcessor(survey)
            profile = processor.process_survey()
            
            # Guardar perfil
            db.session.add(profile)
            db.session.commit()
            
            flash('¡Encuesta completada! Tu perfil financiero ha sido creado.', 'success')
            return redirect(url_for('profile_blueprint.view_profile'))
            
        except Exception as e:
            db.session.rollback()
            flash('Error al procesar la encuesta. Por favor intenta nuevamente.', 'danger')
            print(f"Error: {str(e)}")
    
    return render_template('survey/survey.html', form=form)