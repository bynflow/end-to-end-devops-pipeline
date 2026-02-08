FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# dependencies first (better layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# app code
COPY app ./app

# default port (documentation)
EXPOSE 5000

# run flask app
CMD ["python", "-m", "app.app"]
