#!/bin/sh

# Run migrations
python manage.py migrate

# Load initial data
python manage.py loaddata api/fixtures/products.json

# Create a superuser if it doesn't exist
export DJANGO_SUPERUSER_USERNAME=bob
export DJANGO_SUPERUSER_EMAIL=bob@what.digital
export DJANGO_SUPERUSER_PASSWORD=change123
python manage.py createsuperuser --noinput || true

# Collect static files
python manage.py collectstatic --noinput

# Start the server
gunicorn --bind 0.0.0.0:8000 what_backend.wsgi:application
