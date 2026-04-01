# Pipecat voice bot for Railway: WebRTC client at /client (OpenRouter + Deepgram + Cartesia).
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

RUN pip install --no-cache-dir uv \
    && uv pip install --system \
    "pipecat-ai[webrtc,silero,deepgram,cartesia,openrouter,runner]" \
    "python-dotenv>=1.0.1,<2.0.0"

COPY examples/quickstart/bot_openrouter.py /app/bot.py

EXPOSE 7860
ENV PORT=7860

CMD ["sh", "-c", "exec python /app/bot.py --host 0.0.0.0 --port ${PORT} --transport webrtc"]
