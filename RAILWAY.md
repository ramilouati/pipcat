# Deploy on Railway

This repo includes a small **HTTP API** (`app.py`) you can run on [Railway](https://railway.app): health check, OpenAPI docs, and `POST /chat` using your **OpenRouter** key.

## What gets deployed

- **FastAPI** + **Uvicorn** (`pipecat-ai[runner]` brings `fastapi` and `uvicorn`).
- **Endpoints**: `GET /health`, `GET /`, `POST /chat`, `GET /docs` (Swagger).

This is **not** the full Pipecat voice bot pipeline (that needs WebRTC + STT/TTS + more keys). For a voice assistant on Railway, use the Pipecat runner with WebRTC locally or Pipecat Cloud; this HTTP layer is the simplest way to get a working “web API” on Railway.

## Security

- **Never commit API keys.** Use Railway **Variables** only.
- If a key was ever pasted in chat or committed, **rotate it** in the OpenRouter dashboard.

## Steps

1. Push this repo to GitHub (you already have [ramilouati/pipcat](https://github.com/ramilouati/pipcat)).

2. In Railway: **New Project** → **Deploy from GitHub** → select the repo.

3. Railway should detect the **Dockerfile** (see `railway.toml`).

4. **Variables** (project or service):

   | Name | Value |
   |------|--------|
   | `OPENROUTER_API_KEY` | Your OpenRouter secret key |

   Optional:

   | Name | Purpose |
   |------|---------|
   | `OPENROUTER_HTTP_REFERER` | Your site URL (OpenRouter optional header) |
   | `OPENROUTER_APP_TITLE` | App name for OpenRouter |

5. **Generate Domain** (Settings → Networking) to get a public HTTPS URL.

6. Check:

   - `https://YOUR_DOMAIN/health` → `{"status":"ok"}`
   - `https://YOUR_DOMAIN/docs` → Swagger UI

   Example chat:

   ```bash
   curl -s -X POST "https://YOUR_DOMAIN/chat" \
     -H "Content-Type: application/json" \
     -d '{"message":"Say hello in one sentence."}'
   ```

## Local run (same as Railway)

```bash
uv sync --extra runner --extra openrouter
set OPENROUTER_API_KEY=sk-or-v1-...
uv run uvicorn app:app --host 0.0.0.0 --port 7860
```

Then open `http://127.0.0.1:7860/docs`.

## Troubleshooting

- **Build fails**: Ensure the repo includes `pyproject.toml`, `uv.lock`, `src/`, and `Dockerfile`.
- **503 on /chat**: `OPENROUTER_API_KEY` missing in Railway Variables.
- **502**: Model name wrong, OpenRouter quota, or network error; read the `detail` in the JSON error.
