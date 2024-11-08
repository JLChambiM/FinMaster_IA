from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.forms.survey import SurveyForm
from app.models import Survey
from app import db
from datetime import datetime

bp = Blueprint('survey_blueprint', __name__, url_prefix='/survey')

@bp.route('/purpose')
@login_required
def purpose():
    """Muestra la página de propósito de la encuesta"""
    return render_template('survey/purpose.html')

@bp.route('/start', methods=['GET', 'POST'])
@login_required
def start():
    """Maneja el formulario de la encuesta"""
    form = SurveyForm()
    
    if form.validate_on_submit():
        try:
            survey = Survey(
                # Datos del usuario
                user_id=current_user.id,
                created_at=datetime.utcnow(),
                is_completed=True,
                completed_at=datetime.utcnow(),
                
                # Paso 1: Información básica
                monthly_income=form.monthly_income.data,
                monthly_expenses=form.monthly_expenses.data,
                current_savings=form.current_savings.data,
                
                # Paso 2: Deudas y préstamos
                has_debts=form.has_debts.data,
                total_debt=form.total_debt.data if form.has_debts.data else 0,
                monthly_debt_payment=form.monthly_debt_payment.data if form.has_debts.data else 0,
                
                # Paso 3: Objetivos financieros
                primary_goal=form.primary_goal.data,
                goal_timeframe=form.goal_timeframe.data,
                goal_amount=form.goal_amount.data,
                
                # Paso 4: Perfil de riesgo
                risk_tolerance=form.risk_tolerance.data,
                investment_experience=form.investment_experience.data,
                
                # Paso 5: Hábitos financieros
                has_budget=form.has_budget.data,
                tracks_expenses=form.tracks_expenses.data,
                has_emergency_fund=form.has_emergency_fund.data
            )
            
            db.session.add(survey)
            db.session.commit()
            
            flash('¡Encuesta completada exitosamente! Revisa tus recomendaciones personalizadas.', 'success')
            return redirect(url_for('main_blueprint.dashboard'))
            
        except Exception as e:
            db.session.rollback()
            flash('Error al guardar la encuesta. Por favor intenta nuevamente.', 'danger')
            print(f"Error guardando la encuesta: {str(e)}")
    
    if form.errors:
        print("Errores de validación:", form.errors)
        flash('Por favor verifica los campos marcados en rojo.', 'danger')
    
    return render_template('survey/survey.html', form=form)