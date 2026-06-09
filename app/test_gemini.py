from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv("app/.env")

# Create Groq client
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

# Generate response
response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {
            "role": "user",
            "content": "Introduce yourself as a helpful AI voice assistant."
        }
    ]
)

# Print response
print(response.choices[0].message.content)