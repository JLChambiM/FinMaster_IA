import google.generativeai as genai
import os

class ChatService:
    def __init__(self):
        try:
            api_key = self._load_env_manually().get('GOOGLE_API_KEY')
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

    def get_response(self, message: str, user) -> str:
        """Genera una respuesta para el mensaje del usuario"""
        try:
            # Crear el contexto para el asistente
            context = """Eres un asistente financiero educativo experto. Tu objetivo es:
            1. Responder preguntas sobre conceptos financieros
            2. Explicar términos financieros de manera simple
            3. Dar consejos educativos sobre finanzas personales
            4. Ayudar a entender mejor la salud financiera

            Mantén tus respuestas:
            - Breves y claras (máximo 3-4 líneas)
            - Educativas y fáciles de entender
            - Enfocadas en enseñar conceptos financieros
            """

            response = self.model.generate_content([
                {"role": "user", "parts": [{"text": context}]},
                {"role": "user", "parts": [{"text": message}]}
            ])

            return response.text

        except Exception as e:
            print(f"Error generando respuesta: {str(e)}")
            return "Lo siento, hubo un error al procesar tu mensaje. ¿Podrías intentar preguntarme de otra manera?"