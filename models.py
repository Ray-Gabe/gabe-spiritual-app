from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

def create_models(db):
    """Create model classes with database reference"""
    
    class User(UserMixin, db.Model):
        __tablename__ = 'users'
        
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(80), unique=True, nullable=False)
        password_hash = db.Column(db.String(256), nullable=False)
        name = db.Column(db.String(100), nullable=False)
        age_range = db.Column(db.String(20), nullable=False)
        created_at = db.Column(db.DateTime, default=datetime.utcnow)
        last_login = db.Column(db.DateTime)
        
        # Relationship to conversation history
        conversations = db.relationship('Conversation', backref='user', lazy=True, cascade='all, delete-orphan')
        
        def set_password(self, password):
            """Hash and set the user's password"""
            self.password_hash = generate_password_hash(password)
        
        def check_password(self, password):
            """Check if provided password matches the hash"""
            return check_password_hash(self.password_hash, password)
        
        def update_last_login(self):
            """Update the last login timestamp"""
            self.last_login = datetime.utcnow()
            db.session.commit()
    
    class Conversation(db.Model):
        __tablename__ = 'conversations'
        
        id = db.Column(db.Integer, primary_key=True)
        user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
        user_message = db.Column(db.Text, nullable=False)
        gabe_response = db.Column(db.Text, nullable=False)
        mood = db.Column(db.String(20))
        is_crisis = db.Column(db.Boolean, default=False)
        is_prayer = db.Column(db.Boolean, default=False)
        timestamp = db.Column(db.DateTime, default=datetime.utcnow)
        
        def to_dict(self):
            """Convert conversation to dictionary for JSON serialization"""
            return {
                'id': self.id,
                'user_message': self.user_message,
                'gabe_response': self.gabe_response,
                'mood': self.mood,
                'is_crisis': self.is_crisis,
                'is_prayer': self.is_prayer,
                'timestamp': self.timestamp.isoformat() if self.timestamp else None
            }
    
    return User, Conversation
