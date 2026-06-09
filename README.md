# 🎓 AI College Voice Assistant

An AI-powered realtime voice assistant designed for educational institutions to automate student support and college information services.

This project enables students to interact with an intelligent college assistant using natural voice conversations. The assistant can answer queries related to admissions, courses, placements, departments, facilities, and academic information using voice-based interaction.

The system combines:

* Speech-to-Text (STT)
* Retrieval-Augmented Generation (RAG)
* Large Language Models (LLM)
* Text-to-Speech (TTS)
* Telephony Integration

to create a fully conversational AI voice assistant.

---

# 🚀 Features

* 🎤 Real-time voice interaction
* 🧠 AI conversational memory
* 📄 PDF-based knowledge retrieval (RAG)
* 🔍 Semantic search using FAISS vector database
* 🔊 Natural AI voice responses
* 💬 Continuous multi-turn conversations
* 📞 Twilio phone call integration
* 🌍 Public webhook support using ngrok
* ⚡ Fast AI response generation using Groq

---

# 🛠️ Technologies Used

## Backend

* Python
* FastAPI
* LangChain

## AI & LLM

* Groq LLM
* Sentence Transformers

## Voice Technologies

* Deepgram (Speech-to-Text)
* ElevenLabs (Text-to-Speech)

## Database & Retrieval

* FAISS Vector Database

## Telephony

* Twilio
* ngrok

---

# 🧠 System Architecture

Student Voice
↓
Speech-to-Text (Deepgram)
↓
RAG Semantic Search (FAISS)
↓
LLM Reasoning (Groq)
↓
Text-to-Speech (ElevenLabs)
↓
AI Voice Response

---

# 📞 Twilio Phone Call Integration

The project supports real-time phone call interaction using Twilio and FastAPI.

## Call Flow

Student Call
↓
Twilio Phone Number
↓
ngrok Public URL
↓
FastAPI Voice Server
↓
AI Voice Assistant
↓
AI Voice Response to Caller

---

# 📚 Use Cases

* College admission assistant
* Student helpdesk automation
* Academic information assistant
* Campus support assistant
* AI-powered educational support system

---

# 🔮 Future Improvements

* Streamlit dashboard
* LiveKit realtime streaming
* Multi-language support
* Cloud deployment
* Admin analytics dashboard
* Appointment booking system

---

# 📂 Project Structure

```bash
app/
│
├── college_voice_agent.py
├── continuous_voice_agent.py
├── memory_voice_agent.py
├── rag_setup.py
├── rag_chat.py
├── twilio_server.py
├── test_deepgram.py
├── test_elevenlabs.py
├── test_gemini.py
│
knowledge_base/
│
faiss_index/
│
README.md
requirements.txt
```

---

# ▶️ How to Run the Project

## Install dependencies

```bash
pip install -r requirements.txt
```

## Start FastAPI server

```bash
uvicorn app.twilio_server:app --host 0.0.0.0 --port 8000
```

## Start ngrok

```bash
ngrok http 8000
```

---

# 📞 Demo Phone Number

Twilio Test Number:

```text
+1 435 344 4214
```

(Note: This is a Twilio trial number used only for project demonstration.)

---

# 👨‍💻 Author

## Abdul Zawid

AI & Python Developer
Built as an advanced AI-powered conversational voice assistant project using modern Generative AI technologies.
