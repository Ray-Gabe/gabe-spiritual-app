"""
Enhanced Spiritual Features for GABE
Includes prayer journal, daily reminders, scripture recommendations, and spiritual growth tracking
"""

import datetime
import json
import random
from typing import Dict, List, Optional

class SpiritualFeatures:
    def __init__(self):
        self.scripture_database = self._load_scripture_database()
        self.growth_milestones = self._load_growth_milestones()
        
    def _load_scripture_database(self) -> Dict[str, List[Dict]]:
        """Load scripture verses organized by emotional needs"""
        return {
            "sad": [
                {
                    "verse": "The Lord is close to the brokenhearted and saves those who are crushed in spirit.",
                    "reference": "Psalm 34:18",
                    "theme": "God's comfort in sadness"
                },
                {
                    "verse": "He heals the brokenhearted and binds up their wounds.",
                    "reference": "Psalm 147:3",
                    "theme": "Divine healing"
                },
                {
                    "verse": "Weeping may stay for the night, but rejoicing comes in the morning.",
                    "reference": "Psalm 30:5",
                    "theme": "Hope after sorrow"
                },
                {
                    "verse": "Cast all your anxiety on him because he cares for you.",
                    "reference": "1 Peter 5:7",
                    "theme": "God's care"
                }
            ],
            "anxious": [
                {
                    "verse": "Do not be anxious about anything, but in every situation, by prayer and petition, with thanksgiving, present your requests to God.",
                    "reference": "Philippians 4:6",
                    "theme": "Peace through prayer"
                },
                {
                    "verse": "Therefore do not worry about tomorrow, for tomorrow will worry about itself. Each day has enough trouble of its own.",
                    "reference": "Matthew 6:34",
                    "theme": "Living in the present"
                },
                {
                    "verse": "When anxiety was great within me, your consolation brought me joy.",
                    "reference": "Psalm 94:19",
                    "theme": "God's consolation"
                },
                {
                    "verse": "Peace I leave with you; my peace I give you. I do not give to you as the world gives. Do not let your hearts be troubled and do not be afraid.",
                    "reference": "John 14:27",
                    "theme": "Divine peace"
                }
            ],
            "angry": [
                {
                    "verse": "In your anger do not sin: Do not let the sun go down while you are still angry.",
                    "reference": "Ephesians 4:26",
                    "theme": "Righteous anger"
                },
                {
                    "verse": "Everyone should be quick to listen, slow to speak and slow to become angry.",
                    "reference": "James 1:19",
                    "theme": "Wisdom in anger"
                },
                {
                    "verse": "A gentle answer turns away wrath, but a harsh word stirs up anger.",
                    "reference": "Proverbs 15:1",
                    "theme": "Gentle responses"
                },
                {
                    "verse": "Above all else, guard your heart, for everything you do flows from it.",
                    "reference": "Proverbs 4:23",
                    "theme": "Heart protection"
                }
            ],
            "hopeful": [
                {
                    "verse": "For I know the plans I have for you, declares the Lord, plans to prosper you and not to harm you, to give you hope and a future.",
                    "reference": "Jeremiah 29:11",
                    "theme": "God's good plans"
                },
                {
                    "verse": "May the God of hope fill you with all joy and peace as you trust in him, so that you may overflow with hope by the power of the Holy Spirit.",
                    "reference": "Romans 15:13",
                    "theme": "Overflowing hope"
                },
                {
                    "verse": "Those who hope in the Lord will renew their strength. They will soar on wings like eagles.",
                    "reference": "Isaiah 40:31",
                    "theme": "Renewed strength"
                }
            ],
            "grateful": [
                {
                    "verse": "Give thanks in all circumstances; for this is God's will for you in Christ Jesus.",
                    "reference": "1 Thessalonians 5:18",
                    "theme": "Gratitude in all things"
                },
                {
                    "verse": "Every good and perfect gift is from above, coming down from the Father of the heavenly lights.",
                    "reference": "James 1:17",
                    "theme": "God as giver"
                },
                {
                    "verse": "Enter his gates with thanksgiving and his courts with praise; give thanks to him and praise his name.",
                    "reference": "Psalm 100:4",
                    "theme": "Thankful worship"
                }
            ]
        }
    
    def _load_growth_milestones(self) -> List[Dict]:
        """Define spiritual growth milestones to track"""
        return [
            {
                "milestone": "First Prayer Request",
                "description": "Shared your first prayer request with GABE",
                "points": 10
            },
            {
                "milestone": "Daily Conversations",
                "description": "Talked with GABE for 7 consecutive days",
                "points": 25
            },
            {
                "milestone": "Scripture Explorer",
                "description": "Asked for scripture recommendations 5 times",
                "points": 15
            },
            {
                "milestone": "Emotional Journey",
                "description": "Shared different emotions (sad, anxious, hopeful) in conversations",
                "points": 20
            },
            {
                "milestone": "Prayer Warrior",
                "description": "Completed 10 prayer sessions with GABE",
                "points": 30
            },
            {
                "milestone": "Faithful Friend",
                "description": "Maintained regular conversations for 30 days",
                "points": 50
            }
        ]
    
    def get_scripture_recommendation(self, mood: str, context: str = "") -> Dict:
        """Get appropriate scripture based on user's emotional state"""
        mood_scriptures = self.scripture_database.get(mood, self.scripture_database["hopeful"])
        
        # Select random scripture from the mood category
        selected_scripture = random.choice(mood_scriptures)
        
        return {
            "verse": selected_scripture["verse"],
            "reference": selected_scripture["reference"],
            "theme": selected_scripture["theme"],
            "personal_note": self._generate_personal_note(mood, selected_scripture["theme"])
        }
    
    def _generate_personal_note(self, mood: str, theme: str) -> str:
        """Generate a personal note to accompany the scripture"""
        notes = {
            "sad": [
                f"This verse reminds us that God sees your tears and is close to you right now.",
                f"Remember, {theme.lower()} is one of God's greatest gifts to His children.",
                f"Your sadness is valid, and God wants to walk through this with you."
            ],
            "anxious": [
                f"When worry fills your mind, this scripture offers {theme.lower()} as God's promise.",
                f"Your anxiety doesn't surprise God - He has peace ready for you.",
                f"Take a deep breath and remember that {theme.lower()} is available to you right now."
            ],
            "angry": [
                f"Your feelings are valid, and this verse guides us toward {theme.lower()}.",
                f"God understands your anger and offers wisdom for {theme.lower()}.",
                f"In moments of anger, {theme.lower()} can be our pathway to peace."
            ],
            "hopeful": [
                f"Your hope is beautiful, and this verse affirms {theme.lower()} in your life.",
                f"God delights in your hopeful heart and has {theme.lower()} in store.",
                f"Keep holding onto hope - {theme.lower()} is part of God's character."
            ],
            "grateful": [
                f"Your gratitude reflects God's heart, and this verse celebrates {theme.lower()}.",
                f"Thankfulness opens our eyes to see {theme.lower()} everywhere.",
                f"Your grateful spirit is a gift that honors {theme.lower()}."
            ]
        }
        
        mood_notes = notes.get(mood, notes["hopeful"])
        return random.choice(mood_notes)
    
    def create_prayer_journal_entry(self, user_name: str, prayer_request: str, 
                                  gabe_response: str, mood: str) -> Dict:
        """Create a prayer journal entry"""
        return {
            "id": f"prayer_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "date": datetime.datetime.now().isoformat(),
            "user_name": user_name,
            "prayer_request": prayer_request,
            "gabe_response": gabe_response,
            "mood": mood,
            "scripture_given": None,
            "follow_up_needed": True,
            "follow_up_date": (datetime.datetime.now() + datetime.timedelta(days=3)).isoformat()
        }
    
    def generate_daily_reminder(self, user_name: str, recent_mood: str = "peaceful") -> Dict:
        """Generate a daily spiritual reminder"""
        reminders = {
            "morning": [
                f"Good morning, {user_name}! Today is a gift from God. How can I pray with you today?",
                f"Rise and shine, {user_name}! God has new mercies waiting for you this morning.",
                f"Hello {user_name}! What's one thing you're grateful for as this new day begins?"
            ],
            "afternoon": [
                f"Hope your day is going well, {user_name}! Need a moment of prayer or encouragement?",
                f"Afternoon blessing, {user_name}! Remember, God is with you in every moment.",
                f"Taking a midday pause, {user_name}? I'm here if you need spiritual refreshment."
            ],
            "evening": [
                f"Evening peace to you, {user_name}! How has God shown up in your day?",
                f"As the day winds down, {user_name}, what prayer can I offer for your rest?",
                f"Good evening, {user_name}! Let's end this day with gratitude and prayer."
            ]
        }
        
        current_hour = datetime.datetime.now().hour
        if current_hour < 12:
            time_period = "morning"
        elif current_hour < 17:
            time_period = "afternoon"
        else:
            time_period = "evening"
        
        message = random.choice(reminders[time_period])
        scripture = self.get_scripture_recommendation(recent_mood)
        
        return {
            "time_period": time_period,
            "message": message,
            "scripture": scripture,
            "type": "daily_reminder"
        }
    
    def check_growth_milestone(self, user_stats: Dict) -> Optional[Dict]:
        """Check if user has achieved any new spiritual growth milestones"""
        # This would integrate with user statistics from Firebase
        # For now, return structure for implementation
        
        milestones_to_check = [
            {
                "condition": "prayer_count >= 1",
                "milestone": "First Prayer Request"
            },
            {
                "condition": "consecutive_days >= 7", 
                "milestone": "Daily Conversations"
            },
            {
                "condition": "scripture_requests >= 5",
                "milestone": "Scripture Explorer"
            }
        ]
        
        # Implementation would check user_stats against conditions
        # Return achieved milestone if found
        return None
    
    def get_mood_based_encouragement(self, mood: str, user_name: str) -> str:
        """Generate mood-specific encouragement"""
        encouragements = {
            "sad": [
                f"Your tears are precious to God, {user_name}. He sees every one and cares deeply.",
                f"It's okay to not be okay, {user_name}. God meets us in our sadness with comfort.",
                f"This sadness won't last forever, {user_name}. God has joy stored up for you."
            ],
            "anxious": [
                f"Your worries are safe with God, {user_name}. He can handle what feels too big for you.",
                f"Peace isn't the absence of problems, {user_name}, but the presence of God in them.",
                f"One breath at a time, {user_name}. God's peace is available right now."
            ],
            "angry": [
                f"Your anger makes sense, {user_name}. God can use even this for good.",
                f"It's okay to feel angry, {user_name}. Let's bring this to God together.",
                f"God sees the injustice that angers you, {user_name}. He cares about what you care about."
            ],
            "hopeful": [
                f"Your hope is beautiful, {user_name}! God delights in your trusting heart.",
                f"Keep holding onto that hope, {user_name}. God has good things in store.",
                f"Your hope inspires me, {user_name}. It reflects God's faithfulness."
            ]
        }
        
        mood_encouragements = encouragements.get(mood, encouragements["hopeful"])
        return random.choice(mood_encouragements)