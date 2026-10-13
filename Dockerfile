# Backend image: Python + Chromium (playwright) + Tesseract. Render-ready.
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# Chromium runtime libs + Tesseract engine (Debian package names).
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 \
    libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 \
    libgbm1 libasound2 libpango-1.0-0 libcairo2 \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt \
 && python -m playwright install chromium

COPY backend ./backend
COPY data ./data
RUN mkdir -p runs

EXPOSE 8000
# Render injects $PORT; default 8000 for local `docker run`.
CMD ["sh", "-c", "uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
