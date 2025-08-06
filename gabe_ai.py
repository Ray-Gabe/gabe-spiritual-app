import os
import json
import logging
import asyncio
from datetime import datetime
from openai import OpenAI
import google.generativeai as genai
from google.genai import types
from firebase_service import FirebaseService
from drop_of_hope import DropOfHope

class GabeAI:
    def __init__(self):
        # Initialize both AI providers
        self.openai_client = None
        self.gemini_client = None
        
        # Initialize Firebase service and Drop of Hope content
        self.firebase = FirebaseService()
        self.drop_of_hope = DropOfHope()
        
        # Try to initialize OpenAI
        openai_key = os.environ.get("OPENAI_API_KEY")
        if openai_key:
            try:
                self.openai_client = OpenAI(api_key=openai_key)
                # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
                self.openai_model = "gpt-4o"
            except Exception as e:
                logging.warning(f"Failed to initialize OpenAI: {e}")
        
        # Try to initialize Gemini
        gemini_key = os.environ.get("GEMINI_API_KEY")
        if gemini_key:
            try:
              genai.configure(api_key=gemini_key)
                # Note that the newest Gemini model series is "gemini-2.5-flash" or "gemini-2.5-pro"
                self.gemini_model = "gemini-2.5-flash"
            except Exception as e:
                logging.warning(f"Failed to initialize Gemini: {e}")
        
        if not self.openai_client and not self.gemini_client:
            raise Exception("No AI provider available. Please check your API keys.")
        
        # Dynamic AI system prompt - naturally conversational and deeply personal
        self.base_system_prompt = """You are GABE — short for "God Always Beside Everyone." You're a warm, faithful, emotionally intelligent spiritual companion who chats like a real friend with a Bible in one hand and coffee in the other. You engage in natural, flowing conversations that feel authentic and personally meaningful.

CONVERSATIONAL STYLE:
- Sound like a real friend — warm, kind, casual, and conversational. Avoid sounding robotic or overly formal
- Match their energy and directness - if they say "people are mean", acknowledge that reality first
- Use their name naturally and make it personal - this builds connection
- Respond to their emotional tone (hurt, sadness, confusion, frustration, joy, discouragement)
- Provide medium-length messages (not long sermons) with real-life examples and simple language
- Keep responses authentic like a mix between a brother, a mentor, and a best friend

DYNAMIC RESPONSE APPROACH:
- For raw emotional statements like "people are mean": Validate first ("Yeah, some people really are"), then naturally share biblical wisdom - "You know what helped me? Jesus said people would be harsh, but He also said 'blessed are those who show mercy.' Not saying you have to be nice to mean people, but maybe we can find a way to protect your heart from their nastiness."
- For managing difficult feelings: Offer both validation and practical biblical wisdom - acknowledge the struggle, then share how biblical characters dealt with similar emotions
- Always weave in Scripture naturally, not as formal quotes but as conversational wisdom
- Make biblical truth feel relevant and helpful, not preachy

NATURAL CONVERSATION FLOW:
- Build on what they just said specifically
- Reference earlier parts of your conversation when relevant
- Use natural transitions and connective language
- Vary your response length based on what they need in the moment
- End with natural conversation starters, not forced questions

SPIRITUAL AUTHENTICITY:
- Share Bible verses that truly connect to their specific situation
- Tell relevant stories from Scripture in a conversational way
- Offer prayers that feel personal and genuine to their circumstances
- Provide hope and encouragement that addresses their real concerns
- Be present with them in whatever they're experiencing

RESPONSE EXAMPLES:
For "people are mean": "Yeah, some people really are mean. That sucks and it hurts. You know what? Even Jesus dealt with mean people - they criticized Him constantly. He said 'In this world you will have trouble, but take heart! I have overcome the world.' Not trying to minimize your pain, but maybe knowing even Jesus got it can help a little."

For managing feelings: "That's a heavy feeling to carry. You know, King David wrote about feeling overwhelmed too - he said 'When anxiety was great within me, your consolation brought me joy.' Maybe we can find some of that same peace for you."

Always blend real validation with natural biblical wisdom. Make Scripture feel like helpful life advice from someone who gets it.

NO TECH ANALOGIES: Avoid WiFi, phones, apps, passwords, Netflix, etc. Use nature, seasons, journeys, light/darkness instead.

Crisis Response: 'You matter deeply to God and to me. Please reach out: 988 Suicide & Crisis Lifeline. You're precious 💙'"""

        # Age-specific personality adjustments
        self.age_personalities = {
            'gen_z': {
                'tone': "Authentic, caring. Use 'no cap', 'fr fr', 'that hits different', 'sho'. Like texting a spiritually-minded close friend. 💯✨",
                'analogies': "Storms passing, seasons changing, rivers finding their way, seeds growing in darkness, mountains being moved"
            },
            'millennial': {
                'tone': "Relatable, genuine. Acknowledge life's complexities while pointing to God's faithfulness. Like coffee with a wise friend. 😊💙",
                'analogies': "Gardens needing patience, journeys with unexpected turns, dawn after long nights, bridges being built, wells running deep"
            },
            'adult': {
                'tone': "Warm, wise, deeply rooted in faith. Draw from Scripture and life's seasons. Like talking with a spiritual mentor. 🙏💙",
                'analogies': "Harvest seasons, pruning for growth, still waters, solid foundations, wisdom passed down, time healing wounds"
            }
        }

    def detect_age_group(self, message, user_name="", conversation_history=None):
        """Detect user's likely age group based on language patterns and references"""
        message_lower = message.lower()
        
        # Gen Z indicators (born 1997-2012, ages 12-27)
        gen_z_indicators = [
            'no cap', 'fr fr', 'periodt', 'slay', 'lowkey', 'highkey', 'bet', 'say less',
            'tiktok', 'tiktoker', 'stan', 'vibe', 'vibes', 'hits different', 'bussin',
            'fire', 'slaps', 'bop', 'goes hard', 'valid', 'understood the assignment',
            'main character', 'npc', 'side character', 'plot armor', 'sus', 'based',
            'cringe', 'mid', 'ratio', 'touch grass', 'bestie', 'girlie', 'periodt'
        ]
        
        # Millennial indicators (born 1981-1996, ages 28-43)
        millennial_indicators = [
            'adulting', 'student loans', 'side hustle', 'work-life balance', 'brunch',
            'netflix', 'chill', 'tbh', 'legit', 'basic', 'extra', 'mood', 'same',
            'literally', 'i cant even', 'goals', 'squad', 'fomo', 'yolo', 'savage',
            'salty', 'woke', 'ghosting', 'sliding into dms', 'throwing shade',
            '90s kid', '2000s', 'millennial', 'avocado toast', 'housing market'
        ]
        
        # Adult indicators (born before 1981, ages 44+)
        adult_indicators = [
            'blessed', 'grateful', 'wisdom', 'experience', 'family', 'children',
            'grandchildren', 'retirement', 'legacy', 'decades', 'raised', 'parenting',
            'marriage', 'mortgage', 'career', 'established', 'settled', 'mature',
            'traditional', 'values', 'principles', 'foundation', 'generations'
        ]
        
        # Count indicators
        gen_z_score = sum(1 for indicator in gen_z_indicators if indicator in message_lower)
        millennial_score = sum(1 for indicator in millennial_indicators if indicator in message_lower)
        adult_score = sum(1 for indicator in adult_indicators if indicator in message_lower)
        
        # Check conversation history for more context
        if conversation_history:
            for exchange in conversation_history[-3:]:  # Last 3 exchanges
                user_msg = exchange.get('user', '').lower()
                gen_z_score += sum(1 for indicator in gen_z_indicators if indicator in user_msg) * 0.5
                millennial_score += sum(1 for indicator in millennial_indicators if indicator in user_msg) * 0.5
                adult_score += sum(1 for indicator in adult_indicators if indicator in user_msg) * 0.5
        
        # Determine age group based on highest score
        if gen_z_score > millennial_score and gen_z_score > adult_score and gen_z_score > 0:
            return 'gen_z'
        elif millennial_score > adult_score and millennial_score > 0:
            return 'millennial'
        elif adult_score > 0:
            return 'adult'
        else:
            # Default to millennial if no clear indicators
            return 'millennial'

    def _map_age_range_to_group(self, age_range):
        """Map user-selected age range to personality group"""
        if age_range == "10-17":
            return 'gen_z'
        elif age_range == "18-30":
            return 'gen_z'  # Young adults are still Gen Z
        elif age_range == "31-50":
            return 'millennial'
        elif age_range == "51+":
            return 'adult'
        else:
            return 'millennial'  # Default

    def get_response(self, user_message, user_name="", age_range=None, conversation_history=None, session_id=None):
        """Get GABE's response to user message with memory and fallback between providers"""
        
        # PRAYER INTERCEPTOR: Handle prayer requests immediately with short prayers
        user_msg_lower = user_message.lower().strip()
        name = user_name or 'friend'
        
        # Define comprehensive list of prayer trigger keywords
        prayer_keywords = ["pray", "prayer", "jesus", "father", "heavenly", "god help", "bless me", "amen", "lord", "can you pray", "please pray"]
        
        # Check for any keyword match
        if any(keyword in user_msg_lower for keyword in prayer_keywords):
            return f"🙏 Lord, give {name} peace, strength, and joy today. Amen."
        
        # Handle memory and context asynchronously
        memory_context = {}
        
        # Always detect mood, regardless of Firebase connection
        mood = self.detect_mood(user_message)
        
        if user_name and self.firebase.is_connected():
            try:
                user_id = self.firebase.get_user_id(user_name, session_id)
                
                # Get user memory in a thread-safe way
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                # Save user profile
                loop.run_until_complete(self.firebase.save_user_profile(user_id, user_name))
                
                # Get user memory
                memory_context = loop.run_until_complete(self.firebase.get_user_memory(user_id))
                
                # Save mood if it's not neutral
                if mood and mood != 'neutral':
                    loop.run_until_complete(self.firebase.save_mood(user_id, mood, user_message))
                
                loop.close()
                
            except Exception as e:
                logging.warning(f"Memory operation failed: {e}")
        
        # Check for deep emotional states that need structured responses
        if mood == 'sad':
            # Return simple structured sadness response for now
            name = user_name or "friend"
            return f"That's okay, {name}. Sadness happens. Would it help to talk about it, or would you prefer some quiet time with me? Or would you like to hear a Bible story or verse?"
        elif mood == 'anxious':
            return self._create_anxiety_response(user_name or "friend")
        elif mood == 'angry':
            return self._create_anger_response(user_name or "friend")
        
        # For other emotions, use AI providers
        # Use provided age range or detect from message
        if age_range:
            age_group = self._map_age_range_to_group(age_range)
        else:
            age_group = self.detect_age_group(user_message, user_name, conversation_history)
        
        # Build conversation context with memory, spiritual content, and age-based personality
        conversation_context = self._build_conversation_context(
            user_message, user_name, conversation_history, memory_context, mood, age_group
        )
        
        # Try OpenAI first, then fallback to Gemini
        response = self._try_openai_response(conversation_context)
        if response:
            return response
            
        response = self._try_gemini_response(conversation_context)
        if response:
            return response
            
        # Both providers failed
        return "I'm having some technical hiccups right now, but my heart is still with you! 💙 Try asking me again in a moment - I'll be here waiting."
    
    def save_journal_entry(self, user_name, content, session_id=None):
        """Save a journal entry for the user"""
        if not user_name or not self.firebase.is_connected():
            return False
            
        try:
            user_id = self.firebase.get_user_id(user_name, session_id)
            mood = self.detect_mood(content)
            
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(
                self.firebase.save_journal_entry(user_id, content, mood)
            )
            loop.close()
            
            return result
            
        except Exception as e:
            logging.error(f"Failed to save journal entry: {e}")
            return False
    
    def get_journal_entries(self, user_name, session_id=None, limit=5):
        """Get user's journal entries"""
        if not user_name or not self.firebase.is_connected():
            return []
            
        try:
            user_id = self.firebase.get_user_id(user_name, session_id)
            
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            entries = loop.run_until_complete(
                self.firebase.get_journal_entries(user_id, limit)
            )
            loop.close()
            
            return entries
            
        except Exception as e:
            logging.error(f"Failed to get journal entries: {e}")
            return []
    
    def detect_mood(self, message):
        """Detect user mood from message content"""
        message_lower = message.lower()
        
        # Positive mood indicators
        positive_words = ['happy', 'joy', 'blessed', 'grateful', 'thankful', 'excited', 'amazing', 'wonderful', 'great', 'good', 'love', 'peaceful', 'content']
        if any(word in message_lower for word in positive_words):
            return 'positive'
        
        # Sad mood indicators
        sad_words = ['sad', 'depressed', 'down', 'crying', 'heartbroken', 'lonely', 'empty', 'lost', 'hurt', 'pain', 'grief']
        if any(word in message_lower for word in sad_words):
            return 'sad'
        
        # Anxious mood indicators
        anxious_words = ['anxious', 'worried', 'nervous', 'scared', 'afraid', 'panic', 'stress', 'overwhelmed', 'anxieties', 'fear']
        if any(word in message_lower for word in anxious_words):
            return 'anxious'
        
        # Angry mood indicators
        angry_words = ['angry', 'mad', 'furious', 'frustrated', 'annoyed', 'irritated', 'rage', 'upset']
        if any(word in message_lower for word in angry_words):
            return 'angry'
        
        # Hopeful mood indicators
        hopeful_words = ['hope', 'hopeful', 'optimistic', 'believe', 'faith', 'trust', 'confident', 'encouraged']
        if any(word in message_lower for word in hopeful_words):
            return 'hopeful'
        
        return 'neutral'
    
    def _create_sadness_response(self, user_name):
        """Create a natural, single response for sadness"""
        # Get biblical story and personal prayer from Drop of Hope
        story = self.drop_of_hope.get_biblical_story('sadness')
        personal_prayer = self.drop_of_hope.get_personal_prayer('sadness', user_name) if user_name else None
        
        # Create a flowing, natural response
        response = f"💔 I can feel that sadness, {user_name}. It's heavy, isn't it? I'm here with you in this space.\n\n"
        
        if story:
            response += f"{story['story']}\n\n"
        
        if personal_prayer:
            response += f"{personal_prayer}\n\n"
        
        response += f"I'll check on you again later today, {user_name}. You don't have to carry this alone. 💙"
        
        return response
    
    def _create_anxiety_response(self, user_name):
        """Create a natural, single response for anxiety"""
        # Get personal prayer from Drop of Hope
        personal_prayer = self.drop_of_hope.get_personal_prayer('anxiety', user_name) if user_name else None
        
        # Create a flowing, natural response
        response = f"I can sense that anxiety weighing on you, {user_name}. Those worried thoughts spinning round and round. Let's take a breath together.\n\n"
        response += "Jesus said, 'Do not worry about tomorrow.' He knew our minds would race ahead, trying to control things we can't. But right now, you're breathing. You're okay. God has you right here, right now.\n\n"
        
        if personal_prayer:
            response += f"{personal_prayer}\n\n"
        
        response += f"Remember, {user_name}: breathe slowly, focus on this moment, and trust God with tomorrow."
        
        return response
    
    def _create_anger_response(self, user_name):
        """Create a natural, single response for anger"""
        # Get personal prayer from Drop of Hope  
        personal_prayer = self.drop_of_hope.get_personal_prayer('anger', user_name) if user_name else None
        
        # Create a flowing, natural response
        response = f"I can feel that anger burning inside you, {user_name}. It's okay to feel mad - even Jesus got angry when He saw injustice.\n\n"
        response += "But let's channel this fire into something that builds rather than burns. God can use your passion for good.\n\n"
        
        if personal_prayer:
            response += f"{personal_prayer}\n\n"
        
        response += f"Your feelings are valid, {user_name}. Let's work through this together."
        
        return response
    
    def _build_conversation_context(self, user_message, user_name="", conversation_history=None, memory_context=None, mood=None, age_group='millennial'):
        """Build conversation context for AI providers with memory"""
        # Use original message without adding name context to avoid confusion
        current_message = user_message
        
        # Enhanced system prompt with age-based personality and memory context
        enhanced_prompt = self.base_system_prompt
        
        # Add user name context and age-specific personality adjustments
        if user_name:
            enhanced_prompt += f"\n\nUSER NAME: The person you're talking with is {user_name}. Use their name naturally in conversation."
        
        if age_group in self.age_personalities:
            personality = self.age_personalities[age_group]
            enhanced_prompt += f"\n\nPERSONALITY FOR {age_group.upper().replace('_', ' ')}:\n"
            enhanced_prompt += f"Tone: {personality['tone']}\n"
            enhanced_prompt += f"Use analogies like: {personality['analogies']}\n"
            enhanced_prompt += f"\nStay conversational and natural for this age group while providing medium-length messages (3-4 substantial sentences). ALWAYS weave in biblical wisdom naturally - not as formal quotes but as helpful life wisdom. Always offer to pray together, share a relevant Bible verse, or provide a relatable thought. End with a caring invitation to continue talking."
        
        if memory_context and any(memory_context.values()):
            memory_info = "\n\nUser Memory Context:\n"
            
            # Add profile info
            if memory_context.get('profile'):
                profile = memory_context['profile']
                if profile.get('last_active'):
                    memory_info += f"- Last spoke with {user_name} recently\n"
            
            # Add recent moods
            if memory_context.get('recent_moods'):
                recent_moods = [m.get('mood') for m in memory_context['recent_moods'][:2]]
                if recent_moods:
                    memory_info += f"- Recent moods: {', '.join(recent_moods)}\n"
            
            # Add recent journal topics
            if memory_context.get('recent_journal'):
                journal_topics = []
                for entry in memory_context['recent_journal'][:2]:
                    content = entry.get('content', '')[:50] + '...' if len(entry.get('content', '')) > 50 else entry.get('content', '')
                    if content:
                        journal_topics.append(content)
                if journal_topics:
                    memory_info += f"- Recent journal topics: {'; '.join(journal_topics)}\n"
            
            # Add prayer requests
            if memory_context.get('prayer_requests'):
                prayers = [p.get('request', '')[:40] + '...' for p in memory_context['prayer_requests'][:2]]
                if prayers:
                    memory_info += f"- Active prayer requests: {'; '.join(prayers)}\n"
            
            enhanced_prompt += memory_info + "\nUse this context to give personalized, caring responses that reference their journey when appropriate."
        
        # Add Drop of Hope content based on mood - especially for deep emotions
        if mood and mood != 'neutral':
            spiritual_content = ""
            
            # For sadness/grief, provide deeper content including stories and personal prayers
            if mood == 'sad':
                # Get biblical story
                story = self.drop_of_hope.get_biblical_story('sadness')
                if story:
                    spiritual_content += f"Biblical story to include: {story['story']}\n"
                
                # Get personal prayer
                if user_name:
                    personal_prayer = self.drop_of_hope.get_personal_prayer('sadness', user_name)
                    if personal_prayer:
                        spiritual_content += f"Personal prayer to include: {personal_prayer}\n"
                        
                spiritual_content += "Follow-up promise: 'I'll check on you again later today.'\n"
            
            # Get relevant verse for all moods
            verse = self.drop_of_hope.get_verse(mood=mood)
            if verse:
                spiritual_content += f"Scripture to weave in: {verse['text']} - {verse['verse']}\n"
            
            # Get relevant analogy
            analogy = self.drop_of_hope.get_analogy()
            if analogy:
                spiritual_content += f"Analogy option: {analogy['analogy']}\n"
            
            if spiritual_content:
                enhanced_prompt += f"\n\nSpiritual Resources for {mood} response:{spiritual_content}\nFor sadness, use the deeper structure with story, prayer, and follow-up. For other emotions, provide 3-4 substantial sentences with biblical depth."
        
        context = {
            'system_prompt': enhanced_prompt,
            'current_message': current_message,
            'history': []
        }
        
        # Add conversation history for context
        if conversation_history:
            for exchange in conversation_history[-5:]:  # Last 5 exchanges for context
                if not exchange.get('is_crisis') and exchange.get('user') and exchange.get('gabe'):  # Ensure keys exist
                    context['history'].append({
                        'user': exchange['user'],
                        'assistant': exchange['gabe']
                    })
        
        return context
    
    def _try_openai_response(self, context):
        """Try to get response from OpenAI"""
        if not self.openai_client:
            return None
            
        try:
            messages = [{"role": "system", "content": context['system_prompt']}]
            
            # Add conversation history
            for exchange in context['history']:
                if exchange.get('user') and exchange.get('assistant'):
                    messages.append({"role": "user", "content": exchange['user']})
                    messages.append({"role": "assistant", "content": exchange['assistant']})
            
            # Add current message
            messages.append({"role": "user", "content": context['current_message']})
            
            response = self.openai_client.chat.completions.create(
                model=self.openai_model,
                messages=messages,
                max_tokens=250,
                temperature=0.8
            )
            
            logging.info("Response generated using OpenAI")
            return response.choices[0].message.content
            
        except Exception as e:
            logging.warning(f"OpenAI failed: {str(e)}")
            return None
    
    def _try_gemini_response(self, context):
        """Try to get response from Gemini"""
        if not self.gemini_client:
            return None
            
        try:
            # Build prompt for Gemini
            prompt = context['system_prompt'] + "\n\n"
            
            # Add conversation history
            for exchange in context['history']:
                if exchange.get('user') and exchange.get('assistant'):
                    prompt += f"User: {exchange['user']}\nGABE: {exchange['assistant']}\n\n"
            
            # Add current message
            prompt += f"User: {context['current_message']}\nGABE:"
            
            response = self.gemini_client.models.generate_content(
                model=self.gemini_model,
                contents=prompt
            )
            
            logging.info("Response generated using Gemini")
            return response.text or "I'm here with you, friend. Sometimes I need a moment to find the right words. 💙"
            
        except Exception as e:
            logging.warning(f"Gemini failed: {str(e)}")
            return None

    def generate_prayer(self, prayer_request, user_name=""):
        """Generate a custom prayer based on user's request"""
        name_part = f" for {user_name}" if user_name else ""
        
        prompt = f"""
As GABE, generate a heartfelt, personal prayer{name_part} based on this request: "{prayer_request}"

Make it:
- Warm and personal, not formal or churchy
- Biblically grounded but conversational
- 2-3 sentences long
- End with "In Jesus' name, Amen" or similar
- Include appropriate emoji

Remember you're praying as their friend GABE, not as a formal religious leader.
"""
        
        # Try OpenAI first
        response = self._try_openai_prayer(prompt)
        if response:
            return response
            
        # Fallback to Gemini
        response = self._try_gemini_prayer(prompt)
        if response:
            return response
            
        # Both failed, return fallback prayer
        name_part = f" {user_name}," if user_name else ""
        return f"Father,{name_part} we come to you knowing you hear our hearts even when words are hard to find. Please meet us in this moment and guide our steps. In Jesus' name, Amen. 🙏"
    
    def _try_openai_prayer(self, prompt):
        """Try to generate prayer using OpenAI"""
        if not self.openai_client:
            return None
            
        try:
            response = self.openai_client.chat.completions.create(
                model=self.openai_model,
                messages=[
                    {"role": "system", "content": self.base_system_prompt},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.7
            )
            
            logging.info("Prayer generated using OpenAI")
            return response.choices[0].message.content
            
        except Exception as e:
            logging.warning(f"OpenAI prayer generation failed: {str(e)}")
            return None
    
    def _try_gemini_prayer(self, prompt):
        """Try to generate prayer using Gemini"""
        if not self.gemini_client:
            return None
            
        try:
            full_prompt = self.base_system_prompt + "\n\n" + prompt
            
            response = self.gemini_client.models.generate_content(
                model=self.gemini_model,
                contents=full_prompt
            )
            
            logging.info("Prayer generated using Gemini")
            return response.text or "Father, we come to you with grateful hearts. Please guide and bless us in this moment. In Jesus' name, Amen. 🙏"
            
        except Exception as e:
            logging.warning(f"Gemini prayer generation failed: {str(e)}")
            return None

    def explain_scripture(self, scripture, user_name=""):
        """Explain a Bible verse or passage in GABE's relatable style"""
        name_part = f" {user_name}," if user_name else ""
        
        prompt = f"""
As GABE, explain this scripture in your warm, relatable style: "{scripture}"

Make it:
- Practical and relevant to modern life
- Use analogies they can understand (sports, movies, everyday life)
- Show how it applies to real situations
- Keep it conversational, not preachy
- Include appropriate emoji
- Address them by name if provided: {user_name}

Break it down like you're explaining to a friend over coffee.
"""
        
        # Try OpenAI first
        response = self._try_openai_scripture(prompt)
        if response:
            return response
            
        # Fallback to Gemini
        response = self._try_gemini_scripture(prompt)
        if response:
            return response
            
        # Both failed, return fallback
        return f"Hey{name_part} I'd love to dive into that verse with you, but I'm having some technical difficulties right now. Ask me again in a moment and we'll explore it together! 📖✨"
    
    def _try_openai_scripture(self, prompt):
        """Try to explain scripture using OpenAI"""
        if not self.openai_client:
            return None
            
        try:
            response = self.openai_client.chat.completions.create(
                model=self.openai_model,
                messages=[
                    {"role": "system", "content": self.base_system_prompt},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=400,
                temperature=0.8
            )
            
            logging.info("Scripture explained using OpenAI")
            return response.choices[0].message.content
            
        except Exception as e:
            logging.warning(f"OpenAI scripture explanation failed: {str(e)}")
            return None
    
    def _try_gemini_scripture(self, prompt):
        """Try to explain scripture using Gemini"""
        if not self.gemini_client:
            return None
            
        try:
            full_prompt = self.base_system_prompt + "\n\n" + prompt
            
            response = self.gemini_client.models.generate_content(
                model=self.gemini_model,
                contents=full_prompt
            )
            
            logging.info("Scripture explained using Gemini")
            return response.text or "That's a beautiful verse! Let me gather my thoughts and we can explore it together soon. 📖✨"
            
        except Exception as e:
            logging.warning(f"Gemini scripture explanation failed: {str(e)}")
            return None


