# Pipecat voice bot. WebRTC: UI at /client. Daily: no /client — open / (redirects to Daily room).
# Railway sets PORT; bind 0.0.0.0 for public access.

FROM python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libglib2.0-0 \
    libgl1 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libxcb1 \
    && rm -rf /var/lib/apt/lists/*

# Install from local source so runtime uses repo patches (e.g., Twilio TURN in runner).
COPY pyproject.toml uv.lock README.md LICENSE MANIFEST.in ./
COPY src ./src

RUN pip install --no-cache-dir uv \
    && uv pip install --system \
    -e ".[daily,webrtc,silero,deepgram,cartesia,openrouter,runner]" \
    "python-dotenv>=1.0.1,<2.0.0"

COPY bot_openrouter.py /app/bot.py

EXPOSE 7860
ENV PORT=7860

# Default `webrtc`: Pipecat serves /client (browser mic). Use `daily` only if you have a Daily.co plan + DAILY_API_KEY (GET / redirects to Daily; unpaid accounts may see Daily billing pages).
CMD ["sh", "-c", "exec python /app/bot.py --host 0.0.0.0 --port ${PORT} --transport ${PIPECAT_TRANSPORT:-webrtc}"]
