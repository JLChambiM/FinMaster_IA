from app import db
from datetime import datetime

class Survey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    is_completed = db.Column(db.Boolean, default=False)

    # Paso 1: Información básica
    monthly_income = db.Column(db.Float)
    monthly_expenses = db.Column(db.Float)
    current_savings = db.Column(db.Float)
    
    # Paso 2: Deudas y préstamos
    has_debts = db.Column(db.Boolean, default=False)
    total_debt = db.Column(db.Float)
    monthly_debt_payment = db.Column(db.Float)
    
    # Paso 3: Objetivos financieros
    primary_goal = db.Column(db.String(100))
    goal_timeframe = db.Column(db.Integer)  # en meses
    goal_amount = db.Column(db.Float)
    
    # Paso 4: Perfil de riesgo
    risk_tolerance = db.Column(db.String(20))  # 'conservative', 'moderate', 'aggressive'
    investment_experience = db.Column(db.String(20))  # 'none', 'beginner', 'intermediate', 'advanced'
    
    # Paso 5: Hábitos financieros
    has_budget = db.Column(db.Boolean, default=False)
    tracks_expenses = db.Column(db.Boolean, default=False)
    has_emergency_fund = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Survey {self.id} de {self.user_id}>'