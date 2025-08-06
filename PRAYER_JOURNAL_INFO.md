# Prayer Journal Storage Information

## Current Storage System

Your prayer journal is currently stored in your browser session, which means:

### How It Works:
- **Session Storage**: Entries are saved during your current conversation session
- **Automatic Saving**: Conversations containing prayer-related keywords are automatically saved
- **Manual Saving**: You can manually save scripture verses using the "Save to Journal" button

### How to Access:
1. **Click the Star Button** in the chat header (top-right)
2. **Select "View Prayer Journal"** from the spiritual features panel
3. Your saved entries will display with dates, prayers, and moods

### What Gets Saved:
- Prayer requests and conversations
- Scripture verses you save
- Your emotional mood at the time
- Date and time of each entry
- GABE's responses to your prayers

### Current Limitations:
- **Session-based**: Entries are lost when you close the browser
- **Temporary Storage**: Not persistent between visits

### Automatic Saving Triggers:
The system automatically saves entries when your messages contain words like:
- pray, prayer, praying
- god, lord, jesus
- faith, blessing, amen
- And other spiritual keywords

### Future Enhancement:
The system is designed to integrate with Firebase for permanent storage across sessions and devices when configured.

## API Endpoints Available:
- `GET /api/prayer_journal` - Retrieve all entries
- `POST /api/prayer_journal` - Save new entry
- Both endpoints are working and tested