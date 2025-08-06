# GABE - Spiritual Companion

A conversational spiritual companion that provides empathetic responses with text-to-speech.

## Setup Instructions for Replit

1. **Install Required Packages**
   Add these to your `pyproject.toml` or run in the Shell:
   ```bash
   pip install gtts pygame
   ```

2. **Run the Program**
   ```bash
   python gabe_companion.py
   ```

## Features

- **Name Collection**: GABE asks for your name and uses it throughout the conversation
- **Emotion Detection**: Specifically detects sadness and responds with a multi-step caring process
- **Text-to-Speech**: Every message is both printed and spoken aloud using Google TTS
- **Thoughtful Timing**: Natural pauses between messages to create presence
- **Biblical Stories**: Shares about Job and Jesus to provide spiritual comfort
- **Personal Prayer**: Offers heartfelt prayer by name for those who are sad
- **Follow-up Promise**: Commits to checking in later for deeper emotional support

## Special Sadness Response Flow

When GABE detects sadness, it follows this specific pattern:

1. **Acknowledgment** - "I can feel that sadness, [name]"
2. **Presence** - Sits with you for a moment (3-5 second pause)
3. **Biblical Story** - Tells about Job's suffering and Jesus weeping
4. **Personal Prayer** - Prays specifically for you by name
5. **Follow-up Promise** - Commits to checking in later today and before bedtime

## Supported Sad Words

The program detects: sad, sadness, depressed, down, heartbroken, broken, crying, cry, hurt, hurting, pain, painful, grief, grieving, lost, empty, hopeless, despair, devastated, crushed

## Technical Notes

- Uses `gtts` (Google Text-to-Speech) for audio generation
- Uses `pygame` for audio playback
- Creates temporary audio files that are automatically cleaned up
- Graceful fallback if audio isn't available
- Cross-platform compatible (Windows, Mac, Linux)

## Example Usage

```
GABE - God Always Beside Everyone
Your Spiritual Companion
==================================================

Hello! I'm GABE, your spiritual companion.
What's your name? John

Nice to meet you, John! 💙
How are you feeling today? Tell me what's on your heart.
Your response: I'm feeling really sad today

💔 I can feel that sadness, John.
I won't try to fix it right now.
I'll just sit with you for a moment... no pressure.

[Natural pauses and biblical story follow...]
```

## Customization

You can modify the responses, add more emotion detection, or extend the biblical stories by editing the `gabe_companion.py` file.