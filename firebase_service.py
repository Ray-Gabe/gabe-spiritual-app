import os
import json
import logging
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
import firebase_admin
from firebase_admin import credentials, firestore

class FirebaseService:
    def __init__(self):
        """Initialize Firebase connection"""
        self.db = None
        self._initialize_firebase()
    
    def _initialize_firebase(self):
        """Initialize Firebase with service account or use Firestore emulator"""
        try:
            # Check if Firebase is already initialized
            if firebase_admin._apps:
                app = firebase_admin.get_app()
                self.db = firestore.client(app)
                return
            
            # Try to initialize with service account
            firebase_creds = os.environ.get('FIREBASE_SERVICE_ACCOUNT')
            if firebase_creds:
                try:
                    cred_dict = json.loads(firebase_creds)
                    cred = credentials.Certificate(cred_dict)
                    firebase_admin.initialize_app(cred)
                    self.db = firestore.client()
                    logging.info("Firebase initialized with service account")
                    return
                except Exception as e:
                    logging.warning(f"Failed to initialize with service account: {e}")
            
            # Check for environment project ID
            project_id = os.environ.get('FIREBASE_PROJECT_ID') or os.environ.get('GOOGLE_CLOUD_PROJECT')
            if project_id:
                try:
                    firebase_admin.initialize_app(options={'projectId': project_id})
                    self.db = firestore.client()
                    logging.info(f"Firebase initialized with project ID: {project_id}")
                    return
                except Exception as e:
                    logging.warning(f"Failed to initialize with project ID: {e}")
            
            # Gracefully handle no Firebase configuration
            logging.info("No Firebase configuration found - running without persistent memory")
            self.db = None
            
        except Exception as e:
            logging.warning(f"Firebase initialization failed - running without persistent memory: {e}")
            self.db = None
    
    def is_connected(self) -> bool:
        """Check if Firebase is properly connected"""
        return self.db is not None
    
    def get_user_id(self, user_name: str, session_id: str = None) -> str:
        """Generate a consistent user ID from name and session"""
        # Simple user ID generation - in production, use proper auth
        if user_name:
            return f"user_{user_name.lower().replace(' ', '_')}"
        elif session_id:
            return f"session_{session_id}"
        else:
            return f"anonymous_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    async def save_user_profile(self, user_id: str, name: str, **kwargs) -> bool:
        """Save or update user profile information"""
        if not self.is_connected():
            return False
            
        try:
            user_ref = self.db.collection('users').document(user_id)
            profile_data = {
                'name': name,
                'created_at': datetime.now(timezone.utc),
                'last_active': datetime.now(timezone.utc),
                **kwargs
            }
            
            # Update or create profile
            user_ref.set(profile_data, merge=True)
            logging.info(f"User profile saved for {user_id}")
            return True
            
        except Exception as e:
            logging.error(f"Failed to save user profile: {e}")
            return False
    
    async def get_user_profile(self, user_id: str) -> Optional[Dict]:
        """Retrieve user profile information"""
        if not self.is_connected():
            return None
            
        try:
            user_ref = self.db.collection('users').document(user_id)
            doc = user_ref.get()
            
            if doc.exists:
                return doc.to_dict()
            return None
            
        except Exception as e:
            logging.error(f"Failed to get user profile: {e}")
            return None
    
    async def save_journal_entry(self, user_id: str, content: str, mood: str = None) -> bool:
        """Save a journal entry for the user"""
        if not self.is_connected():
            return False
            
        try:
            journal_ref = self.db.collection('users').document(user_id).collection('journal')
            entry_data = {
                'content': content,
                'mood': mood,
                'timestamp': datetime.now(timezone.utc),
                'date': datetime.now(timezone.utc).strftime('%Y-%m-%d')
            }
            
            journal_ref.add(entry_data)
            logging.info(f"Journal entry saved for {user_id}")
            return True
            
        except Exception as e:
            logging.error(f"Failed to save journal entry: {e}")
            return False
    
    async def get_journal_entries(self, user_id: str, limit: int = 10) -> List[Dict]:
        """Retrieve user's journal entries"""
        if not self.is_connected():
            return []
            
        try:
            journal_ref = (self.db.collection('users').document(user_id)
                          .collection('journal')
                          .order_by('timestamp', direction=firestore.Query.DESCENDING)
                          .limit(limit))
            
            docs = journal_ref.stream()
            entries = []
            
            for doc in docs:
                entry = doc.to_dict()
                entry['id'] = doc.id
                entries.append(entry)
            
            return entries
            
        except Exception as e:
            logging.error(f"Failed to get journal entries: {e}")
            return []
    
    async def save_mood(self, user_id: str, mood: str, context: str = None) -> bool:
        """Save user's mood for the day"""
        if not self.is_connected():
            return False
            
        try:
            today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
            mood_ref = (self.db.collection('users').document(user_id)
                       .collection('moods').document(today))
            
            mood_data = {
                'mood': mood,
                'context': context,
                'timestamp': datetime.now(timezone.utc),
                'date': today
            }
            
            mood_ref.set(mood_data, merge=True)
            logging.info(f"Mood saved for {user_id}: {mood}")
            return True
            
        except Exception as e:
            logging.error(f"Failed to save mood: {e}")
            return False
    
    async def get_recent_moods(self, user_id: str, days: int = 7) -> List[Dict]:
        """Get user's recent moods"""
        if not self.is_connected():
            return []
            
        try:
            mood_ref = (self.db.collection('users').document(user_id)
                       .collection('moods')
                       .order_by('timestamp', direction=firestore.Query.DESCENDING)
                       .limit(days))
            
            docs = mood_ref.stream()
            moods = []
            
            for doc in docs:
                mood_data = doc.to_dict()
                mood_data['id'] = doc.id
                moods.append(mood_data)
            
            return moods
            
        except Exception as e:
            logging.error(f"Failed to get recent moods: {e}")
            return []
    
    async def save_prayer_request(self, user_id: str, request: str) -> bool:
        """Save a prayer request"""
        if not self.is_connected():
            return False
            
        try:
            prayer_ref = self.db.collection('users').document(user_id).collection('prayers')
            prayer_data = {
                'request': request,
                'timestamp': datetime.now(timezone.utc),
                'status': 'active'  # active, answered, ongoing
            }
            
            prayer_ref.add(prayer_data)
            logging.info(f"Prayer request saved for {user_id}")
            return True
            
        except Exception as e:
            logging.error(f"Failed to save prayer request: {e}")
            return False
    
    async def get_prayer_requests(self, user_id: str, limit: int = 5) -> List[Dict]:
        """Get user's prayer requests"""
        if not self.is_connected():
            return []
            
        try:
            prayer_ref = (self.db.collection('users').document(user_id)
                         .collection('prayers')
                         .where('status', '==', 'active')
                         .order_by('timestamp', direction=firestore.Query.DESCENDING)
                         .limit(limit))
            
            docs = prayer_ref.stream()
            prayers = []
            
            for doc in docs:
                prayer_data = doc.to_dict()
                prayer_data['id'] = doc.id
                prayers.append(prayer_data)
            
            return prayers
            
        except Exception as e:
            logging.error(f"Failed to get prayer requests: {e}")
            return []
    
    async def save_conversation_context(self, user_id: str, topic: str, context: str) -> bool:
        """Save conversation context for memory"""
        if not self.is_connected():
            return False
            
        try:
            context_ref = self.db.collection('users').document(user_id).collection('contexts')
            context_data = {
                'topic': topic,
                'context': context,
                'timestamp': datetime.now(timezone.utc),
                'last_mentioned': datetime.now(timezone.utc)
            }
            
            # Check if topic already exists and update
            existing = context_ref.where('topic', '==', topic).limit(1).stream()
            doc_id = None
            for doc in existing:
                doc_id = doc.id
                break
            
            if doc_id:
                context_ref.document(doc_id).set(context_data, merge=True)
            else:
                context_ref.add(context_data)
            
            logging.info(f"Conversation context saved for {user_id}: {topic}")
            return True
            
        except Exception as e:
            logging.error(f"Failed to save conversation context: {e}")
            return False
    
    async def get_user_memory(self, user_id: str) -> Dict[str, Any]:
        """Get comprehensive user memory for personalized responses"""
        if not self.is_connected():
            return {}
            
        try:
            memory = {
                'profile': await self.get_user_profile(user_id),
                'recent_moods': await self.get_recent_moods(user_id, 3),
                'recent_journal': await self.get_journal_entries(user_id, 3),
                'prayer_requests': await self.get_prayer_requests(user_id, 3)
            }
            
            return memory
            
        except Exception as e:
            logging.error(f"Failed to get user memory: {e}")
            return {}