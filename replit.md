# GABE - Gabriel: God's Messenger

## Overview

GABE (God Always Beside Everyone) is a Progressive Web App (PWA) spiritual companion chatbot built with Flask and integrated with OpenAI's GPT-4o model. The application provides a mobile-first, installable chat interface that offers spiritual guidance, biblical wisdom, prayer support, and crisis intervention resources. Named after the angel Gabriel, GABE serves as a modern-day messenger bringing hope, encouragement, and divine guidance to users through conversational AI.

## User Preferences

Preferred communication style: Simple, everyday language.

## Recent Changes (July 24, 2025)

- **In-Chat Name & Age Collection**: Moved user onboarding from landing page to chat conversation flow with name and age group selection
- **Age-Based Personality System**: Implemented 4 distinct personality modes (10-17, 18-30, 31-50, 51+) with tailored communication styles
- **WhatsApp-Style Chat Interface**: Transformed chat to authentic WhatsApp design with message bubbles, tails, and signature colors
- **User Avatar System**: Added circular avatars with initials (G for GABE, user's first letter) similar to WhatsApp contacts
- **Updated Branding**: Changed from "Gabriel: God's Messenger" to "GUIDANCE AND BLESSING EVERYDAY" with tagline "BECAUSE EVEN PRAYERS START WITH A CONVERSATION"
- **Natural Language Refinement**: Reduced robotic formality, increased casual authenticity with phrases like "Sho, that's heavy"
- **Enhanced Name Usage**: Integrated frequent name usage throughout conversations for personal connection
- **Intuitive Response Patterns**: Replaced repetitive questions with acknowledgments like "This one hits deep"
- **Enhanced System Prompt**: Updated GABE to respond more like a caring friend - first reflecting empathy, then offering encouragement with analogies, ending with gentle invitations
- **Text-to-Speech Integration**: Added speaker buttons on GABE responses with Web Speech API for voice output
- **Mood Tracking Visualization**: Added colored mood indicators on user messages (positive, sad, anxious, hopeful, angry)
- **Expanded Drop of Hope Content**: Integrated 50+ Bible verses, analogies, prayers, and encouragements that adapt to user's emotional state
- **Voice Input Enhancement**: Voice recognition transcribes to text field allowing editing before sending
- **Memory-Enhanced Responses**: GABE remembers conversations, moods, and journal entries for personalized spiritual guidance
- **Dual AI Provider Support**: Gemini 1.5-flash primary with OpenAI GPT-4o fallback for reliability
- **Firebase Integration**: Full persistent memory system for journaling, mood tracking, and prayer requests
- **Clickable Age Selection**: Changed from typing age to clicking buttons for better UX (10-17, 18-30, 31-50, 51+)
- **Spiritual Content Overhaul**: Completely redesigned AI responses to prioritize biblical comfort, removed tech analogies, added scripture-focused examples
- **Enhanced Analogies**: Improved spiritual analogies using nature, seasons, biblical imagery instead of technology references
- **Biblical Response Examples**: Added specific examples for sadness including Psalm 34:18 and Jesus weeping, focused on God's character and presence
- **Chunked Conversation System**: Implemented multi-step emotional responses that replace paragraph dumps with 3-4 line chunks delivered with natural timing
- **Speech-Synchronized Delivery**: Each message chunk waits for text-to-speech completion before displaying next message, preventing voice cutoff
- **Enhanced Emotional Support**: Deep emotions (sadness, anxiety, anger) trigger thoughtful 3-chunk conversations with biblical stories, personal prayers, and follow-up care
- **Streamlined Chunked Messages**: Consolidated to single substantial messages per chunk with prayers containing 4-5 full sentences for natural text-to-speech delivery
- **Faith-Based Prayer Enhancement**: Updated all prayers to focus on personal faith, overcoming challenges, and victory through Jesus, ending with "In JESUS NAME Amen"
- **Voice Toggle Control**: Added user-controlled voice toggle switch in chat header allowing users to enable/disable text-to-speech functionality
- **Verified Chunked Conversation Flow**: Confirmed complete spiritual support system works correctly - sadness detection → biblical story → empowering prayer → final encouragement
- **Background Music System Removed**: Removed background music system as it could only produce simple tones rather than quality instrumental worship music
- **Enhanced Spiritual Features with Modal Interface**: Created dedicated modal windows for prayer journal and scripture recommendations, replacing in-chat displays with professional split-screen interfaces
- **Prayer Journal Modal System**: Beautiful windowed interface showing journal entries with dates, prayers, moods, and responses - includes "Start New Prayer" functionality
- **Scripture Modal System**: Dedicated scripture window with verse display, personal notes, and integrated save-to-journal functionality
- **Automatic Prayer Saving**: System detects prayer-related conversations and automatically saves them to the prayer journal
- **Revolutionary Natural Conversation System**: Completely replaced hard-coded responses with OpenAI GPT-4o powered natural conversations through new GabeCompanion class
- **Dynamic Conversation Memory**: AI remembers conversation themes, emotional states, and user patterns for deeply personalized responses
- **Intelligent Context Building**: System analyzes conversation history to provide relevant, flowing responses that build on previous exchanges
- **Emotional Intelligence Enhancement**: Advanced mood detection with natural conversation adaptation based on user's emotional state
- **Age-Adaptive Personality**: Dynamic personality adjustment (Gen Z, Millennial, Adult) integrated into natural conversation flow
- **Robust Three-Tier Failover System**: Gemini 1.5-flash primary, OpenAI GPT-4o secondary, intelligent spiritual fallbacks ensuring conversations never fail
- **Optimized Gemini Integration**: Gemini responses now properly constrained to natural, concise spiritual guidance matching desired conversation style
- **Scripture Modal Functionality Verified**: Scripture recommendation modal window system working correctly with proper modal display and content population
- **Enhanced Natural Conversation System**: Updated GABE's core personality with Spirit-led companion approach featuring emotional flow routing, natural conversation patterns, and elimination of robotic chatbot language for authentic spiritual dialogue
- **Standalone Spiritual Features**: Prayer journal and scripture recommendations now work as independent overlay windows that appear only when specifically requested, separate from chat conversation
- **Enhanced Gemini-Friendly Dialogue Management**: Completely rebuilt auto-response system with cleaner state management, preventing message spam and API errors
- **Multi-Level Inactivity System**: Sophisticated 3-tier timer system (1.5min, 5min, 10min) with question detection, WhatsApp-style typing animations, and biblical encouragements without emojis for voice compatibility
- **Smart Question Detection**: Auto-followup only activates when GABE's last message wasn't a question, allowing natural conversation flow
- **Biblical Encouragement Integration**: Random scripture verses provided during check-ins with proper timing and spiritual relevance
- **Streamlined User Onboarding**: Simplified name and age collection flow using the new dialogue management system with proper state tracking
- **365-Character Bible Story System**: Implemented 3-part Bible stories (David & Goliath, Moses & Red Sea, Daniel, etc.) delivered in chunks with natural timing and ending with "Would you like to hear another story or a prayer?"
- **Complete Conversation Flow Restoration**: Fixed conversation stopping issue and restored proper sadness response flow with options for talking, quiet time, or Bible stories/verses
- **Dual AI System with Gemini Primary**: Successfully implemented Gemini 2.5-flash as primary provider with OpenAI GPT-4o fallback, ensuring conversations never fail
- **Prayer Closure System**: Added automatic closure for prayer requests with mood-specific Bible verses and "GABE is always by your side — you are never alone" message
- **Story Continuation Logic**: Implemented multi-part Bible story system that continues naturally when users respond positively
- **Verified Working State**: All conversation flows tested and confirmed working perfectly - sadness responses, story continuations, prayer closures, and voice integration
- **Fixed Authentication Chat Error**: Resolved critical chat error where user object was being accessed incorrectly, now properly uses current_user.name for authenticated conversations
- **Enhanced Logout Button Visibility**: Created prominent logout button with background, text label, and hover effects for better user experience
- **Duplicate Welcome Message Fix**: Fixed issue where authenticated users received multiple welcome messages by streamlining conversation initialization flow
- **Resolved Conversation History Bug**: Fixed critical 'user' key error in gabe_ai.py by adding proper defensive programming to safely access conversation history dictionary keys
- **Verified Working Chat System**: Confirmed complete resolution of technical difficulties - GABE now responds properly to all messages with appropriate spiritual guidance, biblical comfort, and prayer support
- **Dual AI Failover Success**: Validated seamless failover from OpenAI to Gemini when quota limits are reached, ensuring conversations never fail
- **Enhanced System Prompt Integration**: Incorporated best elements from user's proposed prompt including "Bible in one hand, coffee in the other" personality, medium-length message guidance, and clearer friend-like conversational style while maintaining advanced age-adaptation and memory features
- **Improved Biblical Integration Guidelines**: Updated system to always offer prayer, Bible verses, or relatable thoughts naturally, ensuring spiritual wisdom feels like helpful life advice rather than formal counseling
- **Fully Functional Contextual Support System**: Implemented complete P-S-A button system (Prayer, Story, Analogy) that appears after 2 conversations, detects conversation mood, and provides contextually relevant spiritual content based on actual user concerns
- **Conversation-Aware Spiritual Guidance**: System analyzes last 5 messages to detect emotional state and provides targeted spiritual support (e.g., diamond analogy for dealing with mean people when user discusses being hurt by others)
- **Personal Prayer Experience**: All prayers use first-person pronouns ("me", "I", "my") for authentic personal prayer experience instead of generic third-person language
- **Smart Emotional Crisis Detection**: Advanced system detects strong emotional signals and provides immediate crisis intervention resources while maintaining contextual spiritual support
- **Professional Chat Integration**: P-S-A buttons permanently integrated into chat input bar with hover effects and professional styling, providing continuous access to mood-appropriate spiritual content
- **Verified User Testing Success**: Contextual support system tested and confirmed working - correctly detects sad mood from conversation about mean people and delivers relevant Prayer, Story, and Analogy content
- **Faith in Action Star Button Fix**: Resolved critical JavaScript loading issue where `gamified-spiritual-features.js` file was missing, causing Faith in Action panel buttons (Morning Devotion, Prayer Challenge, Bible Study, etc.) to not function - all spiritual activity buttons now work correctly with proper XP tracking and modal displays
- **Interactive Bible Study Feature**: Completely replaced Scripture Adventure with comprehensive Bible study system featuring 3 study courses ("Trusting God in Difficult Times", "Love in Action: Serving Others", "Your Identity in Christ") with scripture readings, reflection questions, progress tracking, and XP rewards
- **Scripture Adventure Removal Completed**: Successfully removed all references to Scripture Adventure from codebase including HTML templates, JavaScript functions, and help documentation per user feedback
- **Bible Study Integration Success**: Fixed user data initialization issues and confirmed working Bible Study modal system with proper XP tracking and session management
- **Modern GABE Chat Interface**: Complete visual overhaul of conversation screen with professional purple-to-violet gradients, glass-morphism styling, enhanced message bubbles with blue gradients for users and clean glass-effect for GABE, larger gradient avatars with shadows, modern input area with gradient buttons, smooth message slide-in animations, and shimmer effects on header
- **Activity-Specific Voice Celebrations**: Enhanced voice celebration system with activity-specific encouraging phrases - prayer activities get "Amen!", "God bless you!", "Beautiful prayer!", devotions get "Well done!", "God is pleased!", scripture study gets "Great job!", "Keep studying!", with random selection for authentic spiritual encouragement
- **Enhanced Faith in Action Panel Styling**: Upgraded visual design with modern gradients, shimmer hover effects on level/XP displays, improved typography with gradient text headers, enhanced backdrop blur effects, smooth animations, and professional glassmorphism styling for better user engagement
- **Optimal Dual AI System**: Gemini 2.5-flash as PRIMARY provider with OpenAI GPT-4o as FALLBACK, ensuring conversations continue seamlessly even during API quota limitations, with proper error handling and transparent failover functionality for maximum reliability
- **Fixed Conversation Context Issue**: Resolved critical context confusion where GABE misinterpreted user responses as name corrections by removing problematic name prefix from messages and updating system prompt to handle user names properly
- **Session Management Enhancement**: Added session clearing functionality with reset button in chat header to allow users to start fresh conversations and clear stored names/preferences
- **Conversation Flow Fix**: Resolved critical conversation fragmentation issue by removing complex chunked response system and implementing natural, flowing single responses for emotional states (sadness, anxiety, anger) that include biblical stories and personalized prayers without breaking conversation flow
- **Enhanced Hopeful Prayer System**: Completely solved overwhelming prayer length problem by implementing comprehensive prayer detection at app.py level before crisis detection - any message containing prayer keywords returns personalized, hopeful prayer with meaningful spiritual content, personal connection ("you've got a friend now"), and ongoing support ("I'm GABE, and I'm not going anywhere")
- **Prayer Priority Over Crisis**: Prayer detection now happens before crisis detection, ensuring spiritual requests like "father help me" get prayer responses instead of crisis alerts
- **Successful Prayer Length Fix**: Eliminated all long paragraph prayers by intercepting prayer requests before they reach AI providers, ensuring consistent short prayers that are voice-friendly and non-overwhelming
- **Comprehensive Keyword Coverage**: Enhanced prayer detection with broader keyword matching including "jesus", "father", "heavenly", "lord", "bless me" for maximum prayer request coverage
- **Prayer Text Alignment Fix**: Resolved critical CSS conflict where duplicate `.message-content` definition with `display: flex` was preventing proper line break rendering in prayer responses
- **Name Safeguarding System**: Added validation to prevent inappropriate names like "prayer", "god", "help" from appearing in prayer text, automatically converting to "friend" for natural reading
- **Modal Authentication System**: Implemented comprehensive login/registration system using Flask-Login with PostgreSQL database integration
- **Original Landing Page Preserved**: Maintained the original GABE landing page design with angel figure and familiar interface
- **Modal Login Window**: Added beautiful modal window that appears when "Start Chat" is clicked, containing both login and registration forms
- **Database-Backed User Management**: Created User and Conversation models with proper relationships and password hashing
- **Seamless User Experience**: Authenticated users go directly to chat when clicking "Start Chat", new users see the registration modal
- **Persistent Conversation History**: All conversations now saved to database per user with proper authentication requirements
- **Enhanced Crisis Detection Precision**: Refined crisis detection to prevent false positives on positive messages like "thank you this helped" while maintaining accurate detection of genuine emergencies
- **Integrated P-S-A Contextual Support**: Completed professional P-S-A button system (Prayer, Story, Analogy) with GABE's personality integration, personal introductions, and follow-up messages that maintain natural conversation flow
- **Silent Button Appearance**: P-S-A buttons appear seamlessly after 2 messages without announcement, integrating naturally into chat interface
- **Contextual Support Follow-ups**: Each P-S-A button click triggers personalized follow-up messages from GABE to continue conversation naturally and reinforce friendship connection
- **Faith in Action Layout Optimization**: Moved badges and rewards to compact icon buttons (🏆 🎁) next to Level/XP display, creating more space for main spiritual activity buttons while maintaining full functionality
- **Complete Bible Reading Functionality**: Fixed all Bible Reading modal interactions with working reading plan selection, audio toggle, completion tracking, and sharing features
- **JavaScript Duplication Resolution**: Eliminated duplicate class declarations causing conflicts by removing redundant gamified-features.js file and ensuring proper method binding

## System Architecture

### Frontend Architecture
- **Progressive Web App (PWA)**: Built with modern web standards for native app-like experience
- **Mobile-First Design**: Responsive interface optimized for mobile devices with floating chat UI
- **Client-Side Framework**: Vanilla JavaScript with Bootstrap 5.3.0 for styling
- **Service Worker**: Implements offline caching and app installation capabilities
- **Modern CSS**: Custom CSS with CSS variables, gradients, and responsive design patterns

### Backend Architecture
- **Flask Framework**: Lightweight Python web framework handling HTTP requests and session management
- **Modular Design**: Separated concerns with dedicated classes for AI interaction and crisis detection
- **Session-Based Memory**: Conversation history stored in Flask sessions for continuity
- **RESTful API**: JSON-based API endpoints for chat functionality

### AI Integration
- **Dual AI Providers**: OpenAI GPT-4o primary with Gemini 2.5-flash fallback for reliability
- **Custom System Prompt**: Detailed personality guidelines for spiritual companion role (updated for shorter, more emotional responses)
- **Memory-Enhanced Context**: Integrates user memory from Firebase including journal entries, moods, and prayer requests
- **Mood Detection**: Automatically detects and tracks user emotional states from conversations

## Key Components

### Core Modules

1. **app.py** - Main Flask application with routing, session management, and API endpoints
2. **gabe_ai.py** - Dual AI provider integration (OpenAI + Gemini) with memory-enhanced responses
3. **firebase_service.py** - Firebase integration for persistent user memory, journaling, and mood tracking
4. **crisis_detection.py** - Crisis keyword detection and mental health resource provision
5. **templates/index.html** - Single-page application with PWA features and journal quick actions
6. **static/js/app.js** - Frontend JavaScript handling chat interface, PWA functionality, and journaling features

### PWA Components

1. **manifest.json** - App metadata for installation and native-like behavior
2. **sw.js** - Service worker for offline functionality and caching
3. **Icons** - Multiple icon sizes for various device requirements

### Frontend Features

- Welcome screen with name collection
- Real-time chat interface with typing indicators
- Voice input with Web Speech API and microphone button
- Journal quick actions for writing and viewing entries
- Message history display
- Install prompt for PWA installation
- Responsive design for all screen sizes

## Data Flow

1. **User Interaction**: User enters message through chat interface
2. **Crisis Check**: Message analyzed for crisis keywords before AI processing
3. **AI Processing**: Message sent to OpenAI with conversation context and system prompt
4. **Response Generation**: AI generates contextual spiritual guidance response
5. **Session Storage**: Conversation history updated in Flask session
6. **Frontend Update**: Response displayed in chat interface with typing animation

### Crisis Detection Flow
- Keywords scanned against predefined crisis indicators
- Immediate crisis resources provided when detected
- Conversation continues with heightened awareness mode

## External Dependencies

### Backend Dependencies
- **Flask**: Web framework and routing
- **OpenAI**: GPT-4o API integration for conversational AI
- **Werkzeug**: WSGI utilities and proxy handling

### Frontend Dependencies
- **Bootstrap 5.3.0**: UI framework and responsive components
- **Feather Icons**: Lightweight icon library
- **Google Fonts (Inter)**: Typography

### Environment Variables
- **OPENAI_API_KEY**: Required for AI functionality
- **SESSION_SECRET**: Flask session security (optional, has default)

## Deployment Strategy

### PWA Requirements
- HTTPS required for service worker and installation features
- Proper manifest.json configuration for app store-like behavior
- Service worker implementation for offline capability

### Hosting Considerations
- Static file serving for PWA assets
- Session management capability
- Environment variable support for API keys
- Mobile-optimized delivery

### Future Integration
- Designed to be embeddable into future "Pathways" website
- Modular architecture allows for easy integration
- Standalone functionality maintained

### Performance Optimizations
- CDN usage for external libraries
- Efficient caching strategy in service worker
- Minimal bundle size for fast mobile loading
- Progressive enhancement for offline use

The application follows modern web development best practices with a focus on spiritual care, crisis awareness, and mobile-first user experience. The modular architecture enables easy maintenance and future enhancements while maintaining the core spiritual companion functionality.