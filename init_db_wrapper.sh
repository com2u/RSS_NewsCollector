#!/bin/bash
# Wrapper script to initialize PostgreSQL using init_db.sql with environment variable substitution

set -e

# Ensure the database is initialized only on first run
if [ ! -f "/var/lib/postgresql/data/.init_done" ]; then
  echo "Waiting for PostgreSQL to be ready..."
  until pg_isready -h localhost -p ${POSTGRES_PORT} -U ${POSTGRES_USER}; do
    sleep 2
  done

  echo "Initializing database schema from init_db.sql..."
  psql -v user="${POSTGRES_USER}" -v password="${POSTGRES_PASSWORD}" -f /docker-entrypoint-initdb.d/init_db.sql

  # Mark initialization as done
  touch /var/lib/postgresql/data/.init_done
else
  echo "Database already initialized — skipping init script."
fi
