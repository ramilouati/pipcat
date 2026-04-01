"""Optional minimal FastAPI app for local health checks.

Production Railway deploy uses the root **Dockerfile**, which runs the Pipecat
voice bot (`bot_openrouter.py` → Web UI at **/client**). This file is not used
by that image.

For local API-only testing you can run:
  uv run uvicorn app:app --host 0.0.0.0 --port 7860
"""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.responses import Response

app = FastAPI(
    title="Pipecat",
    description="Minimal health app. Voice Web UI is served by the Pipecat runner at /client.",
    version="1.0.0",
)


@app.get("/health")
def health() -> dict[str, str]:
    """Health check."""
    return {"status": "ok"}


@app.get("/")
def root() -> dict[str, str]:
    """Service info."""
    return {
        "service": "pipecat",
        "note": "Deploy with root Dockerfile for voice + /client. See RAILWAY.md.",
        "health": "/health",
    }


@app.get("/favicon.ico", include_in_schema=False)
def favicon() -> Response:
    return Response(status_code=204)
