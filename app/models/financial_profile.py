from app import db
from datetime import datetime
import json

class FinancialProfile(db.Model):
    __tablename__ = 'financial_profile'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    survey_id = db.Column(db.Integer, db.ForeignKey('survey.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Métricas calculadas
    savings_ratio = db.Column(db.Float)
    debt_ratio = db.Column(db.Float)
    financial_health_score = db.Column(db.Integer)
    emergency_fund_months = db.Column(db.Float)
    risk_score = db.Column(db.Integer)
    
    # Categorización
    risk_profile = db.Column(db.String(20))
    investor_type = db.Column(db.String(50))
    financial_status = db.Column(db.String(50))
    
    # Recomendaciones y metas
    recommendations = db.Column(db.Text)
    suggested_goals = db.Column(db.Text)
    action_items = db.Column(db.Text)
    
    # Relaciones
    user = db.relationship('User', backref=db.backref('financial_profiles', lazy=True))
    survey = db.relationship('Survey', backref=db.backref('financial_profile', uselist=False))

    def __init__(self, **kwargs):
        super(FinancialProfile, self).__init__(**kwargs)

    def set_recommendations(self, recommendations: list):
        """Guarda las recomendaciones como JSON"""
        self.recommendations = json.dumps(recommendations)

    def get_recommendations(self) -> list:
        """Obtiene las recomendaciones desde JSON"""
        return json.loads(self.recommendations) if self.recommendations else []

    def set_suggested_goals(self, goals: list):
        """Guarda las metas sugeridas como JSON"""
        self.suggested_goals = json.dumps(goals)

    def get_suggested_goals(self) -> list:
        """Obtiene las metas sugeridas desde JSON"""
        return json.loads(self.suggested_goals) if self.suggested_goals else []

    def set_action_items(self, items: list):
        """Guarda los items de acción como JSON"""
        self.action_items = json.dumps(items)

    def get_action_items(self) -> list:
        """Obtiene los items de acción desde JSON"""
        return json.loads(self.action_items) if self.action_items else []

    def to_dict(self):
        """Convierte el perfil a un diccionario"""
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'savings_ratio': self.savings_ratio,
            'debt_ratio': self.debt_ratio,
            'financial_health_score': self.financial_health_score,
            'emergency_fund_months': self.emergency_fund_months,
            'risk_score': self.risk_score,
            'risk_profile': self.risk_profile,
            'investor_type': self.investor_type,
            'financial_status': self.financial_status,
            'recommendations': self.get_recommendations(),
            'suggested_goals': self.get_suggested_goals(),
            'action_items': self.get_action_items()
        }

    def __repr__(self):
        return f'<FinancialProfile {self.id} for User {self.user_id}>'