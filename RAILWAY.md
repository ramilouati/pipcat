# Deploy on Railway (Pipecat voice Web UI)

This repo’s root **Dockerfile** runs the Pipecat development runner with transport selected by `PIPECAT_TRANSPORT` (default: **`webrtc`**): browser UI at **`/client`** (mic → Deepgram STT → OpenRouter LLM → Cartesia TTS).

### Why you were redirected to Daily and asked for payment

If `PIPECAT_TRANSPORT` was **`daily`** (older default), opening **`/`** hits Pipecat’s Daily flow: it creates a [Daily.co](https://www.daily.co/) room and **HTTP-redirects your browser to Daily’s site**. If your Daily account needs a paid plan or billing details, Daily shows their payment page — that is **not** Railway billing; it’s Daily.

**Fix:** Use **`webrtc`** (default now) so **`/`** redirects to **`/client/`** (Pipecat’s WebRTC UI) and you do **not** need Daily for basic voice. Only set `PIPECAT_TRANSPORT=daily` when you intentionally use Daily rooms **and** have `DAILY_API_KEY` + an active Daily plan.

### `/client` with Daily — why it “doesn’t work”

Pipecat’s runner **only mounts `/client` when `PIPECAT_TRANSPORT=webrtc`**. That route serves the bundled Small WebRTC test UI.

With **`PIPECAT_TRANSPORT=daily`**, the runner **does not define `/client` at all** (404 is expected). The flow is:

1. Open **`https://YOUR_DOMAIN/`** (the **root**, not `/client`).
2. The server creates a Daily room (using `DAILY_API_KEY`), starts the bot, and **redirects you to a `*.daily.co` URL** — that is Daily’s web client where you join with mic/cam.

So: **WebRTC** → use **`/client`**. **Daily** → use **`/`** and complete the redirect to Daily’s page.

Redeploy after pulling the latest **Dockerfile** so the image includes `pipecat-ai[daily]`; otherwise the bot can fail when it tries to join the room as a Daily participant.

## Variables (Railway → Variables)

| Name | Required |
|------|----------|
| `OPENROUTER_API_KEY` | Yes |
| `DEEPGRAM_API_KEY` | Yes |
| `CARTESIA_API_KEY` | Yes |
| `PIPECAT_TRANSPORT` | Optional; default **`webrtc`**. Use `daily` only with Daily set up below. |

For `daily` transport only:

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
5. **WebRTC:** leave `PIPECAT_TRANSPORT` unset or set `webrtc`. Open **`/client`** (or `/` → redirects to `/client/`).
6. **Daily:** set `PIPECAT_TRANSPORT=daily` and **`DAILY_API_KEY`**. Open **`/`** only — you will be redirected to **Daily’s site**, not `/client`.

## Checks

- `GET /health` may be served by the Pipecat runner if exposed; otherwise use logs for “Uvicorn running”.
- Voice smoke test: speak one sentence; you should hear a reply.
- If client stays on "connecting" with `webrtc`, switch to `daily`.

## Local (same image)

**WebRTC only (no Daily):** start Docker Desktop, then from the repo root:

```bash
docker compose up --build
```

Or manually:

```bash
docker build -t pipecat-local .
docker run --rm -p 7860:7860 --env-file .env -e PIPECAT_TRANSPORT=webrtc pipecat-local
```

Open **`http://localhost:7860/`** (redirects to `/client/`) or **`http://localhost:7860/client`**. Your `.env` needs at least `OPENROUTER_API_KEY`, `DEEPGRAM_API_KEY`, and `CARTESIA_API_KEY`. You do **not** need `DAILY_API_KEY` for this mode.

If Docker reports it cannot connect to the daemon, start **Docker Desktop** on Windows and retry.

## Note on `app.py`

`app.py` is a tiny optional FastAPI app for local `uvicorn app:app` only. **It is not used** by the production Docker image above. There is **no `/chat`** page in production.

## Security

- Never commit API keys. Use Railway Variables only.
- Rotate keys if they were ever exposed.
