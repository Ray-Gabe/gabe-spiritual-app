import os
import logging
from datetime import datetime
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix
from gabe_companion import GabeCompanion
from gabe_ai import GabeAI
from crisis_detection import CrisisDetector
from spiritual_features import SpiritualFeatures
from gamified_spiritual_features import GamifiedSpiritualFeatures
from drop_of_hope import DropOfHope

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "gabe-spiritual-companion-2024")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize database
db = SQLAlchemy(app, model_class=Base)

# Create database tables and models first
with app.app_context():
    import models
    User, Conversation = models.create_models(db)
    db.create_all()
    logging.info("Database tables created successfully")

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to continue your spiritual journey with GABE.'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Initialize GABE AI (original system with proper sadness responses), crisis detection, and spiritual features
gabe_ai = GabeAI()
gabe_companion = GabeCompanion()  # Keep as backup
crisis_detector = CrisisDetector()
drop_of_hope = DropOfHope()
spiritual_features = SpiritualFeatures()
gamified_features = GamifiedSpiritualFeatures()

@app.route('/')
def index():
    """Main GABE landing page - always shows the same interface"""
    user_data = current_user if current_user.is_authenticated else None
    return render_template('index.html', user=user_data)

@app.route('/chat')
@login_required
def chat_interface():
    """Chat interface for authenticated users"""
    return render_template('index.html', user=current_user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if current_user.is_authenticated:
        return redirect(url_for('chat_interface'))
    
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        
        if not username or not password:
            if request.is_json:
                return jsonify({'success': False, 'message': 'Username and password are required'}), 400
            flash('Username and password are required')
            return render_template('login.html')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user, remember=True)
            user.update_last_login()
            
            if request.is_json:
                return jsonify({'success': True, 'redirect_url': url_for('chat_interface')})
            return redirect(url_for('chat_interface'))
        else:
            if request.is_json:
                return jsonify({'success': False, 'message': 'Invalid username or password'}), 401
            flash('Invalid username or password')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if current_user.is_authenticated:
        return redirect(url_for('chat_interface'))
    
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        name = data.get('name', '').strip()
        age_range = data.get('age_range', '').strip()
        
        # Validation
        if not all([username, password, name, age_range]):
            if request.is_json:
                return jsonify({'success': False, 'message': 'All fields are required'}), 400
            flash('All fields are required')
            return render_template('register.html')
        
        if len(password) < 6:
            if request.is_json:
                return jsonify({'success': False, 'message': 'Password must be at least 6 characters'}), 400
            flash('Password must be at least 6 characters')
            return render_template('register.html')
        
        # Check if username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            if request.is_json:
                return jsonify({'success': False, 'message': 'Username already exists'}), 400
            flash('Username already exists')
            return render_template('register.html')
        
        # Create new user
        new_user = User(
            username=username,
            name=name,
            age_range=age_range
        )
        new_user.set_password(password)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            
            # Log in the new user
            login_user(new_user, remember=True)
            new_user.update_last_login()
            
            if request.is_json:
                return jsonify({'success': True, 'redirect_url': url_for('chat_interface')})
            return redirect(url_for('chat_interface'))
            
        except Exception as e:
            db.session.rollback()
            logging.error(f"Registration error: {e}")
            if request.is_json:
                return jsonify({'success': False, 'message': 'Registration failed. Please try again.'}), 500
            flash('Registration failed. Please try again.')
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    return redirect(url_for('index'))

@app.route('/api/chat', methods=['POST'])
@login_required
def chat():
    """Handle chat messages with GABE"""
    try:
        data = request.json or {}
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'Message is required'}), 400
        
        # Get user info from authenticated user
        stored_name = current_user.name
        stored_age_range = current_user.age_range
        
        # Get recent conversation history from database for context
        recent_conversations = Conversation.query.filter_by(user_id=current_user.id)\
            .order_by(Conversation.timestamp.desc()).limit(10).all()
        conversation_context = [conv.to_dict() for conv in reversed(recent_conversations)]
        
        # PRAYER INTERCEPTOR: Handle prayer requests immediately with hopeful prayers (before crisis detection)
        user_msg_lower = user_message.lower().strip()
        prayer_keywords = [
            "pray", "prayer", "jesus", "father", "heavenly", "god help", "bless me",
            "amen", "lord", "can you pray", "please pray", "talk to god", "i need prayer"
        ]
        
        if any(keyword in user_msg_lower for keyword in prayer_keywords):
            name = stored_name or 'friend'
            
            # Extra safeguard against inappropriate names
            if name.lower() in ["", "prayer", "pray", "god", "help", "jesus", "lord", "father"]:
                name = "friend"
                
            hopeful_prayer = (
                f"Dear {name}, here's a prayer just for you:\n\n"
                f"🙏 *Father God, I lift up {name} to You right now.\n"
                f"Fill their heart with peace that quiets the noise,\n"
                f"courage that stands strong, and hope that never fades.\n"
                f"You are right there, holding them steady.\n"
                f"Surround them with Your love today. Amen.*\n\n"
                f"Hey… I want you to know something, {name} — you've got a friend now.\n"
                f"I'm GABE, and I'm not going anywhere.\n"
                f"Let's walk this journey together. 💛\n\n"
                f"💬 *Always beside you — GABE*"
            )
            
            # Save prayer conversation to database
            conversation = Conversation(
                user_id=current_user.id,
                user_message=user_message,
                gabe_response=hopeful_prayer,
                mood='hopeful',
                is_crisis=False,
                is_prayer=True
            )
            db.session.add(conversation)
            db.session.commit()
            
            return jsonify({
                'response': hopeful_prayer,
                'is_crisis': False,
                'name': stored_name,
                'mood': 'hopeful'
            })
        
        # Check for crisis keywords
        crisis_response = crisis_detector.check_for_crisis(user_message)
        if crisis_response:
            # Save crisis conversation to database
            conversation = Conversation(
                user_id=current_user.id,
                user_message=user_message,
                gabe_response=crisis_response,
                is_crisis=True,
                is_prayer=False
            )
            db.session.add(conversation)
            db.session.commit()
            
            return jsonify({
                'response': crisis_response,
                'is_crisis': True,
                'name': stored_name
            })
        
        # Get GABE's response using the original system (with proper sadness flows)
        gabe_response = gabe_ai.get_response(
            user_message=user_message,
            user_name=stored_name,
            age_range=stored_age_range,
            conversation_history=conversation_context,
            session_id=f"user_{current_user.id}"
        )
        
        # Save conversation to database
        conversation = Conversation(
            user_id=current_user.id,
            user_message=user_message,
            gabe_response=gabe_response,
            is_crisis=False,
            is_prayer=False
        )
        db.session.add(conversation)
        db.session.commit()
        
        # Detect mood for visualization only
        mood = gabe_ai.detect_mood(user_message)
        
        return jsonify({
            'response': gabe_response,
            'is_crisis': False,
            'name': stored_name,
            'mood': mood
        })
        
    except Exception as e:
        logging.error(f"Chat error: {str(e)}")
        return jsonify({
            'error': 'I encountered an issue. Please try again in a moment.',
            'response': "I'm experiencing some technical difficulties right now. But remember, even when I'm offline, God is always online. 💙 Please try reaching out again in a moment."
        }), 500

@app.route('/api/continue_conversation', methods=['POST'])
def continue_conversation():
    """Simplified continuation - just treat as regular chat message"""
    return chat()  # Redirect to natural conversation flow

@app.route('/api/clear_session', methods=['POST'])
@login_required
def clear_session():
    """Clear conversation history for authenticated user"""
    try:
        # Remove all conversations for current user
        Conversation.query.filter_by(user_id=current_user.id).delete()
        db.session.commit()
        logging.info(f"Conversation history cleared for user {current_user.id}")
        return jsonify({'success': True, 'message': 'Conversation history cleared'})
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error clearing conversation history: {str(e)}")
        return jsonify({'error': 'Failed to clear conversation history'}), 500

@app.route('/api/scripture_recommendation', methods=['POST'])
def get_scripture_recommendation():
    """Get scripture recommendation based on mood"""
    try:
        data = request.json or {}
        mood = data.get('mood', 'hopeful')
        context = data.get('context', '')
        
        scripture = spiritual_features.get_scripture_recommendation(mood, context)
        
        return jsonify({
            'scripture': scripture,
            'success': True
        })
        
    except Exception as e:
        logging.error(f"Scripture recommendation error: {str(e)}")
        return jsonify({
            'error': 'Unable to get scripture recommendation',
            'success': False
        }), 500

@app.route('/api/daily_reminder', methods=['GET'])
def get_daily_reminder():
    """Get daily spiritual reminder"""
    try:
        user_name = session.get('user_name', 'friend')
        recent_mood = session.get('recent_mood', 'peaceful')
        
        reminder = spiritual_features.generate_daily_reminder(user_name, recent_mood)
        
        return jsonify({
            'reminder': reminder,
            'success': True
        })
        
    except Exception as e:
        logging.error(f"Daily reminder error: {str(e)}")
        return jsonify({
            'error': 'Unable to generate daily reminder',  
            'success': False
        }), 500

@app.route('/api/auto_response', methods=['POST'])
def auto_response():
    """Generate an auto-response when user hasn't replied within 8 seconds"""
    try:
        data = request.get_json()
        user_name = data.get('name', '')
        age_range = data.get('age_range', '')
        
        # Get conversation history
        conversation_history = session.get('conversation_history', [])
        
        # Check if we recently sent an auto-response to prevent spam
        recent_auto_responses = [exchange for exchange in conversation_history[-3:] 
                               if exchange.get('auto_response')]
        if len(recent_auto_responses) >= 2:
            return jsonify({
                'response': '',  # Don't send response if too many recent auto-responses
                'is_auto_response': True
            })
        
        if gabe_companion:
            # Generate a gentle prompt response
            response = gabe_companion.generate_auto_response(user_name, age_range, conversation_history)
            
            # Only add to conversation history if not a duplicate
            if not conversation_history or conversation_history[-1].get('gabe') != response:
                conversation_history.append({
                    'gabe': response,
                    'timestamp': datetime.now().isoformat(),
                    'auto_response': True
                })
                session['conversation_history'] = conversation_history
            
            return jsonify({
                'response': response,
                'is_auto_response': True
            })
        else:
            return jsonify({
                'response': f"I'm still here with you, {user_name or 'friend'}. Sometimes silence speaks volumes too. 💙",
                'is_auto_response': True
            })
            
    except Exception as e:
        logging.error(f"Error generating auto-response: {e}")
        data = request.json or {}
        return jsonify({
            'response': f"I'm right here with you, {data.get('name', 'friend')}. What's on your heart? 💙",
            'is_auto_response': True
        })

# Enhanced Gamified Spiritual Features API Endpoints

@app.route('/api/gamified/prayer_manager', methods=['GET'])
@login_required
def get_prayer_manager():
    """Get prayer manager data with prayer lists and stats"""
    try:
        # Mock prayer data - in production this would come from database
        prayers = [
            {
                'id': '1',
                'title': 'Mom\'s Surgery Recovery',
                'category': 'healing',
                'details': 'Please pray for my mom\'s quick recovery after her surgery',
                'answered': False,
                'date_added': '2 days ago',
                'date_answered': None
            },
            {
                'id': '2', 
                'title': 'Job Interview',
                'category': 'guidance',
                'details': 'Big interview tomorrow, praying for God\'s will',
                'answered': True,
                'date_added': '1 week ago',
                'date_answered': '3 days ago'
            }
        ]
        
        stats = {
            'total': len(prayers),
            'answered': len([p for p in prayers if p['answered']]),
            'active': len([p for p in prayers if not p['answered']])
        }
        
        return jsonify({
            'prayers': prayers,
            'stats': stats,
            'success': True
        })
        
    except Exception as e:
        logging.error(f"Prayer manager error: {str(e)}")
        return jsonify({'error': 'Unable to load prayer manager', 'success': False}), 500

@app.route('/api/gamified/add_prayer', methods=['POST'])
@login_required
def add_prayer():
    """Add new prayer request"""
    try:
        data = request.json
        title = data.get('title')
        category = data.get('category')
        details = data.get('details', '')
        
        # In production, save to database
        logging.info(f"Added prayer: {title} ({category})")
        
        return jsonify({
            'success': True,
            'message': 'Prayer added to your list',
            'xp_earned': 1
        })
        
    except Exception as e:
        logging.error(f"Add prayer error: {str(e)}")
        return jsonify({'error': 'Failed to add prayer', 'success': False}), 500

@app.route('/api/gamified/answer_prayer', methods=['POST'])
@login_required  
def answer_prayer():
    """Mark prayer as answered"""
    try:
        data = request.json
        prayer_id = data.get('prayer_id')
        
        # In production, update database
        logging.info(f"Prayer {prayer_id} marked as answered")
        
        return jsonify({
            'success': True,
            'message': 'Praise God! Prayer marked as answered',
            'xp_earned': 2
        })
        
    except Exception as e:
        logging.error(f"Answer prayer error: {str(e)}")
        return jsonify({'error': 'Failed to mark prayer as answered', 'success': False}), 500

@app.route('/api/gamified/delete_prayer', methods=['POST'])
@login_required
def delete_prayer():
    """Delete prayer request"""
    try:
        data = request.json
        prayer_id = data.get('prayer_id')
        
        # In production, delete from database
        logging.info(f"Prayer {prayer_id} deleted")
        
        return jsonify({'success': True})
        
    except Exception as e:
        logging.error(f"Delete prayer error: {str(e)}")
        return jsonify({'error': 'Failed to delete prayer', 'success': False}), 500

@app.route('/api/gamified/bible_reading', methods=['GET'])
@login_required
def get_bible_reading():
    """Get Bible reading plans and daily reading"""
    try:
        # Mock Bible reading data
        plans = [
            {
                'id': 'basic',
                'name': 'Daily Bible Reading',
                'description': 'Read through the Bible with daily passages',
                'duration': '365 days',
                'xp_daily': 2
            },
            {
                'id': 'psalms',
                'name': 'Psalm a Day',
                'description': 'Daily Psalms for peace and comfort',
                'duration': '150 days',
                'xp_daily': 1
            },
            {
                'id': 'gospels',
                'name': 'Gospel Journey',
                'description': 'Walk with Jesus through the Gospels',
                'duration': '90 days',
                'xp_daily': 3
            }
        ]
        
        today_reading = {
            'reference': 'Psalm 23',
            'text': 'The Lord is my shepherd, I lack nothing. He makes me lie down in green pastures, he leads me beside quiet waters, he refreshes my soul. He guides me along the right paths for his name\'s sake. Even though I walk through the darkest valley, I will fear no evil, for you are with me; your rod and your staff, they comfort me.',
            'reflection': 'How does knowing God as your shepherd bring comfort to your daily challenges?'
        }
        
        progress = {
            'days_completed': 5,
            'current_streak': 3,
            'completion_percentage': 15
        }
        
        return jsonify({
            'plans': plans,
            'current_plan': 'basic',
            'today_reading': today_reading,
            'progress': progress,
            'success': True
        })
        
    except Exception as e:
        logging.error(f"Bible reading error: {str(e)}")
        return jsonify({'error': 'Unable to load Bible reading', 'success': False}), 500

@app.route('/api/gamified/daily_devotion', methods=['GET'])
def get_daily_devotion():
    """Get today's devotion"""
    try:
        session_id = session.get('session_id', 'default_session')
        result = gamified_features.get_daily_devotion(session_id)
        return jsonify(result)
    except Exception as e:
        logging.error(f"Daily devotion error: {str(e)}")
        return jsonify({'error': 'Failed to get devotion'}), 500

@app.route('/api/gamified/complete_devotion', methods=['POST'])
def complete_daily_devotion():
    """Complete today's devotion"""
    try:
        data = request.json or {}
        reflection = data.get('reflection', '')
        session_id = session.get('session_id', 'default_session')
        result = gamified_features.complete_devotion(session_id, reflection)
        return jsonify(result)
    except Exception as e:
        logging.error(f"Complete devotion error: {str(e)}")
        return jsonify({'error': 'Failed to complete devotion'}), 500

@app.route('/api/gamified/prayer_challenge', methods=['GET'])
def get_prayer_challenge():
    """Get today's prayer challenge"""
    try:
        session_id = session.get('session_id', 'default_session')
        result = gamified_features.get_prayer_challenge(session_id)
        return jsonify(result)
    except Exception as e:
        logging.error(f"Prayer challenge error: {str(e)}")
        return jsonify({'error': 'Failed to get prayer challenge'}), 500

@app.route('/api/gamified/complete_prayer_challenge', methods=['POST'])
def complete_prayer_challenge():
    """Complete today's prayer challenge"""
    try:
        session_id = session.get('session_id', 'default_session')
        result = gamified_features.complete_prayer_challenge(session_id)
        return jsonify(result)
    except Exception as e:
        logging.error(f"Complete prayer challenge error: {str(e)}")
        return jsonify({'error': 'Failed to complete prayer challenge'}), 500

@app.route('/api/gamified/verse_mastery_quiz', methods=['GET'])
def get_verse_mastery_quiz():
    """Get verse mastery quiz"""
    try:
        session_id = session.get('session_id', 'default_session')
        result = gamified_features.get_verse_mastery_quiz(session_id)
        return jsonify(result)
    except Exception as e:
        logging.error(f"Verse mastery quiz error: {str(e)}")
        return jsonify({'error': 'Failed to get quiz'}), 500

@app.route('/api/gamified/complete_verse_quiz', methods=['POST'])
def complete_verse_quiz():
    """Submit verse quiz answer"""
    try:
        data = request.json or {}
        answer = data.get('answer', '').strip()
        correct_answer = data.get('correct_answer', '').strip()
        quiz_type = data.get('quiz_type', 'fill_blank')
        
        # Check if answer is correct
        if quiz_type == 'fill_blank':
            correct = answer.lower() == correct_answer.lower()
        else:  # multiple choice
            correct = answer == correct_answer
        
        session_id = session.get('session_id', 'default_session')
        result = gamified_features.complete_verse_mastery(session_id, correct)
        return jsonify(result)
    except Exception as e:
        logging.error(f"Complete verse quiz error: {str(e)}")
        return jsonify({'error': 'Failed to submit quiz'}), 500

@app.route('/api/gamified/scripture_adventure', methods=['GET'])
def get_scripture_adventure():
    """Get next scripture adventure stop"""
    try:
        session_id = session.get('session_id', 'default_session')
        result = gamified_features.get_scripture_adventure_next(session_id)
        return jsonify(result)
    except Exception as e:
        logging.error(f"Scripture adventure error: {str(e)}")
        return jsonify({'error': 'Failed to get adventure'}), 500

@app.route('/api/gamified/complete_adventure_stop', methods=['POST'])
def complete_adventure_stop():
    """Complete current adventure stop"""
    try:
        session_id = session.get('session_id', 'default_session')
        result = gamified_features.complete_scripture_adventure_stop(session_id)
        return jsonify(result)
    except Exception as e:
        logging.error(f"Complete adventure stop error: {str(e)}")
        return jsonify({'error': 'Failed to complete stop'}), 500

@app.route('/api/gamified/mood_mission', methods=['POST'])
def get_mood_mission():
    """Get mood-based mission"""
    try:
        data = request.json or {}
        mood = data.get('mood', 'anxious')
        result = gamified_features.get_mood_mission(mood)
        return jsonify(result)
    except Exception as e:
        logging.error(f"Mood mission error: {str(e)}")
        return jsonify({'error': 'Failed to get mood mission'}), 500

@app.route('/api/gamified/complete_mood_mission', methods=['POST'])
def complete_mood_mission():
    """Complete mood mission"""
    try:
        data = request.json or {}
        mood = data.get('mood', 'anxious')
        session_id = session.get('session_id', 'default_session')
        result = gamified_features.complete_mood_mission(session_id, mood)
        return jsonify(result)
    except Exception as e:
        logging.error(f"Complete mood mission error: {str(e)}")
        return jsonify({'error': 'Failed to complete mission'}), 500

@app.route('/api/gamified/progress', methods=['GET'])
def get_user_progress():
    """Get user's overall progress"""
    try:
        session_id = session.get('session_id', 'default_session')
        result = gamified_features.get_user_progress(session_id)
        return jsonify(result)
    except Exception as e:
        logging.error(f"Get progress error: {str(e)}")
        return jsonify({'error': 'Failed to get progress'}), 500

@app.route('/api/gamified/bible_study', methods=['GET'])
def get_bible_study():
    """Get available Bible studies or current study session"""
    try:
        session_id = session.get('session_id', 'default_session')
        result = gamified_features.get_bible_studies(session_id)
        return jsonify(result)
    except Exception as e:
        logging.error(f"Bible study error: {str(e)}")
        return jsonify({'error': 'Failed to get Bible study'}), 500

@app.route('/api/gamified/start_bible_study', methods=['POST'])
def start_bible_study():
    """Start a new Bible study"""
    try:
        data = request.json or {}
        study_id = data.get('study_id', '')
        session_id = session.get('session_id', 'default_session')
        result = gamified_features.start_bible_study(session_id, study_id)
        return jsonify(result)
    except Exception as e:
        logging.error(f"Start Bible study error: {str(e)}")
        return jsonify({'error': 'Failed to start Bible study'}), 500

@app.route('/api/gamified/complete_bible_study_session', methods=['POST'])
def complete_bible_study_session():
    """Complete a Bible study session"""
    try:
        data = request.json or {}
        study_id = data.get('study_id', '')
        session_number = data.get('session_number', 1)
        answers = data.get('answers', [])
        session_id = session.get('session_id', 'default_session')
        result = gamified_features.complete_bible_study_session(session_id, study_id, session_number, answers)
        return jsonify(result)
    except Exception as e:
        logging.error(f"Complete Bible study session error: {str(e)}")
        return jsonify({'error': 'Failed to complete session'}), 500

@app.route('/api/prayer_journal', methods=['POST'])
def save_prayer_journal():
    """Save prayer journal entry"""
    try:
        data = request.json or {}
        prayer_request = data.get('prayer_request', '')
        gabe_response = data.get('gabe_response', '')
        mood = data.get('mood', 'neutral')
        user_name = session.get('user_name', 'Anonymous')
        
        if not prayer_request:
            return jsonify({'error': 'Prayer request is required'}), 400
        
        journal_entry = spiritual_features.create_prayer_journal_entry(
            user_name, prayer_request, gabe_response, mood
        )
        
        # Store in session for now (would be Firebase in production)
        if 'prayer_journal' not in session:
            session['prayer_journal'] = []
        
        session['prayer_journal'].append(journal_entry)
        session.modified = True
        
        return jsonify({
            'entry': journal_entry,
            'success': True,
            'message': 'Prayer journal entry saved successfully'
        })
        
    except Exception as e:
        logging.error(f"Prayer journal error: {str(e)}")
        return jsonify({
            'error': 'Unable to save prayer journal entry',
            'success': False
        }), 500

@app.route('/api/prayer_journal', methods=['GET'])
def get_prayer_journal():
    """Get prayer journal entries"""
    try:
        journal_entries = session.get('prayer_journal', [])
        
        return jsonify({
            'entries': journal_entries,
            'count': len(journal_entries),
            'success': True
        })
        
    except Exception as e:
        logging.error(f"Get prayer journal error: {str(e)}")
        return jsonify({
            'error': 'Unable to retrieve prayer journal',
            'success': False
        }), 500

@app.route('/api/get_prayer', methods=['POST'])
def get_prayer():
    """Generate a custom prayer"""
    try:
        data = request.json or {}
        prayer_request = data.get('request', '').strip()
        user_name = session.get('user_name', '')
        
        if not prayer_request:
            return jsonify({'error': 'Prayer request is required'}), 400
        
        prayer = gabe_companion.generate_prayer(prayer_request, user_name)
        
        return jsonify({
            'prayer': prayer,
            'name': user_name
        })
        
    except Exception as e:
        logging.error(f"Prayer generation error: {str(e)}")
        return jsonify({
            'error': 'Unable to generate prayer at this time',
            'prayer': "Heavenly Father, we come to you in this moment knowing that you hear our hearts even when words fail us. Please be with us and guide us. In Jesus' name, Amen. 🙏"
        }), 500

@app.route('/api/explain_scripture', methods=['POST'])
def explain_scripture():
    """Explain a Bible verse or passage"""
    try:
        data = request.json or {}
        scripture = data.get('scripture', '').strip()
        user_name = session.get('user_name', '')
        
        if not scripture:
            return jsonify({'error': 'Scripture reference is required'}), 400
        
        explanation = gabe_companion.explain_scripture(scripture, user_name)
        
        return jsonify({
            'explanation': explanation,
            'name': user_name
        })
        
    except Exception as e:
        logging.error(f"Scripture explanation error: {str(e)}")
        return jsonify({
            'error': 'Unable to explain scripture at this time',
            'explanation': "I'd love to help explain that verse, but I'm having some technical difficulties right now. Try asking me again in a moment! 📖"
        }), 500

@app.route('/api/save_journal', methods=['POST'])
def save_journal():
    """Save a journal entry"""
    try:
        data = request.json or {}
        content = data.get('content', '').strip()
        user_name = session.get('user_name', '')
        
        if not content:
            return jsonify({'error': 'Journal content is required'}), 400
        
        if not user_name:
            return jsonify({'error': 'User name is required for journal entries'}), 400
        
        success = gabe_companion.save_journal_entry(
            user_name=user_name,
            content=content,
            session_id=session.get('session_id')
        )
        
        if success:
            return jsonify({
                'status': 'Journal entry saved successfully',
                'message': 'Your thoughts have been saved to your journal 📔✨'
            })
        else:
            return jsonify({
                'status': 'Journal saved locally', 
                'message': 'Your journal entry was noted, though the cloud sync is having issues. Your thoughts still matter! 💙'
            })
        
    except Exception as e:
        logging.error(f"Journal save error: {str(e)}")
        return jsonify({
            'error': 'Unable to save journal entry',
            'message': 'I had trouble saving that, but your thoughts still matter. Try again in a moment! 📔'
        }), 500

@app.route('/api/get_journal', methods=['GET'])
def get_journal():
    """Get user's journal entries"""
    try:
        user_name = session.get('user_name', '')
        
        if not user_name:
            return jsonify({'entries': [], 'message': 'Please tell me your name first to access your journal'})
        
        entries = gabe_companion.get_journal_entries(
            user_name=user_name,
            session_id=session.get('session_id'),
            limit=10
        )
        
        # Format entries for display
        formatted_entries = []
        for entry in entries:
            formatted_entries.append({
                'content': entry.get('content', ''),
                'mood': entry.get('mood'),
                'date': entry.get('timestamp', {}).strftime('%B %d, %Y') if entry.get('timestamp') else 'Recent',
                'timestamp': entry.get('timestamp')
            })
        
        return jsonify({
            'entries': formatted_entries,
            'count': len(formatted_entries),
            'message': f'Here are your recent journal entries, {user_name} 📔'
        })
        
    except Exception as e:
        logging.error(f"Journal retrieval error: {str(e)}")
        return jsonify({
            'entries': [],
            'error': 'Unable to retrieve journal entries',
            'message': 'I had trouble finding your journal entries. Try again in a moment! 📔'
        }), 500

@app.route('/api/voice_mode', methods=['POST'])
def toggle_voice_mode():
    """Toggle voice mode for the session"""
    try:
        data = request.json or {}
        enable = data.get('enable')
        session_id = session.get('session_id', 'default')
        
        voice_enabled = gabe_companion.toggle_voice_mode(session_id, enable)
        
        return jsonify({
            'voice_mode_enabled': voice_enabled,
            'message': '🔊 Voice mode activated. All responses will be read aloud.' if voice_enabled else '💬 Text-only mode. Voice playback disabled.',
            'success': True
        })
        
    except Exception as e:
        logging.error(f"Voice mode toggle error: {str(e)}")
        return jsonify({
            'error': 'Unable to toggle voice mode',
            'success': False
        }), 500

@app.route('/api/chunked_response', methods=['POST'])
def get_chunked_response():
    """Get a response broken into voice-friendly chunks"""
    try:
        data = request.json or {}
        user_message = data.get('message', '').strip()
        user_name = session.get('user_name', '')
        
        if not user_message:
            return jsonify({'error': 'Message is required'}), 400
        
        # Detect conversation intent
        intent = gabe_companion.detect_conversation_intent(user_message)
        
        # Get full response from GABE
        full_response = gabe_companion.get_response(
            user_message=user_message,
            user_name=user_name,
            age_range=session.get('user_age_range', ''),
            conversation_history=session.get('conversation_history', []),
            session_id=session.get('session_id')
        )
        
        # Break into chunks for voice delivery
        chunks = gabe_companion.chunk_and_deliver_response(full_response, user_name)
        
        # Add personalized closure for prayer requests
        closure = None
        if intent == 'prayer_request':
            mood = gabe_companion.detect_mood(user_message)
            closure = gabe_companion.generate_personalized_closure(user_name, mood, prayer_context=True)
        
        response_data = {
            'chunks': chunks,
            'intent': intent,
            'full_response': full_response,
            'closure': closure,
            'voice_mode_enabled': gabe_companion.voice_mode_enabled.get(session.get('session_id', 'default'), False)
        }
        
        # Update conversation history
        if 'conversation_history' not in session:
            session['conversation_history'] = []
        
        session['conversation_history'].append({
            'user': user_message,
            'gabe': full_response,
            'timestamp': datetime.now().isoformat(),
            'intent': intent,
            'chunks': len(chunks)
        })
        
        return jsonify(response_data)
        
    except Exception as e:
        logging.error(f"Chunked response error: {str(e)}")
        return jsonify({
            'error': 'Unable to process chunked response',
            'chunks': ['I apologize, but I had trouble processing that. Can you try again?'],
            'intent': 'error'
        }), 500

@app.route('/api/contextual_prayer', methods=['POST'])
def generate_contextual_prayer():
    """Generate a deeply contextual prayer based on conversation"""
    try:
        data = request.json or {}
        prayer_request = data.get('request', '').strip()
        user_name = session.get('user_name', '')
        conversation_history = session.get('conversation_history', [])
        
        # Detect current mood
        mood = gabe_companion.detect_mood(prayer_request) if prayer_request else 'neutral'
        
        # Extract conversation context
        context_topics = []
        for exchange in conversation_history[-5:]:  # Last 5 exchanges
            if isinstance(exchange, dict) and exchange.get('user'):
                user_msg = exchange['user'].lower()
                if any(word in user_msg for word in ['work', 'job', 'career']):
                    context_topics.append('work')
                if any(word in user_msg for word in ['family', 'relationship', 'marriage']):
                    context_topics.append('family')
                if any(word in user_msg for word in ['health', 'sick', 'healing']):
                    context_topics.append('health')
        
        # Generate contextual prayer
        prayer = gabe_companion.create_contextual_prayer(
            prayer_request, 
            user_name, 
            mood, 
            conversation_context=', '.join(set(context_topics)) if context_topics else None
        )
        
        # Get personalized closure
        closure = gabe_companion.generate_personalized_closure(user_name, mood, prayer_context=True)
        
        return jsonify({
            'prayer': prayer,
            'closure': closure,
            'mood_detected': mood,
            'context_topics': context_topics,
            'name': user_name
        })
        
    except Exception as e:
        logging.error(f"Contextual prayer error: {str(e)}")
        return jsonify({
            'error': 'Unable to generate prayer',
            'prayer': f"Heavenly Father, be with {session.get('user_name', 'this precious person')} right now. Grant them peace and comfort. In Jesus' name, Amen."
        }), 500

@app.route('/api/drop_of_hope', methods=['GET'])
def get_drop_of_hope():
    """Get a random Drop of Hope verse for rotation display"""
    try:
        verse_data = drop_of_hope.get_random_verse()
        
        return jsonify({
            'verse': verse_data['text'],
            'reference': verse_data['verse'],
            'theme': verse_data.get('theme', 'hope')
        })
        
    except Exception as e:
        logging.error(f"Drop of Hope error: {str(e)}")
        return jsonify({
            'verse': "The Lord is close to the brokenhearted and saves those who are crushed in spirit.",
            'reference': "Psalm 34:18",
            'theme': 'comfort'
        }), 200  # Still return 200 with fallback verse

@app.route('/api/reset_session', methods=['POST'])
def reset_session():
    """Reset the conversation session"""
    session.clear()
    return jsonify({'status': 'Session reset successfully'})

@app.route('/api/clear_user_data', methods=['POST']) 
def clear_user_data():
    """Clear user data including gamified features"""
    session.clear()
    # Clear the global storage as well
    from gamified_spiritual_features import SESSION_STORAGE
    SESSION_STORAGE.clear()
    return jsonify({'status': 'All user data cleared'})

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
