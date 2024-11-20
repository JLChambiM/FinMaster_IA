from app import db
from datetime import datetime

class FinancialGoal(db.Model):
    __tablename__ = 'financial_goal'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    profile_id = db.Column(db.Integer, db.ForeignKey('financial_profile.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Detalles del objetivo
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))  # ahorro, deuda, inversión, etc.
    
    # Métricas
    target_amount = db.Column(db.Float)  # Monto objetivo
    current_amount = db.Column(db.Float, default=0.0)  # Progreso actual
    initial_amount = db.Column(db.Float)  # Monto inicial
    
    # Plazos
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    target_date = db.Column(db.DateTime)
    
    # Estado
    status = db.Column(db.String(20), default='pending')  # pending, in_progress, completed, cancelled
    is_suggested = db.Column(db.Boolean, default=True)  # True si fue sugerido por IA
    
    # Relaciones
    user = db.relationship('User', back_populates='financial_goals')
    profile = db.relationship('FinancialProfile', back_populates='goals')

    def calculate_progress(self):
        """Calcula el porcentaje de progreso"""
        if self.target_amount and self.target_amount > 0:
            return (self.current_amount / self.target_amount) * 100
        return 0

    def to_dict(self):
        """Convierte el objetivo a un diccionario"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'target_amount': self.target_amount,
            'current_amount': self.current_amount,
            'progress': self.calculate_progress(),
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'target_date': self.target_date.isoformat() if self.target_date else None,
            'status': self.status,
            'is_suggested': self.is_suggested
        }