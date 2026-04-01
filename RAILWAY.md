# Deploy on Railway (Pipecat voice Web UI)

This repo’s root **Dockerfile** runs the Pipecat development runner with transport selected by `PIPECAT_TRANSPORT` (default: `daily`): browser UI at **`/client`** (mic -> Deepgram STT -> OpenRouter LLM -> Cartesia TTS).

## Variables (Railway → Variables)

| Name | Required |
|------|----------|
| `OPENROUTER_API_KEY` | Yes |
| `DEEPGRAM_API_KEY` | Yes |
| `CARTESIA_API_KEY` | Yes |
| `PIPECAT_TRANSPORT` | Recommended (`daily`) |

For `daily` transport:

| Name | Required |
|------|----------|
| `DAILY_API_KEY` | Yes |

Optional for direct room mode:

| Name | Purpose |
|------|---------|
| `DAILY_ROOM_URL` | Reuse a fixed Daily room URL |

Optional headers for OpenRouter:

| Name | Purpose |
|------|---------|
| `OPENROUTER_HTTP_REFERER` | Your public site URL |
| `OPENROUTER_APP_TITLE` | App title for OpenRouter |

## Deploy

1. Push your branch (e.g. `test` or `main`).
2. Railway: **New Project** → **Deploy from GitHub** → select repo.
3. Confirm **Dockerfile** build (see `railway.toml`).
4. **Networking** → **Generate Domain**.
5. Set `PIPECAT_TRANSPORT=daily` in Railway Variables.
6. Open: `https://YOUR_DOMAIN/client` -> **Connect** -> allow microphone.

## Checks

- `GET /health` may be served by the Pipecat runner if exposed; otherwise use logs for “Uvicorn running”.
- Voice smoke test: speak one sentence; you should hear a reply.
- If client stays on "connecting" with `webrtc`, switch to `daily`.

## Local (same image)

```bash
docker build -t pipecat-voice .
docker run --rm -p 7860:7860 --env-file .env pipecat-voice
```

Then open `http://localhost:7860/client`.

## Note on `app.py`

`app.py` is a tiny optional FastAPI app for local `uvicorn app:app` only. **It is not used** by the production Docker image above. There is **no `/chat`** page in production.

## Security

- Never commit API keys. Use Railway Variables only.
- Rotate keys if they were ever exposed.
