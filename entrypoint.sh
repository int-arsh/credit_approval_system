#!/bin/sh

set -e

echo "Waiting for PostgreSQL to be ready..."

# Wait for PostgreSQL with retry logic
until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c '\q' 2>/dev/null; do
  echo "PostgreSQL is unavailable - sleeping"
  sleep 2
done

echo "PostgreSQL is up and ready!"

# Run migrations
echo "Running migrations..."
python manage.py migrate --noinput

# Import data
echo "Importing data..."
python manage.py import_data || echo "Data import completed or already exists"

# Start server
echo "Starting Django server..."
exec python manage.py runserver 0.0.0.0:8000