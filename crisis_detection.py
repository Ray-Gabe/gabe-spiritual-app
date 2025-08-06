import re
import logging

class CrisisDetector:
    def __init__(self):
        # Crisis keywords and phrases
        self.crisis_keywords = [
            # Self-harm indicators (high severity only)
            'kill myself', 'end my life', 'want to die', 'planning suicide',
            'going to hurt myself', 'going to cut myself', 'going to harm myself',
            'better off dead', 'take my own life', 'ready to end it',
            
            # Immediate danger phrases
            'final goodbye', 'last message', 'goodbye world', 'tonight is the night',
            'cant take it anymore and going to', "can't go on anymore and will"
        ]
        
        # Hotline information
        self.crisis_resources = {
            'us': {
                'name': 'National Suicide Prevention Lifeline',
                'number': '988',
                'text': 'Text HOME to 741741'
            },
            'international': {
                'name': 'International Association for Suicide Prevention',
                'website': 'https://www.iasp.info/resources/Crisis_Centres/'
            }
        }

    def check_for_crisis(self, message):
        """Check if message contains crisis indicators"""
        message_lower = message.lower()
        
        # POSITIVE INDICATORS - Do NOT trigger crisis if these are present
        positive_indicators = [
            'thank you', 'thanks', 'helped', 'helping', 'better', 'good', 'great',
            'feel better', 'feeling better', 'appreciate', 'grateful', 'blessed',
            'improving', 'progress', 'hope', 'hopeful', 'encouraged', 'uplifting',
            'this help', 'this helped', 'working', 'awesome', 'amazing'
        ]
        
        # Check for positive indicators first - if found, not a crisis
        for positive in positive_indicators:
            if positive in message_lower:
                return None
        
        # Remove punctuation for better matching
        cleaned_message = re.sub(r'[^\w\s]', ' ', message_lower)
        
        # HIGH SEVERITY crisis keywords that indicate immediate danger
        high_crisis_keywords = [
            'kill myself', 'end my life', 'want to die', 'going to hurt myself',
            'planning suicide', 'better off dead', 'going to end it', 'final goodbye'
        ]
        
        # Check for high severity keywords (immediate crisis)
        for keyword in high_crisis_keywords:
            if keyword in cleaned_message:
                return self._generate_crisis_response(message)
        
        # Check for severe distress patterns with context
        severe_patterns = [
            r'\bi\s+want\s+to\s+die\b',
            r'\bkill\s+me\s+now\b',
            r'\bend\s+it\s+all\s+tonight\b',
            r'\bgive\s+up\s+on\s+life\s+now\b',
            r'\bno\s+reason\s+to\s+live\s+anymore\b'
        ]
        
        for pattern in severe_patterns:
            if re.search(pattern, cleaned_message):
                return self._generate_crisis_response(message)
        
        return None

    def _generate_crisis_response(self, original_message):
        """Generate appropriate crisis response"""
        response = """🚨 Hey friend, I hear you and what you're feeling really matters. You're not alone in this moment, but I need you to reach out to someone who can help you right now.

**IMMEDIATE HELP:**
🇺🇸 **Crisis Text Line:** Text HOME to **741741**
🇺🇸 **National Suicide Prevention Lifeline:** **988**
🌍 **International:** https://www.iasp.info/resources/Crisis_Centres/

**If you're in immediate danger, please call 911 (US) or your local emergency number.**

I'm here to support you, but I can't replace real-time human help. You matter way too much, and there are people trained to walk through this darkness with you. 

Please reach out right now. Your life has value and purpose, even when it doesn't feel like it. 💙

*Remember: I'm not a licensed counselor, therapist, or doctor - I'm here to support, not replace professional help.*"""

        return response

    def is_mild_distress(self, message):
        """Check for mild distress that needs gentle support but not crisis intervention"""
        message_lower = message.lower()
        
        mild_distress_words = [
            'struggling', 'difficult time', 'hard day', 'feeling down',
            'overwhelmed', 'stressed out', 'having trouble', 'going through',
            'tough situation', 'challenging', 'difficult', 'rough patch'
        ]
        
        return any(phrase in message_lower for phrase in mild_distress_words)

    def get_support_resources(self, mood_type=None):
        """Get relevant support resources based on mood"""
        resources = {
            'general': [
                "🤗 Remember: You're never alone in this journey",
                "📖 Consider reading Psalms when you need comfort",
                "🙏 Prayer is always available - God listens 24/7",
                "👥 Reach out to a trusted friend or family member"
            ],
            'anxiety': [
                "🌬️ Try deep breathing: 4 counts in, hold for 4, out for 4",
                "📖 Read Philippians 4:6-7 about not being anxious",
                "🎵 Listen to calming worship music",
                "🚶‍♀️ Take a gentle walk outside if possible"
            ],
            'sadness': [
                "😢 It's okay to feel sad - even Jesus wept",
                "📖 Psalm 34:18 - God is close to the brokenhearted",
                "☎️ Call someone who cares about you",
                "📝 Journal your feelings to God"
            ]
        }
        
        return resources.get(mood_type or 'general', resources['general'])
