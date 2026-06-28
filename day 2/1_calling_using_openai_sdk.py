from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

response = client.responses.create(
    model="gpt-4o-mini",
    input="write me a email for taking a WFH for today",
    temperature=0,
    max_output_tokens=1000
)

print(response.output_text)
