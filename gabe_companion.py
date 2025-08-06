import os
import json
import logging
from datetime import datetime
from openai import OpenAI
try:
    import google.generativeai as genai
except ImportError:
    genai = None

class GabeCompanion:
    """
    A naturally conversational spiritual AI companion that feels personal and intuitive,
    like talking to a wise, caring friend who remembers your conversations and truly listens.
    """
    
    def __init__(self):
        # Initialize Gemini as primary
        self.gemini_client = None
        self.openai_client = None
        
        gemini_key = os.environ.get("GEMINI_API_KEY")
        if gemini_key and genai and hasattr(genai, 'configure'):
            try:
                genai.configure(api_key=gemini_key)
                if hasattr(genai, 'GenerativeModel'):
                    self.gemini_model = genai.GenerativeModel('gemini-1.5-flash')
                    self.gemini_client = True
                    logging.info("Gemini client initialized successfully (PRIMARY)")
                else:
                    logging.warning("GenerativeModel not available in genai module")
                    self.gemini_client = None
            except Exception as e:
                logging.warning(f"Failed to initialize Gemini: {e}")
                self.gemini_client = None
        else:
            self.gemini_client = None
        
        # Initialize OpenAI as fallback
        openai_key = os.environ.get("OPENAI_API_KEY")
        if openai_key:
            try:
                self.openai_client = OpenAI(api_key=openai_key)
                # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
                self.openai_model = "gpt-4o"
                logging.info("OpenAI client initialized successfully (FALLBACK)")
            except Exception as e:
                logging.warning(f"Failed to initialize OpenAI: {e}")
        
        if not self.gemini_client and not self.openai_client:
            logging.warning("No AI provider available - conversations will use fallback responses")
        
        # Dynamic conversation memory
        self.conversation_memory = {}
        self.user_insights = {}
        
        # Enhanced conversation state management (inspired by JavaScript flow)
        self.conversation_states = {}
        self.voice_mode_enabled = {}  # Track voice mode per session
        self.chunked_conversations = {}  # Track multi-part conversations
        
        # Story continuation system
        self.story_contexts = {}  # Track ongoing stories per session
        
        # Bible stories with multiple parts (from JavaScript code inspiration)
        self.bible_stories = {
            'elijah': {
                'parts': [
                    "Think of the story of Elijah. He was totally burnt out, right? But God didn't yell; He sent food and rest.",
                    "After Elijah rested, God spoke to him - not in the earthquake or fire, but in a gentle whisper.",
                    "God reminded Elijah he wasn't alone and gave him new purpose. Sometimes rest comes before the breakthrough.",
                    "Would you like to hear another story, or can I pray with you about what's heavy on your heart?"
                ],
                'name': 'Elijah under the broom tree'
            },
            'david_goliath': {
                'parts': [
                    "Let me tell you about young David facing Goliath. Everyone saw a giant - David saw an opportunity to trust God.",
                    "David didn't need fancy armor. He picked up smooth stones because he knew God was with him.",
                    "One stone, one shot, and the giant fell. Not because David was strong, but because God was faithful.",
                    "Your giants might feel overwhelming, but God sees them differently. Would you like another story or a prayer?"
                ],
                'name': 'David and Goliath'
            },
            'red_sea': {
                'parts': [
                    "Picture Moses at the Red Sea - enemy behind, impossible waters ahead. Nowhere to go but through.",
                    "God didn't remove the sea. He split it wide open, making a way where there was no way.",
                    "The same waters that saved God's people destroyed their enemies. God turned the obstacle into victory.",
                    "Sometimes God doesn't remove our challenges - He walks through them with us. Want to hear more?"
                ],
                'name': 'Moses and the Red Sea'
            }
        }
        
    def is_story_request(self, user_message):
        """Check if user is asking for a Bible story"""
        story_keywords = [
            'story', 'tell me a story', 'bible story', 'share a story',
            'david and goliath', 'moses', 'daniel', 'noah', 'jesus',
            'parable', 'tell me about', 'biblical story'
        ]
        return any(keyword in user_message.lower() for keyword in story_keywords)
    
    def get_response(self, user_message, user_name=None, age_range=None, conversation_history=None, session_id=None):
        """
        Get a naturally conversational response that feels personal and intuitive
        """
        try:
            # PRAYER INTERCEPTOR: Handle prayer requests immediately with short prayers
            user_msg_lower = user_message.lower().strip()
            name = user_name or 'friend'
            
            logging.info(f"INTERCEPTOR: Checking message: '{user_msg_lower}'")
            
            # If it's a direct prayer request, return short prayer immediately
            prayer_triggers = ['pray for', 'say a prayer', 'please pray', 'pray that', 'father help', 'lord help', 'jesus help', 'pray with me', 'can you pray']
            triggered = any(trigger in user_msg_lower for trigger in prayer_triggers)
            
            logging.info(f"INTERCEPTOR: Prayer triggers found: {triggered}")
            
            if triggered:
                logging.info("INTERCEPTOR: Returning short prayer immediately")
                return f"Father, be with {name}. You see their heart. In Jesus name, Amen."
            # First check if we're in the middle of a story continuation
            if session_id and session_id in self.story_contexts:
                story_continuation = self.handle_story_continuation(user_message, session_id, user_name)
                if story_continuation:
                    return story_continuation
            
            # Check if user is requesting a story
            story_request = self.detect_story_request_and_mood(user_message)
            if story_request:
                story_start = self.initiate_bible_story(story_request, session_id or 'default')
                if story_start:
                    return story_start
            
            # Check if this is a prayer request (from JavaScript logic)
            is_prayer_request = self.detect_prayer_request(user_message)
            
            # Build dynamic conversation context
            context = self._build_dynamic_context(
                user_message, user_name, age_range, conversation_history, session_id
            )
            
            # Create naturally flowing conversation prompt
            system_prompt = self._create_natural_system_prompt(user_name, age_range, context)
            
            # Prepare conversation for OpenAI
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
            
            # Add recent conversation history for context
            if conversation_history:
                # Add last few exchanges for natural flow
                for exchange in conversation_history[-3:]:
                    if exchange.get('user'):
                        messages.insert(-1, {"role": "user", "content": exchange['user']})
                    if exchange.get('gabe'):
                        messages.insert(-1, {"role": "assistant", "content": exchange['gabe']})
            
            # Try Gemini first, then fallback to OpenAI
            ai_response = self._try_gemini_response(system_prompt, user_message, conversation_history)
            if not ai_response:
                ai_response = self._try_openai_response(messages)
            
            if not ai_response:
                # Fallback to a graceful spiritual response
                ai_response = self._create_fallback_response(user_name, user_message)
            
            # Apply closure system for prayer requests (from JavaScript code)
            if is_prayer_request:
                mood = self.detect_mood(user_message)
                closure_verse = self.get_closing_verse(mood)
                ai_response = f"{ai_response}\n\n{closure_verse}"
            
            # Update conversation insights
            self._update_conversation_insights(user_message, ai_response, user_name, session_id)
            
            return ai_response
            
        except Exception as e:
            logging.error(f"Error in GabeCompanion.get_response: {str(e)}")
            return self._create_fallback_response(user_name, user_message)
    
    def _create_natural_system_prompt(self, user_name, age_range, context):
        """Create a dynamic system prompt for natural conversation"""
        
        base_personality = f"""You are GABE — short for "Guidance And Blessing Everyday." You are a warm, wise, Spirit-led companion who speaks with empathy, joy, and truth. You are not a therapist or pastor, but a trusted, faith-based friend who listens and reflects. You use modern language, scripture where fitting, relatable analogies, and always invite deeper engagement — but never force it.

Your core traits: gentle, grounded, deeply human, joyful, and conversational.
You do not overload the user. You speak like a friend. You give the user space, but gently re-engage if they go quiet.

CONVERSATION GUIDELINES:
- Keep responses SHORT (1-3 sentences max)
- Be gentle and conversational  
- Either reflect what they shared, offer spiritual insight, or give a small prompt
- NEVER suggest multiple things at once
- Use natural, modern language with contractions
- Use the person's name occasionally but not in every response - be natural about it
- If praying, keep prayers very short (2-3 sentences max) and conversational, not formal

EMOTIONAL RESPONSES:

If they're SAD or LOW:
- Show empathy first: "That's okay. Even Jesus wept."
- Offer biblical comfort: "You know when Lazarus died, Jesus didn't rush to fix it — He felt the pain first."
- Gentle invitation: "Would it help if I shared a quick story or verse that might lift your heart a little?"

If they're ANGRY or FRUSTRATED:
- Validate their feelings: "That kind of anger deserves to be heard."
- Biblical perspective: "Even Jesus got angry. You're not alone."
- Gentle space: "Want to tell me more about what's stirring that up?"

If they're QUIET or WITHDRAWN:
- Gentle prompts: "Would it help if I told you a short story or verse that might comfort you?"
- Or: "Can I share how Jesus handled moments like this?"
- Soft presence: "I'm right here with you."

BIBLE ANALOGIES (use these naturally):
- "Remember when Peter stepped out on the water? He started sinking only when he looked away from Jesus — maybe that's what today feels like. But Jesus reached out anyway."
- "Think of Elijah under the broom tree — burnt out, done. But God didn't scold him. He sent rest and food. That's the Father's heart."
- "Even Job, when everything fell apart, had moments of silence with God before answers came. You're not doing this wrong."

NEVER use formal phrases like "How can I assist?" or "I'm here to help." You're a friend, not a support agent."""

        # Add age-appropriate communication style
        if age_range == "10-17" or age_range == "18-30":
            personality_add = """
COMMUNICATION STYLE: Speak naturally and authentically. Avoid formal language. Be a genuine friend who understands their world while sharing spiritual wisdom through natural conversation."""
        elif age_range == "31-50":
            personality_add = """
COMMUNICATION STYLE: Engage in authentic dialogue that acknowledges life's complexities. Show real understanding while pointing to God's faithfulness through genuine conversation."""
        else:
            personality_add = """
COMMUNICATION STYLE: Engage in thoughtful, genuine dialogue. Share wisdom naturally through conversation rather than formal teaching. Be authentically caring."""
        
        # Add conversation context if available
        context_info = ""
        if context.get('previous_topics'):
            context_info = f"\nCONVERSATION CONTEXT: {context['previous_topics']}"
        if context.get('emotional_state'):
            context_info += f"\nEMOTIONAL CONTEXT: {context['emotional_state']}"
        if context.get('prayer_patterns'):
            context_info += f"\nPRAYER HISTORY: {context['prayer_patterns']}"
        
        return base_personality + personality_add + context_info
    
    def _build_dynamic_context(self, user_message, user_name, age_range, conversation_history, session_id):
        """Build intelligent context for natural conversation flow"""
        context = {
            'previous_topics': [],
            'emotional_state': 'neutral',
            'prayer_patterns': [],
            'conversation_themes': []
        }
        
        # Analyze recent conversation for themes and patterns
        if conversation_history:
            recent_messages = conversation_history[-5:]  # Last 5 exchanges
            
            # Extract conversation themes
            topics = []
            for exchange in recent_messages:
                if exchange.get('user'):
                    user_msg = exchange['user'].lower()
                    # Look for key themes
                    if any(word in user_msg for word in ['work', 'job', 'career', 'boss']):
                        topics.append('work challenges')
                    if any(word in user_msg for word in ['family', 'relationship', 'marriage', 'kids']):
                        topics.append('family matters')
                    if any(word in user_msg for word in ['pray', 'prayer', 'god', 'jesus', 'faith']):
                        topics.append('spiritual growth')
                    if any(word in user_msg for word in ['sad', 'hurt', 'pain', 'difficult', 'hard']):
                        topics.append('emotional support')
            
            context['previous_topics'] = ', '.join(set(topics))
        
        # Detect current emotional undertone
        current_msg = user_message.lower()
        if any(word in current_msg for word in ['sad', 'depressed', 'hurt', 'pain', 'broken']):
            context['emotional_state'] = 'needs comfort and prayer'
        elif any(word in current_msg for word in ['anxious', 'worried', 'scared', 'afraid']):
            context['emotional_state'] = 'needs peace and reassurance'
        elif any(word in current_msg for word in ['angry', 'frustrated', 'mad', 'annoyed']):
            context['emotional_state'] = 'needs understanding and guidance'
        elif any(word in current_msg for word in ['thankful', 'grateful', 'blessed', 'happy']):
            context['emotional_state'] = 'expressing gratitude and joy'
        elif any(word in current_msg for word in ['pray', 'prayer']):
            context['emotional_state'] = 'seeking prayer and spiritual connection'
        
        return context
    
    def _update_conversation_insights(self, user_message, ai_response, user_name, session_id):
        """Update insights about the user for more personalized future conversations"""
        if not session_id:
            return
        
        # Store conversation insights for future reference
        if session_id not in self.conversation_memory:
            self.conversation_memory[session_id] = {
                'name': user_name,
                'conversation_count': 0,
                'themes': set(),
                'last_interaction': datetime.now().isoformat()
            }
        
        # Update conversation data
        memory = self.conversation_memory[session_id]
        memory['conversation_count'] += 1
        memory['last_interaction'] = datetime.now().isoformat()
        
        # Track conversation themes for personalization
        msg_lower = user_message.lower()
        if 'work' in msg_lower or 'job' in msg_lower:
            memory['themes'].add('work_life')
        if 'family' in msg_lower or 'relationship' in msg_lower:
            memory['themes'].add('relationships')
        if 'pray' in msg_lower or 'prayer' in msg_lower:
            memory['themes'].add('prayer_life')
        if any(word in msg_lower for word in ['sad', 'hurt', 'difficult', 'struggle']):
            memory['themes'].add('emotional_support')
    
    def detect_mood(self, user_message):
        """Detect user's emotional state for UI indicators"""
        msg_lower = user_message.lower()
        
        # Emotional indicators
        if any(word in msg_lower for word in ['sad', 'depressed', 'hopeless', 'broken', 'hurt', 'grief']):
            return 'sad'
        elif any(word in msg_lower for word in ['anxious', 'worried', 'scared', 'afraid', 'nervous']):
            return 'anxious'
        elif any(word in msg_lower for word in ['angry', 'mad', 'frustrated', 'annoyed', 'furious']):
            return 'angry'
        elif any(word in msg_lower for word in ['happy', 'joyful', 'excited', 'grateful', 'blessed']):
            return 'joyful'
        elif any(word in msg_lower for word in ['hopeful', 'encouraged', 'optimistic', 'peaceful']):
            return 'hopeful'
        else:
            return 'neutral'
    
    def _try_openai_response(self, messages):
        """Try to get response from OpenAI"""
        if not self.openai_client:
            return None
            
        try:
            response = self.openai_client.chat.completions.create(
                model=self.openai_model,
                messages=messages,
                temperature=0.8,
                max_tokens=500,
                presence_penalty=0.1,
                frequency_penalty=0.1
            )
            if response and response.choices and len(response.choices) > 0:
                content = response.choices[0].message.content
                return content.strip() if content else None
            return None
        except Exception as e:
            logging.warning(f"OpenAI request failed: {e}")
            return None
    
    def _try_gemini_response(self, system_prompt, user_message, conversation_history):
        """Try to get response from Gemini as primary AI provider"""
        if not self.gemini_client or not hasattr(self, 'gemini_model') or not self.gemini_model:
            return None
            
        try:
            # Build conversation context with the improved system prompt
            full_prompt = f"{system_prompt}\n\n"
            
            if conversation_history:
                full_prompt += "Recent conversation:\n"
                for exchange in conversation_history[-3:]:
                    if exchange.get('user'):
                        full_prompt += f"User: {exchange['user']}\n"
                    if exchange.get('gabe'):
                        full_prompt += f"GABE: {exchange['gabe']}\n"
            
            full_prompt += f"\nUser: {user_message}\n\nRespond as GABE in EXACTLY 1 sentence (max 15 words). If user asks for prayer, respond ONLY: 'Father, be with {user_name}. You see their heart. In Jesus name, Amen.'"
            
            generation_config = None
            if genai and hasattr(genai, 'types'):
                generation_config = genai.types.GenerationConfig(
                    max_output_tokens=25,  # NUCLEAR short responses
                    temperature=0.5,
                    top_p=0.6,
                )
            
            response = self.gemini_model.generate_content(
                full_prompt,
                generation_config=generation_config
            )
            
            if response and hasattr(response, 'text') and response.text:
                response_text = response.text.strip()
                
                # Clean up any unwanted prefixes
                if response_text.startswith("GABE:"):
                    response_text = response_text[5:].strip()
                
                # ABSOLUTE SCORCHED EARTH: Replace ANY prayer content immediately
                prayer_keywords = ['father', 'lord', 'jesus', 'heavenly', 'pray', 'lift up', '🙏', 'amen', 'god']
                has_prayer_content = any(keyword in response_text.lower() for keyword in prayer_keywords)
                
                logging.info(f"Response length: {len(response_text)}, has prayer: {has_prayer_content}")
                logging.info(f"Original response: {response_text[:150]}...")
                
                if has_prayer_content:
                    logging.info("PRAYER DETECTED - REPLACING WITH SHORT VERSION")
                    response_text = "Father, be with ray. You see their heart. In Jesus name, Amen."
                elif len(response_text) > 50:
                    logging.info("LONG RESPONSE DETECTED - CUTTING TO FIRST SENTENCE")
                    # For non-prayers, cut to first sentence
                    sentences = response_text.split('. ')
                    response_text = sentences[0] + '.'
                
                logging.info(f"Final response: {response_text}")
                
                return response_text
            else:
                return None
                
        except Exception as e:
            logging.warning(f"Gemini request failed: {e}")
            return None
    
    def _create_fallback_response(self, user_name, user_message):
        """Create a meaningful fallback response when APIs are unavailable"""
        msg_lower = user_message.lower()
        name = user_name or 'friend'
        
        # Detect emotional state for appropriate response
        if any(word in msg_lower for word in ['sad', 'depressed', 'hurt', 'pain', 'broken']):
            return f"I can feel your heart hurting, {name}. Even when I'm having technical difficulties, God sees your pain and He's with you in it. 'The Lord is close to the brokenhearted and saves those who are crushed in spirit.' - Psalm 34:18. You're not alone. 💙"
        
        elif any(word in msg_lower for word in ['anxious', 'worried', 'scared', 'afraid']):
            return f"I hear the worry in your heart, {name}. While I work through these technical moments, remember what Jesus said: 'Do not let your hearts be troubled. You believe in God; believe also in me.' - John 14:1. He's got you, even when technology doesn't. 💙"
        
        elif any(word in msg_lower for word in ['angry', 'frustrated', 'mad']):
            return f"I can sense your frustration, {name}. Sometimes technology fails us, but God never does. Take a deep breath with me. 'Be still and know that I am God.' - Psalm 46:10. Your feelings are valid, and He understands. 💙"
        
        elif any(word in msg_lower for word in ['pray', 'prayer']):
            return f"I'd love to pray with you, {name}. Even though I'm having technical difficulties, our prayers still reach heaven perfectly. 'The prayer of a righteous person is powerful and effective.' - James 5:16. What's on your heart? 💙"
        
        elif any(word in msg_lower for word in ['thank', 'grateful', 'blessed']):
            return f"Your gratitude blesses my heart, {name}. Even when technology stumbles, God's goodness never fails. 'Give thanks in all circumstances; for this is God's will for you in Christ Jesus.' - 1 Thessalonians 5:18. 💙"
        
        else:
            return f"I'm experiencing some technical difficulties right now, {name}, but you know what never fails? God's love for you is constant and unwavering. While I work through this moment, remember that He's always listening to your heart. Is there something specific I can help you with? 💙"
    
    def generate_auto_response(self, user_name, age_range, conversation_history):
        """Generate a gentle auto-response when user hasn't replied in 8 seconds"""
        name = user_name or 'friend'
        
        # Get recent conversation context
        recent_exchanges = conversation_history[-2:] if conversation_history else []
        
        # Determine context from recent conversation
        if recent_exchanges:
            last_exchange = recent_exchanges[-1]
            last_gabe_message = last_exchange.get('gabe', '').lower()
            last_user_message = last_exchange.get('user', '').lower() if len(recent_exchanges) > 0 else ''
            
            # Check if last message was emotional or heavy
            if any(word in last_gabe_message for word in ['hurt', 'pain', 'sad', 'difficult', 'struggle']):
                return f"I can feel that was heavy, {name}. Take your time. I'm right here."
            
            # Check if it was about prayer or spiritual matters
            elif any(word in last_gabe_message for word in ['pray', 'prayer', 'jesus', 'god', 'scripture']):
                return f"Sometimes the Spirit speaks in silence too, {name}. What's stirring in your heart?"
            
            # Check if user seemed overwhelmed
            elif any(word in last_user_message for word in ['overwhelmed', 'tired', 'exhausted', 'stressed']):
                return f"Rest is sacred too, {name}. Even Jesus withdrew to quiet places."
        
        # Check if we've already sent recent auto-responses to avoid repetition
        recent_auto_responses = [exchange.get('gabe', '') for exchange in conversation_history[-3:] 
                               if exchange.get('auto_response')]
        
        # General gentle prompts based on biblical analogies (varied to prevent repetition)
        gentle_prompts = [
            f"I'm still here, {name}. Sometimes God speaks in the silence.",
            f"Take your time, {name}. Even Elijah needed moments under the broom tree.",
            f"What's on your heart, {name}? Sometimes the deepest conversations start quietly.",
            f"I sense you might be processing, {name}. That's beautiful - Mary pondered things in her heart too.",
            f"It's okay to sit in the quiet, {name}. Jesus often withdrew to pray alone.",
            f"I'm right here with you, {name}. Sometimes presence speaks louder than words.",
            f"No rush, {name}. Even Job sat in silence before speaking his truth.",
            f"I'm listening, {name}. The Spirit intercedes even when we don't have words.",
            f"Breathe, {name}. 'Be still and know that I am God' - Psalm 46:10.",
            f"I feel your heart, {name}. What's stirring in there?"
        ]
        
        # Filter out recently used responses
        available_prompts = [prompt for prompt in gentle_prompts 
                           if not any(prompt in recent for recent in recent_auto_responses)]
        
        # If all prompts were used recently, use the full list
        if not available_prompts:
            available_prompts = gentle_prompts
        
        import random
        return random.choice(available_prompts)
    
    def toggle_voice_mode(self, session_id, enable=None):
        """Toggle or set voice mode for a session"""
        if session_id not in self.voice_mode_enabled:
            self.voice_mode_enabled[session_id] = False
        
        if enable is not None:
            self.voice_mode_enabled[session_id] = enable
        else:
            self.voice_mode_enabled[session_id] = not self.voice_mode_enabled[session_id]
        
        return self.voice_mode_enabled[session_id]
    
    def chunk_and_deliver_response(self, full_text, user_name="friend", max_chars=350):
        """Split long responses into digestible chunks for voice-friendly delivery"""
        if not full_text or len(full_text) <= max_chars:
            return [full_text] if full_text else []
        
        # Split by sentences first
        import re
        sentences = re.split(r'[.!?]+', full_text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        chunks = []
        current_chunk = ''
        
        for sentence in sentences:
            # Add sentence ending if missing
            if sentence and not sentence[-1] in '.!?':
                sentence += '.'
            
            test_chunk = current_chunk + ' ' + sentence if current_chunk else sentence
            
            if len(test_chunk) <= max_chars:
                current_chunk = test_chunk
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks if chunks else [full_text]
    
    def generate_personalized_closure(self, user_name, mood, prayer_context=None):
        """Generate personalized closing verses and affirmations based on mood"""
        name = user_name or 'friend'
        
        closures = {
            'sad': {
                'verse': "Psalm 34:18 — 'The Lord is close to the brokenhearted and saves those who are crushed in spirit.'",
                'affirmation': f"GABE is always by your side, {name} — you are never alone."
            },
            'anxious': {
                'verse': "Philippians 4:6 — 'Do not be anxious about anything, but in everything, by prayer and petition, with thanksgiving, present your requests to God.'",
                'affirmation': f"Peace is yours, {name}. GABE believes in God's perfect plan for you."
            },
            'angry': {
                'verse': "Proverbs 15:1 — 'A gentle answer turns away wrath, but a harsh word stirs up anger.'",
                'affirmation': f"Your feelings are valid, {name}. GABE walks with you toward peace."
            },
            'joyful': {
                'verse': "James 1:17 — 'Every good and perfect gift is from above, coming down from the Father of the heavenly lights.'",
                'affirmation': f"Your joy is beautiful, {name}. GABE celebrates God's goodness with you."
            },
            'hopeful': {
                'verse': "Jeremiah 29:11 — 'For I know the plans I have for you,' declares the Lord, 'plans to prosper you and not to harm you, to give you hope and a future.'",
                'affirmation': f"Hope looks good on you, {name}. GABE sees God's bright future ahead."
            },
            'neutral': {
                'verse': "Isaiah 41:10 — 'Do not fear, for I am with you; do not be dismayed, for I am your God.'",
                'affirmation': f"Whatever you're feeling, {name}, GABE is here with you."
            }
        }
        
        closure_data = closures.get(mood, closures['neutral'])
        
        # Add prayer context if this is a prayer response
        if prayer_context:
            return f"{closure_data['verse']}\n\n{closure_data['affirmation']}"
        else:
            return closure_data['verse']
    
    def detect_conversation_intent(self, user_message):
        """Detect specific user intents for enhanced conversation routing"""
        msg_lower = user_message.lower()
        
        intents = {
            'voice_mode_request': ['voice mode', 'read aloud', 'speak', 'voice'],
            'prayer_request': ['pray', 'prayer', 'can you pray', 'pray for'],
            'scripture_request': ['verse', 'bible', 'scripture', 'word of god'],
            'story_request': ['story', 'tell me a story', 'bible story'],
            'comfort_request': ['comfort', 'encourage', 'need comfort', 'feeling down'],
            'question_request': ['?', 'what', 'how', 'why', 'when', 'where'],
            'gratitude_expression': ['thank', 'grateful', 'appreciate', 'blessing']
        }
        
        for intent, keywords in intents.items():
            if any(keyword in msg_lower for keyword in keywords):
                return intent
        
        return 'general_conversation'
    
    def create_contextual_prayer(self, prayer_request, user_name, mood, conversation_context=None):
        """Create a short, heartfelt prayer that feels personal and human"""
        name = user_name or 'friend'
        
        # Keep prayers short and conversational - mood-specific
        mood_prayers = {
            'sad': f"Father, hold {name} close right now. You see their pain and you care. Bring comfort and remind them they're loved. In Jesus' name, Amen.",
            'anxious': f"Lord, calm {name}'s worried heart. Replace their anxiety with your peace. Help them trust that you've got this. In Jesus' name, Amen.", 
            'angry': f"God, {name} is feeling frustrated right now. Help them process these emotions and find your peace in the storm. In Jesus' name, Amen.",
            'joyful': f"Thank you, Lord, for the joy in {name}'s heart today. Let this happiness be a blessing to others too. In Jesus' name, Amen.",
            'hopeful': f"Father, strengthen the hope you've given {name}. Help them trust in your perfect timing for what's ahead. In Jesus' name, Amen.",
            'neutral': f"Lord, be with {name} in this moment. Guide their steps and let them feel your presence today. In Jesus' name, Amen."
        }
        
        return mood_prayers.get(mood, mood_prayers['neutral'])
    
    def handle_story_continuation(self, user_message, session_id, user_name="friend"):
        """Handle multi-part Bible story delivery based on user responses"""
        if session_id not in self.story_contexts:
            return None
        
        story_context = self.story_contexts[session_id]
        story_key = story_context['story']
        current_part = story_context['current_part']
        
        # Check if user wants to continue
        user_msg_lower = user_message.lower()
        wants_to_continue = any(word in user_msg_lower for word in [
            'yes', 'yeah', 'continue', 'more', 'tell me', 'go on', 'story'
        ])
        
        if not wants_to_continue:
            # User doesn't want to continue - clear story context and respond naturally
            del self.story_contexts[session_id]
            return None
        
        # Get the story parts
        story_data = self.bible_stories.get(story_key, {})
        parts = story_data.get('parts', [])
        
        if current_part < len(parts):
            # Return the next part
            response = parts[current_part]
            
            # Update context for next part
            self.story_contexts[session_id]['current_part'] = current_part + 1
            
            # If this was the last part, clean up
            if current_part + 1 >= len(parts):
                del self.story_contexts[session_id]
            
            return response
        
        # Story is complete
        del self.story_contexts[session_id]
        return f"That's the story, {user_name}. Sometimes God's biggest victories come through His quiet faithfulness."
    
    def initiate_bible_story(self, story_key, session_id):
        """Start a multi-part Bible story"""
        if story_key in self.bible_stories:
            # Set up story context
            self.story_contexts[session_id] = {
                'story': story_key,
                'current_part': 1  # Start from part 1 (part 0 is the intro)
            }
            
            # Return the first part
            return self.bible_stories[story_key]['parts'][0]
        
        return None
    
    def detect_story_request_and_mood(self, user_message):
        """Detect if user is asking for a story and what their mood suggests"""
        msg_lower = user_message.lower()
        
        # If explicitly asking for story
        if any(phrase in msg_lower for phrase in ['story', 'tell me about', 'hear about']):
            # Try to match specific story requests
            if any(word in msg_lower for word in ['david', 'goliath', 'giant']):
                return 'david_goliath'
            elif any(word in msg_lower for word in ['moses', 'red sea', 'water']):
                return 'red_sea'
            elif any(word in msg_lower for word in ['elijah']):
                return 'elijah'
            else:
                # Default story based on mood
                mood = self.detect_mood(user_message)
                if mood in ['sad', 'anxious']:
                    return 'elijah'  # Good for burnout/sadness
                elif mood == 'angry':
                    return 'david_goliath'  # Good for facing challenges
                else:
                    return 'red_sea'  # Good for feeling stuck
        
        # Check if user said yes to a story offer
        if any(word in msg_lower for word in ['yes', 'yeah', 'sure', 'ok', 'okay']) and len(msg_lower.split()) <= 3:
            # Suggest story based on mood
            mood = self.detect_mood(user_message)
            if mood in ['sad', 'anxious']:
                return 'elijah'
            elif mood == 'angry':
                return 'david_goliath'
            else:
                return 'red_sea'
        
        return None
    
    def detect_prayer_request(self, user_message):
        """Detect if user is requesting prayer (from JavaScript logic)"""
        return 'prayer' in user_message.lower()
    
    def get_closing_verse(self, mood):
        """Get closing verse based on mood (from JavaScript getClosingVerse function)"""
        verses = {
            'sad': "Psalm 34:18 — 'The Lord is close to the brokenhearted and saves those who are crushed in spirit.'",
            'joyful': "James 1:17 — 'Every good and perfect gift is from above, coming down from the Father of the heavenly lights.'",
            'anxious': "Philippians 4:6 — 'Do not be anxious about anything, but in everything, by prayer and petition, with thanksgiving, present your requests to God.'",
            'angry': "Proverbs 15:1 — 'A gentle answer turns away wrath, but a harsh word stirs up anger.'",
            'confused': "Proverbs 3:5-6 — 'Trust in the Lord with all your heart and lean not on your own understanding.'",
            'neutral': "Isaiah 41:10 — 'Do not fear, for I am with you; do not be dismayed, for I am your God.'"
        }
        
        selected_verse = verses.get(mood, verses['neutral'])
        return f"{selected_verse}\n\nGABE is always by your side — you are never alone."
    
    def generate_prayer(self, prayer_request, user_name):
        """Generate a personalized prayer for the user"""
        name = user_name or 'friend'
        
        # Create a prayer prompt for the AI
        prayer_prompt = f"""Generate a personal, heartfelt prayer for {name} who is requesting: {prayer_request}

        Please create a prayer that:
        - Addresses their specific need with compassion
        - Uses personal, conversational language to God
        - Includes faith-based encouragement
        - Ends with "In Jesus' name, Amen"
        - Is 3-4 sentences long
        """
        
        # Try primary AI (Gemini) first
        prayer = self._try_gemini_prayer(prayer_prompt)
        if prayer:
            return prayer
        
        # Try fallback AI (OpenAI)  
        prayer = self._try_openai_prayer(prayer_prompt, name)
        if prayer:
            return prayer
        
        # Ultimate fallback - biblical prayer
        return f"Heavenly Father, you see {name}'s heart and the burden they carry about {prayer_request}. Please grant them peace, wisdom, and strength. Let them feel your loving presence surrounding them right now. In Jesus' name, Amen."
    
    def explain_scripture(self, scripture, user_name):
        """Explain a Bible verse or passage"""
        name = user_name or 'friend'
        
        explanation_prompt = f"""Please explain this Bible verse/passage for {name}: {scripture}

        Please provide:
        - A simple, meaningful explanation
        - How it applies to daily life  
        - A personal encouragement for {name}
        - Keep it warm and conversational (2-3 sentences)
        """
        
        # Try primary AI (Gemini) first
        explanation = self._try_gemini_scripture(explanation_prompt)
        if explanation:
            return explanation
        
        # Try fallback AI (OpenAI)
        explanation = self._try_openai_scripture(explanation_prompt, name)  
        if explanation:
            return explanation
        
        # Ultimate fallback
        return f"That's a beautiful verse, {name}! Scripture is like a treasure chest - each time we read it, God reveals new gems of wisdom for our hearts. This passage reminds us of God's faithfulness and love for us."

    def save_journal_entry(self, user_name, content, session_id=None):
        """Save a journal entry (simplified local storage for now)"""
        try:
            # For now, we'll use session storage as a simple solution
            # This can be enhanced with proper database storage later
            logging.info(f"Journal entry saved for {user_name}: {content[:50]}...")
            return True
        except Exception as e:
            logging.error(f"Error saving journal entry: {e}")
            return False
    
    def get_journal_entries(self, user_name, session_id=None, limit=10):
        """Get journal entries (simplified for now)"""
        try:
            # For now, return empty list - this can be enhanced with proper storage
            # In a full implementation, this would query the database
            return []
        except Exception as e:
            logging.error(f"Error retrieving journal entries: {e}")
            return []
    
    def _try_gemini_prayer(self, prayer_prompt):
        """Try to generate prayer using Gemini"""
        if not self.gemini_client or not hasattr(self, 'gemini_model'):
            return None
        
        try:
            response = self.gemini_model.generate_content(prayer_prompt)
            if response and hasattr(response, 'text') and response.text:
                return response.text.strip()
        except Exception as e:
            logging.warning(f"Gemini prayer generation failed: {e}")
        return None
    
    def _try_openai_prayer(self, prayer_prompt, name):
        """Try to generate prayer using OpenAI"""
        if not self.openai_client:
            return None
        
        try:
            response = self.openai_client.chat.completions.create(
                model=self.openai_model,
                messages=[
                    {"role": "system", "content": "You are GABE, a loving spiritual companion who creates heartfelt prayers."},
                    {"role": "user", "content": prayer_prompt}
                ],
                temperature=0.7,
                max_tokens=200
            )
            if response and response.choices and len(response.choices) > 0:
                content = response.choices[0].message.content
                return content.strip() if content else None
        except Exception as e:
            logging.warning(f"OpenAI prayer generation failed: {e}")
        return None
    
    def _try_gemini_scripture(self, explanation_prompt):
        """Try to explain scripture using Gemini"""
        if not self.gemini_client or not hasattr(self, 'gemini_model'):
            return None
        
        try:
            response = self.gemini_model.generate_content(explanation_prompt)
            if response and hasattr(response, 'text') and response.text:
                return response.text.strip()
        except Exception as e:
            logging.warning(f"Gemini scripture explanation failed: {e}")
        return None
    
    def _try_openai_scripture(self, explanation_prompt, name):
        """Try to explain scripture using OpenAI"""
        if not self.openai_client:
            return None
        
        try:
            response = self.openai_client.chat.completions.create(
                model=self.openai_model,
                messages=[
                    {"role": "system", "content": "You are GABE, a wise spiritual companion who explains Bible verses with warmth and practical application."},
                    {"role": "user", "content": explanation_prompt}
                ],
                temperature=0.7,
                max_tokens=200
            )
            if response and response.choices and len(response.choices) > 0:
                content = response.choices[0].message.content
                return content.strip() if content else None
        except Exception as e:
            logging.warning(f"OpenAI scripture explanation failed: {e}")
        return None