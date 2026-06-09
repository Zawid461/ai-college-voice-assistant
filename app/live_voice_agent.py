import os
import sounddevice as sd
from scipy.io.wavfile import write
from dotenv import load_dotenv
import pygame

# Deepgram
from deepgram import (
    DeepgramClient,
    PrerecordedOptions,
    FileSource,
)

# Groq
from openai import OpenAI

# ElevenLabs
from elevenlabs.client import ElevenLabs

# -----------------------------
# LOAD ENV VARIABLES
# -----------------------------
load_dotenv("app/.env")

# -----------------------------
# API CLIENTS
# -----------------------------
deepgram = DeepgramClient(
    os.getenv("DEEPGRAM_API_KEY")
)

groq_client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

eleven_client = ElevenLabs(
    api_key=os.getenv("ELEVENLABS_API_KEY")
)

# YOUR VOICE ID
VOICE_ID = "SAz9YHcvj6GT2YYXdXww"

# -----------------------------
# RECORD AUDIO
# -----------------------------
duration = 5  # seconds
sample_rate = 44100

print("\nSpeak now...\n")

audio_data = sd.rec(
    int(duration * sample_rate),
    samplerate=sample_rate,
    channels=1,
    dtype='int16'
)

sd.wait()

audio_path = "app/live_input.wav"

write(audio_path, sample_rate, audio_data)

print("Recording complete!")

# -----------------------------
# SPEECH TO TEXT
# -----------------------------
with open(audio_path, "rb") as file:
    buffer_data = file.read()

payload: FileSource = {
    "buffer": buffer_data,
}

options = PrerecordedOptions(
    model="nova-2",
    smart_format=True,
)

response = deepgram.listen.prerecorded.v("1").transcribe_file(
    payload,
    options
)

user_text = response.results.channels[0].alternatives[0].transcript

print("\nYOU SAID:\n")
print(user_text)

# -----------------------------
# LLM RESPONSE
# -----------------------------
chat_response = groq_client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {
            "role": "system",
            "content": "You are a helpful AI voice assistant."
        },
        {
            "role": "user",
            "content": user_text
        }
    ]
)

ai_response = chat_response.choices[0].message.content

print("\nAI RESPONSE:\n")
print(ai_response)

# -----------------------------
# TEXT TO SPEECH
# -----------------------------
audio = eleven_client.text_to_speech.convert(
    voice_id="SAz9YHcvj6GT2YYXdXww",
    model_id="eleven_multilingual_v2",
    text=ai_response
)

output_path = "app/ai_response.mp3"

with open(output_path, "wb") as f:
    for chunk in audio:
        f.write(chunk)

print("\nAI voice generated!")

# -----------------------------
# PLAY AI AUDIO
# -----------------------------
pygame.init()
pygame.mixer.init()

pygame.mixer.music.load(output_path)
pygame.mixer.music.play()

print("\nPlaying AI response...\n")

while pygame.mixer.music.get_busy():
    continue