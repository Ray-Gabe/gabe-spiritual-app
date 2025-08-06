"""
GABE Faith-in-Action Gamified Framework
Transforms spiritual growth into engaging, trackable experiences
"""
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import random

# Global session storage for user data
SESSION_STORAGE = {}

class GamifiedSpiritualFeatures:
    def __init__(self):
        """Initialize the gamified spiritual features system"""
        self.logger = logging.getLogger(__name__)
        
        # XP and Level System
        self.level_thresholds = {
            'Seed': 0,
            'Shepherd': 10,
            'Disciple': 25,
            'Warrior': 50,
            'Servant Leader': 100
        }
        
        # Badge definitions
        self.badge_definitions = {
            'Faith Seed': {'description': 'Started your spiritual journey', 'requirement': 'first_action'},
            'Devotion Keeper': {'description': '3-day devotion streak', 'requirement': 'devotion_streak_3'},
            'Prayer Warrior': {'description': '5 prayer challenges completed', 'requirement': 'prayer_count_5'},
            'Verse Sage': {'description': 'Mastered 10 verses', 'requirement': 'verse_mastery_10'},
            'Peacemaker': {'description': 'Completed a forgiveness prayer challenge', 'requirement': 'forgiveness_prayer'},
            'Shepherd': {'description': 'Reached Shepherd level', 'requirement': 'level_shepherd'},
            'Scripture Explorer': {'description': 'Completed 5 adventure stops', 'requirement': 'adventure_stops_5'},
            'Emotional Resilience': {'description': 'Completed mood missions for 3 different emotions', 'requirement': 'mood_variety_3'}
        }
        
        # Morning & Evening Devotions
        self.devotions = {
            'morning': {
                'title': '🌅 MORNING DEVOTION: "Start with Stillness"',
                'greeting': 'Good morning, {name}. Time to pray and start your day with God.',
                'verse_reference': 'Psalm 46:10',
                'verse_text': 'Be still, and know that I am God.',
                'word': 'Before the day demands your attention, God invites you to stillness — not silence, but surrender. In the quiet, He strengthens you. You don\'t need to rush — you need to rest in Him first.',
                'application': 'Take 3 deep breaths and whisper, "God, I trust You today." That moment of peace can shape your entire day.',
                'prayer': 'Heavenly Father, Thank You for the gift of today. As I step into the hours ahead, I choose stillness before You. Quiet my heart from anxiety and noise. Help me walk with peace, speak with kindness, and act with purpose. Let my choices reflect Your wisdom and my heart reflect Your love. Be with me in every moment, and lead me where You want me to go. In Jesus\' name, Amen.',
                'closing': '📖 GABE is always by your side — you are never alone.'
            },
            'evening': {
                'title': '🌙 EVENING DEVOTION: "Lay It Down"',
                'greeting': 'Good evening, {name}. You\'ve made it through the day. Let\'s pause, reflect, and pray together.',
                'verse_reference': '1 Peter 5:7',
                'verse_text': 'Cast all your anxiety on Him because He cares for you.',
                'word': 'You weren\'t meant to carry it all. God sees the pressure, the thoughts, the unspoken worries — and He\'s asking you to hand them over. Lay it down tonight. Rest in Him, not just sleep.',
                'application': 'Think of one thing that\'s weighing on your heart. Whisper it to God. Then say, "I release it to You." That\'s how peace begins.',
                'prayer': 'Lord, Thank You for walking with me today — through the joys, the stress, the quiet moments, and the mess. As night falls, I place my thoughts, my worries, and my plans in Your hands. Refresh my body, renew my mind, and fill my heart with peace. Watch over me and those I love. In Jesus\' name, Amen.',
                'closing': '💬 GABE is always by your side — you are never alone.'
            }
        }
        
        # Prayer challenges bank
        self.prayer_challenges = [
            'Pray for someone who has hurt you and ask God to heal their heart',
            'Write a prayer of gratitude for three specific things from this week',
            'Pray for a world leader or someone in authority',
            'Ask God to show you how to serve someone in need today',
            'Pray for wisdom in a decision you\'re facing',
            'Thank God for His faithfulness in a difficult season of your life',
            'Pray for peace in a conflict situation you know about',
            'Ask God to help you forgive yourself for something you regret'
        ]
        
        # Interactive Bible Studies
        self.bible_studies = {
            'trusting_god': {
                'id': 'trusting_god',
                'title': 'Trusting God in Difficult Times',
                'description': 'Learn to trust God\'s goodness when life feels uncertain',
                'sessions': 3,
                'duration': '10-15 min each',
                'xp_reward': 5,
                'sessions_data': [
                    {
                        'session_number': 1,
                        'title': 'God\'s Faithfulness in the Past',
                        'scripture_reference': 'Psalm 77:11-12',
                        'scripture_text': 'I will remember the deeds of the Lord; yes, I will remember your miracles of long ago. I will consider all your works and meditate on all your mighty deeds.',
                        'questions': [
                            'When have you seen God\'s faithfulness in your life before?',
                            'How can remembering God\'s past goodness help you trust Him today?',
                            'What "mighty deeds" of God do you want to remember more often?'
                        ],
                        'xp_reward': 4
                    },
                    {
                        'session_number': 2,
                        'title': 'Trusting God\'s Character',
                        'scripture_reference': 'Romans 8:28',
                        'scripture_text': 'And we know that in all things God works for the good of those who love him, who have been called according to his purpose.',
                        'questions': [
                            'What does this verse teach you about God\'s character?',
                            'How might God be working for good in a difficult situation you\'re facing?',
                            'What helps you remember that God\'s purposes are always loving?'
                        ],
                        'xp_reward': 4
                    },
                    {
                        'session_number': 3,
                        'title': 'Casting Your Anxieties',
                        'scripture_reference': '1 Peter 5:7',
                        'scripture_text': 'Cast all your anxiety on him because he cares for you.',
                        'questions': [
                            'What anxieties do you need to cast on God today?',
                            'How does knowing God cares for you change your perspective on worry?',
                            'What practical steps can you take to "cast" your worries on God?'
                        ],
                        'xp_reward': 4
                    }
                ]
            },
            'love_in_action': {
                'id': 'love_in_action',
                'title': 'Love in Action: Serving Others',
                'description': 'Discover practical ways to show God\'s love to others',
                'sessions': 3,
                'duration': '12-18 min each',
                'xp_reward': 5,
                'sessions_data': [
                    {
                        'session_number': 1,
                        'title': 'The Greatest Commandment',
                        'scripture_reference': 'Matthew 22:37-39',
                        'scripture_text': 'Jesus replied: "Love the Lord your God with all your heart and with all your soul and with all your mind. This is the first and greatest commandment. And the second is like it: Love your neighbor as yourself."',
                        'questions': [
                            'What does it mean to love God with "all" your heart, soul, and mind?',
                            'Who is your "neighbor" that God is calling you to love?',
                            'How can loving God more deeply help you love others better?'
                        ],
                        'xp_reward': 4
                    },
                    {
                        'session_number': 2,
                        'title': 'Practical Love',
                        'scripture_reference': '1 John 3:18',
                        'scripture_text': 'Dear children, let us not love with words or speech but with actions and in truth.',
                        'questions': [
                            'What\'s the difference between loving with words vs. loving with actions?',
                            'What specific action could you take this week to show love to someone?',
                            'How does loving "in truth" guide the way we serve others?'
                        ],
                        'xp_reward': 4
                    },
                    {
                        'session_number': 3,
                        'title': 'Serving the Least',
                        'scripture_reference': 'Matthew 25:40',
                        'scripture_text': 'The King will reply, "Truly I tell you, whatever you did for one of the least of these brothers and sisters of mine, you did for me."',
                        'questions': [
                            'Who are "the least of these" in your community?',
                            'How does serving others connect us to Jesus?',
                            'What barriers prevent you from serving more, and how can you overcome them?'
                        ],
                        'xp_reward': 4
                    }
                ]
            },
            'identity_in_christ': {
                'id': 'identity_in_christ',
                'title': 'Your Identity in Christ',
                'description': 'Understand who you are as God\'s beloved child',
                'sessions': 4,
                'duration': '8-12 min each',
                'xp_reward': 6,
                'sessions_data': [
                    {
                        'session_number': 1,
                        'title': 'Chosen and Beloved',
                        'scripture_reference': 'Ephesians 1:4',
                        'scripture_text': 'For he chose us in him before the creation of the world to be holy and blameless in his sight. In love...',
                        'questions': [
                            'What does it mean that God chose you before creation?',
                            'How does being "chosen" change how you see yourself?',
                            'What does God\'s love for you look like in your daily life?'
                        ],
                        'xp_reward': 3
                    },
                    {
                        'session_number': 2,
                        'title': 'Children of God',
                        'scripture_reference': '1 John 3:1',
                        'scripture_text': 'See what great love the Father has lavished on us, that we should be called children of God! And that is what we are!',
                        'questions': [
                            'What does it mean to be called a "child of God"?',
                            'How has God "lavished" His love on you?',
                            'How should being God\'s child affect your daily decisions?'
                        ],
                        'xp_reward': 3
                    },
                    {
                        'session_number': 3,
                        'title': 'New Creation',
                        'scripture_reference': '2 Corinthians 5:17',
                        'scripture_text': 'Therefore, if anyone is in Christ, the new creation has come: The old has gone, the new is here!',
                        'questions': [
                            'What "old" things in your life has God made new?',
                            'How does being a "new creation" give you hope?',
                            'What areas of your life still need God\'s transforming work?'
                        ],
                        'xp_reward': 3
                    },
                    {
                        'session_number': 4,
                        'title': 'More Than Conquerors',
                        'scripture_reference': 'Romans 8:37',
                        'scripture_text': 'No, in all these things we are more than conquerors through him who loved us.',
                        'questions': [
                            'What challenges are you facing that God can help you conquer?',
                            'How does Christ\'s love make you "more than a conqueror"?',
                            'How can you encourage someone else with this truth this week?'
                        ],
                        'xp_reward': 3
                    }
                ]
            }
        }

        # Verse mastery collection
        self.verses_for_mastery = [
            {'reference': 'John 3:16', 'text': 'For God so loved the world that he gave his one and only Son, that whoever believes in him shall not perish but have eternal life.', 'theme': 'love'},
            {'reference': 'Romans 8:28', 'text': 'And we know that in all things God works for the good of those who love him, who have been called according to his purpose.', 'theme': 'hope'},
            {'reference': 'Philippians 4:6', 'text': 'Do not be anxious about anything, but in every situation, by prayer and petition, with thanksgiving, present your requests to God.', 'theme': 'anxiety'},
            {'reference': 'Psalm 34:18', 'text': 'The Lord is close to the brokenhearted and saves those who are crushed in spirit.', 'theme': 'sadness'},
            {'reference': 'James 1:17', 'text': 'Every good and perfect gift is from above, coming down from the Father of the heavenly lights.', 'theme': 'gratitude'}
        ]
        
        # Scripture adventure path
        self.scripture_adventure = [
            {'book': 'Genesis', 'theme': 'Beginnings', 'lesson': 'God creates and calls us into relationship'},
            {'book': 'Exodus', 'theme': 'Deliverance', 'lesson': 'God rescues His people from bondage'},
            {'book': 'Psalms', 'theme': 'Worship', 'lesson': 'Honest prayers and praise in all seasons'},
            {'book': 'Proverbs', 'theme': 'Wisdom', 'lesson': 'Living skillfully according to God\'s design'},
            {'book': 'Matthew', 'theme': 'The King', 'lesson': 'Jesus as the promised Messiah'},
            {'book': 'John', 'theme': 'Life', 'lesson': 'Jesus as the source of eternal life'},
            {'book': 'Acts', 'theme': 'Mission', 'lesson': 'The Holy Spirit empowers the church'},
            {'book': 'Romans', 'theme': 'Grace', 'lesson': 'Salvation through faith, not works'},
            {'book': 'Ephesians', 'theme': 'Unity', 'lesson': 'Our identity and purpose in Christ'}
        ]
        
        # Mood-based missions
        self.mood_missions = {
            'sad': {
                'challenge': 'Read Psalm 34:18 and write one thing you\'re grateful for today',
                'comfort': 'God is close to you in this sadness. You\'re not alone.',
                'badge': 'Comfort Seeker'
            },
            'anxious': {
                'challenge': 'Take 3 deep breaths and pray: "God, I trust You with my worries"',
                'comfort': 'God invites you to cast all your anxiety on Him because He cares for you.',
                'badge': 'Peace Finder'
            },
            'grateful': {
                'challenge': 'List 5 things you\'re thankful for and pray a prayer of praise',
                'comfort': 'Your grateful heart brings joy to God\'s heart.',
                'badge': 'Gratitude Keeper'
            },
            'angry': {
                'challenge': 'Pray for someone who has made you angry and ask for a soft heart',
                'comfort': 'God sees your anger and offers His peace to calm your heart.',
                'badge': 'Peacemaker'
            },
            'tired': {
                'challenge': 'Ask God for rest and strength, then take a few minutes of quiet time',
                'comfort': 'Come to Jesus, all who are weary, and He will give you rest.',
                'badge': 'Rest Seeker'
            }
        }
    
    def get_user_data(self, session_id: str) -> Dict:
        """Get user's gamification data from storage"""
        global SESSION_STORAGE
        
        # Try to get from Flask session first, then from global storage
        from flask import session
        flask_session_key = f'gamified_data_{session_id}'
        
        existing_data = None
        if flask_session_key in session:
            self.logger.info(f"Loading user data from Flask session for {session_id}")
            existing_data = session[flask_session_key].copy()
        elif session_id in SESSION_STORAGE:
            self.logger.info(f"Loading user data from global storage for {session_id}")
            existing_data = SESSION_STORAGE[session_id].copy()
        
        # Ensure bible_studies field exists
        if existing_data:
            if 'bible_studies' not in existing_data:
                existing_data['bible_studies'] = {}
            if 'studies_completed' not in existing_data:
                existing_data['studies_completed'] = 0
            # Save updated data back
            SESSION_STORAGE[session_id] = existing_data
            session[flask_session_key] = existing_data
            return existing_data
        else:
            # Initialize with default data for new users
            default_data = {
                'xp': 0,
                'level': 'Seed',
                'streak': {
                    'devotion': 0,
                    'prayer': 0,
                    'last_devotion': None,
                    'last_prayer': None
                },
                'badges': [],
                'completed_challenges': [],
                'scripture_adventure_position': 0,
                'verse_mastery_progress': [],
                'mood_missions_completed': [],
                'total_actions': 0,
                'bible_studies': {},  # {study_id: {'current_session': 1, 'completed_sessions': [], 'answers': {}}}
                'studies_completed': 0
            }
            
            self.logger.info(f"Created new user data for session {session_id}")
            # Save to both storages
            SESSION_STORAGE[session_id] = default_data.copy()
            session[flask_session_key] = default_data.copy()
            return default_data.copy()
    
    def save_user_data(self, session_id: str, data: Dict):
        """Save user's gamification data to storage"""
        global SESSION_STORAGE
        from flask import session
        
        # Save to both global storage and Flask session for persistence
        SESSION_STORAGE[session_id] = data.copy()
        flask_session_key = f'gamified_data_{session_id}'
        session[flask_session_key] = data.copy()
        
        self.logger.info(f"Saved gamification data for session {session_id}: XP={data.get('xp', 0)}, Level={data.get('level', 'Seed')}")
        return True
    
    def award_xp(self, user_data: Dict, amount: int = 1) -> Dict:
        """Award XP and check for level up"""
        user_data['xp'] += amount
        user_data['total_actions'] += 1
        
        # Check for level up
        old_level = user_data['level']
        for level, threshold in self.level_thresholds.items():
            if user_data['xp'] >= threshold:
                user_data['level'] = level
        
        # Award level badge if leveled up
        if user_data['level'] != old_level and user_data['level'] != 'Seed':
            badge_name = user_data['level']
            if badge_name not in user_data['badges']:
                user_data['badges'].append(badge_name)
        
        return user_data
    
    def check_and_award_badges(self, user_data: Dict) -> List[str]:
        """Check conditions and award new badges"""
        new_badges = []
        
        # Check each badge requirement
        if user_data['total_actions'] >= 1 and 'Faith Seed' not in user_data['badges']:
            user_data['badges'].append('Faith Seed')
            new_badges.append('Faith Seed')
        
        if user_data['streak']['devotion'] >= 3 and 'Devotion Keeper' not in user_data['badges']:
            user_data['badges'].append('Devotion Keeper')
            new_badges.append('Devotion Keeper')
        
        if len([c for c in user_data['completed_challenges'] if c.startswith('prayer')]) >= 5 and 'Prayer Warrior' not in user_data['badges']:
            user_data['badges'].append('Prayer Warrior')
            new_badges.append('Prayer Warrior')
        
        if len(user_data['verse_mastery_progress']) >= 10 and 'Verse Sage' not in user_data['badges']:
            user_data['badges'].append('Verse Sage')
            new_badges.append('Verse Sage')
        
        if user_data['scripture_adventure_position'] >= 5 and 'Scripture Explorer' not in user_data['badges']:
            user_data['badges'].append('Scripture Explorer')
            new_badges.append('Scripture Explorer')
        
        # Check for emotional resilience (3 different mood missions)
        unique_moods = set([m.split('_')[1] for m in user_data['mood_missions_completed'] if '_' in m])
        if len(unique_moods) >= 3 and 'Emotional Resilience' not in user_data['badges']:
            user_data['badges'].append('Emotional Resilience')
            new_badges.append('Emotional Resilience')
        
        return new_badges
    
    def get_daily_devotion(self, session_id: str) -> Dict:
        """Get morning or evening devotion based on time of day"""
        from flask import session as flask_session
        
        user_data = self.get_user_data(session_id)
        today = datetime.now().date().isoformat()
        current_hour = datetime.now().hour
        
        # Determine if morning (5 AM - 2 PM) or evening (2 PM - 5 AM next day)
        is_morning = 5 <= current_hour < 14
        devotion_type = 'morning' if is_morning else 'evening'
        
        # Get user's name from session if available
        user_name = flask_session.get('user_name', 'friend')
        
        # Check if already completed today
        streak_key = f'last_{devotion_type}_devotion'
        if user_data['streak'].get(streak_key) == today:
            return {
                'type': 'already_completed',
                'message': f'You\'ve already completed your {devotion_type} devotion today! Come back {"tonight" if is_morning else "tomorrow morning"} for the next one.',
                'streak': user_data['streak'].get(f'{devotion_type}_devotion', 0),
                'devotion_type': devotion_type
            }
        
        # Get the appropriate devotion and personalize it
        devotion = self.devotions[devotion_type].copy()
        devotion['greeting'] = devotion['greeting'].format(name=user_name)
        
        return {
            'type': 'new_devotion',
            'devotion': devotion,
            'devotion_type': devotion_type,
            'current_streak': user_data['streak'].get(f'{devotion_type}_devotion', 0)
        }
    
    def complete_devotion(self, session_id: str, reflection_answer: str = "") -> Dict:
        """Mark morning or evening devotion as complete and award XP"""
        user_data = self.get_user_data(session_id)
        today = datetime.now().date().isoformat()
        yesterday = (datetime.now().date() - timedelta(days=1)).isoformat()
        current_hour = datetime.now().hour
        
        # Determine if morning or evening devotion
        is_morning = 5 <= current_hour < 14
        devotion_type = 'morning' if is_morning else 'evening'
        
        # Update appropriate streak
        streak_key = f'{devotion_type}_devotion'
        last_key = f'last_{devotion_type}_devotion'
        
        # Initialize streak fields if they don't exist
        if streak_key not in user_data['streak']:
            user_data['streak'][streak_key] = 0
        if last_key not in user_data['streak']:
            user_data['streak'][last_key] = None
        
        # Update streak logic
        if user_data['streak'][last_key] == yesterday:
            user_data['streak'][streak_key] += 1
        else:
            user_data['streak'][streak_key] = 1
        
        user_data['streak'][last_key] = today
        
        # Also update the general devotion streak for backwards compatibility
        if user_data['streak']['last_devotion'] == yesterday:
            user_data['streak']['devotion'] += 1
        else:
            user_data['streak']['devotion'] = 1
        user_data['streak']['last_devotion'] = today
        
        # Award XP
        user_data = self.award_xp(user_data, 2)
        
        # Check for new badges
        new_badges = self.check_and_award_badges(user_data)
        
        # Save data
        self.save_user_data(session_id, user_data)
        
        return {
            'xp_earned': 2,
            'new_level': user_data['level'],
            'streak': user_data['streak']['devotion'],
            'new_badges': new_badges,
            'total_xp': user_data['xp']
        }
    
    def get_prayer_challenge(self, session_id: str) -> Dict:
        """Get today's prayer challenge"""
        user_data = self.get_user_data(session_id)
        today = datetime.now().date().isoformat()
        
        # Check if already completed today
        if user_data['streak']['last_prayer'] == today:
            return {
                'type': 'already_completed',
                'message': 'You\'ve already completed today\'s prayer challenge! Come back tomorrow.',
                'streak': user_data['streak']['prayer']
            }
        
        # Get today's challenge
        challenge_index = hash(today) % len(self.prayer_challenges)
        challenge = self.prayer_challenges[challenge_index]
        
        return {
            'type': 'new_challenge',
            'challenge': challenge,
            'current_streak': user_data['streak']['prayer']
        }
    
    def complete_prayer_challenge(self, session_id: str) -> Dict:
        """Mark prayer challenge as complete"""
        user_data = self.get_user_data(session_id)
        today = datetime.now().date().isoformat()
        yesterday = (datetime.now().date() - timedelta(days=1)).isoformat()
        
        # Update streak
        if user_data['streak']['last_prayer'] == yesterday:
            user_data['streak']['prayer'] += 1
        else:
            user_data['streak']['prayer'] = 1
        
        user_data['streak']['last_prayer'] = today
        user_data['completed_challenges'].append(f"prayer_{today}")
        
        # Award XP
        user_data = self.award_xp(user_data, 2)
        
        # Check for new badges
        new_badges = self.check_and_award_badges(user_data)
        
        self.save_user_data(session_id, user_data)
        
        return {
            'xp_earned': 2,
            'new_level': user_data['level'],
            'streak': user_data['streak']['prayer'],
            'new_badges': new_badges,
            'total_xp': user_data['xp']
        }
    
    def get_verse_mastery_quiz(self, session_id: str) -> Dict:
        """Get a verse mastery quiz question"""
        # Select random verse
        verse = random.choice(self.verses_for_mastery)
        
        # Create fill-in-the-blank or multiple choice
        quiz_type = random.choice(['fill_blank', 'multiple_choice'])
        
        if quiz_type == 'fill_blank':
            words = verse['text'].split()
            blank_index = random.randint(2, len(words) - 2)  # Avoid first/last words
            blank_word = words[blank_index]
            quiz_text = ' '.join(words[:blank_index] + ['_____'] + words[blank_index + 1:])
            
            return {
                'type': 'fill_blank',
                'reference': verse['reference'],
                'quiz_text': quiz_text,
                'correct_answer': blank_word.lower().strip('.,!?'),
                'theme': verse['theme']
            }
        
        else:  # multiple choice
            # Create options
            correct_ref = verse['reference']
            wrong_refs = [v['reference'] for v in self.verses_for_mastery if v['reference'] != correct_ref]
            options = [correct_ref] + random.sample(wrong_refs, 2)
            random.shuffle(options)
            
            return {
                'type': 'multiple_choice',
                'text': verse['text'],
                'question': 'Which verse is this?',
                'options': options,
                'correct_answer': correct_ref,
                'theme': verse['theme']
            }
    
    def complete_verse_mastery(self, session_id: str, correct: bool) -> Dict:
        """Handle verse mastery completion"""
        user_data = self.get_user_data(session_id)
        
        if correct:
            # Award XP and track progress
            user_data = self.award_xp(user_data, 1)
            user_data['verse_mastery_progress'].append(datetime.now().isoformat())
            
            # Check for new badges
            new_badges = self.check_and_award_badges(user_data)
            
            self.save_user_data(session_id, user_data)
            
            return {
                'correct': True,
                'xp_earned': 1,
                'new_badges': new_badges,
                'total_xp': user_data['xp'],
                'verses_mastered': len(user_data['verse_mastery_progress'])
            }
        else:
            return {
                'correct': False,
                'encouragement': 'Keep studying! God\'s Word is worth learning.',
                'total_xp': user_data['xp']
            }
    
    def get_scripture_adventure_next(self, session_id: str) -> Dict:
        """Get next scripture adventure stop"""
        user_data = self.get_user_data(session_id)
        position = user_data['scripture_adventure_position']
        
        if position >= len(self.scripture_adventure):
            return {
                'type': 'completed',
                'message': 'Congratulations! You\'ve completed the entire Scripture Adventure journey!'
            }
        
        current_stop = self.scripture_adventure[position]
        
        return {
            'type': 'new_stop',
            'stop': current_stop,
            'position': position + 1,
            'total_stops': len(self.scripture_adventure)
        }
    
    def complete_scripture_adventure_stop(self, session_id: str) -> Dict:
        """Complete current adventure stop"""
        user_data = self.get_user_data(session_id)
        user_data['scripture_adventure_position'] += 1
        
        # Award XP
        user_data = self.award_xp(user_data, 3)  # Higher XP for adventure progress
        
        # Check for new badges
        new_badges = self.check_and_award_badges(user_data)
        
        self.save_user_data(session_id, user_data)
        
        return {
            'xp_earned': 3,
            'new_level': user_data['level'],
            'new_badges': new_badges,
            'total_xp': user_data['xp'],
            'next_available': user_data['scripture_adventure_position'] < len(self.scripture_adventure)
        }
    
    def get_mood_mission(self, mood: str) -> Dict:
        """Get mood-specific mission"""
        if mood.lower() not in self.mood_missions:
            mood = 'anxious'  # Default fallback
        
        mission = self.mood_missions[mood.lower()]
        
        return {
            'mood': mood,
            'challenge': mission['challenge'],
            'comfort': mission['comfort'],
            'badge': mission['badge']
        }
    
    def complete_mood_mission(self, session_id: str, mood: str) -> Dict:
        """Complete mood mission"""
        user_data = self.get_user_data(session_id)
        mission_id = f"mood_{mood.lower()}_{datetime.now().date().isoformat()}"
        user_data['mood_missions_completed'].append(mission_id)
        
        # Award XP
        user_data = self.award_xp(user_data, 1)
        
        # Check for new badges
        new_badges = self.check_and_award_badges(user_data)
        
        self.save_user_data(session_id, user_data)
        
        return {
            'xp_earned': 1,
            'new_badges': new_badges,
            'total_xp': user_data['xp'],
            'comfort_message': f"You\'ve taken a step toward emotional and spiritual health. God sees your heart."
        }
    
    def get_user_progress(self, session_id: str) -> Dict:
        """Get complete user progress overview"""
        user_data = self.get_user_data(session_id)
        
        # Calculate next level progress
        current_level = user_data['level']
        level_names = list(self.level_thresholds.keys())
        current_index = level_names.index(current_level)
        
        if current_index < len(level_names) - 1:
            next_level = level_names[current_index + 1]
            next_threshold = self.level_thresholds[next_level]
            progress_to_next = user_data['xp'] - self.level_thresholds[current_level]
            needed_for_next = next_threshold - self.level_thresholds[current_level]
            progress_percentage = (progress_to_next / needed_for_next) * 100
        else:
            next_level = "Max Level Reached"
            progress_percentage = 100
        
        return {
            'level': user_data['level'],
            'xp': user_data['xp'],
            'next_level': next_level,
            'progress_percentage': min(progress_percentage, 100),
            'badges': user_data['badges'],
            'streaks': user_data['streak'],
            'adventure_progress': user_data['scripture_adventure_position'],
            'verses_mastered': len(user_data['verse_mastery_progress']),
            'total_actions': user_data['total_actions'],
            'studies_completed': user_data.get('studies_completed', 0)
        }
    
    def get_bible_studies(self, session_id: str) -> Dict:
        """Get available Bible studies or current study session"""
        user_data = self.get_user_data(session_id)
        
        # Check if user has an active study session
        for study_id, progress in user_data['bible_studies'].items():
            if progress['current_session'] <= len(self.bible_studies[study_id]['sessions_data']):
                # Return current session
                study = self.bible_studies[study_id]
                session_number = progress['current_session']
                session_data = study['sessions_data'][session_number - 1]
                
                return {
                    'type': 'study_session',
                    'session': {
                        'study_id': study_id,
                        'title': study['title'],
                        'session_number': session_number,
                        'scripture_reference': session_data['scripture_reference'],
                        'scripture_text': session_data['scripture_text'],
                        'questions': session_data['questions'],
                        'xp_reward': session_data['xp_reward']
                    }
                }
        
        # No active study, return available studies
        available_studies = []
        for study_id, study in self.bible_studies.items():
            available_studies.append({
                'id': study['id'],
                'title': study['title'],
                'description': study['description'],
                'sessions': study['sessions'],
                'duration': study['duration'],
                'xp_reward': study['xp_reward']
            })
        
        return {
            'type': 'study_list',
            'studies': available_studies
        }
    
    def start_bible_study(self, session_id: str, study_id: str) -> Dict:
        """Start a new Bible study"""
        user_data = self.get_user_data(session_id)
        
        if study_id not in self.bible_studies:
            return {'success': False, 'message': 'Study not found'}
        
        # Initialize study progress
        user_data['bible_studies'][study_id] = {
            'current_session': 1,
            'completed_sessions': [],
            'answers': {}
        }
        
        self.save_user_data(session_id, user_data)
        
        return {'success': True, 'message': 'Study started successfully'}
    
    def complete_bible_study_session(self, session_id: str, study_id: str, session_number: int, answers: List[str]) -> Dict:
        """Complete a Bible study session"""
        user_data = self.get_user_data(session_id)
        
        if study_id not in self.bible_studies:
            return {'success': False, 'message': 'Study not found'}
        
        if study_id not in user_data['bible_studies']:
            return {'success': False, 'message': 'Study not started'}
        
        study = self.bible_studies[study_id]
        session_data = study['sessions_data'][session_number - 1]
        
        # Save answers
        user_data['bible_studies'][study_id]['answers'][f'session_{session_number}'] = answers
        
        # Mark session as completed
        if session_number not in user_data['bible_studies'][study_id]['completed_sessions']:
            user_data['bible_studies'][study_id]['completed_sessions'].append(session_number)
        
        # Award XP
        user_data = self.award_xp(user_data, session_data['xp_reward'])
        
        # Check if study is complete
        total_sessions = len(study['sessions_data'])
        completed_sessions = len(user_data['bible_studies'][study_id]['completed_sessions'])
        
        if completed_sessions >= total_sessions:
            # Study completed
            user_data['studies_completed'] += 1
            # Move to next session (will show study list next time)
            user_data['bible_studies'][study_id]['current_session'] = total_sessions + 1
            study_complete = True
        else:
            # Move to next session
            user_data['bible_studies'][study_id]['current_session'] = session_number + 1
            study_complete = False
        
        # Check for new badges
        new_badges = self.check_and_award_badges(user_data)
        
        self.save_user_data(session_id, user_data)
        
        return {
            'success': True,
            'xp_earned': session_data['xp_reward'],
            'new_level': user_data['level'],
            'new_badges': new_badges,
            'total_xp': user_data['xp'],
            'study_complete': study_complete,
            'message': 'Great reflection! Your insights are valuable for spiritual growth.' if not study_complete else f'Congratulations! You\'ve completed the "{study["title"]}" study!'
        }