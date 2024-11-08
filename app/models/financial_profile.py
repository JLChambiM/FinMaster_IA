from app import db
from datetime import datetime
import json

class FinancialProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    survey_id = db.Column(db.Integer, db.ForeignKey('survey.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Métricas calculadas
    savings_ratio = db.Column(db.Float)
    debt_ratio = db.Column(db.Float)
    financial_health_score = db.Column(db.Integer)
    
    # Categorización
    risk_profile = db.Column(db.String(20))
    investor_type = db.Column(db.String(50))
    financial_status = db.Column(db.String(50))
    
    # Recomendaciones y metas
    recommendations = db.Column(db.Text)
    suggested_goals = db.Column(db.Text)
    action_items = db.Column(db.Text)

    def set_recommendations(self, recommendations):
        self.recommendations = json.dumps(recommendations)

    def get_recommendations(self):
        return json.loads(self.recommendations) if self.recommendations else []

    def set_suggested_goals(self, goals):
        self.suggested_goals = json.dumps(goals)

    def get_suggested_goals(self):
        return json.loads(self.suggested_goals) if self.suggested_goals else []

    def set_action_items(self, items):
        self.action_items = json.dumps(items)

    def get_action_items(self):
        return json.loads(self.action_items) if self.action_items else []