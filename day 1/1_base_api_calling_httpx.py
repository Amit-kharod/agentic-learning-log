from dotenv import load_dotenv
import os
import httpx

load_dotenv()

OPENAI_API_TOKEN=os.getenv("OPENAI_API_KEY")
URL="https://api.openai.com/v1/chat/completions"
MODEL="gpt-4o-mini"

headers= {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {OPENAI_API_TOKEN}"
}

payload = {
    "model": MODEL,
    "messages": [
        {"role": "system", "content": "you are a helpful assistant"},
        {"role": "user", "content": "what is size of the moon"}
    ],
    "max_tokens": 100,
    "temperature": 0.7
}

response = httpx.post(URL, headers=headers,json=payload)


data = response.json()

print(data["choices"][0]["message"]["content"])



