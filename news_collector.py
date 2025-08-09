#!/usr/bin/env python3
"""
File: news_collector.py
Path: /home/com2u/src/NewsCollector/news_collector.py

Purpose:
This agent reads news from RSS feeds specified in rss.json, maintains an in-memory list of the last 30 news items per source,
checks for new articles every cycle (default 5 minutes), and stores new articles in a PostgreSQL database.

Reasoning and Changes:
- Load RSS sources from rss.json
- Fetch feeds and parse items
- Maintain a dictionary of last processed items per source
- Avoid reprocessing existing news
- Store metadata in PostgreSQL (source, title, description, timestamp, link, etc.)
- Output logs for debugging (written to stdout)
- Use environment variables for secrets (PostgreSQL credentials, cycle time)
"""

import os
import time
import json
import feedparser
import psycopg2
from psycopg2 import sql
from datetime import datetime
from collections import deque

# Load configuration
CYCLE_TIME = int(os.getenv("CYCLE_TIME", 300))  # default 5 minutes (300 seconds)
DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("POSTGRES_HOST")
DB_PORT = os.getenv("POSTGRES_PORT")

# Load RSS sources from file
with open("rss.json", "r") as f:
    RSS_SOURCES = json.load(f).get("sources", [])

# In-memory store {source_url: deque}
news_cache = {src: deque(maxlen=30) for src in RSS_SOURCES}

def connect_db():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

def setup_db():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS news (
        id SERIAL PRIMARY KEY,
        source TEXT,
        title TEXT,
        description TEXT,
        published TIMESTAMP,
        link TEXT UNIQUE,
        fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    conn.commit()
    cur.close()
    conn.close()

def news_exists(link):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM news WHERE link = %s LIMIT 1;", (link,))
    exists = cur.fetchone() is not None
    cur.close()
    conn.close()
    return exists

def store_news(source, title, description, published, link):
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO news (source, title, description, published, link)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (link) DO NOTHING;
        """, (source, title, description, published, link))
        conn.commit()
        cur.close()
        conn.close()
        print(f"[{datetime.now()}] [NEW] Stored news: {title} from {source}")
    except Exception as e:
        print(f"[{datetime.now()}] [ERROR] Failed to store news: {e}")

def fetch_and_store():
    for src in RSS_SOURCES:
        feed = feedparser.parse(src)
        for entry in feed.entries:
            title = entry.get("title", "")
            description = entry.get("description", "")
            published_str = entry.get("published", None)
            published_dt = None
            if published_str:
                try:
                    published_dt = datetime(*entry.published_parsed[:6])
                except Exception:
                    published_dt = datetime.now()
            link = entry.get("link", "")

            # Avoid duplicates with in-memory cache
            if link in news_cache[src]:
                print(f"[{datetime.now()}] [SKIP] Already processed (in memory): {title}")
                continue

            # Avoid duplicates in DB
            if news_exists(link):
                print(f"[{datetime.now()}] [SKIP] Already exists in DB: {title}")
                news_cache[src].append(link)
                continue

            # Store news
            store_news(src, title, description, published_dt, link)
            news_cache[src].append(link)

if __name__ == "__main__":
    setup_db()
    print(f"[{datetime.now()}] Starting News Collector. Cycle every {CYCLE_TIME} seconds.")
    while True:
        fetch_and_store()
        time.sleep(CYCLE_TIME)
