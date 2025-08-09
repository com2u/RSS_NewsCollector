# News Collector

## Overview
The News Collector fetches and stores financial and economic news from predefined RSS feeds into a PostgreSQL database.  
It avoids duplicates by using both an in-memory cache and database checks.  
The default update cycle time is 5 minutes (configurable via environment variables).  
Runs in Docker with persistent PostgreSQL storage.

## Features
- Reads RSS feeds from `rss.json`
- Keeps last 30 entries per feed in memory
- Skips duplicates based on in-memory and database checks
- Stores new entries with source, title, description, publish timestamp, and link
- Provides debug logs for stored/skipped news
- Dockerized setup with PostgreSQL and persistent storage

## Prerequisites
- Docker
- Docker Compose

## Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/news-collector.git
   cd news-collector
   ```
2. Create `.env` from `.env.example` and set your own values:
   ```bash
   cp .env.example .env
   ```
   **Do not commit `.env`** — it contains sensitive credentials.

## Running the Application
```bash
docker-compose up --build
```
To view logs:
```bash
docker logs -f news_collector
```

## Stopping the Application
```bash
docker-compose down
```

## Persistent Database
The PostgreSQL data directory is mounted to the host at `./postgres_data`, ensuring data survives container rebuilds or removals.

## File Overview
- `rss.json` — List of RSS sources
- `news_collector.py` — Python agent fetching and storing news
- `init_db.sql` — PostgreSQL setup script
- `.env` — Environment variables (private)
- `.env.example` — Example environment variables without credentials
- `Dockerfile` — Container image build instructions for the News Collector
- `docker-compose.yml` — Service orchestration for the app and DB
- `.gitignore` — Ignores environment files, local data, and system/editor files

## License
MIT

## Contact
Patrick Hess  
[GitHub](https://github.com/com2u)  
[LinkedIn](https://www.linkedin.com/in/patrick-hess-63592568/)
