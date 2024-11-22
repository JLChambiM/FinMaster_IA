import google.generativeai as genai
from app.models import Survey, FinancialProfile, LearningGoal
from datetime import datetime, timedelta
import os
import re

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
        try:
            print("Iniciando generación de objetivos de aprendizaje...")
            prompt = self._create_prompt(survey, profile)
            
            response = self.model.generate_content([
                {
                    "role": "user",
                    "parts": [{"text": """Eres un asesor financiero educativo experto. 
                    Tu tarea es sugerir objetivos de aprendizaje personalizados para mejorar 
                    la educación financiera del usuario basándote en su perfil."""}]
                },
                {
                    "role": "user",
                    "parts": [{"text": prompt}]
                }
            ])
            
            learning_goals = self._process_response(response.text)
            return self._create_goal_objects(learning_goals, profile)
            
        except Exception as e:
            print(f"Error generando objetivos: {str(e)}")
            return self._get_fallback_goals(profile)

    def _create_prompt(self, survey: Survey, profile: FinancialProfile) -> str:
        health_status = "excelente" if profile.financial_health_score >= 80 else \
                       "buena" if profile.financial_health_score >= 60 else \
                       "regular" if profile.financial_health_score >= 40 else "necesita mejoras"

        return f"""
        Basado en este perfil financiero, sugiere 3-5 objetivos de aprendizaje financiero:

        PERFIL ACTUAL:
        - Salud financiera: {profile.financial_health_score}/100 ({health_status})
        - Tiene presupuesto: {"Sí" if survey.has_budget else "No"}
        - Tiene deudas: {"Sí" if survey.has_debts else "No"}
        - Experiencia en inversiones: {survey.investment_experience}
        - Tolerancia al riesgo: {survey.risk_tolerance}
        
        Sugiere objetivos de aprendizaje en estas categorías:
        1. Conceptos Básicos (basic_concepts)
        2. Presupuesto (budgeting)
        3. Manejo de Deudas (debt_management)
        4. Ahorro (savings)
        5. Inversión Básica (investment_basics)

        Para cada objetivo, proporciona:
        OBJETIVO:
        - Título: [título corto y claro]
        - Descripción: [descripción detallada]
        - Categoría: [una de las categorías mencionadas]
        - Importancia: [high/medium/low]
        """

    def _process_response(self, response_text: str) -> list:
        print("\n=== PROCESANDO OBJETIVOS DE APRENDIZAJE ===")
        goals = []
        current_goal = {}
        
        lines = response_text.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            if 'OBJETIVO:' in line.upper():
                if current_goal and 'title' in current_goal:
                    goals.append(current_goal.copy())
                current_goal = {}
                continue
                
            try:
                if 'Título:' in line:
                    current_goal['title'] = line.split('Título:')[1].strip()
                elif 'Descripción:' in line:
                    current_goal['description'] = line.split('Descripción:')[1].strip()
                elif 'Categoría:' in line:
                    category = line.split('Categoría:')[1].strip().lower()
                    current_goal['category'] = category
                elif 'Importancia:' in line:
                    importance = line.split('Importancia:')[1].strip().lower()
                    if importance in ['high', 'medium', 'low']:
                        current_goal['importance'] = importance
                    else:
                        current_goal['importance'] = 'medium'
            except Exception as e:
                print(f"Error procesando línea: {str(e)}")
                continue
                
        if current_goal and 'title' in current_goal:
            goals.append(current_goal.copy())
            
        return goals

    def _create_goal_objects(self, goals_data: list, profile: FinancialProfile) -> list:
        goal_objects = []
        
        for goal_data in goals_data:
            try:
                goal = LearningGoal(
                    user_id=profile.user_id,
                    profile_id=profile.id,
                    title=goal_data.get('title', 'Objetivo de Aprendizaje'),
                    description=goal_data.get('description', ''),
                    category=goal_data.get('category', 'basic_concepts'),
                    importance=goal_data.get('importance', 'medium'),
                    status='pending'
                )
                goal_objects.append(goal)
                
            except Exception as e:
                print(f"Error creando objetivo: {str(e)}")
                continue
                
        return goal_objects

    def _get_fallback_goals(self, profile: FinancialProfile) -> list:
        return [
            LearningGoal(
                user_id=profile.user_id,
                profile_id=profile.id,
                title="Entender conceptos financieros básicos",
                description="Aprender sobre ingresos, gastos, ahorro y presupuesto",
                category="basic_concepts",
                importance="high",
                status="pending"
            ),
            LearningGoal(
                user_id=profile.user_id,
                profile_id=profile.id,
                title="Crear y mantener un presupuesto",
                description="Aprender a crear y seguir un presupuesto mensual efectivo",
                category="budgeting",
                importance="high",
                status="pending"
            )
        ]