from app import db
from datetime import datetime

class LearningGoal(db.Model):
    __tablename__ = 'learning_goal'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    profile_id = db.Column(db.Integer, db.ForeignKey('financial_profile.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Categorías de aprendizaje
    CATEGORIES = {
        'basic_concepts': 'Conceptos Básicos',
        'budgeting': 'Presupuesto',
        'debt_management': 'Manejo de Deudas',
        'savings': 'Ahorro',
        'investment_basics': 'Inversión Básica'
    }

    # Detalles del objetivo
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))
    importance = db.Column(db.String(20))  # high, medium, low
    status = db.Column(db.String(20), default='pending')  # pending, in_progress, completed

    # Relaciones
    user = db.relationship('User', back_populates='learning_goals')
    profile = db.relationship('FinancialProfile', back_populates='learning_goals')

    @property
    def category_info(self):
        """Retorna información de la categoría"""
        category_data = {
            'basic_concepts': {
                'name': 'Conceptos Básicos',
                'icon': 'bi-book',
                'color': 'primary'
            },
            'budgeting': {
                'name': 'Presupuesto',
                'icon': 'bi-calculator',
                'color': 'success'
            },
            'debt_management': {
                'name': 'Manejo de Deudas',
                'icon': 'bi-credit-card',
                'color': 'danger'
            },
            'savings': {
                'name': 'Ahorro',
                'icon': 'bi-piggy-bank',
                'color': 'info'
            },
            'investment_basics': {
                'name': 'Inversión Básica',
                'icon': 'bi-graph-up',
                'color': 'warning'
            }
        }
        return category_data.get(self.category, {
            'name': 'Otro',
            'icon': 'bi-star',
            'color': 'secondary'
        })