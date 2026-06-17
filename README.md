# agentic-learning-log

A weekly journal for tracking my learning progress about agentic systems.

## Day 1 — Calling the LLM API directly over HTTP

Before reaching for an SDK or any abstraction layer, I wanted to see what an
LLM API call actually looks like under the hood. So I made a raw HTTP request
to the OpenAI Chat Completions endpoint using `httpx`.

Code: [`day 1/1_base_api_calling_httpx.py`](day%201/1_base_api_calling_httpx.py)

### What I learned

- **Keys live in the environment, not the code.** Loaded `OPENAI_API_KEY` from a
  `.env` file with `python-dotenv` (`load_dotenv()` + `os.getenv(...)`), and kept
  `.env` out of git via `.gitignore` so the secret never gets committed.
- **The endpoint:** `POST https://api.openai.com/v1/chat/completions`.
- **Headers:** the request needs `Content-Type: application/json` and
  `Authorization: Bearer <API_KEY>`.
- **The request body (payload):**
  - `model` — which model to use (I used `gpt-4o-mini`).
  - `messages` — a list of role/content objects (`system`, `user`, etc.) that
    represent the conversation.
  - `max_tokens` — caps the length of the response.
  - `temperature` — controls randomness/creativity of the output.
- **Making the call:** `httpx.post(URL, headers=headers, json=payload)` — passing
  the dict as `json=` serializes it and sets the JSON content type automatically.
- **Reading the response:** the model's reply is nested at
  `response.json()["choices"][0]["message"]["content"]`.

### Takeaway

An "AI API call" is just a normal HTTPS POST with a JSON body and an auth header.
The SDKs and abstraction layers are conveniences built on top of exactly this —
good to have seen the bare version first.
