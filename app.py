"""Railway / web deployment entrypoint: lightweight HTTP API.

Uses OpenRouter (OpenAI-compatible chat). Set OPENROUTER_API_KEY in Railway
Variables (not in git).
"""

from __future__ import annotations

import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
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
        "chat": "POST /chat",
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(body: ChatRequest) -> ChatResponse:
    """Send a user message to OpenRouter and return the assistant reply."""
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
