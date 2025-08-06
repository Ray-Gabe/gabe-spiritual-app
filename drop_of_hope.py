import random
from datetime import datetime

class DropOfHope:
    """Content pool for spiritual encouragement, verses, and wisdom"""
    
    def __init__(self):
        self.verses = [
            {
                "verse": "Jeremiah 29:11",
                "text": "For I know the plans I have for you, declares the Lord, plans to prosper you and not to harm you, to give you hope and a future.",
                "theme": "hope"
            },
            {
                "verse": "Isaiah 41:10",
                "text": "Fear not, for I am with you; be not dismayed, for I am your God; I will strengthen you, I will help you, I will uphold you with my righteous right hand.",
                "theme": "strength"
            },
            {
                "verse": "Philippians 4:13",
                "text": "I can do all things through Christ who strengthens me.",
                "theme": "strength"
            },
            {
                "verse": "Romans 8:28",
                "text": "And we know that in all things God works for the good of those who love him, who have been called according to his purpose.",
                "theme": "purpose"
            },
            {
                "verse": "Psalm 23:4",
                "text": "Even though I walk through the valley of the shadow of death, I will fear no evil, for you are with me; your rod and your staff, they comfort me.",
                "theme": "comfort"
            },
            {
                "verse": "Matthew 11:28",
                "text": "Come to me, all you who are weary and burdened, and I will give you rest.",
                "theme": "rest"
            },
            {
                "verse": "Psalm 46:1",
                "text": "God is our refuge and strength, an ever-present help in trouble.",
                "theme": "strength"
            },
            {
                "verse": "1 Peter 5:7",
                "text": "Cast all your anxiety on him because he cares for you.",
                "theme": "anxiety"
            },
            {
                "verse": "Joshua 1:9",
                "text": "Be strong and courageous. Do not be afraid; do not be discouraged, for the Lord your God will be with you wherever you go.",
                "theme": "courage"
            },
            {
                "verse": "Psalm 139:14",
                "text": "I praise you because I am fearfully and wonderfully made; your works are wonderful, I know that full well.",
                "theme": "identity"
            },
            {
                "verse": "Psalm 34:18",
                "text": "The Lord is close to the brokenhearted and saves those who are crushed in spirit.",
                "theme": "sadness"
            },
            {
                "verse": "Isaiah 40:29",
                "text": "He gives strength to the weary and increases the power of the weak.",
                "theme": "strength"
            },
            {
                "verse": "2 Corinthians 4:17",
                "text": "For our light and momentary troubles are achieving for us an eternal glory that far outweighs them all.",
                "theme": "perspective"
            },
            {
                "verse": "Psalm 30:5",
                "text": "Weeping may stay for the night, but rejoicing comes in the morning.",
                "theme": "hope"
            },
            {
                "verse": "Isaiah 43:2",
                "text": "When you pass through the waters, I will be with you; and when you pass through the rivers, they will not sweep over you.",
                "theme": "protection"
            }
        ]
        
        self.analogies = [
            {
                "situation": "feeling stuck",
                "analogy": "You're like a butterfly in a cocoon right now - it feels dark and tight, but transformation is happening. What looks like being stuck is actually becoming.",
                "theme": "growth"
            },
            {
                "situation": "facing challenges",
                "analogy": "Like a river meeting rocks, you don't have to break them - just find your way around. God makes a path where there seems to be none.",
                "theme": "guidance"
            },
            {
                "situation": "feeling overwhelmed",
                "analogy": "You're like a tree in a storm - bend, don't break. Your roots in God's love run deeper than any wind blows strong.",
                "theme": "resilience"
            },
            {
                "situation": "doubt",
                "analogy": "Doubt is like walking in fog - everything feels unclear, but the ground is still solid under your feet. Keep taking one faithful step at a time.",
                "theme": "faith"
            },
            {
                "situation": "loneliness",
                "analogy": "Even a lighthouse stands alone on the cliff, but it guides countless ships safely home. Your light matters, even when you can't see who it's helping.",
                "theme": "purpose"
            },
            {
                "situation": "new beginnings",
                "analogy": "You're like a seed that's been planted in rich soil - trust the process even when all you see is darkness. God is growing something beautiful.",
                "theme": "hope"
            },
            {
                "situation": "healing",
                "analogy": "Healing is like tending a garden with God - some days you plant hope, some days you water with tears, some days you just rest in His timing.",
                "theme": "healing"
            },
            {
                "situation": "waiting",
                "analogy": "Waiting is like watching a sunrise - it seems slow, but suddenly the whole sky is painted with God's glory. Your breakthrough is coming.",
                "theme": "patience"
            },
            {
                "situation": "sadness",
                "analogy": "Sadness is like winter soil - it looks barren, but it's being prepared for new life. Even tears water the ground where hope will grow.",
                "theme": "comfort"
            },
            {
                "situation": "fear",
                "analogy": "Fear is like standing at the edge of the Red Sea - it looks impossible, but God specializes in making ways where there are none.",
                "theme": "courage"
            },
            {
                "situation": "loss",
                "analogy": "Grief is like the valley of shadows - dark and deep, but even there you're not walking alone. The Shepherd is right beside you.",
                "theme": "comfort"
            },
            {
                "situation": "struggling with faith",
                "analogy": "Faith sometimes feels like holding onto a rope in the dark - you can't see where it leads, but you trust the One holding the other end.",
                "theme": "trust"
            }
        ]
        
        self.prayers = [
            {
                "type": "morning",
                "prayer": "Lord, as I start this day, help me remember that You go before me. Give me wisdom for decisions, strength for challenges, and peace that passes understanding. Amen."
            },
            {
                "type": "evening",
                "prayer": "Father, thank You for carrying me through today. Forgive where I fell short, and help me rest in Your love. Prepare my heart for tomorrow. Amen."
            },
            {
                "type": "anxiety",
                "prayer": "God, You know the worries weighing on my heart. I place them in Your hands and ask for Your peace. Help me trust Your timing and plan. Amen."
            },
            {
                "type": "strength",
                "prayer": "Lord, when I feel weak, be my strength. When I'm discouraged, be my hope. Remind me that Your power is made perfect in my weakness. Amen."
            },
            {
                "type": "gratitude",
                "prayer": "Thank You, God, for Your countless blessings - both seen and unseen. Help me live with a grateful heart and share Your love with others. Amen."
            },
            {
                "type": "sadness",
                "prayer": "Lord, You see my tears and know my pain. Be close to my broken heart and remind me that weeping may last for the night, but joy comes in the morning. Amen."
            },
            {
                "type": "fear",
                "prayer": "God, when fear tries to overwhelm me, remind me that You have not given me a spirit of fear, but of power, love, and sound mind. Be my courage. Amen."
            },
            {
                "type": "healing",
                "prayer": "Father, You are the Great Physician. Heal what is broken in me - body, mind, and spirit. Help me trust Your timing and Your ways. Amen."
            }
        ]
        
        # Biblical stories for deeper responses
        self.biblical_stories = [
            {
                "emotion": "sadness",
                "story": "You know, Job lost everything - his family, his health, even his hope. But even in his darkest moments, he still cried TO God, not away from Him. God didn't leave Job in that pit, and He's not leaving you either."
            },
            {
                "emotion": "sadness", 
                "story": "Even Jesus wept when He saw Mary's grief at Lazarus' tomb. Your tears matter deeply to Him - He doesn't rush you through your pain."
            },
            {
                "emotion": "fear",
                "story": "David faced Goliath when everyone else was paralyzed with fear. But he knew God was bigger than any giant. Whatever giant you're facing, God is still bigger."
            },
            {
                "emotion": "doubt",
                "story": "Thomas needed to see Jesus' scars before he could believe. Jesus didn't shame him for his doubt - He showed up and let Thomas touch the wounds. He'll show up for your doubts too."
            },
            {
                "emotion": "overwhelmed",
                "story": "Moses felt overwhelmed leading God's people through the wilderness. God told him, 'My presence will go with you, and I will give you rest.' That same presence is with you today."
            }
        ]
        
        # Personal prayers by name for deeper emotional moments  
        self.personal_prayers = [
            {
                "emotion": "sadness",
                "prayer_template": "🙏 Jesus, I lift up {name} to You right now. You see the sadness in {name}'s heart and You understand every pain they're carrying. Lord, sit with {name} in this difficult moment. Speak gently to the places in {name}'s soul that no one else can see. Bring Your peace and comfort to {name}. Remind {name} that You are close to the brokenhearted and You will never leave them alone. In JESUS NAME Amen."
            },
            {
                "emotion": "fear", 
                "prayer_template": "🙏 Father, {name} is facing fear right now and You know exactly what's causing their anxiety. Lord, wrap {name} in Your perfect love that casts out all fear. Give {name} courage to take the next step, knowing You're walking beside them every moment. Fill {name} with Your peace that passes understanding. In JESUS NAME Amen."
            },
            {
                "emotion": "grief",
                "prayer_template": "🙏 Lord, {name} is walking through the deep valley of grief right now. Be {name}'s Good Shepherd in this dark and difficult place. Let {name} feel Your presence even when everything else feels empty and broken. Carry the burdens that are too heavy for {name} to bear alone. Comfort {name} with Your unfailing love. In JESUS NAME Amen."
            },
            {
                "emotion": "overwhelmed",
                "prayer_template": "🙏 God, {name} feels completely overwhelmed right now and You see every burden they're carrying. Help {name} cast all their cares on You because You care deeply for {name}. Give {name} rest for their weary soul and strength for each new day. Show {name} Your peace in the midst of the storm. In JESUS NAME Amen."
            },
            {
                "emotion": "anxiety",
                "prayer_template": "🙏 Father, {name} is struggling with anxiety and worry right now. You know every fearful thought racing through {name}'s mind. Lord, calm {name}'s anxious heart with Your presence. Remind {name} that You are in control and that You work all things together for good. Fill {name} with Your perfect peace. In JESUS NAME Amen."
            },
            {
                "emotion": "anger",
                "prayer_template": "🙏 God, You see the anger in {name}'s heart and You understand every reason behind it. Lord, help {name} overcome this anger with Your love and grace. Give them the strength to forgive as You have forgiven them. Transform this fire into righteous passion for good and help them walk in Your peace. Fill them with Your Spirit so they can respond with wisdom and love. In JESUS NAME Amen."
            }
        ]
        
        self.encouragements = [
            "Your story isn't over - God is still writing beautiful chapters in your life.",
            "You're not behind in life. You're exactly where God needs you to be for what He's preparing you for.",
            "Your current struggle is developing strength you'll need for your next season.",
            "God doesn't waste pain. He transforms it into purpose.",
            "You're not too broken for God to use. He specializes in beautiful mosaics made from broken pieces.",
            "Your prayers are not bouncing off the ceiling. God hears every word.",
            "This season of waiting is not wasted time. God is working in ways you can't see.",
            "Your value doesn't decrease because someone couldn't see your worth.",
            "God's timing isn't late. It's never late. It's always right on time.",
            "You're not a mistake. You're a masterpiece in progress."
        ]
    
    def get_verse(self, theme=None, mood=None):
        """Get a Bible verse based on theme or mood"""
        if theme:
            matching_verses = [v for v in self.verses if v['theme'] == theme]
            if matching_verses:
                return random.choice(matching_verses)
        
        if mood:
            theme_map = {
                'sad': 'comfort',
                'anxious': 'peace',
                'angry': 'peace',
                'hopeful': 'hope',
                'positive': 'gratitude'
            }
            mapped_theme = theme_map.get(mood)
            if mapped_theme:
                matching_verses = [v for v in self.verses if v['theme'] == mapped_theme]
                if matching_verses:
                    return random.choice(matching_verses)
        
        return random.choice(self.verses)
    
    def get_random_verse(self):
        """Get a random Bible verse for Drop of Hope display"""
        return random.choice(self.verses)
    
    def get_analogy(self, situation=None):
        """Get a modern analogy or parable"""
        if situation:
            matching = [a for a in self.analogies if situation.lower() in a['situation']]
            if matching:
                return random.choice(matching)
        
        return random.choice(self.analogies)
    
    def get_prayer(self, prayer_type=None, mood=None):
        """Get a prayer based on type or mood"""
        if prayer_type:
            matching = [p for p in self.prayers if p['type'] == prayer_type]
            if matching:
                return random.choice(matching)
        
        if mood:
            type_map = {
                'anxious': 'anxiety',
                'sad': 'sadness',
                'positive': 'gratitude',
                'angry': 'strength',
                'hopeful': 'gratitude'
            }
            mapped_type = type_map.get(mood)
            if mapped_type:
                matching = [p for p in self.prayers if p['type'] == mapped_type]
                if matching:
                    return random.choice(matching)
        
        return random.choice(self.prayers)
    
    def get_biblical_story(self, emotion):
        """Get a biblical story for specific emotions"""
        matching = [s for s in self.biblical_stories if s['emotion'] == emotion]
        if matching:
            return random.choice(matching)
        return None
        
    def get_personal_prayer(self, emotion, name):
        """Get a personal prayer template for specific emotions"""
        if not name:
            return None
            
        # Capitalize first letter of name for proper formatting
        formatted_name = name.strip().capitalize() if name else name
        
        matching = [p for p in self.personal_prayers if p['emotion'] == emotion]
        if matching:
            prayer_template = random.choice(matching)
            return prayer_template['prayer_template'].format(name=formatted_name)
        return None
    
    def get_encouragement(self):
        """Get a random encouragement"""
        return random.choice(self.encouragements)
    
    def get_daily_content(self):
        """Get curated daily content"""
        hour = datetime.now().hour
        
        if 5 <= hour < 12:  # Morning
            return {
                'type': 'morning',
                'verse': self.get_verse('hope'),
                'prayer': self.get_prayer('morning'),
                'encouragement': self.get_encouragement()
            }
        elif 12 <= hour < 18:  # Afternoon
            return {
                'type': 'afternoon',
                'verse': self.get_verse('strength'),
                'analogy': self.get_analogy(),
                'encouragement': self.get_encouragement()
            }
        else:  # Evening
            return {
                'type': 'evening',
                'verse': self.get_verse('peace'),
                'prayer': self.get_prayer('evening'),
                'encouragement': self.get_encouragement()
            }