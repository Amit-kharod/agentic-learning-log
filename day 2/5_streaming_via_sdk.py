from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

stream = client.chat.completions.create(model="gpt-4o-mini",messages=[{
    "role": "user",
    "content": "Write a essay about cow"
}], stream=True)

for chunk in stream:
    delta = chunk.choices[0].delta.content

    if delta:
        print(delta, end="",flush=True)

