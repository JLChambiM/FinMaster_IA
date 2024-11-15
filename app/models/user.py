from app import db, login_manager
from flask_login import UserMixin
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)

    # Relaciones actualizadas
    surveys = db.relationship('Survey', back_populates='user', lazy=True)
    financial_profiles = db.relationship('FinancialProfile', 
                                      back_populates='user',
                                      lazy=True,
                                      order_by='desc(FinancialProfile.created_at)')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_latest_survey(self):
        from .survey import Survey
        return Survey.query.filter_by(user_id=self.id).order_by(Survey.created_at.desc()).first()

    def get_profile(self):
        """Obtiene el perfil más reciente"""
        return self.financial_profiles[0] if self.financial_profiles else None

class OAuth(OAuthConsumerMixin, db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))