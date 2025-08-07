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
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI', 'sqlite:///gabe.db')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
# Initialize database
db = SQLAlchemy(app)

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
    """Main GABE landing page - Original Beautiful Design"""
    user_data = current_user if current_user.is_authenticated else None
    
    if user_data:
        # If user is logged in, show personalized welcome
        return f"""
<!DOCTYPE html>
<html>
<head>
    <title>GABE - Your Spiritual Companion</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        /* Your Complete Original CSS Here */
        :root {{
          --primary-blue: #2563EB;
          --primary-ocean: #1E40AF;
          --secondary-sky: #0EA5E9;
          --accent-indigo: #6366F1;
          --gradient-peaceful: linear-gradient(135deg, #DBEAFE 0%, #EBF8FF 100%);
          --gradient-divine: linear-gradient(135deg, #2563EB 0%, #6366F1 100%);
          --shadow-elevated: 0 20px 60px rgba(45, 55, 72, 0.12);
          --radius-xl: 32px;
        }}
        
        * {{
          margin: 0;
          padding: 0;
          box-sizing: border-box;
        }}
        
        body {{
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
          background: linear-gradient(135deg, #87CEEB 0%, #4682B4 50%, #1E40AF 100%);
          min-height: 100vh;
          display: flex;
          align-items: center;
          justify-content: center;
          padding: 20px;
        }}
        
        .welcome-card {{
          background: rgba(255, 255, 255, 0.95);
          border-radius: 40px;
          padding: 40px 30px;
          box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
          text-align: center;
          max-width: 400px;
          width: 100%;
          backdrop-filter: blur(20px);
        }}
        
        .angel-container {{
          margin-bottom: 30px;
        }}
        
        .angel-circle {{
          width: 120px;
          height: 120px;
          background: linear-gradient(135deg, #e8f4fd 0%, #d1e7dd 100%);
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          margin: 0 auto 20px;
          position: relative;
          box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        }}
        
        .angel-face {{
          font-size: 40px;
          position: relative;
        }}
        
        .halo {{
          position: absolute;
          top: -15px;
          left: 50%;
          transform: translateX(-50%);
          width: 50px;
          height: 8px;
          background: linear-gradient(90deg, #FFD700, #FFA500);
          border-radius: 50px;
          box-shadow: 0 0 15px rgba(255, 215, 0, 0.6);
        }}
        
        .welcome-title {{
          font-size: 48px;
          font-weight: 800;
          color: #1E40AF;
          margin-bottom: 10px;
          letter-spacing: -1px;
        }}
        
        .welcome-subtitle {{
          font-size: 20px;
          font-weight: 600;
          color: #4682B4;
          margin-bottom: 30px;
          letter-spacing: 0.5px;
        }}
        
        .user-greeting {{
          font-size: 32px;
          font-weight: 700;
          color: #1E40AF;
          margin-bottom: 30px;
        }}
        
        .chat-btn {{
          background: linear-gradient(135deg, #4169E1 0%, #1E40AF 100%);
          color: white;
          border: none;
          padding: 18px 40px;
          border-radius: 50px;
          font-size: 18px;
          font-weight: 600;
          cursor: pointer;
          margin-bottom: 20px;
          width: 100%;
          transition: all 0.3s ease;
          box-shadow: 0 8px 25px rgba(65, 105, 225, 0.3);
        }}
        
        .chat-btn:hover {{
          transform: translateY(-2px);
          box-shadow: 0 12px 35px rgba(65, 105, 225, 0.4);
        }}
        
        .gabefyed-btn {{
          background: transparent;
          color: #4169E1;
          border: 2px solid #4169E1;
          padding: 16px 40px;
          border-radius: 50px;
          font-size: 16px;
          font-weight: 600;
          cursor: pointer;
          width: 100%;
          transition: all 0.3s ease;
        }}
        
        .gabefyed-btn:hover {{
          background: #4169E1;
          color: white;
          transform: translateY(-2px);
        }}
        
        .logout-link {{
          position: absolute;
          top: 20px;
          right: 20px;
          color: white;
          text-decoration: none;
          background: rgba(255, 255, 255, 0.2);
          padding: 8px 16px;
          border-radius: 20px;
          font-size: 14px;
          transition: all 0.3s ease;
        }}
        
        .logout-link:hover {{
          background: rgba(255, 255, 255, 0.3);
          color: white;
          text-decoration: none;
        }}
    </style>
</head>
<body>
    <a href="/logout" class="logout-link">Logout</a>
    <div class="welcome-card">
        <div class="angel-container">
            <div class="angel-circle">
                <div class="angel-face">
                    😊
                    <div class="halo"></div>
                </div>
            </div>
        </div>
        
        <div class="user-greeting">Hey {user_data.name}!</div>
        
        <button class="chat-btn" onclick="window.location.href='/chat'">
            Chat with GABE
        </button>
        
        <button class="gabefyed-btn" onclick="showGabefyedFeatures()">
            GET GABEFYED
        </button>
    </div>
    
    <script>
        function showGabefyedFeatures() {{
            alert('Gamified spiritual features coming soon! 🌟');
        }}
    </script>
</body>
</html>
        """
    else:
        # Show original welcome form for new users
        return """
<!DOCTYPE html>
<html>
<head>
    <title>GABE - Your Spiritual Companion</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * {
          margin: 0;
          padding: 0;
          box-sizing: border-box;
        }
        
        body {
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
          background: linear-gradient(135deg, #87CEEB 0%, #4682B4 50%, #1E40AF 100%);
          min-height: 100vh;
          display: flex;
          align-items: center;
          justify-content: center;
          padding: 20px;
        }
        
        .welcome-card {
          background: rgba(255, 255, 255, 0.95);
          border-radius: 40px;
          padding: 40px 30px;
          box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
          text-align: center;
          max-width: 400px;
          width: 100%;
          backdrop-filter: blur(20px);
        }
        
        .angel-container {
          margin-bottom: 30px;
        }
        
        .angel-circle {
          width: 120px;
          height: 120px;
          background: linear-gradient(135deg, #e8f4fd 0%, #d1e7dd 100%);
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          margin: 0 auto 20px;
          position: relative;
          box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        }
        
        .angel-face {
          font-size: 40px;
          position: relative;
        }
        
        .halo {
          position: absolute;
          top: -15px;
          left: 50%;
          transform: translateX(-50%);
          width: 50px;
          height: 8px;
          background: linear-gradient(90deg, #FFD700, #FFA500);
          border-radius: 50px;
          box-shadow: 0 0 15px rgba(255, 215, 0, 0.6);
        }
        
        .welcome-title {
          font-size: 48px;
          font-weight: 800;
          color: #1E40AF;
          margin-bottom: 10px;
          letter-spacing: -1px;
        }
        
        .welcome-subtitle {
          font-size: 20px;
          font-weight: 600;
          color: #4682B4;
          margin-bottom: 8px;
          letter-spacing: 0.5px;
        }
        
        .welcome-tagline {
          font-size: 16px;
          color: #6B7280;
          font-style: italic;
          margin-bottom: 30px;
        }
        
        .welcome-form {
          display: flex;
          flex-direction: column;
          gap: 16px;
        }
        
        .form-input, .form-select {
          padding: 16px 20px;
          border: 2px solid #E5E7EB;
          border-radius: 25px;
          font-size: 16px;
          background: rgba(255, 255, 255, 0.9);
          transition: all 0.3s ease;
        }
        
        .form-input:focus, .form-select:focus {
          outline: none;
          border-color: #4169E1;
          box-shadow: 0 0 0 3px rgba(65, 105, 225, 0.1);
        }
        
        .form-input::placeholder {
          color: #9CA3AF;
        }
        
        .continue-btn {
          background: linear-gradient(135deg, #4169E1 0%, #1E40AF 100%);
          color: white;
          border: none;
          padding: 18px 40px;
          border-radius: 50px;
          font-size: 18px;
          font-weight: 600;
          cursor: pointer;
          margin-top: 10px;
          transition: all 0.3s ease;
          box-shadow: 0 8px 25px rgba(65, 105, 225, 0.3);
        }
        
        .continue-btn:hover {
          transform: translateY(-2px);
          box-shadow: 0 12px 35px rgba(65, 105, 225, 0.4);
        }
        
        .continue-btn:disabled {
          opacity: 0.6;
          cursor: not-allowed;
          transform: none;
        }
        
        .login-link {
          margin-top: 20px;
          color: #4169E1;
          text-decoration: none;
          font-size: 14px;
        }
        
        .login-link:hover {
          text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="welcome-card">
        <div class="angel-container">
            <div class="angel-circle">
                <div class="angel-face">
                    😊
                    <div class="halo"></div>
                </div>
            </div>
        </div>
        
        <h1 class="welcome-title">GABE</h1>
        <h2 class="welcome-subtitle">GUIDANCE AND BLESSING EVERYDAY</h2>
        <p class="welcome-tagline">Because even prayers start with a conversation</p>
        
        <form class="welcome-form" action="/register" method="POST">
            <input type="text" name="name" class="form-input" placeholder="Name" required>
            
            <select name="age_range" class="form-select" required>
                <option value="">Age</option>
                <option value="13-17">13-17</option>
                <option value="18-25">18-25</option>
                <option value="26-35">26-35</option>
                <option value="36-50">36-50</option>
                <option value="51+">51+</option>
            </select>
            
            <input type="text" name="username" class="form-input" placeholder="Choose a username" required>
            <input type="password" name="password" class="form-input" placeholder="Create a password" required>
            
            <button type="submit" class="continue-btn">Continue</button>
        </form>
        
        <a href="/login" class="login-link">Already have an account? Sign in</a>
    </div>
</body>
</html>
        """
    

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
            return redirect(url_for('register'))
        
        if len(password) < 6:
            if request.is_json:
                return jsonify({'success': False, 'message': 'Password must be at least 6 characters'}), 400
            return redirect(url_for('register'))
        
        # Check if username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            if request.is_json:
                return jsonify({'success': False, 'message': 'Username already exists'}), 400
            return redirect(url_for('register'))
        
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
            return redirect(url_for('register'))
    
    return """
<!DOCTYPE html>
<html>
<head>
    <title>GABE Register</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
:root {
  --primary-blue: #2563EB;
  --gradient-divine: linear-gradient(135deg, #2563EB 0%, #6366F1 100%);
  --shadow-elevated: 0 20px 60px rgba(45, 55, 72, 0.12);
  --radius-xl: 32px;
  --radius-md: 12px;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
  background: linear-gradient(135deg, #DBEAFE 0%, #EBF8FF 20%, #3B82F6 70%, #1E40AF 100%);
  background-size: 400% 400%;
  animation: gradientShift 12s ease-in-out infinite;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

@keyframes gradientShift {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

.register-container {
  background: rgba(255,255,255,0.95);
  border-radius: var(--radius-xl);
  backdrop-filter: blur(20px) saturate(180%);
  box-shadow: var(--shadow-elevated), 0 0 0 1px rgba(255, 255, 255, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.5);
  padding: 3rem 2rem;
  width: 100%;
  max-width: 450px;
  transition: all 0.4s ease;
}

.register-container:hover {
  transform: translateY(-2px);
}

h2 {
  background: var(--gradient-divine);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-weight: 700;
  text-align: center;
  margin-bottom: 2rem;
}

.form-label {
  font-weight: 600;
  color: #374151;
  margin-bottom: 0.5rem;
  display: block;
}

.form-control {
  width: 100%;
  border: 2px solid rgba(37, 99, 235, 0.15);
  border-radius: var(--radius-md);
  padding: 12px 16px;
  margin-bottom: 1rem;
  transition: all 0.3s ease;
  background: rgba(255, 255, 255, 0.9);
  font-size: 16px;
}

.form-control:focus {
  outline: none;
  border-color: var(--primary-blue);
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

.btn-primary {
  background: var(--gradient-divine);
  color: white;
  border: none;
  padding: 14px;
  border-radius: var(--radius-md);
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  width: 100%;
  font-size: 16px;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(37, 99, 235, 0.3);
}

.text-center {
  text-align: center;
}

.mt-3 {
  margin-top: 1rem;
}

.mt-2 {
  margin-top: 0.5rem;
}

a {
  color: var(--primary-blue);
  text-decoration: none;
  transition: color 0.3s ease;
}

a:hover {
  color: #1d4ed8;
  text-decoration: underline;
}
    </style>
</head>
<body>
    <div class="register-container">
        <h2>🙏 Join GABE</h2>
        <form method="POST">
            <div>
                <label class="form-label">Name</label>
                <input type="text" name="name" class="form-control" required>
            </div>
            <div>
                <label class="form-label">Username</label>
                <input type="text" name="username" class="form-control" required>
            </div>
            <div>
                <label class="form-label">Password</label>
                <input type="password" name="password" class="form-control" required>
            </div>
            <div>
                <label class="form-label">Age Range</label>
                <select name="age_range" class="form-control" required>
                    <option value="">Select Age Range</option>
                    <option value="13-17">13-17</option>
                    <option value="18-25">18-25</option>
                    <option value="26-35">26-35</option>
                    <option value="36-50">36-50</option>
                    <option value="51+">51+</option>
                </select>
            </div>
            <button type="submit" class="btn-primary">Register</button>
        </form>
        <div class="text-center mt-3">
            <a href="/login">Already have an account? Login here</a>
        </div>
        <div class="text-center mt-2">
            <a href="/">← Back to Home</a>
        </div>
    </div>
</body>
</html>
    """


@app.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    return redirect(url_for('index'))

# [Rest of your API routes remain exactly the same...]
}}

.form-control:focus {{
  outline: none;
  border-color: var(--primary-blue);
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}}

.badge {{
  padding: 0.375rem 0.75rem;
  border-radius: var(--radius-sm);
  font-size: 0.75rem;
  font-weight: 600;
}}

.bg-success {{
  background: #10b981;
  color: white;
}}

.d-flex {{
  display: flex;
}}

.justify-content-between {{
  justify-content: space-between;
}}

.align-items-center {{
  align-items: center;
}}

.mb-2 {{
  margin-bottom: 0.5rem;
}}

.mb-3 {{
  margin-bottom: 1rem;
}}

.me-2 {{
  margin-right: 0.5rem;
}}

.text-center {{
  text-align: center;
}}

.p-3 {{
  padding: 1rem;
}}
    </style>
</head>
<body>
    <div style="min-height: 100vh; display: flex; align-items: center; justify-content: center; padding: 2rem;">
        <div class="chat-container">
            <div class="d-flex justify-content-between align-items-center mb-3">
                <h2>🙏 GABE - Your Spiritual Companion</h2>
                <div>
                    {'<span class="badge bg-success">Logged in as ' + user_name + '</span> <a href="/logout" class="btn-outline-danger">Logout</a>' if user_data else '<a href="/login" class="btn-primary me-2">Login</a><a href="/register" class="btn-outline-primary">Register</a>'}
                </div>
            </div>
            
            <div class="chat-box mb-3" id="chatBox">
                <div class="mb-2">
                    <strong>GABE:</strong> Hello {user_name}! I'm GABE, your spiritual companion. I'm here to offer guidance, prayers, and support on your spiritual journey. How can I help you today? 🙏
                </div>
            </div>
            
            {'<div><input type="text" class="form-control mb-2" id="messageInput" placeholder="Share what\'s on your heart..."><button class="btn-primary" onclick="sendMessage()">Send Message</button></div>' if user_data else '<div class="text-center p-3"><p>Please login to start your conversation with GABE</p></div>'}
        </div>
    </div>
    
    <script>
        function sendMessage() {{
            const input = document.getElementById('messageInput');
            const message = input.value.trim();
            if (!message) return;
            
            const chatBox = document.getElementById('chatBox');
            chatBox.innerHTML += '<div class="mb-2"><strong>You:</strong> ' + message + '</div>';
            input.value = '';
            
            // Send to backend
            fetch('/api/chat', {{
                method: 'POST',
                headers: {{'Content-Type': 'application/json'}},
                body: JSON.stringify({{'message': message}})
            }})
            .then(response => response.json())
            .then(data => {{
                chatBox.innerHTML += '<div class="mb-2"><strong>GABE:</strong> ' + data.response + '</div>';
                chatBox.scrollTop = chatBox.scrollHeight;
            }})
            .catch(error => {{
                chatBox.innerHTML += '<div class="mb-2 text-danger"><strong>GABE:</strong> I\'m having trouble right now, but I\'m still here with you. 💙</div>';
            }});
        }}
        
        // Enter key support
        document.getElementById('messageInput')?.addEventListener('keypress', function(e) {{
            if (e.key === 'Enter') sendMessage();
        }});
    </script>
</body>
</html>
    """

@app.route('/chat')
@login_required
def chat_interface():
    """Chat interface for authenticated users - embedded HTML"""
    return f"""
<!DOCTYPE html>
<html>
<head>
    <title>GABE Chat - Your Spiritual Companion</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
/* GABE - World-Class Spiritual Companion Styles */
:root {{
  --primary-blue: #2563EB;
  --primary-ocean: #1E40AF;
  --secondary-sky: #0EA5E9;
  --accent-indigo: #6366F1;
  --warm-cream: #F9F7F4;
  --soft-mist: #F5F7FA;
  --text-forest: #2D3748;
  --text-slate: #64748B;
  --spiritual-gold: #F59E0B;
  --peace-blue: #DBEAFE;
  --hope-blue: #EBF8FF;
  --gradient-primary: linear-gradient(135deg, #2563EB 0%, #1E40AF 100%);
  --gradient-warm: linear-gradient(135deg, #6366F1 0%, #0EA5E9 100%);
  --gradient-peaceful: linear-gradient(135deg, #DBEAFE 0%, #EBF8FF 100%);
  --gradient-sunset: linear-gradient(135deg, #3B82F6 0%, #1E40AF 50%, #0EA5E9 100%);
  --gradient-divine: linear-gradient(135deg, #2563EB 0%, #6366F1 100%);
  --shadow-soft: 0 4px 20px rgba(37, 99, 235, 0.15);
  --shadow-chat: 0 12px 40px rgba(45, 55, 72, 0.08);
  --shadow-elevated: 0 20px 60px rgba(45, 55, 72, 0.12);
  --shadow-floating: 0 8px 32px rgba(37, 99, 235, 0.1);
  --radius-sm: 8px;
  --radius-md: 12px;
  --radius-lg: 20px;
  --radius-xl: 32px;
  --space-sm: 1rem;
  --space-md: 1.5rem;
  --space-lg: 2rem;
  --space-xl: 3rem;
}}

* {{
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}}

body {{
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
  background: linear-gradient(135deg, #DBEAFE 0%, #EBF8FF 20%, #3B82F6 70%, #1E40AF 100%);
  background-size: 400% 400%;
  animation: gradientShift 12s ease-in-out infinite;
  min-height: 100vh;
  color: var(--text-forest);
  overflow-x: hidden;
}}

@keyframes gradientShift {{
  0% {{ background-position: 0% 50%; }}
  50% {{ background-position: 100% 50%; }}
  100% {{ background-position: 0% 50%; }}
}}

.chat-container {{
  background: rgba(255, 255, 255, 0.95);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-elevated), 0 0 0 1px rgba(255, 255, 255, 0.3);
  backdrop-filter: blur(20px) saturate(180%);
  border: 1px solid rgba(255, 255, 255, 0.5);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  margin: 2rem auto;
  max-width: 800px;
  width: 95%;
}}

.chat-box {{
  height: 500px;
  overflow-y: auto;
  border: 1px solid rgba(37, 99, 235, 0.15);
  padding: 15px;
  background: rgba(255, 255, 255, 0.8);
  border-radius: var(--radius-md);
  margin-bottom: var(--space-md);
  backdrop-filter: blur(10px);
}}

.message {{
  margin-bottom: 10px;
  padding: 12px 16px;
  border-radius: var(--radius-md);
  max-width: 80%;
  word-wrap: break-word;
  box-shadow: var(--shadow-soft);
}}

.user-message {{
  background: var(--gradient-primary);
  color: white;
  margin-left: auto;
  text-align: right;
  border-bottom-right-radius: 4px;
}}

.gabe-message {{
  background: rgba(255, 255, 255, 0.95);
  color: var(--text-forest);
  margin-right: auto;
  border-bottom-left-radius: 4px;
  border-left: 3px solid var(--primary-blue);
}}

h2 {{
  background: var(--gradient-divine);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-weight: 700;
  margin-bottom: var(--space-md);
}}

.btn-primary {{
  background: var(--gradient-primary);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: var(--radius-md);
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: var(--shadow-floating);
}}

.btn-primary:hover {{
  transform: translateY(-2px);
  box-shadow: var(--shadow-elevated);
  background: var(--gradient-warm);
}}

.btn-sm {{
  padding: 6px 12px;
  font-size: 0.875rem;
}}

.btn-outline-danger {{
  background: transparent;
  color: #dc2626;
  border: 2px solid #dc2626;
  padding: 6px 12px;
  border-radius: var(--radius-sm);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  text-decoration: none;
}}

.btn-outline-danger:hover {{
  background: #dc2626;
  color: white;
  transform: translateY(-1px);
  text-decoration: none;
}}

.form-control {{
  border: 2px solid rgba(37, 99, 235, 0.15);
  border-radius: var(--radius-sm);
  padding: 12px 16px;
  transition: all 0.3s ease;
  background: rgba(255, 255, 255, 0.9);
  font-size: 16px;
}}

.form-control:focus {{
  outline: none;
  border-color: var(--primary-blue);
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}}

.input-group {{
  display: flex;
  gap: 12px;
  align-items: stretch;
}}

.input-group .form-control {{
  flex: 1;
}}

.badge {{
  padding: 0.5rem 1rem;
  border-radius: var(--radius-sm);
  font-size: 0.875rem;
  font-weight: 600;
}}

.bg-success {{
  background: #10b981;
  color: white;
}}

.d-flex {{ display: flex; }}
.justify-content-between {{ justify-content: space-between; }}
.align-items-center {{ align-items: center; }}
.mb-3 {{ margin-bottom: 1rem; }}
.me-2 {{ margin-right: 0.5rem; }}
.mt-2 {{ margin-top: 0.5rem; }}
.text-center {{ text-align: center; }}
.text-muted {{ color: #6b7280; }}
.p-4 {{ padding: 1.5rem; }}

small {{
  font-size: 0.875rem;
}}
    </style>
</head>
<body>
    <div class="chat-container p-4">
        <div class="d-flex justify-content-between align-items-center mb-3">
            <h2>🙏 GABE Chat</h2>
            <div>
                <span class="badge bg-success me-2">Welcome, {current_user.name}!</span>
                <a href="/logout" class="btn-sm btn-outline-danger">Logout</a>
            </div>
        </div>
        
        <div class="chat-box mb-3" id="chatBox">
            <div class="gabe-message message">
                <strong>GABE:</strong> Welcome back, {current_user.name}! I'm so glad you're here. I'm ready to listen, offer guidance, and walk alongside you on your spiritual journey. What's on your heart today? 🙏✨
            </div>
        </div>
        
        <div class="input-group">
            <input type="text" class="form-control" id="messageInput" placeholder="Share what's on your heart..." onkeypress="handleKeyPress(event)">
            <button class="btn-primary" onclick="sendMessage()" id="sendBtn">Send Message</button>
        </div>
        
        <div class="mt-2 text-center">
            <small class="text-muted">Press Enter to send • GABE is here to listen and support you</small>
        </div>
    </div>
    
    <script>
        function sendMessage() {{
            const input = document.getElementById('messageInput');
            const message = input.value.trim();
            if (!message) return;
            
            const chatBox = document.getElementById('chatBox');
            const sendBtn = document.getElementById('sendBtn');
            
            // Add user message
            chatBox.innerHTML += '<div class="user-message message"><strong>You:</strong> ' + message + '</div>';
            input.value = '';
            sendBtn.disabled = true;
            sendBtn.textContent = 'Sending...';
            
            // Send to backend
            fetch('/api/chat', {{
                method: 'POST',
                headers: {{'Content-Type': 'application/json'}},
                body: JSON.stringify({{'message': message}})
            }})
            .then(response => response.json())
            .then(data => {{
                chatBox.innerHTML += '<div class="gabe-message message"><strong>GABE:</strong> ' + data.response + '</div>';
                chatBox.scrollTop = chatBox.scrollHeight;
                sendBtn.disabled = false;
                sendBtn.textContent = 'Send Message';
                input.focus();
            }})
            .catch(error => {{
                chatBox.innerHTML += '<div class="gabe-message message" style="color: #dc2626;"><strong>GABE:</strong> I\'m having a moment of technical difficulty, but I\'m still here with you in spirit. Please try again in just a moment. 💙</div>';
                sendBtn.disabled = false;
                sendBtn.textContent = 'Send Message';
            }});
        }}
        
        function handleKeyPress(event) {{
            if (event.key === 'Enter') {{
                sendMessage();
            }}
        }}
        
        // Focus on input when page loads
        document.getElementById('messageInput').focus();
    </script>
</body>
</html>
    """

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
            return redirect(url_for('login'))
        
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
            return redirect(url_for('login'))
    
    return """
<!DOCTYPE html>
<html>
<head>
    <title>GABE Login</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
:root {
  --primary-blue: #2563EB;
  --gradient-peaceful: linear-gradient(135deg, #DBEAFE 0%, #EBF8FF 100%);
  --gradient-divine: linear-gradient(135deg, #2563EB 0%, #6366F1 100%);
  --shadow-elevated: 0 20px 60px rgba(45, 55, 72, 0.12);
  --radius-xl: 32px;
  --radius-md: 12px;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
  background: linear-gradient(135deg, #DBEAFE 0%, #EBF8FF 20%, #3B82F6 70%, #1E40AF 100%);
  background-size: 400% 400%;
  animation: gradientShift 12s ease-in-out infinite;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

@keyframes gradientShift {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

.login-container {
  background: rgba(255,255,255,0.95);
  border-radius: var(--radius-xl);
  backdrop-filter: blur(20px) saturate(180%);
  box-shadow: var(--shadow-elevated), 0 0 0 1px rgba(255, 255, 255, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.5);
  padding: 3rem 2rem;
  width: 100%;
  max-width: 400px;
  transition: all 0.4s ease;
}

.login-container:hover {
  transform: translateY(-2px);
}

h2 {
  background: var(--gradient-divine);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-weight: 700;
  text-align: center;
  margin-bottom: 2rem;
}

.form-label {
  font-weight: 600;
  color: #374151;
  margin-bottom: 0.5rem;
  display: block;
}

.form-control {
  width: 100%;
