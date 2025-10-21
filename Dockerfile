FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# (Often needed for building wheels)
RUN apt-get update && apt-get install -y --no-install-recommends \
      build-essential \
    && rm -rf /var/lib/apt/lists/*

# 1) Export requirements from Pipfile.lock
COPY Pipfile Pipfile.lock ./
RUN pip install --upgrade pip pipenv \
 && pipenv requirements > requirements.txt

# 2) Install runtime deps from requirements.txt (no venv inside image)
RUN pip install -r requirements.txt

# 3) Copy your app code
COPY app ./app

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
