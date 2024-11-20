from app.models import Survey, FinancialProfile
from app.services.recommendation_generator import RecommendationGenerator
from datetime import datetime
from app.services.goal_generator import GoalGenerator

class SurveyProcessor:
    def __init__(self, survey: Survey):
        self.survey = survey
        self.recommendation_generator = RecommendationGenerator()
        self.goal_generator = GoalGenerator()  # Agregar esta línea

    def process_survey(self) -> FinancialProfile:
        """Procesa la encuesta y genera un perfil financiero con recomendaciones y objetivos"""
        
        # Primero creamos el perfil básico
        profile = self._create_financial_profile()
        
        try:
            # Generar recomendaciones
            recommendations = self.recommendation_generator.generate_recommendations(
                self.survey, profile
            )
            
            # Guardar las recomendaciones en el perfil
            profile.set_recommendations(recommendations.get('recommendations', []))
            profile.set_suggested_goals(recommendations.get('suggested_goals', []))
            profile.set_action_items(recommendations.get('action_items', []))
            
            # Generar objetivos financieros
            goals = self.goal_generator.generate_goals(self.survey, profile)
            
            # Los objetivos se guardarán en la base de datos después de guardar el perfil
            
        except Exception as e:
            print(f"Error al generar recomendaciones o objetivos: {str(e)}")
            
        return profile, goals  # Retornamos también los objetivos

    def _create_financial_profile(self) -> FinancialProfile:
        """Crea un perfil financiero basado en la encuesta"""
        metrics = self._calculate_metrics()
        
        profile = FinancialProfile(
            user_id=self.survey.user_id,
            survey_id=self.survey.id,
            created_at=datetime.utcnow(),
            
            # Métricas calculadas
            savings_ratio=metrics['savings_ratio'],
            debt_ratio=metrics['debt_to_income_ratio'],
            financial_health_score=metrics['financial_health_score'],
            emergency_fund_months=self._calculate_emergency_fund_months(),
            risk_score=metrics['risk_score'],
            
            # Categorización
            risk_profile=self.survey.risk_tolerance,
            investor_type=self._determine_investor_type(metrics['risk_score']),
            financial_status=self._determine_financial_status(metrics['financial_health_score'])
        )

        return profile

    def _calculate_metrics(self) -> dict:
        """Calcula métricas financieras básicas"""
        metrics = {
            'savings_ratio': self._calculate_savings_ratio(),
            'debt_to_income_ratio': self._calculate_debt_ratio(),
            'emergency_fund_months': self._calculate_emergency_fund_months(),
            'risk_score': self._calculate_risk_score(),
            'financial_health_score': self._calculate_financial_health_score()
        }
        return metrics

    def _calculate_savings_ratio(self) -> float:
        """Calcula el ratio de ahorro mensual"""
        if self.survey.monthly_income and self.survey.monthly_income > 0:
            return ((self.survey.monthly_income - self.survey.monthly_expenses) 
                   / self.survey.monthly_income * 100)
        return 0.0

    def _calculate_debt_ratio(self) -> float:
        """Calcula el ratio de deuda respecto a ingresos"""
        if self.survey.monthly_income > 0 and self.survey.has_debts:
            return (self.survey.monthly_debt_payment / self.survey.monthly_income * 100)
        return 0.0

    def _calculate_emergency_fund_months(self) -> float:
        """Calcula cuántos meses de fondo de emergencia tiene"""
        if self.survey.monthly_expenses and self.survey.monthly_expenses > 0:
            return self.survey.current_savings / self.survey.monthly_expenses
        return 0.0

    def _calculate_risk_score(self) -> int:
        """Calcula puntuación de riesgo del 1 al 10"""
        base_score = 5

        # Ajustar por tolerancia al riesgo
        risk_scores = {
            'conservative': -2,
            'moderate': 0,
            'aggressive': 2
        }
        base_score += risk_scores.get(self.survey.risk_tolerance, 0)

        # Ajustar por experiencia
        experience_scores = {
            'none': -1,
            'beginner': 0,
            'intermediate': 1,
            'advanced': 2
        }
        base_score += experience_scores.get(self.survey.investment_experience, 0)

        return max(1, min(10, base_score))

    def _calculate_financial_health_score(self) -> int:
        """Calcula puntuación de salud financiera del 0 al 100"""
        score = 0
        
        # Ratio de ahorro (30 puntos)
        savings_ratio = self._calculate_savings_ratio()
        score += min(30, savings_ratio / 2)  # 20% ahorro = 10 puntos

        # Fondo de emergencia (20 puntos)
        emergency_months = self._calculate_emergency_fund_months()
        score += min(20, emergency_months * 3.33)  # 6 meses = 20 puntos

        # Deuda (20 puntos)
        if not self.survey.has_debts:
            score += 20
        else:
            debt_ratio = self._calculate_debt_ratio()
            score += max(0, 20 - (debt_ratio / 2))

        # Hábitos financieros (30 puntos)
        if self.survey.has_budget:
            score += 10
        if self.survey.tracks_expenses:
            score += 10
        if self.survey.has_emergency_fund:
            score += 10

        return min(100, max(0, int(score)))

    def _determine_investor_type(self, risk_score: int) -> str:
        """Determina el tipo de inversor basado en el score de riesgo"""
        if risk_score <= 3:
            return 'conservative'
        elif risk_score <= 7:
            return 'moderate'
        else:
            return 'aggressive'

    def _determine_financial_status(self, health_score: int) -> str:
        """Determina el estado financiero basado en el score de salud"""
        if health_score >= 80:
            return 'excellent'
        elif health_score >= 60:
            return 'good'
        elif health_score >= 40:
            return 'fair'
        else:
            return 'needs_improvement'