from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv("app/.env")

# Create client
client = ElevenLabs(
    api_key=os.getenv("ELEVENLABS_API_KEY")
)

# Get all available voices
voices = client.voices.get_all()

print("AVAILABLE VOICES:\n")

for voice in voices.voices:
    print(f"Name: {voice.name}")
    print(f"Voice ID: {voice.voice_id}")
    print("-" * 40)