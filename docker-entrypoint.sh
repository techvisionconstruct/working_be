#!/bin/bash

# Wait for database to be ready
if [ "$ENVIRONMENT" = "production" ] || [ "$ENVIRONMENT" = "staging" ]; then
    DB_HOST_VAR="${ENVIRONMENT^^}_DB_HOST"
    DB_PORT_VAR="${ENVIRONMENT^^}_DB_PORT"
    
    echo "Waiting for PostgreSQL..."
    while ! nc -z ${!DB_HOST_VAR} ${!DB_PORT_VAR}; do
      sleep 0.1
    done
    echo "PostgreSQL started"
fi

# Create directories for static and media files
mkdir -p /app/staticfiles
mkdir -p /app/mediafiles

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start server
echo "Starting server..."
exec "$@"