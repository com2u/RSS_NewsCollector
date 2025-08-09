-- PostgreSQL initialization script for News Collector

-- Create role and user if not exists
DO
$$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_roles WHERE rolname = 'comu2'
   ) THEN
      CREATE ROLE :user WITH LOGIN PASSWORD :'password';
      ALTER ROLE comu2 CREATEDB CREATEROLE;
   END IF;
END
$$;

-- Create database if not exists
DO
$$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_database WHERE datname = 'newsdb'
   ) THEN
      CREATE DATABASE newsdb OWNER comu2;
   END IF;
END
$$;

-- Connect to database and create table
\connect newsdb

CREATE TABLE IF NOT EXISTS news (
    id SERIAL PRIMARY KEY,
    source TEXT,
    title TEXT,
    description TEXT,
    published TIMESTAMP,
    link TEXT UNIQUE,
    fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
