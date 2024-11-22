from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.services.chat_service import ChatService

bp = Blueprint('chat_blueprint', __name__, url_prefix='/chat')

@bp.route('/message', methods=['POST'])
@login_required
def message():
    try:
        message = request.json.get('message', '')
        chat_service = ChatService()
        response = chat_service.get_response(message, current_user)
        return jsonify({'response': response})
    except Exception as e:
        print(f"Error en chat: {str(e)}")
        return jsonify({'response': 'Lo siento, hubo un error al procesar tu mensaje.'}), 500