import google.generativeai as genai
from app.models import Survey, FinancialProfile
import os

def load_env_manually():
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

class RecommendationGenerator:
    def __init__(self):
        try:
            # Cargar API key manualmente
            env_vars = load_env_manually()
            api_key = env_vars.get('GOOGLE_API_KEY')
            
            if not api_key:
                raise ValueError("API key no encontrada")
                
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-pro')
        except Exception as e:
            print(f"Error al inicializar Gemini: {str(e)}")
            raise

    def generate_recommendations(self, survey: Survey, profile: FinancialProfile) -> dict:
        """Genera recomendaciones personalizadas basadas en el perfil financiero"""
        try:
            # Crear el prompt para Gemini
            prompt = self._create_prompt(survey, profile)
            
            # Llamar a la API de Gemini
            response = self.model.generate_content([
                {
                    "role": "user",
                    "parts": [{"text": """Eres un asesor financiero experto que proporciona 
                     recomendaciones claras, accionables y personalizadas basadas en el perfil financiero 
                     de las personas. Tus consejos deben ser específicos, prácticos y adaptados a la 
                     situación particular de cada persona."""}]
                },
                {
                    "role": "user",
                    "parts": [{"text": prompt}]
                }
            ])
            
            # Procesar la respuesta
            recommendations = self._process_response(response.text)
            return recommendations
            
        except Exception as e:
            print(f"Error al generar recomendaciones: {str(e)}")
            return self._get_fallback_recommendations()

    def _create_prompt(self, survey: Survey, profile: FinancialProfile) -> str:
        # Crear un prompt detallado basado en el perfil del usuario
        health_status = "excelente" if profile.financial_health_score >= 80 else \
                       "buena" if profile.financial_health_score >= 60 else \
                       "regular" if profile.financial_health_score >= 40 else "necesita mejoras"

        return f"""
        Por favor, analiza el siguiente perfil financiero y proporciona recomendaciones personalizadas:

        DATOS FINANCIEROS BÁSICOS:
        - Ingresos mensuales: ${survey.monthly_income:,.2f}
        - Gastos mensuales: ${survey.monthly_expenses:,.2f}
        - Ahorros actuales: ${survey.current_savings:,.2f}
        - Ratio de ahorro: {profile.savings_ratio:.1f}%
        - Salud financiera: {profile.financial_health_score}/100 ({health_status})

        DEUDAS:
        - Tiene deudas: {"Sí" if survey.has_debts else "No"}
        {f"- Deuda total: ${survey.total_debt:,.2f}" if survey.has_debts else ""}
        {f"- Pago mensual: ${survey.monthly_debt_payment:,.2f}" if survey.has_debts else ""}

        OBJETIVOS Y PERFIL:
        - Objetivo principal: {survey.primary_goal}
        - Monto objetivo: ${survey.goal_amount:,.2f}
        - Plazo objetivo: {survey.goal_timeframe} meses
        - Tolerancia al riesgo: {survey.risk_tolerance}
        - Experiencia en inversiones: {survey.investment_experience}

        HÁBITOS FINANCIEROS:
        - Tiene presupuesto: {"Sí" if survey.has_budget else "No"}
        - Registra gastos: {"Sí" if survey.tracks_expenses else "No"}
        - Tiene fondo de emergencia: {"Sí" if survey.has_emergency_fund else "No"}

        Basado en este perfil, proporciona:
        1. Un RESUMEN BREVE (2-3 oraciones) de su situación financiera actual
        2. 3-5 RECOMENDACIONES específicas y personalizadas
        3. 2-3 OBJETIVOS FINANCIEROS sugeridos con plazos
        4. 3 ACCIONES INMEDIATAS que debería implementar esta semana

        Las recomendaciones deben ser:
        - Específicas y accionables
        - Adaptadas a su situación particular
        - Realistas considerando sus ingresos y gastos
        - Priorizadas según sus necesidades más urgentes

        Formato de respuesta:
        RESUMEN:
        [Resumen aquí]

        RECOMENDACIONES:
        1. [Primera recomendación]
        2. [Segunda recomendación]
        ...

        OBJETIVOS SUGERIDOS:
        1. [Primer objetivo]
        2. [Segundo objetivo]
        ...

        ACCIONES INMEDIATAS:
        1. [Primera acción]
        2. [Segunda acción]
        3. [Tercera acción]
        """

    def _process_response(self, response_text: str) -> dict:
        """Procesa la respuesta de Gemini y la estructura en un diccionario"""
        sections = response_text.split('\n\n')
        result = {
            'summary': '',
            'recommendations': [],
            'suggested_goals': [],
            'action_items': []
        }
        
        current_section = None
        for section in sections:
            if 'RESUMEN:' in section:
                result['summary'] = section.replace('RESUMEN:', '').strip()
            elif 'RECOMENDACIONES:' in section:
                current_section = 'recommendations'
            elif 'OBJETIVOS SUGERIDOS:' in section:
                current_section = 'suggested_goals'
            elif 'ACCIONES INMEDIATAS:' in section:
                current_section = 'action_items'
            elif current_section and section.strip():
                items = [item.strip() for item in section.split('\n') 
                        if item.strip() and item[0].isdigit()]
                result[current_section].extend(items)
        
        return result

    def _get_fallback_recommendations(self) -> dict:
        """Retorna recomendaciones predeterminadas en caso de error"""
        return {
            'summary': 'No se pudieron generar recomendaciones personalizadas en este momento.',
            'recommendations': [
                'Establece un presupuesto mensual detallado',
                'Crea un fondo de emergencia',
                'Revisa y optimiza tus gastos mensuales'
            ],
            'suggested_goals': [
                'Ahorrar el equivalente a 3 meses de gastos para emergencias',
                'Reducir gastos discrecionales en 10%'
            ],
            'action_items': [
                'Registrar todos los gastos durante una semana',
                'Identificar y eliminar gastos innecesarios',
                'Establecer una transferencia automática para ahorros'
            ]
        }