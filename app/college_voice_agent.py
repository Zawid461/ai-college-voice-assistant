import os
import time
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

# LangChain / RAG
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

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

# -----------------------------
# VOICE ID
# -----------------------------
VOICE_ID = "SAz9YHcvj6GT2YYXdXww"

# -----------------------------
# LOAD EMBEDDINGS
# -----------------------------
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# -----------------------------
# LOAD VECTOR DATABASE
# -----------------------------
vectorstore = FAISS.load_local(
    "faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
)

print("\nCollege AI Voice Assistant Ready!\n")

# -----------------------------
# MEMORY
# -----------------------------
conversation_history = [
    {
        "role": "system",
        "content": """
You are an intelligent AI college assistant.

Answer student questions using the provided college knowledge base.

Be:
- helpful
- professional
- concise
- friendly
"""
    }
]

# -----------------------------
# MAIN LOOP
# -----------------------------
while True:

    # -------------------------
    # RECORD AUDIO
    # -------------------------
    duration = 5
    sample_rate = 44100

    print("\nSpeak now...\n")

    audio_data = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype='int16'
    )

    sd.wait()

    audio_path = "app/student_input.wav"

    write(audio_path, sample_rate, audio_data)

    print("Recording complete!")

    # -------------------------
    # SPEECH TO TEXT
    # -------------------------
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

    print("\nSTUDENT ASKED:\n")
    print(user_text)

    # -------------------------
    # EXIT
    # -------------------------
    if "exit" in user_text.lower():
        print("\nGoodbye!\n")
        break

    # -------------------------
    # RAG SEARCH
    # -------------------------
    docs = vectorstore.similarity_search(
        user_text,
        k=3
    )

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    print("\nRetrieved Knowledge:\n")
    print(context[:1000])

    # -------------------------
    # CREATE RAG PROMPT
    # -------------------------
    rag_prompt = f"""
Answer the student's question using ONLY the provided college information.

College Information:
{context}

Student Question:
{user_text}
"""

    # -------------------------
    # SAVE USER MESSAGE
    # -------------------------
    conversation_history.append(
        {
            "role": "user",
            "content": rag_prompt
        }
    )

    # -------------------------
    # AI RESPONSE
    # -------------------------
    chat_response = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=conversation_history
    )

    ai_response = chat_response.choices[0].message.content

    print("\nAI RESPONSE:\n")
    print(ai_response)

    # -------------------------
    # SAVE AI RESPONSE
    # -------------------------
    conversation_history.append(
        {
            "role": "assistant",
            "content": ai_response
        }
    )

    # -------------------------
    # TEXT TO SPEECH
    # -------------------------
    audio = eleven_client.text_to_speech.convert(
        voice_id=VOICE_ID,
        model_id="eleven_multilingual_v2",
        text=ai_response
    )

    output_path = f"app/college_ai_response_{int(time.time())}.mp3"

    with open(output_path, "wb") as f:
        for chunk in audio:
            f.write(chunk)

    print("\nAI voice generated!")

    # -------------------------
    # PLAY AUDIO
    # -------------------------
    pygame.init()
    pygame.mixer.init()

    pygame.mixer.music.load(output_path)
    pygame.mixer.music.play()

    print("\nAI is speaking...\n")

    while pygame.mixer.music.get_busy():
        continue