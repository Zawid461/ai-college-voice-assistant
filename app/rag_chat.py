from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

from openai import OpenAI
from dotenv import load_dotenv

import os

# -----------------------------
# LOAD ENV VARIABLES
# -----------------------------
load_dotenv("app/.env")

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

print("\nRAG system loaded successfully!")

# -----------------------------
# GROQ CLIENT
# -----------------------------
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

# -----------------------------
# CHAT LOOP
# -----------------------------
while True:

    question = input("\nAsk a question: ")

    if question.lower() == "exit":
        break

    # -------------------------
    # SEARCH RELEVANT CHUNKS
    # -------------------------
    docs = vectorstore.similarity_search(
        question,
        k=3
    )

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    print("\nRetrieved Context:\n")
    print(context[:1000])

    # -------------------------
    # CREATE PROMPT
    # -------------------------
    prompt = f"""
You are a helpful college assistant.

Answer ONLY from the provided context.

Context:
{context}

Question:
{question}
"""

    # -------------------------
    # AI RESPONSE
    # -------------------------
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    answer = response.choices[0].message.content

    print("\nAI ANSWER:\n")
    print(answer)