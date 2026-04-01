"""Railway / web deployment entrypoint: lightweight HTTP API.

Uses OpenRouter (OpenAI-compatible chat). Set OPENROUTER_API_KEY in Railway
Variables (not in git).
"""

from __future__ import annotations

import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, Response
from pydantic import BaseModel, Field

app = FastAPI(
    title="Pipecat web API",
    description="Minimal chat API for Railway. Use /docs for OpenAPI.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    """Request body for POST /chat."""

    message: str = Field(..., min_length=1, max_length=32000)
    model: str = Field(
        default="meta-llama/llama-3.3-70b-instruct",
        description="OpenRouter model id, e.g. openai/gpt-4o-mini",
    )


class ChatResponse(BaseModel):
    """Assistant reply."""

    reply: str
    model: str


@app.get("/health")
def health() -> dict[str, str]:
    """Railway health check."""
    return {"status": "ok"}


@app.get("/")
def root() -> dict[str, str]:
    """Service info."""
    return {
        "service": "pipecat-web",
        "docs": "/docs",
        "health": "/health",
        "chat_page": "GET /chat (browser UI)",
        "chat_api": "POST /chat (JSON API)",
    }


def _run_chat(body: ChatRequest) -> ChatResponse:
    """Shared OpenRouter call for POST /chat."""
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=503,
            detail="OPENROUTER_API_KEY is not set. Add it in Railway Variables.",
        )

    try:
        from openai import OpenAI
    except ImportError as e:
        raise HTTPException(status_code=500, detail=f"openai package missing: {e}") from e

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
        default_headers={
            "HTTP-Referer": os.environ.get("OPENROUTER_HTTP_REFERER", "https://railway.app"),
            "X-Title": os.environ.get("OPENROUTER_APP_TITLE", "Pipecat Railway"),
        },
    )

    try:
        completion = client.chat.completions.create(
            model=body.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant. Be concise.",
                },
                {"role": "user", "content": body.message},
            ],
            temperature=0.7,
        )
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e)) from e

    choice = completion.choices[0].message
    text = (choice.content or "").strip()
    if not text:
        raise HTTPException(status_code=502, detail="Empty model response")

    return ChatResponse(reply=text, model=body.model)


@app.get("/chat", response_class=HTMLResponse, include_in_schema=True)
@app.get("/chat/", response_class=HTMLResponse, include_in_schema=False)
def chat_page() -> str:
    """Browser UI: opening /chat in a tab uses GET; the page POSTs JSON to /chat."""
    return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Chat</title>
  <style>
    :root { font-family: system-ui, sans-serif; max-width: 40rem; margin: 2rem auto; padding: 0 1rem; }
    h1 { font-size: 1.25rem; }
    textarea { width: 100%; min-height: 5rem; padding: 0.5rem; box-sizing: border-box; }
    button { margin-top: 0.5rem; padding: 0.5rem 1rem; cursor: pointer; }
    #out { margin-top: 1rem; white-space: pre-wrap; border: 1px solid #ccc; padding: 1rem; border-radius: 6px; min-height: 3rem; }
    .err { color: #b00; }
    .hint { color: #555; font-size: 0.9rem; margin-top: 1rem; }
  </style>
</head>
<body>
  <h1>Pipecat chat (OpenRouter)</h1>
  <p>Type a message and send. This page calls <code>POST /chat</code> from your browser.</p>
  <textarea id="msg" placeholder="Your message..."></textarea>
  <div><button type="button" id="send">Send</button></div>
  <div id="out" aria-live="polite"></div>
  <p class="hint">API: <code>POST /chat</code> with JSON <code>{"message":"..."}</code> · <a href="/docs">OpenAPI docs</a></p>
  <script>
    const out = document.getElementById("out");
    const msg = document.getElementById("msg");
    document.getElementById("send").onclick = async () => {
      const message = (msg.value || "").trim();
      if (!message) { out.innerHTML = '<span class="err">Enter a message.</span>'; return; }
      out.textContent = "Thinking…";
      try {
        const r = await fetch("/chat", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ message }),
        });
        const data = await r.json().catch(() => ({}));
        if (!r.ok) {
          out.innerHTML = '<span class="err">' + (data.detail || r.statusText || r.status) + "</span>";
          return;
        }
        out.textContent = data.reply || JSON.stringify(data);
      } catch (e) {
        out.innerHTML = '<span class="err">' + e + "</span>";
      }
    };
  </script>
</body>
</html>"""


@app.post("/chat", response_model=ChatResponse)
@app.post("/chat/", response_model=ChatResponse, include_in_schema=False)
async def chat(body: ChatRequest) -> ChatResponse:
    """Send a user message to OpenRouter and return the assistant reply (JSON)."""
    return _run_chat(body)


@app.get("/favicon.ico", include_in_schema=False)
def favicon() -> Response:
    """Avoid 404 noise when browsers request /favicon.ico."""
    return Response(status_code=204)
