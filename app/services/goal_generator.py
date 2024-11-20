import google.generativeai as genai
from app.models import Survey, FinancialProfile, FinancialGoal
from datetime import datetime, timedelta
import os

class GoalGenerator:
    def __init__(self):
        try:
            env_vars = self._load_env_manually()
            api_key = env_vars.get('GOOGLE_API_KEY')
            
            if not api_key:
                raise ValueError("API key no encontrada")
                
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-pro')
        except Exception as e:
            print(f"Error al inicializar Gemini: {str(e)}")
            raise

    def _load_env_manually(self):
        """Carga manual del archivo .env"""
        env_vars = {}
        try:
            with open('.env', 'r') as file:
                for line in file:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        key, value = line.split('=', 1)
                        env_vars[key.strip()] = value.strip()
        except Exception as e:
            print(f"Error leyendo .env: {e}")
        return env_vars

    def generate_goals(self, survey: Survey, profile: FinancialProfile) -> list:
        """Genera objetivos financieros basados en el perfil del usuario"""
        try:
            prompt = self._create_prompt(survey, profile)
            response = self.model.generate_content([
                {
                    "role": "user",
                    "parts": [{"text": """Eres un asesor financiero experto especializado en 
                    establecer objetivos financieros realistas y alcanzables. Tu tarea es analizar 
                    el perfil financiero y sugerir objetivos específicos, medibles y con plazos definidos."""}]
                },
                {
                    "role": "user",
                    "parts": [{"text": prompt}]
                }
            ])
            
            goals = self._process_response(response.text)
            return self._create_goal_objects(goals, profile)
            
        except Exception as e:
            print(f"Error al generar objetivos: {str(e)}")
            return self._get_fallback_goals(profile)

    def _create_prompt(self, survey: Survey, profile: FinancialProfile) -> str:
        health_status = "excelente" if profile.financial_health_score >= 80 else \
                       "buena" if profile.financial_health_score >= 60 else \
                       "regular" if profile.financial_health_score >= 40 else "necesita mejoras"

        return f"""
        Analiza este perfil financiero y sugiere 3-5 objetivos financieros específicos:

        PERFIL FINANCIERO:
        - Ingresos mensuales: ${survey.monthly_income:,.2f}
        - Gastos mensuales: ${survey.monthly_expenses:,.2f}
        - Ahorros actuales: ${survey.current_savings:,.2f}
        - Ratio de ahorro: {profile.savings_ratio:.1f}%
        - Salud financiera: {profile.financial_health_score}/100 ({health_status})
        
        DEUDAS:
        - Tiene deudas: {"Sí" if survey.has_debts else "No"}
        {f"- Deuda total: ${survey.total_debt:,.2f}" if survey.has_debts else ""}
        {f"- Pago mensual: ${survey.monthly_debt_payment:,.2f}" if survey.has_debts else ""}
        
        OBJETIVO PRINCIPAL:
        - {survey.primary_goal}
        - Monto objetivo: ${survey.goal_amount:,.2f}
        - Plazo: {survey.goal_timeframe} meses

        Por favor, sugiere objetivos que:
        1. Sean específicos y medibles
        2. Tengan montos y plazos definidos
        3. Estén alineados con su capacidad financiera actual
        4. Consideren la reducción de deudas si existen
        5. Incluyan la construcción de ahorros de emergencia

        Formato de respuesta para cada objetivo:
        OBJETIVO:
        - Título: [título corto]
        - Descripción: [descripción detallada]
        - Categoría: [ahorro/deuda/inversión]
        - Monto objetivo: [cantidad en USD]
        - Plazo: [número de meses]
        """

    def _process_response(self, response_text: str) -> list:
        """Procesa la respuesta de la IA y extrae los objetivos"""
        goals = []
        current_goal = {}
        
        lines = response_text.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('OBJETIVO:'):
                if current_goal:
                    goals.append(current_goal.copy())
                current_goal = {}
            elif line.startswith('- Título:'):
                current_goal['title'] = line.replace('- Título:', '').strip()
            elif line.startswith('- Descripción:'):
                current_goal['description'] = line.replace('- Descripción:', '').strip()
            elif line.startswith('- Categoría:'):
                current_goal['category'] = line.replace('- Categoría:', '').strip()
            elif line.startswith('- Monto objetivo:'):
                amount_str = line.replace('- Monto objetivo:', '').strip()
                amount_str = amount_str.replace('$', '').replace(',', '')
                try:
                    current_goal['target_amount'] = float(amount_str)
                except:
                    current_goal['target_amount'] = 0.0
            elif line.startswith('- Plazo:'):
                months_str = line.replace('- Plazo:', '').strip()
                months_str = months_str.replace('meses', '').strip()
                try:
                    current_goal['timeframe'] = int(months_str)
                except:
                    current_goal['timeframe'] = 12

        if current_goal:
            goals.append(current_goal)
            
        return goals

    def _create_goal_objects(self, goals_data: list, profile: FinancialProfile) -> list:
        """Convierte los datos de objetivos en objetos FinancialGoal"""
        goal_objects = []
        
        for goal_data in goals_data:
            goal = FinancialGoal(
                user_id=profile.user_id,
                profile_id=profile.id,
                title=goal_data.get('title', 'Objetivo Sin Título'),
                description=goal_data.get('description', ''),
                category=goal_data.get('category', 'ahorro'),
                target_amount=goal_data.get('target_amount', 0.0),
                current_amount=0.0,
                initial_amount=0.0,
                start_date=datetime.utcnow(),
                target_date=datetime.utcnow() + timedelta(days=30 * goal_data.get('timeframe', 12)),
                status='pending',
                is_suggested=True
            )
            goal_objects.append(goal)
            
        return goal_objects

    def _get_fallback_goals(self, profile: FinancialProfile) -> list:
        """Retorna objetivos predeterminados en caso de error"""
        return [
            FinancialGoal(
                user_id=profile.user_id,
                profile_id=profile.id,
                title="Crear Fondo de Emergencia",
                description="Establecer un fondo de emergencia equivalente a 3 meses de gastos",
                category="ahorro",
                target_amount=profile.survey.monthly_expenses * 3 if profile.survey else 5000,
                status='pending',
                target_date=datetime.utcnow() + timedelta(days=180),
                is_suggested=True
            ),
            FinancialGoal(
                user_id=profile.user_id,
                profile_id=profile.id,
                title="Optimizar Gastos Mensuales",
                description="Reducir gastos mensuales en un 10%",
                category="ahorro",
                target_amount=profile.survey.monthly_expenses * 0.1 if profile.survey else 200,
                status='pending',
                target_date=datetime.utcnow() + timedelta(days=90),
                is_suggested=True
            )
        ]