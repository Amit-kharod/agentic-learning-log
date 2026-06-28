# agentic-learning-log

A journal for tracking my learning progress about agentic systems. Each "day"
is a focused study session, dated with when it actually happened — the gaps
between days can be anywhere from a day to a couple of weeks.

## Day 1 — Calling the LLM API directly over HTTP

*2026-06-17*

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

## Day 2 — The OpenAI SDK, tokens, cost, and streaming

*2026-06-27*

Having seen the raw HTTP version on Day 1, I switched to the official OpenAI
Python SDK (`openai`) and dug into what actually happens to the text we send —
tokens, cost, and how responses stream back.

Code:

- [`day 2/1_calling_using_openai_sdk.py`](day%202/1_calling_using_openai_sdk.py) — the Day 1 call, now via the SDK
- [`day 2/2_tokenizer.py`](day%202/2_tokenizer.py) — splitting text into tokens with `tiktoken`
- [`day 2/3_cli_token_cost_calc.py`](day%202/3_cli_token_cost_calc.py) — a CLI that counts tokens in a file and prices the call
- [`day 2/5_streaming_via_sdk.py`](day%202/5_streaming_via_sdk.py) — streaming a response chunk by chunk

### What I learned

- **The SDK is just the HTTP call, wrapped.** `client = OpenAI()` picks up the
  API key from the environment automatically. Two ways to call it:
  - `client.responses.create(model=..., input=..., temperature=..., max_output_tokens=...)` → read `response.output_text`.
  - `client.chat.completions.create(model=..., messages=[...])` → the Day 1 message format.
- **Temperature** controls randomness. `temperature=0` makes the output
  (near-)deterministic — good for a task like "write me a WFH email" where I want
  a consistent answer rather than something creative.
- **Tokens are sub-word chunks, not words.** With `tiktoken` I could watch a
  single word get split into several tokens (e.g. `strawberry` / `pomegranate`
  coming apart piece by piece). This is also why models are bad at "count the
  letters" tasks — they see tokens, not characters.
- **Non-English text costs more tokens.** Hindi (and other non-Latin scripts)
  break into many more tokens per word than English, because the tokenizer and
  model are trained mostly on English. More tokens = more cost and more of the
  context window used to say the same thing.
- **Pricing is per token.** Built a small CLI: count the tokens in a file with
  `tiktoken`, then multiply by the price-per-token (price-per-million ÷
  1,000,000) to estimate the dollar cost of a call before sending it.
- **Streaming.** With `stream=True` the response arrives as a sequence of chunks;
  iterate them and print `chunk.choices[0].delta.content` as it comes in, instead
  of waiting for the whole reply. This is what produces the "typing" effect in
  chat UIs.

### Transformer mental model (the big one)

Started building intuition for what happens inside the model when it predicts the
next token:

1. **Tokenize + embed** — the input is split into tokens, and each token becomes
   a vector (an embedding). Position information is added too, so word order
   matters.
2. **Attention + feed-forward, stacked** — the vectors pass through many repeated
   layers. In each layer, *attention* lets every token look at the other tokens
   and pull in context (what this word means *given* the rest of the sentence);
   then a separate *feed-forward* sub-layer processes each token on its own.
   Stacking this over many layers progressively enriches each token's
   representation.
3. **Predict the next token** — at the end, the last position's vector is turned
   into a raw score (a *logit*) for every token in the vocabulary. `softmax`
   converts those scores into a probability distribution, and we *sample* from it
   to choose the next token. (Temperature reshapes this distribution before
   sampling — which ties back to the temperature setting above.)

### Takeaway

The SDK doesn't add magic — it's the Day 1 HTTP call with conveniences on top.
The real substance is underneath: text becomes tokens, tokens cost money and fill
the context window, and the model itself is a stack of attention + feed-forward
layers that turns those tokens into a probability distribution over the next one.
