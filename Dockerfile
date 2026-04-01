# Pipecat Railway image: FastAPI + OpenRouter chat API (app.py)
# Build with: docker build -t pipecat-railway .
# Railway sets PORT automatically.

FROM python:3.12-slim-bookworm

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml uv.lock README.md LICENSE MANIFEST.in ./
COPY src ./src

RUN pip install --no-cache-dir uv \
    && uv pip install --system -e ".[runner,openrouter]"

COPY app.py ./

EXPOSE 7860
ENV PORT=7860

CMD ["sh", "-c", "exec uvicorn app:app --host 0.0.0.0 --port ${PORT}"]
