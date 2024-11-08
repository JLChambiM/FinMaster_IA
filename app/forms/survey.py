from flask_wtf import FlaskForm
from wtforms import FloatField, SelectField, BooleanField, StringField, IntegerField
from wtforms.validators import DataRequired, Optional, NumberRange

class SurveyForm(FlaskForm):
    # Paso 1: Información de Ingresos
    monthly_income = FloatField('Ingresos Mensuales', 
        validators=[DataRequired(message="Este campo es requerido")],
        render_kw={"placeholder": "Ej: 5000.00"})
    
    monthly_expenses = FloatField('Gastos Mensuales',
        validators=[DataRequired(message="Este campo es requerido")],
        render_kw={"placeholder": "Ej: 3000.00"})
    
    current_savings = FloatField('Ahorros Actuales',
        validators=[DataRequired(message="Este campo es requerido")],
        render_kw={"placeholder": "Ej: 10000.00"})

    # Paso 2: Deudas y Préstamos
    has_debts = BooleanField('¿Tienes deudas actualmente?')
    
    total_debt = FloatField('Deuda Total',
        validators=[Optional()],
        render_kw={"placeholder": "Ej: 15000.00"})
    
    monthly_debt_payment = FloatField('Pago Mensual de Deudas',
        validators=[Optional()],
        render_kw={"placeholder": "Ej: 500.00"})

    # Paso 3: Objetivos Financieros
    primary_goal = SelectField('Objetivo Financiero Principal',
        choices=[
            ('emergency_fund', 'Crear un fondo de emergencia'),
            ('save_home', 'Ahorrar para una casa'),
            ('save_car', 'Ahorrar para un coche'),
            ('invest', 'Invertir para el futuro'),
            ('pay_debt', 'Pagar deudas'),
            ('retirement', 'Planificar jubilación'),
            ('other', 'Otro')
        ],
        validators=[DataRequired(message="Por favor selecciona un objetivo")])
    
    goal_timeframe = IntegerField('Plazo para alcanzar el objetivo (meses)',
        validators=[NumberRange(min=1, max=600, message="Por favor ingresa un plazo válido")],
        render_kw={"placeholder": "Ej: 24"})
    
    goal_amount = FloatField('Monto objetivo',
        validators=[DataRequired(message="Este campo es requerido")],
        render_kw={"placeholder": "Ej: 50000.00"})

    # Paso 4: Perfil de Riesgo
    risk_tolerance = SelectField('Tolerancia al Riesgo',
        choices=[
            ('conservative', 'Conservador - Prefiero seguridad sobre rendimiento'),
            ('moderate', 'Moderado - Balance entre seguridad y rendimiento'),
            ('aggressive', 'Agresivo - Prefiero mayor rendimiento asumiendo más riesgo')
        ],
        validators=[DataRequired(message="Por favor selecciona tu perfil de riesgo")])
    
    investment_experience = SelectField('Experiencia en Inversiones',
        choices=[
            ('none', 'Sin experiencia'),
            ('beginner', 'Principiante'),
            ('intermediate', 'Intermedio'),
            ('advanced', 'Avanzado')
        ],
        validators=[DataRequired(message="Por favor selecciona tu nivel de experiencia")])

    # Paso 5: Hábitos Financieros
    has_budget = BooleanField('¿Llevas un presupuesto mensual?')
    tracks_expenses = BooleanField('¿Registras tus gastos regularmente?')
    has_emergency_fund = BooleanField('¿Tienes un fondo de emergencia?')