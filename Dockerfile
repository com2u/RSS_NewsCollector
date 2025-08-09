# Dockerfile for News Collector

FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY news_collector.py .
COPY rss.json .
COPY .env .

CMD ["python", "news_collector.py"]
