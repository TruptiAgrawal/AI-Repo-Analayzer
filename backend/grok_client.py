import httpx
import os
from dotenv import load_dotenv


load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

def ask_grok(prompt: str) -> str:
    # Keep the function name same so main.py doesn't need changes
    
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is missing! Check your .env file.")

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": "llama-3.1-8b-instant",   # Free, fast, and very capable
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    response = httpx.post(GROQ_API_URL, json=body, headers=headers, timeout=30)
    result = response.json()

    print("=== GROQ RAW RESPONSE ===")
    print(result)
    print("=========================")

    if "error" in result:
        raise ValueError(f"Groq API error: {result['error']}")

    return result["choices"][0]["message"]["content"]