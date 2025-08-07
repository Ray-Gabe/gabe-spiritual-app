from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from gabe_app.models import db, Conversation
from gabe_app.gabe_ai import GabeAI
from gabe_app.crisis_detection import CrisisDetector
from gabe_app.spiritual_features import SpiritualFeatures
from gabe_app.gamified_spiritual_features import GamifiedSpiritualFeatures
from gabe_app.drop_of_hope import DropOfHope

api_bp = Blueprint('api', __name__, url_prefix='/api')

gabe_ai = GabeAI()
crisis_detector = CrisisDetector()
spiritual_features = SpiritualFeatures()
gamified_features = GamifiedSpiritualFeatures()
drop_of_hope = DropOfHope()

@api_bp.route('/chat', methods=['POST'])
@login_required
def api_chat():
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        if not message:
            return jsonify({'error': 'No message provided'}), 400

        crisis_response = crisis_detector.check_message(message)
        if crisis_response:
            return jsonify({'response': crisis_response})

        response = gabe_ai.get_response(message, current_user.name)
        conversation = Conversation(user_id=current_user.id, user_message=message, gabe_response=response)
        db.session.add(conversation)
        db.session.commit()

        return jsonify({'response': response})

    except Exception as e:
        return jsonify({'error': 'An error occurred. Please try again.'}), 500

@api_bp.route('/prayer', methods=['POST'])
@login_required
def api_prayer():
    try:
        data = request.get_json()
        prayer_type = data.get('type', 'general')
        context = data.get('context', '')
        prayer = spiritual_features.get_prayer(prayer_type, context)
        return jsonify({'prayer': prayer})
    except Exception as e:
        return jsonify({'error': 'Could not generate prayer'}), 500

@api_bp.route('/drop-of-hope', methods=['GET'])
@login_required
def api_drop_of_hope():
    try:
        drop = drop_of_hope.get_daily_drop()
        return jsonify(drop)
    except Exception as e:
        return jsonify({'error': 'Could not retrieve drop of hope'}), 500

@api_bp.route('/spiritual-practice', methods=['POST'])
@login_required
def api_spiritual_practice():
    try:
        data = request.get_json()
        practice_type = data.get('type', 'meditation')
        duration = data.get('duration', 5)
        practice = spiritual_features.get_practice(practice_type, duration)
        return jsonify({'practice': practice})
    except Exception as e:
        return jsonify({'error': 'Could not retrieve spiritual practice'}), 500

@api_bp.route('/gamified/journey', methods=['GET'])
@login_required
def api_gamified_journey():
    try:
        journey_data = gamified_features.get_user_journey(current_user.id)
        return jsonify(journey_data)
    except Exception as e:
        return jsonify({'error': 'Could not retrieve journey data'}), 500

@api_bp.route('/gamified/achievement', methods=['POST'])
@login_required
def api_gamified_achievement():
    try:
        data = request.get_json()
        achievement_id = data.get('achievement_id')
        result = gamified_features.unlock_achievement(current_user.id, achievement_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': 'Could not process achievement'}), 500

@api_bp.route('/conversation-history', methods=['GET'])
@login_required
def api_conversation_history():
    try:
        conversations = Conversation.query.filter_by(user_id=current_user.id).order_by(Conversation.timestamp.desc()).limit(50).all()
        history = [{'timestamp': c.timestamp.isoformat(), 'user_message': c.user_message, 'gabe_response': c.gabe_response} for c in conversations]
        return jsonify({'history': history})
    except Exception as e:
        return jsonify({'error': 'Could not retrieve conversation history'}), 500
